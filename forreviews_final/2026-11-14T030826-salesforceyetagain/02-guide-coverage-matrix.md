# 02 — Coverage matrix against the five live pages

Live pages (all under `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/`):
`crash-course/` · `navigation-breadcrumbs/` · `labs-design/` · `user-management-data/` · `devops-engineer/`

## Verdict per page

| Page | Verdict | Best artifact(s) | What is genuinely missing |
|---|---|---|---|
| crash-course | **Covered (mirror)** | flat `02` (45K) | Nothing structural. Only the corrections in `03` apply |
| navigation-breadcrumbs | **Covered, stale** | B1 `07` + flat `02` §Navigation | Release drift: Background Jobs, Environments > Sandboxes, retired PB/WFR |
| labs-design | **Covered, 2 defects + thin** | flat `02` §Labs | Labs 5–8 absent; "System Properties" table is not real; Lab 4 auth pattern wrong |
| user-management-data | **Partial** | flat `02` §User Management & Data | User lifecycle error; no MFA/SSO, no PSG muting, no permission set licenses, Duplicate Jobs |
| devops-engineer | **Exceeded** | B1, B3, B2, v3 deep dives | Precision gaps only: quick-deploy window, coverage semantics, refresh cadence |

## Section-level matrix

| Page | Section | Covered by | Status |
|---|---|---|---|
| crash-course | What Is Salesforce / Big Picture | flat `02`, B2 | OK |
| crash-course | Navigation | flat `02`, B1 `07` | OK (stale paths, C9) |
| crash-course | Users/Profiles/Roles/Security | flat `02`, B3 principles | Partial (C1, C10, C11) |
| crash-course | Data Integrity & Relationships | flat `02` | OK |
| crash-course | Automation (Flow vs Apex vs VF vs LWC) | flat `02`, B2 | OK |
| crash-course | Code (Apex/VF/LWC) | flat `02`, B2 `01` | OK (add C8) |
| crash-course | Integration (REST/SOAP) | flat `02`, B1 `03` | OK |
| crash-course | Troubleshooting & Governor Limits | flat `02`, B2 `01`, B3 limits | OK (add C4) |
| crash-course | Design Considerations | flat `02`, B3 principles | OK |
| navigation-breadcrumbs | All 10 sections | B1 `07` | OK (add C9) |
| labs-design | Labs 1–4 | flat `02` | OK (fix C6, C7) |
| labs-design | Design Considerations (layers) | flat `02`, B3 | OK |
| labs-design | System Properties | flat `02` | **DEFECT** (C2) |
| user-management-data | Users lifecycle | flat `02` | **DEFECT** (C1) |
| user-management-data | Profiles / Permission Sets | flat `02` | Partial (C11) |
| user-management-data | Roles / Sharing | flat `02`, B3 | OK |
| user-management-data | Licenses | flat `02` | Partial (C13) |
| user-management-data | Import/Export | flat `02` | OK |
| user-management-data | Validation / Record Types | flat `02` | OK |
| user-management-data | FLS / Shield | flat `02` | Partial (C8) |
| user-management-data | Duplicate Management | flat `02` | Partial (C12) |
| devops-engineer | §1–§2 Source of truth, metadata | B1 `02`, B2 `01/02`, B3 | Exceeded |
| devops-engineer | §3 Environments/sandboxes | B1, B3 | Partial (C5) |
| devops-engineer | §4 Branching | B1, B3 | Exceeded |
| devops-engineer | §5 CI/CD | B1 `04`, B2 `04` | Exceeded |
| devops-engineer | §6 Tools | B1 `03`, v3 Gearset | Exceeded (add DevOps Center detail, G11) |
| devops-engineer | §7 Conflict clinic | B1, B2, B3 | Exceeded |
| devops-engineer | §8 Packages | B1, B2 | Exceeded |
| devops-engineer | §9 Tests/validation | B1, B2, B3 | Partial (C3, C4) |
| devops-engineer | §10–§11 Releases/rollback/change control | B1 `05`, B3 | Partial (C14) |
| devops-engineer | §12 Design patterns | B3 principles | Exceeded |

## Page-side gaps (things the published pages lack that the JD tests)

1. Sandbox **refresh cadence numbers** (page says "license-limited" only).
2. **Quick-deploy window length** (page omits).
3. **Coverage semantics** for `RunSpecifiedTests` vs `RunLocalTests` vs `RunAllTestsInOrg`.
4. **Background Jobs** consolidation in Setup paths.
5. **MFA/SSO/My Domain** in user management.
6. **Permission set licenses** and **muting permission sets**.
7. **Duplicate Jobs** (existing-data dedupe) — page covers rules only.
8. **CRUD/FLS enforcement in Apex** (`with sharing` is not FLS).
9. **Backup/restore** in rollback (Git cannot restore rows).
10. **DevOps Center** work-item/promotion model (B1 `03` has it).
11. **Release freeze windows** for banking change control.
