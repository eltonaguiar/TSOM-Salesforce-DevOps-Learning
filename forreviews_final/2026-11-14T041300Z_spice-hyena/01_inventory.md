# 01 — Inventory: every entry and branch

Reviewed at `main` @ `6d0d44c`.

## 1. `forreviews/` entries on `main`

85 files across 7 folders and 11 loose files. "Words" is approximate, from `wc -w` on the markdown.

| Entry | Files | ~Words | Agent/worktree | State | Verdict |
|---|---|---|---|---|---|
| `20261114-020300-salesforceagain-kilo/` | 13 | 36,900 | `salesforceagain` (kilo) | complete | **Best-structured.** Has a JD cross-reference matrix, a source log, and its own self-correction notes. Also the source of the peer's `forreviews_final` |
| `2026-11-14T023507_salesforcemore-v2/` | 24 | 29,100 | `salesforcemore-v2` | complete | **Most self-aware.** Documents its own corrections (`08-cross-bundle-notes.md`). Has the 39 MB figure right |
| `2026-11-14T023507_salesforcemore-v2.md` | 1 | 29,900 | `salesforcemore-v2` | consolidated copy | Duplicate of the folder above in one file. Keep one |
| `20261114-020852-salesforcemore/` | 12 | 17,350 | `salesforcemore` | complete | Has the deprecated-CLI error and the 1% rule. Correct on 39 MB |
| `2026-11-14T023241_salesforceagain-v2/` | 10 | — | `salesforceagain-v2` | complete | Heap 6/12 in 4 places. Marks its own uncertainty with `[Verify]` — good instinct |
| `2026-11-14T023241_salesforceagain-v2.md` | 1 | — | `salesforceagain-v2` | consolidated copy | Duplicate. Keep one |
| `2026-11-14T023312_salesforcemore-v3/` | 8 | 6,600 | `salesforcemore-v3` | complete | Correctly flags the 400 MB and 1% figures as unverified. Best epistemic hygiene of the v3 set |
| `2026-11-14T0210Z-salesforceyetagain-v2/` | 4 | — | `salesforceyetagain-v2` | complete | Heap 6/12. Cert claim correct |
| `2026-11-14T0210Z-salesforceyetagain-v2-*.md` | 4 loose | — | `salesforceyetagain-v2` | consolidated copies | Duplicates of the folder. Keep one |
| `2026-11-14T021036_salesforceyetagain-v3.md` | 1 | — | `salesforceyetagain-v3` | loose | Single file, no folder |
| `salesforceagain-v4-2026-11-14-0230/` | 3 | — | `salesforceagain-v4` | complete | Heap "6 MB (2 MB async)" — the **only** bundle that gets the async figure wrong differently (2 MB, not 12 MB). Callouts "1/transaction". Bad flag at `:278` |

### Duplicate-pair problem

Five entries exist as **both** a folder and a single consolidated `.md` at the `forreviews/` root:

| Folder | Consolidated twin |
|---|---|
| `2026-11-14T023507_salesforcemore-v2/` | `2026-11-14T023507_salesforcemore-v2.md` |
| `2026-11-14T023241_salesforceagain-v2/` | `2026-11-14T023241_salesforceagain-v2.md` |
| `2026-11-14T0210Z-salesforceyetagain-v2/` | 4 loose `*_*.md` files |
| `20261114-020300-salesforceagain-kilo/` | contains its own `00-consolidated-review-copy.md` |

**This is the single biggest structural problem in the repo.** A reader cannot tell which is authoritative,
and a defect fixed in one copy stays live in the other. `salesforceagain-kilo` at least labels its copy
`00-consolidated-review-copy.md`; the others do not label theirs at all.

**Recommendation:** pick the folder form as canonical, delete the loose twins (they are in git history), and
add a one-line `README.md` at the `forreviews/` root naming which entry is which agent's.

## 2. Branches

| Branch | +commits vs `main` | Files | State |
|---|---|---|---|
| `research/salesforceagain-2026-11-14T020300Z` | 4 | 12 files, 3,698 insertions | Split source of the `salesforceagain-kilo` entry. **Redundant** — that entry is on `main` |
| `research/salesforcemore-v2-2026-11-14T021057Z` | 3 | 25 files, 3,189 insertions | Split source of `salesforcemore-v2`. **Redundant** — entry is on `main` |
| `research/salesforceagain-v2-20261114` | 1 | 11 files, 3,720 insertions | Split source of `salesforceagain-v2`. **Redundant** — entry is on `main` |
| `salesforceagain-v3` | 1 | 4 deep-dive files | **Redundant** — all four files are on `main` at `forreviews/2026-11-14_salesforceagain-v3_*.md`, and `main` has 33 files the branch lacks |

All four branches are pre-split sources of entries that were subsequently moved onto `main`. Verified by
`git diff --stat origin/main origin/<branch>`: every branch is *behind* `main`, with `main` carrying the same
content plus the folder organisation. None holds unique review content.

**Recommendation: delete all four.** They are the reason a reader cannot tell what is current — a stale
branch tip looks like unpublished work when it is actually superseded.

**Correction to the peer's inventory:** the peer lists `research/salesforceagain-v2-20261114` with tip `—`.
It has a valid tip (1 commit ahead). Their note would have led the merge round to skip a branch that is
nonetheless safe to delete — same conclusion, different reason, and the wrong reason is worth correcting.

## 3. The existing `forreviews_final/`

`forreviews_final/2026-11-14T030820Z_salesforceagain/` — 5 files, added in commit `6d0d44c`
("forreviews_final: cross-reference all bundles, guide pages and peer feedback").

| File | Covers | Overlap with this folder |
|---|---|---|
| `README.md` | 5 headline findings, index | Their #1 (heap) — I confirm it and add the root cause. Their #4 (1% rule) — I confirm and extend |
| `01-guide-crossreference.md` | 5 guide pages with `file:line` corrections | Their crash-course line numbers I verified independently (345, 425, 434) |
| `02-bundle-crossreference.md` | 7 bundles, 17 contested claims, authority table | Their authority map is the complement of my error-propagation map |
| `03-defect-register.md` | 51 defects across 8 bundles + 12 self-defects | **No overlap.** I did not duplicate it |
| `04-merge-plan.md` | Target page structure, `<details>` convention, DoD | My `04_publish_recommendation.md` defers to it on page structure |

**This folder adds:** the root cause of the heap conflation, the entry/branch inventory with the duplicate-pair
problem, and the error-propagation matrix. Those are structural; the peer's register is per-defect.

## 4. Guide pages (the target)

Five published pages under `docs/salesforce/` in the guide repo. I read them from
`raw.githubusercontent.com` rather than the rendered HTML, so every line number I cite is the file's own.

| Page | My finding |
|---|---|
| `crash-course.md` | **3 wrong heap figures** — lines 345, 425, 434 — plus line 85 gives a deprecated Setup path (`Setup > Monitor > Logs > Debug Logs`) while line 84 already says `Setup > Debug Logs` |
| `devops-engineer.md` | No factual errors found. 554 lines, 12 sections. The Certifications section is the authority for the cert question |
| `navigation-breadcrumbs.md` | No errors. `Deployment & DevOps` section is a single table with no masking/refresh detail — a gap, not a defect |
| `labs-design.md` | Not checked line-by-line in this pass (deferred to the peer's `01-guide-crossreference.md`) |
| `user-management-data.md` | Not checked line-by-line in this pass. The peer reports it never says "profiles do not merge", which is the one fact a release engineer needs from that page |