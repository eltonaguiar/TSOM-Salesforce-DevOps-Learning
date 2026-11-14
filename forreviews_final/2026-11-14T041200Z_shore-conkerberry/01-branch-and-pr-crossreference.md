# 01 — Branch, bundle and PR cross-reference

**Repo:** `eltonaguiar/TSOM-Salesforce-DevOps-Learning`
**Base:** `origin/main`
**Checked:** 2026-11-14T04:12Z

---

## 1. What is on `main`

### 1.1 `forreviews/` bundles (research drops)

| Bundle | Likely owner | Focus | Unique value | Merge verdict |
|---|---|---|---|---|
| `20261114-020300-salesforceagain-kilo/` | kilo | JD↔page matrix, limits, tools, CI/CD, JD term map, certs | The 00-consolidated copy; 10 artifacts | **Already absorbed** — spot-check only |
| `20261114-020852-salesforcemore/` | kilo | (no README) sibling research | Unknown — no index | **Inspect before relying on it** |
| `20261114-023241-salesforceagain-v2/` | kilo | Round-1 self-contained drop (limits, dependencies, tools, CI/CD, JD, certs) | Per-file merge destinations | **Mostly duplicate** of 020300 |
| `2026-11-14T0210Z-salesforceyetagain-v2/` | kilo | Planning anchors, certs, crash course | 12-anchor plan | **Overlaps** published crash course |
| `2026-11-14T023312_salesforcemore-v3/` | kilo | Deep dive, `[Verify]`-tagged UI paths | Confidence grading on UI paths is genuinely useful | **Keep the confidence-grading idea** |
| `2026-11-14T023507_salesforcemore-v2/` | kilo | Split bundle, source log, merge map | `08-cross-bundle-notes.md` reconciles siblings | **Read 08 before merging** |
| `salesforceagain-v4-2026-11-14-0230/` | kilo | Complete deep-dive single file | One-file orientation | **Duplicate** of the others |
| Loose `*.md` root files in `forreviews/` | kilo | v3 devops deep-dives (Gearset/UI, GitHub CI/CD, governor limits, metadata deps) | Topic-focused, easy to lift | **Lift individual sections** if gaps remain |

**Finding:** 7 bundles + loose files all map to the *same* requisition (276046). There is heavy
duplication. A merge agent should treat `20261114-020300-salesforceagain-kilo/00-consolidated-review-copy.md`
as the canonical research view and only consult the others for the few unique ideas
(confidence-grading, `08-cross-bundle-notes.md`).

### 1.2 `forreviews_final/` outputs already on `main` (from other worktrees)

| Folder | Worktree | Lens |
|---|---|---|
| `2026-11-14T030820Z_salesforceagain/` | salesforceagain | 5-guide cross-reference, defect register (51 defects + 12 self), merge plan |
| `20261114T031017Z_jet-slime/` | jet-slime | Surface cross-ref, code-review findings, Salesforce lens, prioritized actions |
| `2026-11-14T031220Z_chill-egg/` | chill-egg | Branch inventory, guide alignment, corrections, feedback |
| `2026-11-14T030826-salesforceyetagain.md` | salesforceyetagain | Consolidated feedback (loose file) |

**Finding:** the `forreviews_final/` layer is already well covered. `2026-11-14T030820Z_salesforceagain`
contains the strongest defect register; `chill-egg` has the cleanest "close the duplicate PRs" verdict.
This shore-conkerberry slice adds branch/PR verdicts and a short prioritized action list, and must
not restate their defect tables.

---

## 2. Remote branches (5)

| Branch | Contents | On `main`? | Verdict |
|---|---|---|---|
| `origin/main` | Canonical | — | Base |
| `origin/research/salesforceagain-2026-11-14T020300Z` | Backs bundle 020300 | Bundle copied into `forreviews/` | **Already merged in substance** — branch can close |
| `origin/research/salesforcemore-v2-2026-11-14T021057Z` | Backs PR #2 | Bundle in `forreviews/2026-11-14T023507_salesforcemore-v2/` | PR #2 open; substance on main |
| `origin/research/salesforceagain-v2-20261114` | Backs PR #1 | Bundle in `forreviews/20261114-023241-salesforceagain-v2/` | PR #1 open; substance on main |
| `origin/forreviews-split/salesforcemore-v2-2026-11-14T023507Z` | Split-bundle variant | Mirrored on main | **Redundant** |
| `origin/salesforceagain-v3` | v3 deep-dives | Loose files copied to `forreviews/` | **Already merged in substance** — branch can close |

**Finding:** every remote research branch's *content* already exists on `main` under `forreviews/`.
The branches are now redundant. Closing them loses nothing; the PRs (#1, #2) exist only to formally
land content that is already present.

---

## 3. Open PRs (2)

| PR | Head | Title | Content already on `main`? | Verdict |
|---|---|---|---|---|
| #2 | `research/salesforcemore-v2-2026-11-14T021057Z` | research(salesforce-devops): salesforcemore-v2 bundle | Yes — `forreviews/2026-11-14T023507_salesforcemore-v2/` | **Close** after confirming `08-cross-bundle-notes.md` is the copy on main |
| #1 | `research/salesforceagain-v2-20261114` | research(salesforceagain-v2): Round 1 | Yes — `forreviews/20261114-023241-salesforceagain-v2/` | **Close** after confirming files match |

**Caveat before closing:** diff each PR's tree against the matching `forreviews/` folder on `main`.
If any file in the PR is absent from `main`, cherry-pick that one file, then close. Do not merge the
PR tree as a second copy — a second copy is what created the duplication in the first place.

---

## 4. Root-level loose files

`forreviews/` contains flat `*.md` files (e.g. `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md`)
alongside the bundle folders. They are single-file copies of bundle sections. Treat them as
duplicates of the corresponding bundle content; do not merge both.

---

## 5. What this cross-reference concludes

1. `main` already contains 7 equivalent research bundles + 3 other agents' final reviews.
2. No open PR introduces content that is missing from `main`.
3. The next merge agent's job is **curation and correction**, not ingestion.
4. Close #1 and #2 (after a one-file diff), close the 4 redundant research branches, and spend the
   time on the page corrections in `03-feedback-and-actions.md`.
