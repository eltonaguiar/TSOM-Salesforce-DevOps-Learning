# Source log

Access date for all sources: **2026-11-14**.

## Primary sources

| # | Source | URL | Used for | Confidence | Notes |
|---|---|---|---|---|---|
| S1 | Scotiabank job posting, Requisition 276046 | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> | Scope contract: responsibilities and requirements | High | Public posting; captured in `job-description.md` |
| S2 | Salesforce DevOps Engineer training page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> | Current downstream content and section structure | High | Read-only reference; merge target |
| S3 | Apex execution governors and limits | <https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html> | Governor limit tables, async limits, cross-namespace limits | High | Developer docs blocked a direct browser fetch; content retrieved via a reader proxy on 2026-11-14. Verify numbers in the current release. |
| S4 | Metadata API guide | <https://developer.salesforce.com/docs/platform/api-metadata/guide/> | Deploy/retrieve model, metadata vs data | High | The old `meta_limits.htm` URL returned 404; the current deploy limits are on the `deploy()` reference (S23) |
| S5 | Salesforce Help — Sandboxes | <https://help.salesforce.com/s/articleView?id=sf.deploy_sandboxes_parent.htm&type=5> | Sandbox types and refresh | High | Help pages are JavaScript-heavy; use the in-product Help for exact steps |
| S6 | Salesforce Help — Quick Deploy | <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> | Validate vs quick deploy | High | Same access caveat |
| S7 | Salesforce Help — Data Mask | <https://help.salesforce.com/s/articleView?id=sf.data_mask.htm&type=5> | Masking | High | Product availability varies by licence |
| S8 | Salesforce Help — DevOps Center overview | <https://help.salesforce.com/s/articleView?id=sf.devops_center_overview.htm&type=5> | Native pipeline | High | Enablement required |
| S9 | Trailhead — Platform Developer I credential | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Credential description and study trail | High | Credential page is stable; exam weights are not on the page |
| S10 | Trailhead — Platform App Builder credential | <https://trailhead.salesforce.com/credentials/platformappbuilder> | Credential description and study trail | High | Same |
| S11 | Trailhead — Platform Administrator credential | <https://trailhead.salesforce.com/credentials/platformadministrator> | Administrator prerequisite | High | The old "Administrator" credential is now Platform Administrator |
| S12 | Trailhead — Platform Administrator II credential | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Current name for Advanced Administrator | High | Requires Platform Administrator as prerequisite |
| S13 | Trailhead — Platform Developer I study trail | <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> | Curriculum domains | Medium | Trail module list loads dynamically; domains taken from the official exam outline categories |
| S14 | Trailhead — Platform App Builder study trail | <https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-platform-app-builder-certification> | Curriculum domains | Medium | Same |
| S15 | Gearset documentation | <https://docs.gearset.com/en/> | Compare/deploy, CI, pipelines, backup, monitoring | Medium–High | Public docs; UI labels vary by edition |
| S16 | DevOps Launchpad (Gearset) | <https://devopslaunchpad.com/> | Free Salesforce DevOps certificate tracks | High | Lists Fundamentals, CI/CD, Leadership, Backup, Gearset Academy |
| S17 | Copado | <https://www.copado.com/> | Pipeline, user story, promotion, compliance | Medium | Product pages; certification URL returned 404 on 2026-11-14 |
| S18 | AutoRABIT | <https://www.autorabit.com/> | CI, deployment, data, backup, monitoring | Medium | Product pages are JavaScript-heavy; module names vary by edition |
| S19 | Salesforce CLI command reference | <https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/> | `sf` commands and flags | High | Flags move; always confirm with `--help` |
| S20 | GitHub Actions documentation | <https://docs.github.com/en/actions> | Workflows, environments, secrets, approvals | High | Feature availability depends on plan |
| S21 | `sfdx-git-delta` | <https://github.com/scolladon/sfdx-git-delta> | Delta manifest generation | Medium–High | Community plugin; verify command flags |
| S22 | Salesforce Help — API usage / limits | In-product: Setup → Company Information → API Usage | Org API allocation | High | Exact allocation is edition/licence-specific; inspect your org |
| S23 | Metadata API `deploy()` reference | <https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html> | Deploy limits (≈39 MB compressed / ≈600 MB uncompressed; 10,000 / 35,000 files), one deployment at a time, queue order, five test levels | High | Limits can change without notice; re-check on merge |
| S24 | Salesforce CLI deploy messages | <https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md> | `RunRelevantTests` (Beta, API 66.0+) description and the five test levels | High | CLI messages track the current implementation |
| S25 | Gearset docs collections | <https://docs.gearset.com/en/> | Current UI groupings: My connections, Metadata deployments, Continuous delivery, Backup & archiving, Sandbox seeding & compliance, Problem analyzers, Observability, Settings | Medium–High | Labels vary by edition; article lists checked on 2026-11-14 |
| S26 | Copado platform overview | <https://www.copado.com/platform-overview> | Current branding: Copado CI/CD, Copado Essentials, Agentia, Robotic Testing, AI Platform | Medium–High | Product packaging changes; verify the bank's licence |
| S27 | AutoRABIT products | <https://www.autorabit.com/products/> | ARM (CI/CD), Vault (backup/restore), CodeScan (static analysis), Guard (security posture) | Medium–High | Product packaging changes; verify the bank's licence |

## Source-quality notes

- **Official Salesforce docs are the authority for limits and platform behaviour.** Exact numbers change; the research keeps a verify note on every table.
- **Vendor UI paths are the least stable part of this research.** Gearset, Copado, AutoRABIT, and DevOps Center rename menus between editions. The bundle gives the task, the likely navigation, what to click, and what to verify. The merge agent must keep the caveat.
- **Certification exam weights were not copied from memory.** The bundle lists domains and official study-guide links. Add percentages only from the current official exam guide PDF.
- **No internal Scotiabank process is asserted.** The bundle describes a defensible regulated-environment pattern, not the bank's actual runbook.
- **No secrets or customer data.** None is included.
