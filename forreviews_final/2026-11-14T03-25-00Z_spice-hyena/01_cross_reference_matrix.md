# 01 — Cross-reference matrix

Every review item, where it lives, its state, and the verdict. "Domain" = this repo
(`findtorontoevents_antigravity.ca`). "Learning" = the TSOM learning repo that owns the training guides.

Legend for **State**: `stale` = cut from a `main` that has moved on · `conflict` = cannot merge as-is ·
`inherited-red` = fails only because of a `main` defect · `orphan` = no owner/record · `complete` = reviewable.

## 1. Branches ahead of `origin/main`

| Branch | +commits | Last activity | Contents | State | Verdict |
|---|---|---|---|---|---|
| `wiring` | 5 | 2026-11-13 | Inception retirement (36 files) + 2 mermaid-test commits | **inherited-red** + orphan | Retirement is sound; the 2 mermaid commits must not land |
| `scrub/inception-mercury-2026-11-12` | 3 | 2026-11-12 | Retirement, earlier shape | stale | Superseded by `wiring`; do not merge both |
| `salesforceagain-v3` | 6 | 2026-11-14 | Retirement + 4 `forreviews/` Salesforce deep-dives | stale | Its Salesforce content belongs in the learning repo, not here |
| `ollama-checks-v3`, `ollama-checks` | 6 | 2026-11-13 | Retirement + SAM checklist | stale | Diff is retirement + one doc; no unique engineering |
| `multi4-v3` | 6 | 2026-11-13 | Retirement + SAM best-practices doc | stale | Same |
| `samagain-v4` | 6 | 2026-11-13 | Retirement + SAM module reference | stale | Same |
| `docs/freebuff-handoff-2026-11-13` | 3 | 2026-11-12 | Mermaid bench handoff + verification design (1,053 lines) | orphan | Real content; needs an owner and a decision |
| `feat/safe-patch-helper-2026-11-12` | 1 | 2026-11-12 | `tools/safe_patch.py` (257) + record | complete | Mergeable — useful, self-contained, documented. **CI never runs on it** (`tools/` is outside the `paths:` filter) |
| `feat/retired-provider-guard-2026-11-12` | 1 | 2026-11-12 | `tools/check_retired_providers.py` (302) + record | complete | Mergeable — best guard in the set. **CI never runs on it** |
| `feat/ast-reviewer-codemod-2026-11-12` | 1 | 2026-11-12 | `tools/ast_reviewer_codemod.py` (328) + record | complete | Mergeable, narrower use. **CI never runs on it** |
| `feat/hermes-web-menu-entry-2026-11-12` | 1 | 2026-11-12 | `tools/hermes_web.sh` (74) + record | complete | Mergeable; host-specific. **CI never runs on it** |
| `add-kilo-additional-skills` | 1 | 2026-11-02 | `ADDITIONAL_SKILLS__kilo.md` (39) | complete | PR #765; content partly superseded by this repo's `AGENTS.md` |
| `add-kilo-todays-servicenow-salesforce-jobs` | 1 | 2026-11-02 | Job scan (130) | stale | Dated 2026-11-02; snapshot value only |
| `job-search-2026-11-03*` (5 branches) | 42–45 | 2026-11-03 | Job-search ledger/scoring/rounds | stale | Overlapping; consolidate before reviewing any one |
| `gh-pages` | 3,778 | 2026-11-14 | Built site + the two broken-mermaid pages | **not review scope** | Deploy output. Excluded — but see §2 on the mermaid commits |
| `buffy/batch-close-rootcause` | 2 | 2026-10-20 | Resolver exit-time fix | **PR #749**, see `03_pr_reviews.md` | Highest-value PR in the set |
| `copilot/weather-tv-2026-11-01` | 1 | 2026-11-01 | Sci-fi TV watchlist | complete | PR #763 |

Sibling worktrees (`chill-egg`, `cooing-son`, `jet-slime`, `modern-venom`, `nova-currency`,
`salesforceagain`, `salesforceyetagain`, `shore-conkerberry`) all sit on the same five commits — the
retirement — so they add no independent review surface.

## 2. `forreviews/` on `main` (the domain repo)

Only one folder exists: `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` — 5 files, 1,036 lines.

| File | Lines | What it actually is | Verdict |
|---|---|---|---|
| `research_index.md` | 134 | Status tracker + ASCII flow diagram | Meta. Says 4 of 8 deliverables "Pending" |
| `research_plan.md` | 223 | 4-week generic research plan, no Salesforce specifics | Meta. Reusable template, not a finding |
| `crash_course.md` | 206 | Notes on the crash-course page | Digest, not analysis |
| `certifications.md` | 108 | Cert landscape | **Contains a wrong claim** — see below |
| `key_principles.md` | 365 | Design principles | Reasonable, but duplicated from the same page |

**The folder's own index contradicts its name.** It is labelled v4 and dated, but `research_index.md`
lists DevOps, Navigation, Labs, and User-Data as "⏳ Pending — next task". The one topic the track exists
for (DevOps & Release Engineering) has no file here. Anyone reading the folder name would assume v4 is
the finished synthesis; it is a foundation-phase stub.

**Wrong claim in `certifications.md`:**
> `| Specialized | ServiceNow Certified Salesforce Admin | Integration with ServiceNow workflows |`

No such credential exists. The guide itself (`devops-engineer.md`, Certifications section) says the
opposite and names the real ones: Platform Developer I, Platform App Builder, Platform Administrator II
(the credential the posting calls "Advanced Admin"). The one real DevOps-adjacent credential is
**Development Lifecycle and Deployment Architect** — which this file misses entirely while inventing a
cross-vendor cert. This is the same class of error the peer reviewer caught in two other bundles.

## 3. `forreviews_final/` in the learning repo (peer agent)

`forreviews_final/2026-11-14T030820Z_salesforceagain/` — 5 files, published to the learning repo's `main`.
Reviewed in full, and cross-referenced rather than duplicated:

| Their file | What it covers | My overlap |
|---|---|---|
| `01-guide-crossreference.md` | All 5 guides vs their bundle, with `file:line` corrections | Their crash-course heap finding — I verified it independently (§4) |
| `02-bundle-crossreference.md` | 7 bundles, 17 contested claims, authority table | Useful authority map for a merge round |
| `03-defect-register.md` | 51 defects across 8 bundles + 12 in their own | Strongest artifact of the set |
| `04-merge-plan.md` | Target structure, `<details>` convention, DoD | Directly relevant to my §05/§06 |

Their scope is the **learning repo's** bundles. Mine is the **domain repo's** review surface. No item is
duplicated: they found no branch/PR/CI defect here, and I found no bundle-content defect there.

## 4. Claims I independently verified (not taken on trust)

| Claim | Source I checked | Result |
|---|---|---|
| Async Apex heap is 25 MB, not 12 MB | `developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html` — "Total heap size … **10 MB** / **25 MB**"; "Maximum CPU time … 10,000 ms / **60,000 ms**" | **Confirmed.** The published crash course is wrong in 3 places — **lines 345, 425, 434** of `docs/salesforce/crash-course.md` (verified against `raw.githubusercontent.com`, so the numbers are the file's own). The peer bundle `salesforceagain-v4/comprehensive-devops-research.md:88` is also wrong, differently: "6 MB (2 MB async)" — the async figure is off by 12.5× |
| Callouts are 100/transaction | same page + guide (`crash-course.md` line 807) | **Confirmed.** Guide is right. The peer bundle `salesforceagain-v4/comprehensive-devops-research.md:92` says "1/transaction" — **wrong** |
| Inception provider fully retired from swarm engine registry | `api_consult.py` `PROVIDERS` diff, main vs branch | **Confirmed** — `inception` removed; 16 engines remain |
| Heap "doubles" async | arithmetic: 10→25 MB | **Wrong.** 2.5×, and the CPU figure is 6× (10,000 → 60,000 ms) |
| Docstring says "latest bar", code returns first bar | `audit_trail/universal_pick_resolver.py` line 693 docstring vs the loop comment at 705 | **Confirmed** — docstring and code disagree on `main` today |

## 5. Items that are review scope but have no artifact at all

These were found by enumerating branches/PRs and finding no write-up. They are the actual gap.

1. **`main` is red** and no `updates/` record explains it or tracks the fix. A defect that blocks every
   PR for ≥7 days with no owner is the highest-priority missing artifact.
2. **`detect-duplicate-large-blobs` is a no-op gate** — no record of that decision exists.
3. **The 6 `forreviews/` bundles in the learning repo** have no index in this repo pointing at them.
4. **The 5 `job-search-*` branches** have no consolidation note; they overlap heavily.
5. **The two mermaid commits on `wiring`** are deliberate defects with a workflow that publishes them.
   No rationale file explains why that was considered a useful test.