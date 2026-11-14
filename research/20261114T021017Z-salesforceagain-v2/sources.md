# Sources, Access Notes, and Verification Status

**Compiled:** 2026-11-14
**Rule:** every claim that is time-sensitive or edition-dependent is either linked here or explicitly flagged in the file. If a source was blocked, that is recorded rather than hidden.

---

## 1. Primary sources

| # | Source | Used for | Access |
|---|---|---|---|
| 1 | Scotiabank requisition 276046 — <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> | The job description verbatim; all JD decoding in `05` | OK |
| 2 | Published DevOps track — <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> | Cross-reference, anchors, existing structure to extend | OK |
| 3 | Published crash course — <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/> | Understanding what already exists (so this drop adds depth, not duplication) | OK |

---

## 2. Salesforce platform documentation

| Source | Used for | Access / caveat |
|---|---|---|
| Apex Developer Guide — Execution Governors and Limits | Canonical governor limits in `01` | **403 to automated fetch.** Values written from platform knowledge; verify at <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm> |
| Salesforce App Limits Cheat Sheet | Limit taxonomy in `01` | **403 to automated fetch.** Verify at <https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/> |
| Metadata API Developer Guide | Deploy constraints, destructive changes | **403 to automated fetch.** Verify limits and component ceilings before publishing hard numbers |
| Salesforce Help — Limits Quick Reference | Org capacity limits | **JS-only / returned loading shell.** Verify in-org via Setup > Company Information |
| Salesforce Help — Sandboxes / Sandbox Templates / Data Mask | Environment strategy in `05` A6 | Linked in published track; verify edition gating in your org |
| Salesforce Help — Quick Deploy | 10-day quick-deploy window in `01`/`04` | Verify at <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> |
| Salesforce Help — Promote Work Items Through Your Pipeline | DevOps Center promotion in `03` | OK via help article mirror/search |
| DevOps Center Developer Guide | Promotion model, bundles, data model | <https://developer.salesforce.com/docs/platform/devops-center-dev/guide/devops-center-dev-promotions.html> |
| Salesforce Developers Blog — Get Started with DevOps Center | Enabling, hybrid teams, combining work items | <https://developer.salesforce.com/blogs/2022/06/get-up-and-running-with-devops-center-today> |

> **Why the 403s matter:** Salesforce's developer docs and Help site actively block automated fetches. The numbers in `01` are the widely documented canonical values, but a merge agent MUST spot-check the current official pages before publishing exact ceilings (especially component counts, package sizes, and per-24h async caps).

---

## 3. DevOps tool sources

### Gearset

| Source | Used for |
|---|---|
| <https://docs.gearset.com/en/articles/2934192-a-sample-source-driven-development-workflow-for-salesforce> | 7-step workflow (branch → refresh → compare → PR → CI → validation → monitoring) in `03` §2 |
| <https://gearset.com/blog/how-to-deploy-flows-in-salesforce/> | Flow Navigator, comparison filters in `03` §2.4 |
| <https://gearset.com/blog/deploy-lightning-page-in-salesforce/> | Lightning page deploy steps in `03` |
| <https://gearset.com/blog/how-to-deploy-salesforce-reports-and-dashboards/> | Compare/deploy report flow |
| <https://gearset.com/video/scaling-salesforce-development-with-ci-cd> | Manual compare → pipeline maturity |
| <https://gearset.com/salesforce-administrator/> | Capability map (compare/deploy, data, source control, backup) |

**Caveat:** Gearset's Help Center article URLs changed during research (some 404). The paths above resolved via search results; treat UI labels as typical, not guaranteed.

### Copado

| Source | Used for |
|---|---|
| <https://trailhead.salesforce.com/content/learn/modules/salesforce-devops-with-copado/let-innovation-flow-with-continuous-delivery> | Pipeline/promotion concepts |
| <https://www.copado.com/resources/blog/salesforce-ci-cd-best-practices-build-run-test-cddd> | CI/CD best practices |
| <https://docs.essentials.copado.com/en/articles/6935764-best-practices-with-copado-essentials-plus> | Git + CI jobs, back-promotion |
| <https://helpmetest.com/blog/copado-cicd-pipeline-salesforce> | Pipeline connections, branch strategy, quality gates |
| <https://www.copado.com/resources/blog/successful-salesforce-deployment-best-practices-checklist-cddd> | Deploy ordering (objects → Apex → profiles → sharing) |

### AutoRABIT

| Source | Used for |
|---|---|
| <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/deployment-rollback> | Rollback requires "Take Backup"; deployment history |
| <https://knowledgebase.autorabit.com/product-guides/vault-1/vault-features/backup> | Vault backup capabilities |
| <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/backup/start-the-backup> | Full vs incremental backup steps |
| <https://knowledgebase.autorabit.com/fundamentals/what-we-do> | ARM / CodeScan / Vault / Guard product map |
| <https://www.autorabit.com/> | DevSecOps positioning |

### DevOps Center

| Source | Used for |
|---|---|
| <https://hicglobalsolutions.com/blog/devops-center-setup-and-deployment> | Setup → project → pipeline → work item → promote walkthrough |
| <https://www.salesforceben.com/complete-guide-to-salesforce-devops-center-how-to-get-started/> | Enable, permission sets, bundling stage, promotion |
| <https://salesforcedictionary.com/how-to/devops-center> | Gotchas (GitHub-first, unsupported metadata, conflicts resolved in Git) |
| <https://www.dreaminforce.com/salesforce-devops-center-quick-setup-example> | Promotion flow |
| <https://help.salesforce.com/s/articleView?id=platform.devops_center_work_items_promote.htm&type=5> | Promotion limits/guidance |

---

## 4. CI/CD references

| Source | Used for |
|---|---|
| <https://tech.robotpayment.co.jp/entry/2025/08/28/070000> | PR-triggered `sf project deploy validate`, JWT auth pattern |
| <https://medium.com/@AmritWritesHere/step-by-step-how-to-set-up-ci-cd-for-salesforce-using-git-and-github-actions-60e1851b0e2e> | JWT + changed-file deploy |
| <https://soomjeetsahoo.medium.com/implementing-salesforce-ci-cd-with-github-actions-to-validate-deploy-checks-with-pmd-e7a280e46c71> | `sfdx-git-delta`, PMD, `.gitignore` |
| <https://blog.beyondthecloud.dev/blog/simple-salesforce-cicd> | Scratch org CI, auth URL |
| <https://www.kylecapehart.com/posts/github-actions> | `sf org login sfdx-url`, branch protection |
| <https://1sync.co/blog/build-salesforce-deployment-pipeline-with-github-actions> | Branch→environment pipeline |
| <https://qiita.com/krile136/items/01b891fa6cff69bf55ee> | Full vs delta deploy patterns, revert-on-failure |

**Caveat:** all pipeline YAML in `04` is a **reference implementation**, not a copy of any single article. CLI flags must be verified with `sf <cmd> --help` in the target CLI major before publishing.

---

## 5. Certification sources (verified 2026-11-14)

| Credential | URL | Verified |
|---|---|---|
| Platform Developer I | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Page loaded; exam code `Plat-Dev-201` |
| Platform Administrator II | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Page loaded; prerequisite + exam code `Plat-Admn-301` |
| Platform Administrator | <https://trailhead.salesforce.com/credentials/platformadministrator> | Linked from Admin overview |
| Platform App Builder | <https://trailhead.salesforce.com/credentials/platformappbuilder> | Linked from credential pages |
| Platform Developer II | <https://trailhead.salesforce.com/credentials/platformdeveloperii> | Linked from PD1 page |
| Platform Development Lifecycle and Deployment Architect | <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect> | Page loaded; exam code `Plat-Arch-202` |
| Architect overview | <https://trailhead.salesforce.com/credentials/architectoverview> | Linked from credential pages |
| Verification/maintenance | <https://trailhead.salesforce.com/credentials/verification> | Linked from all pages |

**Not stated:** domain weights. Trailhead credential pages are JS-rendered and do not expose the exam guide outline to fetches; the official exam guide PDF is the authority.

---

## 6. Claims that require a re-check before publishing

| Claim | File | Why |
|---|---|---|
| Exact component-count / package-size deployment ceilings | `01` §6.1 | Salesforce docs blocked; edition-dependent |
| Per-24h async execution caps | `01` §4.5 | Changes by release |
| API request formula and payload sizes | `01` §5 | Edition-dependent; confirm entitlement |
| Sandbox refresh intervals | `05` A2 | Licence-dependent |
| Vendor UI labels and edition gating | `03` | Changes by release |
| `sf`/`sgd` CLI flags | `04` | Drift between CLI majors |
| Certification domain weights | `06` | Must come from current official exam guide |

---

## 7. Deliberate omissions

- **No customer data, org IDs, tokens, or endpoints.**
- **No vendor pricing** — commercial and volatile.
- **No screenshots** — text-only round; a diagram pass is a round-2 task.
- **No invented exam percentages.**
