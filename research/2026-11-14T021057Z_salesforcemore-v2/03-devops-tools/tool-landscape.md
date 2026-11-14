# DevOps tool landscape

**Merge target:** section 6 and 6.1 of the downstream page. This file explains what each tool is, what it adds over the Metadata API, and when to choose it.

## 1. The layer cake

```text
Business process: ticket, approval, change window, evidence
        ↑
Vendor platform: Gearset / Copado / AutoRABIT / DevOps Center
  - diff, dependency analysis, CI job, pipeline, approval gate,
    backup, data deployment, monitoring, audit history
        ↑
Salesforce CLI (sf) and Metadata API
  - retrieve, deploy, validate, test, package, report
        ↑
Git + CI runner (GitHub Actions, Azure DevOps, GitLab)
  - source of truth, branch protection, secrets, environments
        ↑
Salesforce orgs: Dev, QA, UAT, Pre-Prod, Prod
```

Every vendor tool is a UI and automation layer over the Metadata API. None of them replaces Git discipline, a test gate, or a rollback tag.

## 2. Tool-by-tool summary

| Tool | What it is | What it adds | What it does not replace |
|---|---|---|---|
| Salesforce CLI (`sf`) | The deploy/retrieve/test/package engine | Scriptability, CI integration, exact control over payload and flags | Git, approvals, a UI for admins |
| DevOps Center | Native Salesforce work items, Git, pipelines | No extra vendor; work-item traceability; native promotion | Vendor-grade dependency analysis, data tooling, backup |
| Gearset | Compare/deploy, CI, pipelines, backup (edition-dependent) | Org/branch diff, dependency hints, CI jobs, approval pipelines, backups, monitoring | Git as source of truth; the CLI in CI |
| Copado | User stories, pipelines, promotions, compliance | Release management, approvals, quality gates, audit evidence | Git hygiene; the Metadata API |
| AutoRABIT | CI/CD, deployment, data, backup, monitoring | CI jobs, data loader, backup/restore, org monitoring | Git hygiene; the Metadata API |
| Change Sets | Setup UI between related orgs | Nothing that scales | Diff, CLI, rollback, branch model, audit-grade evidence |

## 3. Selection matrix

| Situation | Best fit | Why |
|---|---|---|
| Large bank, multi-vendor, audit-heavy, existing Gearset | Gearset for diff/CI/pipelines + GitHub Actions for the gate | Strong diff and dependency hints; CI status checks; backup; audit history |
| Copado already licensed and release management is the priority | Copado pipelines + Git | User stories, promotions, quality gates, compliance evidence |
| AutoRABIT already licensed, data tooling is needed | AutoRABIT CI + data loader + backup | CI, data, backup, monitoring in one platform |
| No vendor budget, small team, strong CLI skills | `sf` CLI + GitHub Actions | Lowest cost, full control, but you build the UI and the audit pack |
| Native-only mandate | DevOps Center | No extra vendor; work items and pipelines; still needs Git discipline |
| Legacy org with no pipeline | Change Sets only as a documented exception | Fast for a tiny fix; not a release process |

## 4. What interviewers listen for

They are not checking whether you memorized a menu. They are checking whether you understand the division of responsibility:

- **Git** is the source of truth.
- **The CLI/Metadata API** performs the operation.
- **The vendor tool** makes the operation reviewable and repeatable.
- **The CI runner** enforces the gate.
- **The human** approves the production change.
- **The tag and the evidence** make it reversible and auditable.

A good answer: "Gearset and Copado are diff and pipeline layers over the Metadata API. I still keep Git as the source of truth, use the CLI in CI, and treat the vendor UI as the place where a human reviews the diff and promotes the change."

## 5. What to merge

**Merge:** the layer cake, the tool summary table, the selection matrix, and the division-of-responsibility answer.

**Compress:** the selection matrix if the page is short; keep the "vendor tool does not replace Git" line.
