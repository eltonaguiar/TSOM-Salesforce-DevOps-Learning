# Term index — every posting line mapped

**Merge target:** section 14 of the downstream page (term-by-term deep dive). Use this index to check coverage; use `term-entries.md` for the content.

## Responsibilities

| # | Term / posting line | Research unit | Page section |
|---|---|---|---|
| R1 | CI/CD pipelines using Git-based workflows | `04-cicd/`, entry "CI/CD pipelines" | 5, 5.1, 14 |
| R2 | Multi-environment release strategy (Dev, QA, UAT, Pre-Prod, Prod) | `01-salesforce-key-principles/release-model.md`, entry "Multi-environment strategy" | 3, 14 |
| R3 | Scheduled releases, hotfixes, emergency deployments | `01-salesforce-key-principles/release-model.md`, entry "Three release speeds" | 4, 10, 14 |
| R4 | Audit, security, compliance | entry "Audit, security, compliance" | 11, 14 |
| R5 | Metadata lifecycle using source control (Git) | `01-salesforce-key-principles/principles.md`, entry "Git and metadata lifecycle" | 1, 4, 14 |
| R6 | Sandbox strategy (creation, refresh, data masking) | entry "Sandbox strategy" | 3, 14 |
| R7 | Deployment conflicts: profiles/permission sets, record types/layouts, Flows/Apex/dependencies | entries "Permission sets vs profiles", "Record types", "Page layouts", "Flows", "Apex and triggers" | 7, 14 |
| R8 | Best practices to reduce deployment failures and rework | `01-salesforce-key-principles/principles.md`, entry "DevOps-friendly design patterns" | 12, 14 |
| R9 | Partner with Developers, Admins, QA, Platform teams | `01-salesforce-key-principles/principles.md` | What this role owns |
| R10 | DevOps-friendly design patterns | entry "DevOps-friendly design patterns" | 12, 14 |
| R11 | Release processes, runbooks, rollback | entries "Runbook and rollback", "Three release speeds" | 10, 14 |
| R12 | Audit and change management | entry "Audit, security, compliance" | 11, 14 |

## Requirements

| # | Term / posting line | Research unit | Page section |
|---|---|---|---|
| Q1 | Salesforce metadata deployments | entry "Metadata deployments" | 1, 2, 13, 14 |
| Q2 | Git-based source control | entry "Git and metadata lifecycle" | 1, 4, 14 |
| Q3 | Salesforce limits, metadata dependencies, deployment constraints | `02-limits-constraints/` (all files) | 13, 14 |
| Q4 | CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab) | `04-cicd/` (all files) | 5, 5.1, 14 |
| Q5 | Branching strategies (feature, release, hotfix) | `01-salesforce-key-principles/release-model.md`, entry "Branching" | 4, 14 |
| Q6 | Automated testing and validation | entry "Automated testing and validation" | 9, 14 |
| Q7 | Gearset, Copado, AutoRABIT, or equivalent | `03-devops-tools/` (all files) | 6, 6.1, 14 |
| Q8a | Apex and Triggers | entry "Apex and triggers" | 7, 14 |
| Q8b | Flows (before/after save) | entry "Flows" | 7, 14 |
| Q8c | Permission sets vs profiles | entry "Permission sets vs profiles" | 7, 14 |
| Q8d | Record types | entry "Record types" | 7, 14 |
| Q8e | Page layouts | entry "Page layouts" | 7, 14 |
| Q8f | Security model | entry "Security model" | 7, 14 |
| Q9 | Troubleshooting deployment failures and dependency issues | entry "Troubleshooting", `02-limits-constraints/dependencies-and-constraints.md` | 2, 13, 14 |
| Q10 | Salesforce Platform Developer experience | entry "Platform Developer experience" | 14 |
| Q11 | Unlocked packages / managed packages | entries "Unlocked packages" and "Managed packages" | 8, 14 |
| Q12 | Salesforce DX | entry "Salesforce DX" | 1, 14 |
| Q13 | Regulated / enterprise environments | entry "Regulated environments" | 11, 14 |
| Q14 | Certifications (PD1, Advanced Admin, DevOps related) | `05-certifications/` (all files) | Certifications, 14 |

## Cross-cutting terms

| Term | Where |
|---|---|
| Sandbox creation, refresh, masking | entry "Sandbox strategy"; `01-salesforce-key-principles/release-model.md` |
| Data masking | entry "Sandbox strategy"; `02-limits-constraints/other-limits-and-system-settings.md` |
| Change management / CAB | entry "Audit, security, compliance" |
| Rollback / tag | entry "Runbook and rollback" |
| Audit evidence | entry "Audit, security, compliance" |
| System settings / org properties | `02-limits-constraints/other-limits-and-system-settings.md` |
| Governor limits | `02-limits-constraints/governor-limits.md` |
| Metadata dependencies | `02-limits-constraints/dependencies-and-constraints.md` |
| Deployment constraints | `02-limits-constraints/dependencies-and-constraints.md` |
