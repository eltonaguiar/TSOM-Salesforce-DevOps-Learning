# 04 — Gap register + ready-to-paste additions

## Gap register

| ID | Gap | Where it belongs | Priority |
|---|---|---|---|
| G1 | Labs 5–8 (security/FLS lab, Flow fault-path lab, CI delta-deploy lab, rollback drill) | labs-design | P0 |
| G2 | Sandbox refresh cadence + refresh rules | devops-engineer §3 | P0 |
| G3 | Coverage semantics (3 rules) | devops-engineer §9, crash-course governor limits | P0 |
| G4 | Setup path drift (Background Jobs, Environments > Sandboxes, retired PB/WFR) | navigation-breadcrumbs | P0 |
| G5 | User lifecycle 4-state correction | user-management-data | P0 |
| G6 | MFA / SSO / My Domain / integration users | user-management-data | P0 |
| G7 | Permission Set Licenses + muting permission sets | user-management-data, crash-course security | P1 |
| G8 | Duplicate Jobs + bypass header | user-management-data | P1 |
| G9 | CRUD/FLS enforcement in Apex | crash-course code, user-management-data | P1 |
| G10 | Backup & Restore in rollback | devops-engineer §10 | P1 |
| G11 | DevOps Center work-item/promotion model | devops-engineer §6 | P2 |
| G12 | Release calendar / freeze windows for banking | devops-engineer §10–11 | P2 |

## Paste-ready A — sandbox cadence

| Sandbox | Data | Documented refresh interval | Typical use |
|---|---|---|---|
| Developer | metadata only | 1/day | build |
| Developer Pro | metadata only, more storage | 1/day | QA without rows |
| Partial Copy | template sample | every 5 days | UAT |
| Full | all prod data | every 29 days | Pre-Prod, performance |

Rules: refresh source is production, never another sandbox; refresh replaces sandbox content; unmasked Full is customer data (mask before broad login); the next-eligible date is visible in Setup before you commit a date.

## Paste-ready B — path drift

| Older path in the notebook | Current path | Note |
|---|---|---|
| Setup > Apex Jobs | Setup > Background Jobs | Apex Jobs, Batch Jobs, Scheduled Jobs, Flex Queue |
| Setup > Scheduled Jobs | Setup > Background Jobs | same |
| Setup > Sandboxes | Setup > Environments > Sandboxes | quick-find "Sandboxes" still works |
| Setup > Process Builder | retired | migrate to Flow |
| Setup > Workflow Rules | retired | migrate to Flow |

## Paste-ready C — Labs 5–8 (outlines)

**Lab 5 — Security.** Create permission set `CB_Release_Reader` (read Account); set FLS on a sensitive field to hidden; assign to a test user; prove the field is invisible in the UI **and** through the API. Then add a muting permission set inside a PSG and show the subtraction.

**Lab 6 — Flow fault path.** Record-triggered flow with a fault connector → custom error or email. Write a Flow Test (or an Apex test invoking the flow) and assert the fault path executes.

**Lab 7 — CI delta deploy.** GitHub Actions job: retrieve against a CI sandbox, run `sf project deploy start --dry-run --test-level RunLocalTests`, fail the PR on red, write the deploy id into the job summary.

**Lab 8 — Rollback drill.** Tag a release, deploy a deliberately bad change to a sandbox, activate the previous Flow version, then forward-deploy the tag; fill the runbook entries.

## Paste-ready D — user lifecycle (replaces the wrong row)

| State | Can log in | Licence | Reversible | When to use |
|---|---|---|---|---|
| Active | yes | held | — | normal |
| Frozen | no | held | yes (unfreeze) | leave of absence, investigation |
| Deactivated | no | freed | yes (reactivate) | departure; keeps history/ownership |
| Deleted user record | no | freed | no | only via hard-delete process; avoid |

## Paste-ready E — MFA/SSO block

Salesforce requires MFA for all interactive logins (enforced since Feb 2022). My Domain is a prerequisite for SAML/OIDC SSO. Integration users are API-only and exempt from interactive MFA, so they must authenticate with a connected app + JWT bearer flow (or equivalent) and a least-privilege permission set; they must never be a shared human admin.

## Paste-ready F — FLS in Apex

`with sharing` enforces record-level sharing only. It does not enforce object/field permissions. Enforce with `WITH SECURITY_ENFORCED` in SOQL, `Security.stripInaccessible()` before DML, or explicit `Schema.sObjectType.X.fields.Y.isAccessible()` checks. `without sharing` must be justified in review.

## Paste-ready G — coverage block

Production Apex deploys require tests. Org-wide coverage must be ≥ 75% (`RunLocalTests` / `RunAllTestsInOrg`). With `RunSpecifiedTests`, the named tests must cover each deployed class/trigger at ≥ 75%. Any trigger at 0% fails the deploy. Quick deploy reuses a successful validation for up to 10 days if nothing changed.
