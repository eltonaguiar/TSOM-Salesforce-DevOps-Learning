# Job description — Scotiabank Requisition 276046

**Merge target:** page header + JD coverage matrix. Do not paste the whole posting into the page; use it as the scope contract.

**Source:** <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/>
**Captured:** 2026-11-14.

## Header facts

| Field | Value |
|---|---|
| Title | DevOps Engineer (Salesforce) |
| Requisition ID | 276046 |
| Team | Commercial Banking Engineering |
| Location | Canada: Ontario: Toronto (M5H 1A1) |
| Focus | Salesforce release, deployment, and environment management; CI/CD; automation; platform reliability |

## Role summary (verbatim)

> The Commercial Banking Engineering team is seeking a Salesforce DevOps Engineer who will be responsible for ideation support, design, development, and implementation of software to ensure continuous improvement and evolution in the CB Salesforce ecosystem.
>
> We are looking for a Salesforce DevOps Engineer to own and evolve our Salesforce release, deployment, and environment management processes. This role sits at the intersection of Salesforce development, CI/CD, automation, and platform reliability, and plays a critical role in enabling fast, safe, and scalable Salesforce releases in an enterprise environment.
>
> The ideal candidate has hands on experience with Salesforce metadata deployments, DevOps tooling, and environment strategy, and can collaborate effectively with developers, admins, QA, and security teams.

## Responsibilities (verbatim bullets, numbered for mapping)

| ID | Bullet |
|---|---|
| R1 | Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows |
| R2 | Manage multi environment release strategies (Dev, QA, UAT, Pre Prod, Prod) |
| R3 | Coordinate scheduled releases, hotfixes, and emergency deployments |
| R4 | Ensure deployment activities follow audit, security, and compliance standards |
| R5 | Manage Salesforce metadata lifecycle using source control (Git) |
| R6 | Handle sandbox strategy (creation, refresh, data masking) |
| R7 | Resolve deployment conflicts related to: Profiles and Permission Sets; Record Types & Page Layouts; Flows, Apex, and dependencies |
| R8 | Recommend best practices to reduce deployment failures and rework |
| R9 | Partner with Salesforce Developers, Admins, QA, and Platform teams |
| R10 | Provide guidance on DevOps friendly Salesforce design patterns |
| R11 | Document release processes, runbooks, and rollback procedures |
| R12 | Support audit and change management requirements |

## Requirements (verbatim bullets, numbered for mapping)

| ID | Bullet |
|---|---|
| Q1 | Strong experience with Salesforce metadata deployments |
| Q2 | Experience with Git based source control |
| Q3 | Understanding of Salesforce limits, metadata dependencies, and deployment constraints |
| Q4 | Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab, etc.) |
| Q5 | Understanding of branching strategies (feature, release, hotfix) |
| Q6 | Familiar with automated testing and validation concepts |
| Q7 | Hands on experience with Salesforce DevOps tools such as: Gearset, Copado, AutoRabit, or equivalent |
| Q8 | Good understanding of: Apex & Triggers; Flows (Before/After Save); Permission Sets vs Profiles; Record Types, Page Layouts, and Security model |
| Q9 | Ability to troubleshoot deployment failures and dependency issues |
| Q10 | Salesforce Platform Developer experience |
| Q11 | Experience with Unlocked Packages / Managed Packages |
| Q12 | Exposure to Salesforce DX |
| Q13 | Experience in regulated or enterprise environments (banking, insurance, healthcare) |
| Q14 | Salesforce certifications (PD1, Advanced Admin, DevOps related certs) |

## Mapping table

| Requirement | Research file | Downstream page section |
|---|---|---|
| R1, Q4 | `04-cicd/github-actions-salesforce.md`, `04-cicd/auth-secrets-environments.md`, `04-cicd/other-ci-platforms.md` | 5, 5.1 |
| R2, R3 | `01-salesforce-key-principles/release-model.md`, `06-term-deep-dives/term-entries.md` | 3, 4, 10 |
| R4, R12 | `06-term-deep-dives/term-entries.md`, `04-cicd/auth-secrets-environments.md` | 11 |
| R5, Q2 | `01-salesforce-key-principles/principles.md`, `06-term-deep-dives/term-entries.md` | 1, 4 |
| R6 | `02-limits-constraints/other-limits-and-system-settings.md`, `06-term-deep-dives/term-entries.md` | 3 |
| R7, Q8 | `03-devops-tools/`, `06-term-deep-dives/term-entries.md` | 7 |
| R8, R10 | `01-salesforce-key-principles/principles.md`, `06-term-deep-dives/term-entries.md` | 12 |
| R9 | `01-salesforce-key-principles/principles.md` | What this role owns |
| R11 | `06-term-deep-dives/term-entries.md` | 10 |
| Q1 | `02-limits-constraints/dependencies-and-constraints.md` | 1, 2, 13 |
| Q3 | `02-limits-constraints/` (all files) | 13 |
| Q5 | `01-salesforce-key-principles/release-model.md` | 4 |
| Q6 | `04-cicd/github-actions-salesforce.md` | 9 |
| Q7 | `03-devops-tools/` (all files) | 6, 6.1 |
| Q8 | `06-term-deep-dives/term-entries.md` | 7, 14 |
| Q9 | `02-limits-constraints/dependencies-and-constraints.md`, `02-limits-constraints/inspection-and-drills.md` | 2, 13 |
| Q10 | `06-term-deep-dives/term-entries.md` | 14 |
| Q11 | `06-term-deep-dives/term-entries.md` | 8, 14 |
| Q12 | `06-term-deep-dives/term-entries.md` | 1, 14 |
| Q13 | `06-term-deep-dives/term-entries.md` | 11, 14 |
| Q14 | `05-certifications/` | Certifications, 14 |

## What the posting does not say

The posting does not name a specific CI vendor, source-control host, sandbox licence tier, or internal change-management tool. Do not invent them. The page should present a defensible pattern and say that the team's written procedure wins where it differs.
