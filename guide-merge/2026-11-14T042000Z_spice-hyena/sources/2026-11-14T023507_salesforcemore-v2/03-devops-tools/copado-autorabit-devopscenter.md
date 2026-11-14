# Copado, AutoRABIT, DevOps Center, Change Sets, and the CLI

**Merge target:** section 6.1 of the downstream page. The goal is practical familiarity, not a vendor manual.

**Caveat.** These platforms rename modules between releases and editions. The task and the verification step are stable; the labels are not.

## 1. Copado

### 1.1 What it is

A release-management platform built around user stories, pipelines, promotions, deployment steps, quality gates, and audit evidence. Current product branding includes **Copado CI/CD** for enterprise teams, **Copado Essentials** for smaller teams, **Agentia** as the AI layer, **Copado Robotic Testing**, and the **Copado AI Platform**. "Copado Fundamentals" and a Copado "DevOps Center" tier are not current product names; do not use them in an interview.

### 1.2 Practical click-paths (Copado CI/CD)

| Task | Where (common shape) | What you do | What to verify |
|---|---|---|---|
| Create a pipeline | Copado app → Pipelines / Pipeline setup | Define stages: Dev → QA → UAT → Prod; attach orgs | Each stage has one owner and one gate |
| Create a user story | Copado → User Stories | Create a story, link the ticket, attach commits/metadata | The story is the unit of promotion, not a loose commit |
| Commit changes | VS Code / Copado extension or Git | Commit with the story id | The story and the commit agree |
| Validate | Story or pipeline action | Run the validation/deployment step to the target | Tests run; failures block promotion |
| Promote | Pipeline / promotion | Move the story to the next stage; approve at the gate | The approver is not the author |
| Quality gate | Pipeline step / quality gate config | Static analysis, coverage, peer review | The gate is enforced, not advisory |
| Deploy | Promotion action | Execute the deployment steps | Destructive changes and tests are explicit steps |
| Audit | Deployment history / story history | Export the promotion evidence | Ticket, approver, deploy id, test result, timestamp |
| Backup (if licensed) | Copado backup module | Take a backup before the risky step | Backup id recorded in the ticket |

**Copado Essentials** is the simpler standalone product. It may not expose the same enterprise pipeline objects; verify which product the bank actually licenses before you promise a specific workflow.

### 1.3 What it does not replace

Git hygiene, a real test suite, a rollback tag, or a human who reads the diff. Copado makes the process visible; it does not make a bad payload safe.

### 1.4 Interview line

"Copado models the release process: user story, pipeline, promotion, quality gate, deployment, audit. The underlying operation is still Metadata API, and Git is still the source of truth."

## 2. AutoRABIT

### 2.1 What it is

A Salesforce DevOps platform with four current product areas:

| Product | What it does |
|---|---|
| **AutoRABIT ARM** | CI/CD, deployments, version control, testing, sandbox management |
| **AutoRABIT Vault** | Backup/restore, data integrity, archiving; data masking capabilities may sit in Vault or a related module—verify the edition |
| **AutoRABIT CodeScan** | Static code analysis and code quality |
| **AutoRABIT Guard** | Security posture, policy enforcement, misconfiguration detection |

Older material may describe a generic "CI Jobs / Deployment / Data Loader / Backup / Monitoring / Release" module list. Treat that as category-level, not as current product naming.

### 2.2 Practical click-paths

| Task | Where (common shape) | What you do | What to verify |
|---|---|---|---|
| CI job | ARM → CI Jobs / CI | Connect Git repo and branch; choose target org; choose validate or deploy; add tests | The job fails on a test failure |
| Deployment | ARM → Deployment | Compare metadata between orgs/branches; deploy; keep a history | The diff is reviewed, not blindly deployed |
| Data | Vault / data tooling | Seed or migrate records | Data is masked/approved; not bulk customer data without a ticket |
| Backup | Vault → Backup & Restore | Back up metadata/data before a risky release | Backup id and restore path are recorded |
| Monitoring | ARM / Guard | Detect drift and security/compliance issues | Alerts route to the release owner |
| Static analysis | CodeScan | Scan the branch for quality/security findings | The gate is configured and enforced |

### 2.3 Interview line

"AutoRABIT ARM is the CI/CD layer; Vault is backup/restore and data; CodeScan is static analysis; Guard is security posture. The questions are always the promotion path, the back-promotion, and where the secrets live."

## 3. DevOps Center

### 3.1 What it is

Salesforce's native work-item and pipeline product. It connects a Git repo and orgs, tracks work items, and promotes changes through pipeline stages. It is the option when the bank does not want another vendor.

### 3.2 Practical click-paths

| Task | Where | What you do | What to verify |
|---|---|---|---|
| Enable | Setup → search "DevOps Center" | Enable and connect Git/orgs | The connected app and repo permissions are correct |
| Create a pipeline | Setup → DevOps Center → Pipelines | Define stages and orgs | Each stage maps to a real sandbox |
| Create a work item | App Launcher → DevOps Center → Work Items | Create a story/bug, associate changes | The work item is the traceable unit |
| Commit and deploy | VS Code / DevOps Center | Commit with the work item; promote | The commit and work item agree |
| Promote | Work item / pipeline | Move to the next stage; approve | The approver is not the author |
| Audit | Work item history / deployment history | Capture the evidence | Ticket, deploy id, test result |

### 3.3 Limitations to say out loud

DevOps Center is native and improving, but it is not a full replacement for a mature vendor platform's dependency analysis, data tooling, and backup. It still requires branch discipline, tests, and a rollback tag.

### 3.4 Interview line

"DevOps Center is the native option: work items, Git, pipelines, promotion. It does not remove the need for Git discipline or a test gate."

## 4. Change Sets

### 4.1 What they are

A Setup UI mechanism for moving metadata between related orgs. Outbound change set → upload → inbound change set → validate → deploy.

### 4.2 Click-path

1. Source org: Setup → Deploy → Outbound Change Sets → New.
2. Add components manually.
3. Upload to the target org.
4. Target org: Setup → Deploy → Inbound Change Sets → select → Validate → Deploy.

### 4.3 Why they fail at this scale

- No reviewable Git diff.
- No CLI/API automation.
- No dependency analysis; you add components by hand.
- No branch, feature, or hotfix model.
- No rollback tag.
- Profile and permission-set XML conflicts are manual.
- Weak audit evidence compared with a pipeline.
- Only between related orgs.

### 4.4 When a Change Set is still acceptable

A tiny emergency fix in an org that has no pipeline, with a ticket, a validation, a named approver, and a follow-up to backfill Git. In a regulated bank, expect the written procedure to forbid it or to require an exception.

### 4.5 Interview line

"Change Sets are the thing I can explain and then retire. They have no diff, no branch model, and no rollback tag. The answer is the CLI or a vendor pipeline with Git in front."

## 5. Salesforce CLI practical set

```bash
# Auth (interactive for a developer machine; JWT in CI)
sf org login web --alias dev
sf org login jwt --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file server.key --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" --alias ci

# Retrieve and inspect
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev
sf project deploy preview --manifest manifest/package.xml --target-org qa

# Validate and deploy
sf project deploy start --manifest manifest/package.xml --dry-run \
  --test-level RunSpecifiedTests --tests CB_Release_Test --target-org qa
sf project deploy start --manifest manifest/package.xml --target-org qa

# Status and quick deploy
sf project deploy report --job-id <job-id> --target-org qa
sf project deploy quick --job-id <job-id> --target-org prod

# Tests
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 30 --target-org qa

# Packages
sf package version create --package CB_Credit --installation-key-bypass \
  --code-coverage --wait 30
sf package version promote --package 04tXXXXXXXXXXXX
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

Flags move. Confirm with `sf <command> --help` before putting a command in a runbook.

## 6. What to merge

**Merge:** the Copado and DevOps Center task tables, the Change Sets "why fail" list, and the CLI set.

**Compress:** AutoRABIT if the page is short; keep the category-level answer.

**Do not merge:** edition-specific module names as if universal. Keep the caveat.
