# Salesforce Key Principles — Planning Reference

**Worktree:** salesforceyetagain-v2  
**Date:** 2026-11-14T02:10Z  
**Source track:** Salesforce DevOps Engineer — Release Engineering Training (Scotiabank requisition 276046)  
**Related repo:** https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning  
**Live track:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/

---

## 1. Core principles (planning anchors)

| # | Principle | What it means for planning |
|---|-----------|---------------------------|
| 1 | **Git is the source of truth** | Production is a deploy target, not the source. Every metadata change flows through Git. Never edit production in Setup and "remember to copy it later." |
| 2 | **Metadata-driven deployment** | Deploys compile the payload against the target org via the Metadata API. Missing dependencies = failed deploy. The `sf` CLI is the engine; vendor UIs sit on top of it. |
| 3 | **Five-stage environment path** | Dev → QA → UAT → Pre-Prod → Prod, each with a defined sandbox type and promoter. Draw the path before discussing tools. |
| 4 | **Branching discipline** | `main` = production. `feature/<ticket>` short-lived → release branch. `hotfix/<ticket>` cut from `main`, merges to `main` + open release branch. Tag production after each deploy (`release-<date>`). |
| 5 | **CI/CD stages are tool-agnostic** | Validate → Integrate → Stage → Release in GitHub Actions / Azure DevOps / GitLab. Only the YAML header changes. |
| 6 | **Tests are a gate, not an afterthought** | Dry-run (no org change), quick deploy (applies a passed validation inside the window), real deploy. Apex requires tests; 75% coverage is the production gate. |
| 7 | **Rollback is forward deploy** | Metadata does not roll back by itself. Rollback = redeploy the last known-good tag, or reinstall the previous package version. No tag = no rollback. |
| 8 | **Banking change control** | Ticket id in commit + PR, second-person diff review, named approver ≠ author, validation id + prod deploy id, mask-complete evidence for Full sandboxes. |
| 9 | **DevOps-friendly design** | Permission sets over profile edits, one flow owner per release, tests create their own data, no hardcoded ids (use custom metadata / query), Named Credentials for callouts, bulkified Apex. |

---

## 2. Training item map (12 items → requisition 276046 lines)

1. Source of truth — metadata lifecycle in Git; Salesforce DX
2. Metadata that breaks releases — limits, dependencies, deployment constraints
3. Environments and sandboxes — Dev/QA/UAT/Pre-Prod/Prod; create/refresh; data masking
4. Branching — feature, release, hotfix
5. CI/CD — GitHub Actions, Azure DevOps, GitLab
6. DevOps tools — Gearset, Copado, AutoRABIT, or CLI equivalent
7. Conflict clinic — profiles, permission sets, record types, layouts, Flows, Apex
8. Packages — unlocked / managed
9. Tests and validation — automated testing; dry-run vs quick deploy vs real deploy
10. Releases, hotfixes, rollback — runbook template (Lab D)
11. Banking change control — audit, security, compliance artifacts
12. Design patterns you coach — DevOps-friendly design

---

## 3. Crash-course prerequisite (do first)

The DevOps track explicitly says: do the crash course first if Apex, Flow, profiles, and permission sets are still fuzzy. This workstream therefore starts with the crash course, organized as:

- Navigation & breadcrumbs (Setup paths for every admin/dev task)
- Quick-reference Setup paths (objects, security, automation, code, integration, deployment, monitoring, data)
- Labs & design (custom object + Flow, Apex trigger + test, LWC, REST callout; design patterns; system properties; OOB features)
- User management & data (users, profiles, permission sets, roles, licenses, import/export, validation rules, FLS, duplicate management, data design)
- DevOps & release engineering (the 12-item track above)

---

## 4. Work layout (this session)

Folder: `research/2026-11-14T0210Z-salesforceyetagain-v2/`

- `00_planning-salesforce-principles.md` — this file
- `01_certifications-curriculum.md` — Salesforce certifications named in the track + curricula
- `02_crash-course.md` — Salesforce crash course (navigation, Setup paths, labs, user/data, DevOps)

These will be merged in a later round against:
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/