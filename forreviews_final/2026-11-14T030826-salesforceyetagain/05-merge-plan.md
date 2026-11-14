# 05 — Merge plan for the next agent

## Ground truth

- Published pages live in **`eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` → `docs/salesforce/*`**. This repo (`TSOM-Salesforce-DevOps-Learning`) is staging only and is **not** published.
- Do not merge the 175K / 200K / 263K "consolidated review copies" as prose. They are concatenations and will duplicate every section.
- Only `main` exists in the staging repo. No other branch carries `forreviews/` (verified: `gh-pages` and `master` return `No commit found for the ref`).

## Step order

1. **Freeze the inventory.** Copy `01-tree-inventory.md` into the merge branch; mark B1 as primary.
2. **Apply corrections first (C1–C14)** to the page text before adding anything. Cheap, high-value, no new content required.
3. **Port P0 gaps (G1–G6)** from `04-gap-register-and-additions.md`.
4. **Port P1 (G7–G10)**, then P2 if time permits.
5. **Deduplicate**: for each topic take the canonical artifact from `01` and delete the other copies from the merge branch. Never merge two versions of the same table.
6. **Add one provenance block per page**: source artifact(s) + date + confidence. The pages already use this convention — keep it.
7. **Run the QA gate** below before opening the PR.

## Canonical source map

| Target section | Take from | Do not take from |
|---|---|---|
| Principles / planning frame | B3 `salesforce-principles/` (12) | 9-anchor flat, v4 plan |
| Certifications | flat `01` (short) + B1 `06` (detail) | B2 `06`, B3 cert dir |
| Governor limits | B2 `01` | B1 `02`, v3 limits file, crash-course table |
| Metadata dependencies | B2 `02` | B1 `02`, v3 metadata file |
| DevOps tools UI | B1 `03` + v3 Gearset | B2 `03`, v4 |
| CI/CD | B1 `04` | B2 `04`, v3 CI file |
| JD term-by-term | B1 `05` | B2 `05` |
| Setup paths | B1 `07` + correction C9 | flat `02` §Navigation (stale) |
| Environment/release model | B3 `SALESFORCE_DEVOPS_DEEP_DIVE` | v4 |
| Crash course | flat `02` + C4/C6/C8/C13 | 175K / 200K copies |
| Labs | flat `02` §Labs + C6/C7 + new Labs 5–8 | — |
| User/data | flat `02` §User Management & Data + C1/C10/C11/C12 | — |

## Deprecation list (do not merge; keep for history)

- `forreviews_final/2026-11-14T030826-salesforceyetagain.md` (flat) — superseded by this folder.
- `2026-11-14T0210Z-…-README.md` — superseded.
- B5 and B7 (mirror directories), B6 after it is listed.
- The three concatenation files (175K, 200K, 263K).

## QA checklist before PR

- [ ] No page contains two versions of the same table (grep for duplicated headings).
- [ ] Every `Setup >` path is verified in an org or annotated "path may differ by release".
- [ ] Every numeric claim (75%, 10 days, 5/29 days, 800 fields) has a source or a "verify" tag.
- [ ] No invented property keys remain (C2).
- [ ] Labs run end-to-end in a free Developer Edition org.
- [ ] Banking sections name: ticket id, second reviewer, approver ≠ author, validation id, prod deploy id, mask evidence, release tag.
- [ ] Provenance block present on every page.
- [ ] No secrets, org auth files, or customer data in any example.

## Open questions for the human

1. Confirm the authoritative publishing repo is `ServiceNow_Learning_.../docs/salesforce/`.
2. Keep the 11 flat files after merge, or archive them under `forreviews/_archive/`?
3. Is a Salesforce Backup & Restore licence assumed in the bank story? It changes the rollback wording.
