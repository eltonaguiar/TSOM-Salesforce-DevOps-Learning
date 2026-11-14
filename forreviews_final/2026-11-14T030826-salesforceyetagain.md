# Consolidated Feedback for Salesforce DevOps Learning Research

This file cross-references all items under `forreviews/` (and related branches) with the Salesforce training guides referenced on the ServiceNow page.

## Existing items already pushed to `forreviews/` on `main`

| Path | Purpose |
|---|---|
| `2026-11-14T0210Z-salesforceyetagain-v2-README.md` | Index / README for v2 session |
| `2026-11-14T0210Z-salesforceyetagain-v2-00_planning-salesforce-principles.md` | Planning anchors, 12-item training map, crash-course prerequisite |
| `2026-11-14T0210Z-salesforceyetagain-v2-01_certifications-curriculum.md` | Certifications & curricula |
| `2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md` | Salesforce crash course |
| `2026-11-14T021036_salesforceyetagain-v3.md` | Additional v3 research |
| `2026-11-14T023241_salesforceagain-v2.md` | Salesforce research, v2 |
| `2026-11-14T023507_salesforcemore-v2.md` | Additional Salesforce research, v2 |
| `2026-11-14_salesforceagain-v3_devops-gearset-ui-deep-dive.md` | DevOps Gearset/UI deep dive |
| `2026-11-14_salesforceagain-v3_devops-github-cicd-pipeline.md` | DevOps GitHub CI/CD pipeline |
| `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md` | DevOps governor-limits deep dive |
| `2026-11-14_salesforceagain-v3_devops-metadata-dependencies-deep-dive.md` | DevOps metadata-dependencies deep dive |
| `salesforceagain-v4-2026-11-14-0230/` | v4 folder |
| `20261114-020300-salesforceagain-kilo/` | Kilo worktree folder |
| `20261114-020852-salesforcemore/` | salesforcemore folder |
| `20261114-023241-salesforceagain-v2/` | salesforceagain-v2 folder |

## Cross-reference with official Salesforce training guides

| Guide | URL | Coverage status |
|---|---|---|
| Salesforce Crash Course | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/ | Covered in `02_crash-course.md` |
| Navigation & Breadcrumbs | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/ | Referenced across planning & crash-course files |
| Labs & Design | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/ | Referenced across labs sections |
| User Management & Data | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/ | Referenced across certification & user/data files |
| DevOps & Release Engineering | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/ | Covered in the devops deep-dive files |

## Feedback / gaps to address in merge round

1. **No separate `forreviews_final/` directory exists yet** — this file creates it as the destination for consolidated output.
2. **Other branches** (e.g., `add-kilo-additional-skills`, `audit-*`, `buffy/*`, etc.) were checked but contain no additional `forreviews/` content beyond `main`.
3. **Consolidation target**: a later agent should merge all `forreviews/` items against the live pages above and produce a single organized set matching the Salesforce training guide structure.