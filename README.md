# TSOM-Salesforce-DevOps-Learning

Learning resources and training items for the **Salesforce DevOps Engineer** role at Toronto School of Management (TSOM) / Scotiabank.

## Research workspace convention

Research is append-only and agent-scoped.

- Each run creates `research/<UTC timestamp>_<worktree>/`, for example `research/2026-11-14T021057Z_salesforcemore-v2/`.
- Never edit or delete another agent's folder. Add a new folder for a new round.
- Every bundle must contain:
  - `README.md` — scope, status, what to merge, what not to merge.
  - `PLAN.md` — the structured approach and open questions.
  - `00-source-log/SOURCES.md` — URLs, access date, and confidence.
  - `07-merge/merge-map.md` — research file → target page section.
- Facts that can change (exam weights, vendor UI labels, platform limits) carry a "verify at time of use" note.
- No secrets, customer data, org auth files, or customer identifiers.

## Research bundles

| Bundle | Worktree | Scope |
|---|---|---|
| [`2026-11-14T021057Z_salesforcemore-v2`](research/2026-11-14T021057Z_salesforcemore-v2/) | `salesforcemore-v2` | Salesforce DevOps Engineer (Scotiabank requisition 276046): JD analysis, Salesforce key principles, governor/platform limits, system settings, metadata dependencies, deployment constraints, Gearset/Copado/AutoRABIT/DevOps Center click-paths, GitHub Actions CI/CD, certifications and curricula, term-by-term deep dives, and a merge map for the docs site. |

## Merge target

The downstream guide is [Salesforce DevOps Engineer — Release Engineering Training](https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/). The sibling pages are the crash course, navigation breadcrumbs, labs/design, and user/data guides under `docs/salesforce/` in the `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` repository.
