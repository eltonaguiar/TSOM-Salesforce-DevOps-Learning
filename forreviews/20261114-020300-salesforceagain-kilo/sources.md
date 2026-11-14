# Sources

All URLs accessed **2026-11-14 (UTC)** unless stated. Confidence tags follow `00-plan.md` §6.

---

## 1. Job and target page

| # | Source | Type | Confidence |
|---|---|---|---|
| S1 | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> — Requisition 276046, DevOps Engineer (Salesforce), Commercial Banking Engineering, Toronto | Primary | `verified` |
| S2 | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> — published training page | Primary | `verified` |
| S3 | `docs/salesforce/devops-engineer.md` (554 lines, commit `5bf3887`) read from the ServiceNow_Learning worktree `/home/eaguiar2015/wt-sf-devops` | Primary (source) | `verified` |
| S4 | `docs/salesforce/navigation-breadcrumbs.md` — Setup path conventions used by this repo | Primary (source) | `verified` |
| S5 | `docs/salesforce/crash-course.md` — source of the async-heap correction | Primary (source) | `verified` |
| S6 | <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM> — repository that publishes the target page | Primary | `verified` |
| S7 | <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> — this research repository | Primary | `verified` |

---

## 2. Salesforce platform documentation

Fetched through the `r.jina.ai` text-extraction proxy, because `help.salesforce.com` is a
client-rendered application that cannot be scraped as static text. The underlying Salesforce URLs
are listed so the merge round can re-verify in a browser.

| # | Source | Used for | Confidence |
|---|---|---|---|
| S10 | <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm> → *Execution Governors and Limits* | All governor limits, per-transaction and per-org; callout/query/code limits; certified-package namespace limits | `verified` |
| S11 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm> → *Deploying Metadata Using the Metadata API* | Deploy payload ceilings (≈39 MB / ≈600 MB / 10,000 / 35,000 files); one-deploy-at-a-time and non-FIFO queue; Deployment Status charts; 30-day history; cancellation semantics; `checkOnly`; destructive changes; required permissions | `verified` |
| S12 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_retrieve.htm> | Retrieve limits; Big Object index requirement | `verified` |
| S13 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_running_tests.htm> → *Running Tests in a Deployment* | The exact metadata-type list that forces all local tests to run; API 33.0/34.0 behaviour change | `verified` |
| S14 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_run_relevant_tests.htm> → *Run Relevant Apex Tests in a Deployment (Beta)* | `RunRelevantTests`; `@IsTest(critical=true)`; `@IsTest(testFor='…')`; per-class 75% | `verified` |
| S15 | <https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm> → *API Request Limits and Allocations* | Concurrent and 24-hour API allocations; timeout; `DebuggingHeader` allocation; managed-package calls counting; monitoring surfaces; overage policy | `verified` |
| S16 | <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> — Quick Deploy | Referenced for the quick-deploy concept | **Not retrievable** — client-rendered. Quick-deploy behaviour is instead sourced from S11 + S14 + the CLI source in §3 |
| S17 | <https://help.salesforce.com/s/articleView?id=sf.deploy_sandboxes_parent.htm&type=5> — Sandboxes | Referenced | **Not retrievable** — client-rendered. Sandbox facts are sourced from S1/S2 reasoning and `03` vendor behaviour; per-org refresh cadence must be read from `Setup > Sandboxes` |
| S18 | <https://help.salesforce.com/s/articleView?id=sf.overview_limits.htm&type=5> — Limits overview | Referenced | **Not retrievable** — client-rendered |

---

## 3. Salesforce CLI — plugin source used as the authoritative flag reference

Reading the plugin implementation (not the docs page) means every flag name and description below
is the literal string the CLI uses.

| # | Source | Used for | Confidence |
|---|---|---|---|
| S20 | <https://github.com/salesforcecli/plugin-deploy-retrieve> — `messages/deploy.metadata.md` | Exact `--test-level` semantics for all five levels; `--pre-destructive-changes` / `--post-destructive-changes`; `--purge-on-delete`; `--metadata` / `--source-dir` / `--manifest` / `--single-package` / `--metadata-dir`; the "Metadata components are deployed in source format by default" note; the "production orgs never allow source tracking" note | `verified` |
| S21 | Same repo — `messages/commonFlags.md` | `--tests` syntax (repeat the flag, or space-separated, quote names with spaces) | `verified` |
| S22 | Same repo — `src/commands/project/deploy/start.ts`, `validate.ts`, `quick.ts`, `preview.ts`, `report.ts`, `cancel.ts`, `resume.ts` | The existence and flag sets of `sf project deploy validate`, `sf project deploy quick`, `sf project deploy preview`, `sf project deploy report`, `sf project deploy cancel`, `sf project deploy resume` | `verified` |
| S23 | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/guide/project-deploy-start.html> | Referenced for the CLI guide | **403** — Salesforce blocks automated access; S20–S22 used instead |
| S24 | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/guide/project-deploy-quick.html> | Referenced for quick deploy | **403** — as S23 |
| S25 | <https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference.html> — Salesforce CLI Command Reference (CLI 2.153.5) | Command and flag inventory used to check the "flags that do not exist" table | `verified` |
| S26 | <https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-scratch-orgs-editions-and-allocations.html> | Scratch org daily allocations: Developer/trial 6 per day and 3 concurrent; Enterprise 80/40; Unlimited and Performance 200/100 | `verified` |
| S27 | <https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-rest-deploy-recentvalidation.html> | Recent-validation / deploy-via-validation endpoint (`SF_ORG_METADATA_REST_DEPLOY`, `org-metadata-rest-deploy`) — the current documented surface behind the CLI quick-deploy path | `vendor-claim` |
| S28 | <https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_package_version_promote.htm> | `sf package version promote` command reference | `verified` (command name) |
| S29 | <https://www.salesforceben.com/salesforce-development-lifecycle-deployment-architect-certification-guide-tips/> and <https://www.trailblazeprep.com/certifications/dev-lifecycle-deployment-architect> | Existence and naming of the **Salesforce Certified Development Lifecycle and Deployment Architect** credential | `vendor-claim` — confirm the exam outline against the official guide before publishing weights |

---

## 4. Salesforce certifications

| # | Source | Used for | Confidence |
|---|---|---|---|
| S30 | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Credential name "Salesforce Certified Platform Developer"; exam `Plat-Dev-201`; study trail and trailmix links | `verified` |
| S31 | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Credential name "Salesforce Certified Platform Administrator II"; exam `Plat-Admn-301`; **prerequisite: Platform Administrator** | `verified` |
| S32 | <https://trailhead.salesforce.com/credentials/administratoroverview> | The certification landscape by role; absence of a Salesforce DevOps credential | `verified` |
| S33 | <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> | PD1 study-guide trail (module structure) | `verified` for the trail; **exact exam-domain weightings not retrievable** (client-rendered) |
| S34 | <https://trailhead.salesforce.com/content/learn/trails/platform-administrator-certification-study-guide> | Administrator II study-guide trail | `verified` for the trail; weightings not retrievable |
| S35 | <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201> | PD1 exam page (referenced; live exam parameters unverified) | `vendor-claim` / unverified content |
| S36 | <https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301> | Administrator II exam page (referenced) | `vendor-claim` / unverified content |

---

## 5. Gearset

| # | Source | Used for | Confidence |
|---|---|---|---|
| S40 | <https://docs.gearset.com/en/articles/16666562-setting-your-homepage-in-gearset> | Grouped left-navigation structure | `verified` |
| S41 | <https://docs.gearset.com/en/articles/618755-managing-salesforce-org-connections> | Adding, authorising and removing org connections; sharing | `verified` |
| S42 | <https://docs.gearset.com/en/articles/2707810-why-does-gearset-have-two-connected-apps> | Two Connected Apps (`Gearset`, `Gearset Deploy`); manual install requirement | `verified` |
| S43 | <https://docs.gearset.com/en/articles/2288760-what-oauth-version-does-gearset-use> | OAuth 2.0 + PKCE; refresh-token rotation; 30-day idle timeout; IP allowlist | `vendor-claim` |
| S44 | <https://docs.gearset.com/en/articles/16012727-deployment-user-in-salesforce-permission-checklist> | Deployment-user permission checklist | `verified` |
| S45 | <https://docs.gearset.com/en/articles/9155775-running-your-first-comparison> | Compare flow; source/target locations; comparison filters; `Compare now` | `verified` |
| S46 | <https://docs.gearset.com/en/articles/619012-configuring-comparisons> and <https://docs.gearset.com/en/articles/8870853-default-comparison-metadata-filter> | `COMPARISON FILTER` and built-in filters | `verified` |
| S47 | <https://docs.gearset.com/en/articles/595002-exploring-comparison-results> | Result tabs `All items`/`New`/`Changed`/`Deleted`; `Selected items`; table columns; difference types; filters | `verified` |
| S48 | <https://docs.gearset.com/en/articles/3154487-where-are-subcomponents-and-their-dependencies-displayed-in-the-comparison-results> | `Components` as a dependency-tree node, not a tab | `verified` |
| S49 | <https://docs.gearset.com/en/articles/595095-running-your-first-deployment> | `Next` → problem analysis → `Pre-deployment summary` → `Validate deployment` / `Deploy now` | `verified` |
| S50 | <https://docs.gearset.com/en/articles/1376067-setting-apex-test-levels> | The four Gearset Apex test-level options | `verified` |
| S51 | <https://docs.gearset.com/en/articles/625054-metadata-deployment-history> | Deployment history actions: `View details`, `View errors`, PDF report, package download, CSV, `Roll back`, `Clone package`, `Deploy to target` | `verified` |
| S52 | <https://docs.gearset.com/en/articles/625156-validated-packages> | Validation history and `View errors` | `verified` |
| S53 | <https://docs.gearset.com/en/articles/8333138-setting-up-your-first-ci-job-in-gearset> | CI job options: metadata filter, test level, `Deploy deleted items`, `Deploy permissions`, Delta CI, PR validation, SA ruleset, Problem Analyzer, outgoing webhook | `verified` |
| S54 | <https://docs.gearset.com/en/articles/8345280-validation-only-ci-jobs> | `Validation-only CI Job` | `verified` |
| S55 | <https://docs.gearset.com/en/articles/8345275-managing-and-viewing-your-ci-jobs> | CI job history, `View comparison`, `View job performance` | `verified` |
| S56 | <https://docs.gearset.com/en/articles/6115277-an-introduction-to-gearset-pipelines> | Pipeline concept | `verified` |
| S57 | <https://docs.gearset.com/en/articles/12460112-creating-ci-jobs-in-gearset-pipelines> | `Add static environment` / `Create new` — environment, branch, target org, CI job | `verified` |
| S58 | <https://docs.gearset.com/en/articles/12928379-adding-environments-to-a-gitflow-pipeline> and <https://docs.gearset.com/en/articles/14151578-the-gitflow-branching-strategy-in-pipelines> | Gitflow stage → branch mapping | `verified` |
| S59 | <https://docs.gearset.com/en/articles/12656100-getting-started-with-continuous-delivery-rules-in-gearset-pipelines> | `Continuous Delivery Rules`; forward promotion; back propagation; Automation Platform Enterprise | `verified` |
| S60 | <https://docs.gearset.com/en/articles/9859659-pre-and-post-deployment-steps-in-gearset-pipelines> and <https://docs.gearset.com/en/articles/10718514-deployment-steps-library-in-gearset-pipelines> | `Deployment steps`; `Deployment steps library`; `Manual` / `Automatic` step types | `verified` |
| S61 | <https://docs.gearset.com/en/articles/9965863-integrating-with-github-or-github-enterprise-through-a-github-app> | GitHub App repository permissions | `verified` |
| S62 | <https://docs.gearset.com/en/articles/2437757-managing-status-check-rules-in-github> | Required status check setup in GitHub branch protection | `verified` |
| S63 | <https://docs.gearset.com/en/articles/8548816-ci-job-and-pipeline-webhooks> | CI-job and pipeline webhooks; manual trigger | `verified` |
| S64 | <https://docs.gearset.com/en/articles/11496146-running-and-managing-your-backup-job> | Backup tiers (Standard, High frequency, Big Object); 7-year record retention; indefinite metadata retention; `Back up now`; `Job history`; `View changes` | `verified` |
| S65 | <https://docs.gearset.com/en/articles/3277396-creating-your-first-data-backup-job> | Backup job creation flow and first-run baseline | `verified` |
| S66 | <https://docs.gearset.com/en/articles/8425850-what-data-is-backed-up-in-each-run> | Metadata + record data capture | `verified` |
| S67 | <https://docs.gearset.com/en/articles/9311061-what-binary-data-files-or-attachments-are-supported> | `ContentVersion`, `ContentDocumentLink`, `Attachment` support; Bulk API restrictions | `verified` |
| S68 | <https://docs.gearset.com/en/articles/3456807-restoring-deleted-records-without-dependencies> | Restore flow: `Job history` → `View changes` → `View records` → `Restore from previous backup` | `verified` |
| S69 | <https://docs.gearset.com/en/articles/8065268-data-restoration-using-gearset> | Restore with dependencies | `verified` |
| S70 | <https://docs.gearset.com/en/articles/3457045-restoring-metadata-from-a-data-backup-job> | Metadata restore from snapshot; Metadata History rollback | `verified` |
| S71 | <https://docs.gearset.com/en/articles/10147094-how-to-configure-retention-rules-for-your-archived-data> | Archive rules (`Archive data after`, `Delete after`, `Do not archive`) | `verified` |
| S72 | <https://docs.gearset.com/en/articles/10471254-running-your-first-in-place-masking> | In-place masking flow; `Automatically selected sensitive fields`; `Disable automations` | `verified` |
| S73 | <https://docs.gearset.com/en/articles/14737732-what-fields-are-selected-for-masking-by-default> | Default masked fields | `verified` |
| S74 | <https://docs.gearset.com/en/articles/13112693-running-your-first-sandbox-seeding-job> and <https://docs.gearset.com/en/articles/2529785-using-templates-for-sandbox-seeding-compliance> | Sandbox seeding + `Configure masking`; template reuse | `verified` |
| S75 | <https://docs.gearset.com/en/articles/10256103-how-do-i-refresh-a-sandbox-in-my-pipeline> and <https://docs.gearset.com/en/articles/11838948-best-practice-refreshing-and-masking-a-full-copy-sandbox> | The refresh → re-auth → re-sync → redeploy → mask sequence; **Gearset does not perform the refresh** | `verified` |
| S76 | <https://docs.gearset.com/en/articles/604536-org-monitoring-automating-org-change-tracking-and-metadata-backup> | `Change monitoring` | `verified` |
| S77 | <https://docs.gearset.com/en/articles/14134763-how-to-replicate-deployment-errors-using-salesforce-cli> and <https://docs.gearset.com/en/articles/14134708-how-to-replicate-retrieval-issues-using-salesforce-cli> | Salesforce CLI as the troubleshooting/reproduction tool, not a per-org setting | `verified` |
| S78 | <https://docs.gearset.com/en/articles/13938209-what-is-express-deploy> | `Express Deploy` as an open-pilot deployment mode | `vendor-claim` |
| S79 | <https://docs.gearset.com/en/articles/6170088-enforcing-code-review-before-promotion> | Code-review enforcement in pipelines | `verified` |
| S80 | <https://docs.gearset.com/en/articles/5069914-delta-ci> | Delta CI baseline behaviour | `verified` |
| S81 | <https://docs.gearset.com/en/articles/10473502-configuring-gearset-permissions> and <https://docs.gearset.com/en/articles/8989748-gearset-backup-restore-user-permissions> | Team Security; backup/restore permissions; plan gates | `verified` |

---

## 6. Copado

| # | Source | Used for | Confidence |
|---|---|---|---|
| S90 | <https://www.copado.com/copado-essentials> | Essentials Free / Basic / Essentials Plus edition matrix and prices | `vendor-claim` (prices as at 2026-11-14) |
| S91a | <https://www.copado.com/platform-overview> | Enterprise line branded **Copado CI/CD**; **Agentia** as the unified umbrella; Copado Essentials as the standalone line | `vendor-claim` |
| S92 | <https://docs.copado.com/articles/copado-ci-cd-publication/glossary-of-terms> | Object definitions (Pipeline, User Story, Environment, Promotion, Release, Feature/Promotion Branch, Credential, Git Snapshot, Deployment Step, Job Template/Step/Execution, Connection Behavior) and licence types | `verified` |
| S93 | <https://docs.copado.com/articles/copado-ci-cd-publication/pipeline-page> and <https://docs.copado.com/articles/copado-ci-cd-publication/pipeline-configuration> | Pipeline Manager navigation; status icons; drill-downs; `Configure Pipeline` | `verified` |
| S94 | <https://docs.copado.com/articles/copado-ci-cd-publication/how-to-create-a-promotion> and <https://docs.copado.com/articles/copado-ci-cd-publication/promotion-overview> | Promotion routes; `Ready to Promote`; `Add Selected User Stories`; `Create Deployment`; `Deployment Details`; promotion-branch naming; `tag=x.y.z`; 8,000/10,000 file limits; Copado Admin rule for production | `verified` |
| S95 | <https://docs.copado.com/articles/copado-ci-cd-publication/deployment-steps1> | The full deployment-step type list | `verified` |
| S96 | <https://docs.copado.com/articles/copado-ci-cd-publication/deployment-execution-options> | `Deploy Outstanding` vs `Deploy All`; `Deploy Now` vs `Deploy Later` | `verified` |
| S97 | <https://docs.copado.com/articles/copado-ci-cd-publication/creating-a-deployment> | Deployment record types; `Attach Deployment Files`; Advanced (multi-step) | `verified` |
| S98 | <https://docs.copado.com/articles/copado-ci-cd-publication/quality-gates-in-copado-continuous-delivery> | The quality-gate table (Apex Tests with Validation, Validation, Compliance Check, Static Code Analysis, Automation, Test, Manual Approval/Test/PR, URL Callout) | `verified` |
| S99 | <https://docs.copado.com/articles/copado-ci-cd-publication/connection-behaviors> | Connection Behavior fields; automation scope; CDC and API-key prerequisites | `verified` |
| S100 | <https://docs.copado.com/articles/copado-ci-cd-publication/copado-compliance-hub> and <https://docs.copado.com/articles/copado-ci-cd-publication/compliance-scan-and-scan-results> | Compliance objects; active and passive scans; `Compliance Scan Events`; scheduled scans; results tab | `verified` |
| S101 | <https://docs.copado.com/articles/source-format-pipelines-publication/credential-overview> and <https://docs.copado.com/articles/source-format-pipelines-publication/how-to-create-a-credential> | Credential types; creation fields; OAuth/SSO authentication; the 30-day refresh-token TTL | `verified` |
| S102 | <https://docs.copado.com/articles/copado-pipelines-publication/copado-branching-strategy> | The five Copado branching mechanics | `verified` |
| S103 | <https://docs.essentials.copado.com/en/articles/4719394-using-work-items> | Work Item fields and actions; automatic stage progression; `Go Back to Previous Stage` | `verified` |
| S104 | <https://docs.essentials.copado.com/en/articles/6887394-approval-process-with-copado-essentials-plus> | Required approving reviews; approver roles | `verified` |
| S105 | <https://docs.essentials.copado.com/en/articles/6828447-ci-jobs-overview> | Essentials Plus CI Jobs (scheduled validation, metadata backups, webhook deploys, outgoing webhooks) | `verified` |
| S106 | <https://docs.essentials.copado.com/en/articles/5742593-essentials-plus-edition-setup-guide> | Pipeline setup; org connection; integration user recommendation; Git branching behaviour | `verified` |
| S107 | <https://docs.essentials.copado.com/en/articles/7861656-validations-with-copado-essentials> | Validation and test levels; coverage; SA | `verified` |
| S108 | <https://docs.copado.com/articles/copado-ci-cd-publication/copado-pipelines-publication/reference-articles> and `.../creating-a-deployment` | Deployment Activity, Work Items list, `Attach Deployment File` producing `Deploy-{deploymentJobId}.zip` | `verified` |
| S109 | <https://success.copado.com/s/certification-guides> | Copado certification entry point | `vendor-claim` |

---

## 7. AutoRABIT

| # | Source | Used for | Confidence |
|---|---|---|---|
| S120 | <https://www.autorabit.com/products/automated-release-management-ci-cd/> | ARM as the CI/CD product | `vendor-claim` |
| S121 | <https://www.autorabit.com/products/vault-data-backup-recovery/> | Vault as backup/recovery and the home of data masking | `vendor-claim` |
| S122 | <https://knowledgebase.autorabit.com/fundamentals/faq/autorabit-platform-user-definitions> | Standard User vs Platform Integration User licence classes | `verified` |
| S123 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/automation-and-ci/create-a-new-ci-job/deploy-from-version-control-to-a-salesforce-org> | CI Job creation, all sections, all options | `verified` |
| S124 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/automation-and-ci/ci-job-list> | CI Job List filters and row actions; deactivated-job behaviour | `verified` |
| S125 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/dashboard-and-pipelines/pipelines> | Classic ARM Pipeline screen; branch types | `verified` |
| S126 | <https://knowledgebase.autorabit.com/product-guides/arm-1/arm-features/dashboard-and-pipelines/pipelines> and `.../most-recent-runs/release-pipeline-run-details` | ARM New UI `Pipelines → Releases`; stage cards; logs; `Deployment report` / `Deployment logs` | `verified` |
| S127 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/create-and-deploy-changes-in-autorabit> | Deployment creation; `Deployment From`; `Selective` vs `Full`; compare-metadata-and-deploy flow | `verified` |
| S128 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/apex-unit-tests> | Apex test levels; `Run Tests Based On Changes`; `Run Relevant Tests` | `verified` |
| S129 | <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/masking-rules> | Masking Rules (global) and cloning | `verified` |
| S130 | <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/live-data-masking> | Live Data Masking flow; masking-rule fields; `Config Details`; local vs global precedence; rollback retention (7 days) | `verified` |
| S131 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/version-control/change-labels/release-labels> | Release Labels; `Label Type`; `No of Days`; `Create package manifest`; delta metadata types | `verified` |
| S132 | <https://knowledgebase.autorabit.com/product-guides/arm-1/arm-features/deployment/schedule-a-deployment> | Scheduled Deployments (feature flag `SCHEDULED_DEPLOYMENTS`); `Edit`/`Cancel`/`Deploy Now` | `verified` |
| S133 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/monitor-deployments> | Deployment History; promotion/redeploy/rollback/abort; `Quick Deploy` within 96 hours | `verified` |
| S134 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-administration/user-management/arm-credential-manager> | Credential Manager types and scope; Org Administrators only | `verified` |
| S135 | <https://knowledgebase.autorabit.com/product-guides/arm/registration/salesforce-org/salesforce-authentication-using-oauth> | OAuth registration, Connected App scopes and callback, ECA flow | `verified` |
| S136 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/reports/reports-overview> and `.../audit-report` | Weekly reports; Audit Report (CSV, GMT); Job Audit Report PDF; retention windows | `verified` |
| S137 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/reports/deployment-reports` | Deployment report set; code coverage warning; `Audit Log` categories | `verified` |
| S138 | <https://knowledgebase.autorabit.com/llms.txt> | Knowledge-base index; used to confirm the **absence** of a "Test Repository" product | `verified` (negative result) |
| S139 | <https://academy.autorabit.com/?sfwd-courses=arm-core-track> and <https://academy.autorabit.com/?product=admin-certification> | ARM Academy tracks | `vendor-claim` |

---

## 8. Gearset Academy certification

| # | Source | Used for | Confidence |
|---|---|---|---|
| S140 | <https://devopslaunchpad.com/courses/gearset-academy-certification/> | Gearset Academy Certification: audience, lifecycle coverage (deployments, automation, backup, version control, CI/CD, release management, sandbox seeding, restore) | `vendor-claim` |
| S141 | <https://docs.gearset.com/en/articles/8825457-gearset-onboarding-training-courses> and <https://docs.gearset.com/en/articles/4497508-what-is-devops-launchpad> | Training relationship between Gearset and DevOps Launchpad | `vendor-claim` |

---

## 9. Method notes

| Note | Detail |
|---|---|
| **Proxy** | `r.jina.ai` was used to convert client-rendered Salesforce and vendor pages to text. It changes presentation, not content; every citation above points at the canonical source URL, not the proxy URL. |
| **Why the Salesforce CLI source was preferred over the docs page** | `developer.salesforce.com` returned **403** to automated requests during this research. The `salesforcecli/plugin-deploy-retrieve` repository is the implementation, and its `messages/*.md` files are the literal user-facing strings — a stronger source than the rendered docs page. |
| **Negative results** | Where a UI label could not be found, the artifact says so. This is deliberate: "not a current documented label" is a finding, silence would be a gap. The main negative results are listed in `03 §5`. |
| **Vendor pricing** | Copado Essentials prices were read from copado.com on 2026-11-14 and are subject to change. Re-verify before quoting. |
| **Not consulted** | Any local Salesforce org, any live vendor tenant, and any internal Scotiabank material. Every statement about what a bank "typically" does is framed as such. |
