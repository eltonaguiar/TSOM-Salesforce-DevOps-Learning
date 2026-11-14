# Salesforce DevOps Learning — Agent Work Plan

**Worktree/session:** salesforcemore  
**Date-time stamp:** 20261114-020852  
**Folder:** `20261114-020852-salesforcemore/`  
**Source repo (skeleton):** https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning  
**Canonical content (GitHub Pages):** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/  
**Job cross-reference:** Scotiabank DevOps Engineer (Salesforce), Req 276046, Toronto

## Purpose
Capture research, plans, and certification curricula in a date-time stamped, worktree-unique folder so a later agent can merge and organize this work against the GitHub Pages variation pages (Salesforce guides: Crash Course, Navigation & Breadcrumbs, Labs & Design, User Management & Data, DevOps & Release Engineering).

## Phase structure

1. **Planning (this file)** — Salesforce key principles that frame all research.
2. **Source capture** — pull the GitHub Pages Salesforce variation pages + the GitHub repo README into `source-capture/`.
3. **Certification research** — PD1, Platform App Builder, Platform Administrator II (Advanced Admin) curricula into `certification-research/`.
4. **Salesforce key principles deep dive** — limits, metadata model, security, integration, deployment into `salesforce-principles/`.
5. **Handoff** — `merge-against-pages/` holds a mapping matrix showing where each research item maps onto each variation page, ready for the merge agent.

## Salesforce key principles (planning frame)

These principles guide what research to prioritize and how to organize it:

- **Metadata-driven platform:** Everything configurable is metadata (objects, fields, flows, profiles, permission sets). Code (Apex, LWC, Visualforce) is metadata too. Deployments move metadata between orgs via Metadata API / Salesforce CLI / tooling API.
- **Org is not source of truth:** Git is the source of truth; orgs (Dev/QA/UAT/Pre-Prod/Prod) are deploy targets. Drift = incident.
- **Multi-tenant governor limits:** Per-transaction caps on SOQL, DML, CPU, heap, callouts. Release engineering must enforce bulkification and 200-record testing.
- **Security model layers:** Object permissions, field-level security, sharing rules, profiles vs permission sets, roles. Permission sets > profile edits for merge safety.
- **Deployment constraints:** Atomic-ish Metadata API deploys, dependency ordering, one deploy per org at a time, quick-deploy 10-day window, managed packages immutable, destructive changes explicit.
- **Testing as gate:** 75% org-wide coverage for prod Apex deploys; tests create their own data; `RunSpecifiedTests` / `RunLocalTests` / `RunAllTestsInOrg`.
- **Change control in regulated env:** Ticket ID in commit/PR, non-author approver, deploy IDs logged, rollback tag, sandbox masking for PII.

## Deliverables by folder

| Folder | Contents |
|--------|----------|
| `salesforce-principles/` | Key principles deep dives (metadata model, governor limits, security, deployment constraints, integration patterns) |
| `certification-research/` | PD1, Platform App Builder, Platform Administrator II exam guides + skill weights + study mapping |
| `source-capture/` | Raw fetched pages: devops-engineer, crash-course, navigation-breadcrumbs, labs-design, user-management-data, GitHub repo README |
| `merge-against-pages/` | Mapping matrix: research item → variation page section, with merge notes |

## Certification scope (per job posting)

- Platform Developer I (PD1) — Apex, tests, platform model
- Platform App Builder — objects, Flow, security metadata
- Advanced Admin → renamed Platform Administrator II — security, change, environments
- "DevOps related certs" — no official Salesforce DevOps cert; vendor certs (Copado/Gearset/AutoRabit) show tool time only

## Merge targets (variation pages)

1. https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/ (DevOps & Release Engineering)
2. https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/ (Crash Course)
3. https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/ (Navigation & Breadcrumbs)
4. https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/ (Labs & Design)
5. https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/ (User Management & Data)
6. Index/guide hub pages under /docs/salesforce/
