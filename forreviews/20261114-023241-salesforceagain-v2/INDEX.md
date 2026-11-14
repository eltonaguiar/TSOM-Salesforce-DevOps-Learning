# Tracking Index — `salesforceagain-v2`

| Field | Value |
|---|---|
| **Worktree / agent** | `salesforceagain-v2` |
| **Run timestamp (UTC)** | 2026-11-14T02:32:41Z |
| **Canonical run folder** | `research/20261114T021017Z-salesforceagain-v2/` |
| **Pull request** | [#1](https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning/pull/1) |
| **Consolidated single-file copy** | [`../2026-11-14T023241_salesforceagain-v2.md`](../2026-11-14T023241_salesforceagain-v2.md) |
| **Status** | Round 1 research — ready for review/merge |

This subfolder tracks the split, per-topic research for the Salesforce DevOps Engineer role (Scotiabank requisition 276046). The single-file version at the parent level is the quick-review copy; this folder is the editable source with per-file provenance.

## Files (reading order)

| # | File | Covers |
|---|---|---|
| 1 | `README.md` | Run manifest: scope, confidence, merge destinations, known gaps |
| 2 | `PLAN.md` | Structured approach + 7 Salesforce key principles |
| 3 | `01-limits-governors-and-system-properties.md` | Governor limits (sync/async), API/Metadata limits, org capacity, system properties, monitoring |
| 4 | `02-metadata-dependencies-and-deployment-constraints.md` | Dependency graph, deploy order, failure catalogue, profiles/record types/layouts/Flows/Apex, destructive changes |
| 5 | `03-devops-tools-ui-walkthroughs.md` | Gearset / Copado / AutoRABIT / DevOps Center: where to click for compare, deploy, backup, rollback, promote |
| 6 | `04-cicd-github-salesforce.md` | Full GitHub Actions pipeline: JWT auth, delta deploys, PR validation, approvals, quick deploy, rollback |
| 7 | `05-jd-term-by-term.md` | Every requisition line decoded into definition + configuration variations + interview answer |
| 8 | `06-certifications-and-curriculum.md` | PD1, Platform Administrator II (ex-Advanced Admin), Development Lifecycle & Deployment Architect, vendor certs, 8-week plan |
| 9 | `sources.md` | Provenance and access caveats |

## Merge notes

- Intended for the published `docs/salesforce/devops-engineer/` track, under existing anchors (`#6-devops-tools`, `#2-metadata-that-breaks-releases`, etc.).
- Values marked `[Verify]` are edition/version-dependent; confirm against current official Salesforce docs before publishing.
- Certification domain weights are intentionally omitted pending the current official exam guide.
- No secrets, customer data, org IDs, or tokens.

## Conventions

See the repo-level [`CONTRIBUTING.md`](../../CONTRIBUTING.md) for folder naming and commit rules.
