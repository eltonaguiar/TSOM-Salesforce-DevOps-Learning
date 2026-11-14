# Vendor certifications and a study plan

**Merge target:** the Certifications section and the study-order paragraph. This file answers "what should I actually study, in what order, and what counts as evidence?"

## 1. Vendor certification landscape

| Programme | Tracks / credentials | Cost | What it proves | Caveat |
|---|---|---|---|---|
| DevOps Launchpad (Gearset) | Salesforce DevOps Fundamentals; CI/CD for Salesforce; Salesforce DevOps Leadership; Salesforce Backup; **Gearset Academy Certification** | Free | DevOps concepts and Gearset tool use | Catalogue and certificate names can change; verify on the site |
| Copado | **Copado Certified** / Copado Academy tracks | Varies | Copado pipeline, promotion, release management | The public certification URL returned 404 on 2026-11-14; verify the current name with Copado |
| AutoRABIT | **AutoRABIT Academy ARM tracks** (and related product tracks) | Varies | AutoRABIT ARM CI/CD, deployment, data, backup | Product packaging and programme names vary by edition |
| Salesforce developer/architect | PD1, PD2, Application Architect, System Architect, Technical Architect | Paid exams | Platform depth | None is a DevOps-specific credential |

**DevOps Launchpad link:** <https://devopslaunchpad.com/>

The useful, vendor-neutral tracks for this role are **Fundamentals** and **CI/CD**. The **Backup** track is directly relevant to the sandbox/backup questions. **Gearset Academy** is the tool-specific one.

## 2. What to study first

The posting is a DevOps role, not a pure developer role, so the order is:

1. **Platform fundamentals** — objects, fields, relationships, security, automation, the metadata model. If these are fuzzy, the rest is memorization. Use the crash course page and the Platform App Builder/Administrator material.
2. **PD1-level Apex** — triggers, bulkification, testing, order of execution, debug/deployment tools. You need to read code, not write a framework.
3. **Metadata API and the CLI** — retrieve, deploy, validate, test, report, packages. This is the daily tool.
4. **Git and branching** — feature/release/hotfix, pull requests, tags, conflict resolution.
5. **CI/CD** — the five-job pipeline, JWT auth, environment approvals, evidence.
6. **Limits, dependencies, constraints** — the section 13 material. This is the interview differentiator.
7. **Vendor tool** — one of Gearset/Copado/AutoRABIT, hands-on. Learn compare/deploy, CI, pipeline, backup, monitoring, audit.
8. **Regulated-environment controls** — segregation of duties, masking, change windows, emergency path, audit pack.

## 3. A 10-week plan

| Week | Focus | Evidence you can show |
|---|---|---|
| 1 | Platform fundamentals: objects, fields, relationships, security model | A data model diagram and a permission matrix |
| 2 | Automation: validation rules, Flow before/after save, order of execution | A before-save Flow and an after-save Flow, with a test plan |
| 3 | Apex: triggers, handler pattern, bulkification, recursion | A trigger + handler + test that inserts 200 records |
| 4 | Testing and limits | A test class with coverage and a bulk test; a debug log showing `Limits` output |
| 5 | Metadata API and CLI | A retrieve, a dry-run, a real deploy, a destructive change manifest |
| 6 | Git and branching | A repo with `main`, `release/*`, `feature/*`, `hotfix/*`, PR templates, tags |
| 7 | CI/CD | A GitHub Actions workflow that validates a PR and quick-deploys a validated job |
| 8 | Vendor tool | A Gearset/Copado/AutoRABIT compare, validation, pipeline, and backup screenshot (no customer data) |
| 9 | Limits/dependencies/constraints deep dive | A failure lab: missing dependency, profile conflict, inactive Flow, missing named credential |
| 10 | Regulated release simulation | A filled runbook, an audit pack, a rollback rehearsal, a mock interview |

## 4. Portfolio evidence that beats a certificate list

- A public or sanitized repo with a Salesforce DX project, a manifest, and a pipeline.
- A test class that proves bulk safety (200 records, one SOQL, one DML).
- A before/after Flow pair with a written explanation of why each is before/after.
- A permission-set design that avoids profile edits.
- A deployment runbook and a rollback plan for a fake release.
- A one-page "limits and dependencies" cheat sheet you wrote yourself.
- A vendor-tool walkthrough with screenshots from a free trial or Developer org (no customer data).

## 5. How to talk about certifications in the interview

- "I have PD1-level Apex and testing knowledge" is stronger than "I am studying for PD1" if you can show the lab.
- "Advanced Administrator is now Platform Administrator II" shows you are current.
- "There is no official Salesforce DevOps certification; I have hands-on pipeline evidence plus vendor tool time" is the honest, senior answer.
- Do not list a certificate you do not hold. Do not imply a vendor certificate is a Salesforce credential.

## 6. What to merge

**Merge:** the vendor table (with the caveat), the study order, the 10-week plan, and the portfolio evidence list.

**Compress:** the 10-week plan into a 6-step study order if the page is short.

**Do not merge:** specific prices, pass rates, or certificate names that are not verified on the vendor site at merge time.
