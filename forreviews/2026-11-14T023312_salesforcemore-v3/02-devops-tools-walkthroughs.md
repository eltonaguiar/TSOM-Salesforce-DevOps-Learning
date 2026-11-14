# DevOps tools — practical walkthroughs (UI + CLI)

> **Confidence convention:** `[UI: likely]` = stable, long-standing layout. `[UI: verify]` = label
> changed recently or differs by edition. `[CLI: verified]` = command shape matches current `sf` docs;
> always confirm flags with `--help` because flags move between CLI majors.

The tools all sit on the same substrate: the **Metadata API** (and the `sf` CLI that wraps it). No vendor
UI does something the CLI cannot do; the vendors add compare/diff, problem analyzers, pipelines, audit
trails, and backups. Say that in an interview before naming buttons.

---

## Gearset

**What it is:** a UI/CI layer over the Metadata API (and some data APIs) — compare/validate/deploy,
pipelines, and backups.

<details>
<summary><strong>A. Compare &amp; deploy (ad-hoc or delta)</strong></summary>

1. Log in at the Gearset app. Left nav → **Compare and deploy** `[UI: likely]`.
2. **Source**: a **Salesforce org** (e.g. `Dev1`) or **Source control** (GitHub repo + branch).
3. **Target**: the destination org (e.g. `QA`).
4. **Filter**: open **Change filter** / **Metadata filter** `[UI: verify]`. Use a saved filter that
   includes `CustomObject`, `CustomField`, `Flow`, `ApexClass`, `ApexTrigger`, `PermissionSet`,
   `FlexiPage`, `Layout`, `RecordType`, and excludes noisy standard value sets you do not own.
5. Click **Compare now**. Results are color-coded: **New** (source only), **Changed** (line-level XML
   diff), **Deleted** (target only).
6. Select items. **Problem analyzers** flag missing dependencies (e.g. a Flow references a field you did
   not select) and profile risk — accept or consciously override each warning.
7. **Validate** (a `checkOnly` deploy) before deploying. Read Apex test results and compile errors.
8. Deploy, attaching the **change ticket id**. Gearset stores a per-deploy artifact under
   **Deployment history** `[UI: likely]` — that artifact is your rollback seed.

**Practical example:** deploy `Flow: Commercial_Loan_Approval`, `CustomField: Loan__c.Risk_Rating__c`,
and `PermissionSet: Commercial_Loan_Officer` in one comparison so the Flow's field dependency and the
permission granting field access land atomically.
</details>

<details>
<summary><strong>B. CI job (PR/branch validation)</strong></summary>

1. Left nav → **Continuous Integration** `[UI: likely]`.
2. **Add new job**. Source = GitHub repo + branch (or PR trigger). Target = CI/QA sandbox.
3. Set **Apex testing**: `Run local tests` or `Run specified tests`; enable "fail if coverage below 75%".
4. Enable the GitHub **status check** so the job reports green/red on the PR.
5. Optional: Slack/Teams/email notifications.

Functionally identical to the GitHub Actions flow in `03-github-cicd-salesforce.md`; the difference is
Gearset hosts the runner and stores the audit trail.
</details>

<details>
<summary><strong>C. Pipelines / promotion</strong></summary>

1. Left nav → **Pipelines** `[UI: likely]`.
2. Create a pipeline with ordered environments (Dev → QA → UAT → Pre-Prod → Prod).
3. Add a **promotion step** per environment: trigger on branch update or manual approval.
4. Attach **quality gates** (tests, coverage) and **approval gates** (named approver ≠ author).

Use pipelines for the standardized release train; use compare-and-deploy for hotfixes and one-offs.
</details>

<details>
<summary><strong>D. Backup &amp; restore</strong></summary>

1. Left nav → **Backups** (under a data/compliance area) `[UI: verify]`.
2. **Add backup job** → select org, region, frequency, retention.
3. Configure **smart alerts** for anomalous mass delete/update (e.g. > N records in one job).
4. **Restore**: pick a snapshot → filter to the object → select records → review parent/child id mapping
   → restore to target. Restoring data is **not** a metadata rollback and is a separate ticketed action.

**Banking note:** choose a data-residency region that satisfies the bank; confirm backups are encrypted
at rest and access-logged. Backup ≠ sandbox masking; masking is a separate control on refresh.
</details>

---

## Copado

**What it is:** a native Salesforce app (custom objects in a Salesforce org) modeling user stories,
commits, promotions, and deployments. Strong on compliance evidence and back-promotion.

<details>
<summary><strong>A. Commit metadata to a user story</strong></summary>

1. App Launcher → **Copado** → **User Stories** `[UI: likely]`.
2. Open the story (`US-…`), confirm the **credential** points at your dev sandbox.
3. **Commit Changes** → filter metadata → select components → choose **Commit** or **Destructive changes**
   → commit message carries the ticket id.
4. Copado retrieves from the org via the Metadata API and commits to the story's Git branch.
</details>

<details>
<summary><strong>B. Quality gates &amp; promotion</strong></summary>

1. On the story, run **Static Code Analysis** (PMD/CodeScan/Sonar rules) `[UI: verify]`.
2. Gate on zero blockers and coverage threshold.
3. Mark **Ready for Promotion** → create a **Promotion** record (source env → target env).
4. **Deploy**: Copado merges the story branch into the target branch and runs deployment steps
   (metadata deploy → Apex tests → optional data step).
</details>

<details>
<summary><strong>C. Back-promotion</strong></summary>

When UAT/Pre-Prod moves ahead, developer sandboxes drift. Back-promotion merges downstream branch
changes back into developer branches so the next sprint does not re-introduce deleted/renamed metadata.
This is the thing Copado gets right that ad-hoc compare/deploy does not.
</details>

---

## AutoRABIT (ARM)

**What it is:** CI/CD + release automation + data tooling (Vault backup, data masking) in one console.

<details>
<summary><strong>A. CI job</strong></summary>

1. ARM console → **CI/CD → New CI Job** `[UI: likely]`.
2. Source = Git repo/branch; Target = registered org credential.
3. Enable **static code analysis**, **SFDX source→metadata conversion** (if repo is source format and
   the target path expects metadata format), and **incremental/delta deploy**.
4. Test level = `RunLocalTests` (or specified).
</details>

<details>
<summary><strong>B. Vault backup + data masking</strong></summary>

1. **Vault** → create a backup plan (schedule, retention, encrypted storage destination).
2. **Data Masking** → define masking templates for PII fields (email, phone, government id, account
   number, date of birth) and apply during restore/refresh workflows.
3. Masking must complete and be confirmed **before** broad logins to a refreshed Full sandbox.
</details>

---

## Salesforce CLI (`sf`) — the engine under every tool

```bash
# JWT auth for CI (never web login on a runner, never a stored password)
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file ./server.key \
  --username "$SF_CI_USERNAME" \
  --instance-url https://test.salesforce.com \
  --alias ci-org

# Retrieve specific metadata for review
sf project retrieve start \
  --metadata CustomObject:Commercial_Loan__c \
  --metadata Flow:Commercial_Loan_Approval \
  --metadata PermissionSet:Commercial_Loan_Officer \
  --target-org dev-org

# Dry-run validate against the target (no org change)
sf project deploy validate \
  --manifest ./delta/package/package.xml \
  --post-destructive-changes ./delta/destructiveChanges/destructiveChanges.xml \
  --test-level RunSpecifiedTests \
  --tests CommercialLoanApprovalTest \
  --target-org uat-org --wait 60

# Promote an already-validated job inside the change window
sf project deploy quick --job-id 0AfXXXXXXXXXXXXXXX --target-org prod-org --wait 30

# Inspect the result
sf project deploy report --job-id 0AfXXXXXXXXXXXXXXX --target-org prod-org
```

**Delta generation** with `sfdx-git-delta` (plugin provides the `sgt` command):

```bash
sgt --to HEAD --from origin/main --output ./delta --generate-delta
```

`[CLI: verified]` — confirm current flag names with `sf project deploy validate --help`.

### Node wrapper (`@salesforce/cli`) vs legacy (`sfdx`)

Modern CLI is `sf`; older `sfdx` commands still appear in runbooks. For GHA, install `@salesforce/cli`.
Pin the version in CI so a CLI major bump does not silently change flag behavior mid-release.
