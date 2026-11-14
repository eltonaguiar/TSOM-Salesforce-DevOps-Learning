# 03 — Prioritized actions for the next merge agent

Written against `origin/main` as of 2026-11-14T04:12Z. This slice is `shore-conkerberry`; sibling
`forreviews_final/` folders (salesforceagain, jet-slime, chill-egg) already cover the exhaustive
defect register and code-review findings. Read those for line-level detail; this file is the
curation checklist.

---

## P0 — Correctness on published pages (do first)

| # | File | Change | Confidence |
|---|---|---|---|
| 1 | `docs/salesforce/crash-course.md` | Verify heap limit (6/12 MB vs 10/25 MB) against the Apex Developer Guide; update table + "Heap Size" heading + "doubles to 12 MB" sentence if wrong | High that it needs checking |
| 2 | `docs/salesforce/crash-course.md` | `System Log / Apex Logs` row → `Setup > Debug Logs` | High |
| 3 | `docs/salesforce/crash-course.md` | Split the Batch Apex 200/2,000 row (batch scope vs platform-event trigger batch) | Medium |
| 4 | `docs/salesforce/labs-design.md` | Remove internal/undocumented flags from "Important System Properties" | Medium |

## P1 — Small, high-value additions

| # | File | Change |
|---|---|---|
| 5 | `docs/salesforce/user-management-data.md` | One sentence: profiles do not merge → point to DevOps conflict clinic |
| 6 | `docs/salesforce/devops-engineer.md` | Add: one deploy at a time per org; deploy ceiling; Gearset does not refresh sandboxes; debug-log leak checklist |
| 7 | `docs/salesforce/labs-design.md` | Pointer from Deployment Options to the DevOps track (retire Ant as a stopping point) |

## P2 — Repository hygiene

| # | Action | Rationale |
|---|---|---|
| 8 | Diff PR #1 against `forreviews/20261114-023241-salesforceagain-v2/`; cherry-pick any missing file; **close #1** | Content already on `main` |
| 9 | Diff PR #2 against `forreviews/2026-11-14T023507_salesforcemore-v2/`; cherry-pick any missing file; **close #2** | Content already on `main` |
| 10 | Close redundant branches: `research/salesforceagain-2026-11-14T020300Z`, `research/salesforceagain-v2-20261114`, `research/salesforcemore-v2-2026-11-14T021057Z`, `forreviews-split/salesforcemore-v2-2026-11-14T023507Z`, `salesforceagain-v3` | All substance is under `forreviews/` on `main` |
| 11 | Add a short note to `forreviews/` README-style index stating the canonical research copy is `20261114-020300-salesforceagain-kilo/00-consolidated-review-copy.md` | Stops the 7-way duplication from recurring |

## P3 — Do not do

| Don't | Why |
|---|---|
| Merge #1 or #2 as new trees | Duplicates existing `forreviews/` content |
| Add vendor click-path pages | Labels drift; page #5 already keeps them at category level |
| Publish any workflow that archives `server.key` or caches `~/.sfdx`/`~/.sf` | Credential exposure / injection |
| Repeat the "1% per class" rule | It does not exist |

---

## Definition of done

1. The four P0 corrections are applied or explicitly rejected with a source link.
2. The three P1 additions are in.
3. PRs #1/#2 closed (after diff), redundant branches closed.
4. No new research tree merged; `main` carries one canonical copy.
5. Every changed limit or path cites a primary source (developer.salesforce.com or help.salesforce.com).

---

## Hand-off note

If you are the second agent on this cross-reference: this folder
(`2026-11-14T041200Z_shore-conkerberry/`) is complete. Do not edit it. Add your own timestamped
folder. Merge-agent, read the sibling `03-defect-register.md` (salesforceagain) alongside this file —
that one has the exhaustive line-level list; this one has the branch/PR verdicts and the page redline.
