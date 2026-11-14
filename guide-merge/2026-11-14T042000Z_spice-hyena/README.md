# Guide merge — 2026-11-14T042000Z · spice-hyena

All agents' work from `forreviews/`, deduplicated and merged into the five published Salesforce pages.

**Source repo:** `eltonaguiar/TSOM-Salesforce-DevOps-Learning` (`forreviews/` — 85 files, 7 bundles)
**Target pages:** `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` → `docs/salesforce/`
**Live pages at merge time:** guide repo @ `3d532fb`

---

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This file |
| `DEDUPE_MANIFEST.md` | What was merged, what was rejected and why, file-by-file disposition |
| `originals/` | The five live pages, **byte-for-byte as published** (baseline) |
| `merged/` | The five merged pages — drop-in replacements |
| `patches/` | Unified diffs, `originals/` → `merged/`, for line-level review |
| `sources/` | All 85 `forreviews/` files, preserved verbatim so the merge is auditable |
| `SUBQ_DECISION_TRAIL.md` | Five SubQ decision calls used to prioritise what to add, and what verification changed |

---

## How the gaps were prioritised

I did not guess which section needed the most work. I measured coverage of 43 release-engineering topics
across the five pages, then put the ranking to **SubQ** — a decision model — and narrowed it with follow-up
questions.

| Question | Answer | Confidence |
|---|---|---|
| Which page has the most genuinely missing content | `devops-engineer` | 0.887 |
| Which section is most incomplete | §2 vs §9 — split | 0.370 |
| Head-to-head §2 vs §9 | **§2 Metadata that breaks releases** | 0.782 |
| What content is most needed | C vs A — split | 0.268 |
| Head-to-head A vs C | **metadata types / what forces a test run** | 0.706 |

Full reasoning and probability tables in `SUBQ_DECISION_TRAIL.md`.

**Verification overrode the model.** SubQ selected the "24 metadata types that force a full local test run".
That list is correct only for **Metadata API 33.0 and earlier**. Since 34.0, only Apex classes and triggers
force a test run — a `CustomField`/`Profile`/`Flow`/`ValidationRule` payload alone runs **zero tests**. The
list had been copied forward for a decade, including into the research bundles. It is now on the page with the
version distinction, the official example, and why it matters: a config-only deploy that looks validated is
not, because nothing ran.

---

## The short version

The bundles contain **85 files** but not 85 findings. The same research was performed 2–4 times over, and
the same errors were copied with it. So the merge did not go defect-by-defect — it went **upstream**.

**Three things changed:**

1. **Five defects fixed in the published pages** (they were wrong before any agent touched them):

   | Page | Defect |
   |---|---|
   | `crash-course.md` | Heap `6/12 MB` → **`10/25 MB`**. 6/12 is the *callout size* limit, a different row of the same table |
   | `user-management-data.md` | "Deactivated users can't be reactivated" → they **can** |
   | `labs-design.md` | Five **invented** system properties (`org.wideSharing.default`, `setup.locked`…) → real Setup settings |
   | `labs-design.md` Lab 4 | "Password Authentication" with blank credentials → **No Authentication** |
   | `navigation-breadcrumbs.md` | `Setup > Apex Jobs` / `Scheduled Jobs` → `Setup > Background Jobs`; Process Builder / Workflow Rules marked retired |

2. **The missing release-engineering layer added to `devops-engineer.md`** (+116 lines). The pages had no
   coverage of any of this, and every bundle did:

   - Metadata API payload ceilings: **~39 MB compressed / ~600 MB uncompressed / 10,000 files**
   - The **three** different coverage rules (org-wide 75% + triggers need *some* coverage; or per-item 75%
     under `RunSpecifiedTests`)
   - `sf project deploy validate` and the **10-day** quick-deploy window, plus the **3-day**
     `--use-most-recent` limit
   - `validate` is **production-only** — do not run it against a sandbox
   - Destructive changes as a separate manifest; deployment queue is **not FIFO**; intra-payload references
     resolve, so ordering package.xml is not the mechanism

3. **Ten wrong bundle claims rejected**, not merged — including a **10× payload error** (400 MB vs ~39 MB)
   and a **non-existent "1% coverage rule"**.

---

## The single most useful finding

Five bundles publish `6 MB sync / 12 MB async` for heap. Those numbers are **real** — they are the
**callout request/response size** limits, a different row of the same governor-limits table:

| Limit | Sync | Async |
|---|---|---|
| Total heap size | **10 MB** | **25 MB** |
| Max callout request or response size | 6 MB | 12 MB |

The crash course applied the callout row to the heap row. That is why five independent agents reproduced it
faithfully — they copied a plausible-looking pair from the page that was supposed to be authoritative.

Fixing it by swapping 12 for 25 would have left the 6/12 figures orphaned and free to be re-attached to
whatever limit a future reader is reasoning about. The merged page states **both** rows, labelled.

**Verified:** `developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html`

---

## Verification

Every number merged was checked against a primary source. Sources used:

- `apex-gov-limits.html` — heap, CPU, callout size
- `apex_code_coverage_intro.htm` — 75% requirement
- `meta-deploy.html` — 39 MB / 600 MB / 10,000 files / base64 mechanics
- `meta_rest_deploy_recentvalidation.htm` — the two coverage cases, 10-day window
- CLI reference: `project deploy validate`, `project deploy quick`

**Not verified, and not merged:** vendor tool click paths (Gearset / Copado / AutoRABIT), exam weight
percentages, the `RunRelevantTests` API version gate. See `DEDUPE_MANIFEST.md` §3.

---

## Applying

```bash
cd ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM
cp <this-folder>/merged/*.md docs/salesforce/
git diff --stat docs/salesforce/     # +132 lines net across 5 files
```

Or apply the patches individually:

```bash
cd docs/salesforce
for p in <this-folder>/patches/*.patch; do patch -p0 < "$p"; done
```

`sources/` and `originals/` are for audit only — do not copy them into the guide repo.

---

## Open items

| Item | Owner |
|---|---|
| Port `merged/*.md` into the guide repo | whoever owns that repo |
| Verify the "Development Lifecycle and Deployment Architect" credential against the official credential page | unassigned — this is the one unresolved factual dispute between reviewers |
| Confirm current Gearset / Copado / AutoRABIT navigation if a click path is ever published | unassigned |
| Delete the four redundant research branches in this repo | unassigned |
| Delete the five duplicate loose files in `forreviews/` | unassigned |