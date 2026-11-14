# Salesforce DevOps Deep Dive — Bundle `salesforcemore-v3`

| Field | Value |
|---|---|
| **Worktree / agent** | `salesforcemore-v3` |
| **Created (UTC)** | 2026-11-14T02:33:12Z |
| **Branch** | `forreviews/salesforcemore-v3-2026-11-14T023312Z` |
| **Target role** | DevOps Engineer (Salesforce), Scotiabank, Requisition 276046, Commercial Banking Engineering, Toronto |
| **Primary JD source** | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| **Cross-referenced page** | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| **Merge target** | `docs/salesforce/devops-engineer/` and sibling Salesforce guides on the published site |
| **Status** | Round-1 research — ready for review/merge |
| **Confidence** | High on platform mechanics, limits, and CI/CD design; **medium/low on exact vendor UI labels** (they change by edition and monthly release — each click-path is tagged and must be verified in-tenant before publishing) |

> This bundle is written to be merged, not published as-is. Every limit and UI path that could be
> edition- or release-dependent is tagged `[Verify]`. No secrets, tokens, org IDs, or customer rows appear here.

## Contents

| File | Covers | Merge destination |
|---|---|---|
| `01-jd-crossref-and-gaps.md` | JD ↔ published page matrix, corrections to carry into merge | Top of `devops-engineer/` + merge notes |
| `02-devops-tools-walkthroughs.md` | Gearset / Copado / AutoRABIT / `sf` CLI practical paths | `devops-engineer/#6-devops-tools` |
| `03-github-cicd-salesforce.md` | Stage model, rationale, two full workflows, anti-patterns | `devops-engineer/#5-cicd` |
| `04-limits-dependencies-constraints.md` | Governor limits, Metadata API caps, dependency graph, system settings | `devops-engineer/#2` + `#9`; link from crash course |
| `05-jd-term-deep-dives.md` | Term-by-term decoder for the JD | `devops-engineer` throughout |
| `06-certifications-curriculum.md` | Credential mapping, corrections, study order | `devops-engineer/#certifications` |
| `sources.md` | Every source + verification status | Merge bibliography |

## What this bundle adds over the other `forreviews/` copies

1. **UI path confidence grading** — every vendor click-path is labeled so the merge never publishes a guessed button name as fact.
2. **Exact limit tables** — governor limits, per-org/per-24h caps, and Metadata API deployment caps, tied to *what breaks a deploy*.
3. **A concrete metadata-dependency graph** — failure string → root cause → ordered fix.
4. **Two production-shaped GitHub Actions workflows** (delta PR validation + prod quick deploy) with the "why" behind each stage.
5. **Certification curriculum** including the *Development Lifecycle and Deployment Architect* credential that actually matches this JD.

## Rules followed

- Append-only within this folder; the merge round owns consolidation.
- No secrets, tokens, org IDs, or customer data.
- Every number that is edition/release-dependent is flagged `[Verify]`.
