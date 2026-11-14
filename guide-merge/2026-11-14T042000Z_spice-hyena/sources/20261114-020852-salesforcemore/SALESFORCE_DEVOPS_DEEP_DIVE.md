# Salesforce DevOps Engineer — Deep Dive: Scotiabank Req 276046 vs Release-Engineering Training

Cross-references:
- **Job:** DevOps Engineer (Salesforce), Scotiabank Commercial Banking Engineering, Toronto — Requisition 276046
  https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/
- **Training:** Salesforce DevOps Engineer — Release Engineering Training (built from Req 276046)
  https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/#6-devops-tools

This document expands the training page into collapsible sections, gives practical per-tool examples (with Gearset UI paths), a GitHub + Salesforce CI/CD reference, and a term-by-term deep dive of every requirement in the posting.

---

## How to read this

Each `<details>` block is collapsible. Open the ones relevant to your current task:

- **Applying for the role:** start with the JD term deep dive and the interview drill answers.
- **On the job:** use the tool-specific sections (Gearset UI paths, CLI commands, Copado/AutoRabit) and the CI/CD pipeline reference.
- **Preparing a release:** use the branching, sandbox, validation, rollback, and audit-pack sections.

---

<details>
<summary>1. Job-description term deep dive — index</summary>

Every line of the Scotiabank posting is covered below. Click a term to expand its deep dive.

</details>

<details>
<summary>2. Design, implement, and maintain CI/CD pipelines for Salesforce using Git-based workflows</summary>

### What it means
Salesforce metadata lives in orgs, but the source of truth is Git. A pipeline automates retrieve → review → validate → deploy so a human never edits production in Setup and "copies it later."

### Practical anatomy (GitHub Actions example)
```yaml
name: Salesforce CI/CD
on:
  push:
    branches: [release/*]
  pull_request:
    branches: [main, release/*]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: salesforce/actions/setup-sf@v1
      - name: Authenticate to CI org
        run: sf org login jwt --client-id ${{ secrets.SF_CLIENT_ID }} --jwt-key-file server.key --username ${{ secrets.SF_CI_USERNAME }} --set-default --alias ci
      - name: Dry-run deploy + tests
        run: |
          sf project deploy start --dry-run --manifest manifest/package.xml --test-level RunSpecifiedTests --tests CommercialBankingReleaseTest --target-org ci
```

### Git workflow layer
1. Developer works on a short-lived `feature/<ticket>` branch.
2. Pull request → pipeline runs dry-run + tests on a CI sandbox.
3. Reviewer (not the author) approves the diff.
4. Merge to `release/<date>`; pipeline deploys to QA, then UAT.
5. Release manager promotes to Pre-Prod, then Prod inside the change window.
6. Tag prod (`release-2026-11-27`) and write both deploy IDs to the ticket.

### Why this matters for the posting
- "Git based workflows" — metadata in Git, not orgs.
- "Audit, security, compliance" — every deploy tied to a ticket + approver.
- "Reduce deployment failures" — dry-run catches missing dependencies before the window.

</details>

<details>
<summary>3. Manage multi-environment release strategies (Dev, QA, UAT, Pre-Prod, Prod)</summary>

| Stage | Purpose | Typical sandbox | Promoted by |
|-------|---------|-----------------|-------------|
| Dev | Build & unit test | Developer / Developer Pro / scratch org | Developer via Git |
| QA | Automated validation & integration | Developer Pro or Partial Copy | Pipeline on merge |
| UAT | Business tester sign-off | Partial Copy or masked Full | Release engineer |
| Pre-Prod | Dress rehearsal, prod-like metadata/volume | Full or recent Partial | Release engineer |
| Prod | Customers | Production | Release engineer, approved, in window |

### Key rules
- UAT is **not** a scratch org in a bank: commercial-banking orgs carry managed packages, SSO, named credentials, and licenses a scratch org won't reproduce unless encoded.
- Scratch orgs are fine for package builds, not for the Dev→Prod path.
- Refresh cadence is license-limited; Full is slowest. Check Setup > Sandboxes for the next eligible refresh before promising a date.
- Full copies contain customer data (SIN-adjacent IDs, account numbers). Refresh is complete only after masking and access limitation.

</details>

<details>
<summary>4. Coordinate scheduled releases, hotfixes, and emergency deployments</summary>

| Speed | When | Branch | Deploy bar |
|-------|------|--------|------------|
| Scheduled | Release calendar | `release/<date>` | Full validation, UAT sign-off, change ticket, window |
| Hotfix | Prod defect, next release too late | `hotfix/<ticket>` from `main` | Same validation, smaller payload, still a ticket |
| Emergency | Active customer/regulatory harm | `hotfix/<ticket>` from `main` | Short pre-written path, not an unlocked click in Setup |

### Hotfix merge rule
Cut from `main` (what prod runs), not from an open release branch. Merge back to `main` **and** into any open release branch, or the next release resurrects the bug.

### Emergency is not "skip the pipeline"
It's a shorter approval chain. If the runbook names one approver + a validation deploy, that path applies at 2 a.m. too.

</details>

<details>
<summary>5. Ensure deployment activities follow audit, security, and compliance standards</summary>

### Audit pack to keep, every release
- Change-ticket ID in the commit message and pull request.
- A non-author diff review (second pair of eyes).
- Validation deploy ID + prod deploy ID.
- Test run ID + coverage number.
- Named approver different from the author.
- Release tag.
- For Full sandboxes: refresh time, mask-complete confirmation, who may log in.

### Segregation of duties
- Developer who wrote Apex does **not** approve their own prod deploy.
- Pipeline makes it structural: integration user deploys; human approves; identities differ.

### Data hygiene
- No production customer data in slides, debug logs pasted to tickets, or unmasked sandboxes.
- Debug logs can contain field values — turn them off after diagnosis.

</details>

<details>
<summary>6. Manage Salesforce metadata lifecycle using source control (Git)</summary>

### Source of truth rule
Production is a **target**, not the source of truth. Git is the source of truth. If Setup and Git disagree, that is an incident, not a workflow.

### What to commit
- Custom objects, fields, validation rules, Flows, Apex, LWC, permission sets, custom metadata, named credentials **metadata** (not the secret).
- A `package.xml` manifest or package directory the pipeline always deploys.

### What NOT to commit
- Profiles as the place business access lives (use permission sets instead).
- `.sfdx/`, org auth files, consumer secrets, JWT private keys.
- Retrieved junk you did not mean to ship (user lists in `*.profile`, certificate bodies, sandbox-only endpoints).

### Destructive changes
Deletes are a separate `destructiveChanges.xml`, not a side effect of "it wasn't in the folder." A delete in production is not undone by Git — rollback means recreating metadata; records on a deleted custom object are gone.

</details>

<details>
<summary>7. Handle sandbox strategy (creation, refresh, data masking)</summary>

### Sandbox types
| Type | Metadata | Data | Use it for |
|------|----------|------|------------|
| Developer | Yes | No | Isolated build |
| Developer Pro | Yes | No (more room) | QA without rows |
| Partial Copy | Yes | Template sample | UAT with some rows |
| Full | Yes | All of prod | Pre-prod, performance, real shape |

### Masking (bank-critical)
Full copies contain customer data. Salesforce Data Mask is the named product; many banks also use a vendor tool or reviewed script. You must be able to say: what gets masked (email, phone, government ID, account number, birth date), who confirms mask complete, and that unmasked Full sandboxes are not for broad logins.

### Setup paths
- List/refresh sandboxes: Setup > Sandboxes
- Sandbox templates (Partial Copy): Setup > Sandboxes > Sandbox Templates
- Allow inbound deploys: Setup > Deploy > Deployment Settings
- View running deploys: Setup > Deploy > Deployment Status
- Data Mask: App Launcher > Data Mask (after managed package installed)

</details>

<details>
<summary>8. Resolve deployment conflicts — Profiles & Permission Sets</summary>

### Profile problem
`Admin.profile-meta.xml` is a dump of user permissions, object permissions, field permissions, layout assignments, and record-type visibility. Two stories editing it conflict; a bad merge grants/removes access you did not review.

### The fix to coach
Stop putting story access in profiles. Ship a permission set (or permission set group) per persona/feature. Deploy that. Leave the profile alone unless the story truly changes a profile-only setting.

### Legacy orgs
If profiles must be deployed, deploy a thin delta with a tool that supports profile decomposition, and require a second person to read the permission diff. Do not hand-merge a 10,000-line profile.

### Permission sets
Still conflict if every story edits one giant `CB_Admin` permission set. Split by feature/persona. Use permission set groups to bundle for a job function without a monolith.

</details>

<details>
<summary>9. Resolve deployment conflicts — Record Types & Page Layouts</summary>

### Record Type deploy failure modes
A record-type deploy fails, or succeeds and users still can't use it, when any of these are missing:
- The business process and picklist values the record type depends on.
- The page-layout assignment.
- Visibility on the profile or permission set.

**Rule:** Deploy record type, layout, and the permission set granting visibility in **one** payload. Do not deploy the record type Monday and the permission set "later."

### Page layouts
The layout file is not the assignment — assignment lives on profile + record type. Don't confuse classic page layout with Lightning record page (FlexiPage). Testers say "the page is wrong" when the Lightning page was never activated for the app.

</details>

<details>
<summary>10. Resolve deployment conflicts — Flows, Apex, and dependencies</summary>

### Flows
Flow XML does not merge. Two developers editing the same flow lose one side.
- One owner per flow in a release, or split work into subflows.
- Know whether your deploy leaves the new version Draft or Active. Check in a sandbox before promising prod behavior.
- Fast mitigation: activate the previous Flow version in Setup > Flows, then redeploy the last good tag so Git matches org.

### Apex & dependencies
- Deploy the class **and its test** in the same payload.
- A test that does `SELECT Id FROM Account LIMIT 1` and assumes a row passes in Dev, fails in empty QA. Tests create their own data.
- A trigger with no coverage blocks production. A class calling an undeployed class fails at compile in the target. Read the error, add the missing member, redeploy validation. Never "try it in prod."

</details>

<details>
<summary>11. Recommend best practices to reduce deployment failures and rework</summary>

- Dry-run before every real deploy.
- Tests create their own data; no reliance on org data.
- One flow owner per release; subflows for parallel work.
- Permission sets over profile edits.
- Named credentials for callouts; no secrets in Git.
- Custom metadata/custom settings for toggles (ship dark, turn on after deploy).
- Bulkified Apex — ask the 200-record question.
- No `if (org.IsSandbox)` branches as a rule; config belongs in the target.

</details>

<details>
<summary>12. Branching strategies — feature, release, hotfix</summary>

```
main                          ← matches production
  hotfix/<ticket>             ← cut from main only
  release/2026-11-27          ← cut from main when release freezes
    feature/<ticket>-name     ← short-lived, merged into release branch
```

Rules:
- Feature branch lives days, not weeks. Salesforce XML (Flows, profiles) doesn't merge; long branches become "delete one side and hope."
- Release branch is what QA/UAT deploy. Developers do not deploy their feature branch into UAT.
- Tag production after success: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the change-ticket ID — that is the audit trail.

</details>

<details>
<summary>13. Automated testing and validation concepts</summary>

Three distinct actions interviews collapse:

| Action | Changes org? | Why run it |
|--------|--------------|------------|
| Validation / dry-run (`--dry-run`) | No | Prove payload compiles + tests pass against that org |
| Quick deploy | Yes | Promote a validation that already passed, inside the platform window, so you don't pay test runtime again during the change window |
| Real deploy | Yes | First deploy, or validation expired, or payload changed |

Quick deploy only works if nothing changed since validation. If someone hotfixed prod after your validation, quick deploy is no longer an honest rehearsal — re-validate.

Production rules:
- Payload with Apex must run tests.
- Salesforce requires 75% coverage as the production gate.
- `RunSpecifiedTests` = you name tests; your deployed Apex must be covered by them.
- `RunLocalTests` runs local tests, skips managed-package tests — the honest pre-release gate, but slow. Validate before the window, quick-deploy inside it.
- A green Dev sandbox is not evidence. The validation that counts is against the org you're about to change.

Test levels: `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`. Production rejects `NoTestRun` when payload contains Apex.

</details>

<details>
<summary>14. DevOps tools — Gearset, Copado, AutoRabit, or equivalent</summary>

### What they all sit on
Salesforce CLI (`sf`) / Metadata API. Every vendor UI is a UI over this engine. You must be able to run a dry-run and read the failure regardless of tool.

### Gearset
Compare & deploy, CI, backups (edition-dependent). Compare orgs, surface forgotten metadata, gate on tests.

### Copado
User stories, pipelines, compliance packs. Common in large programs. Pipeline and promotion path, not just "we have Copado."

### AutoRabit
CI/CD and data tooling in the same category. Same interview answer: promotion path, back-promotion, where secrets live.

### Change Sets
Setup UI between related orgs. Why they fail at this job's scale: no reviewable diff, no hotfix branch, unmergeable profile XML, no rollback tag. Know them, then retire them for this role.

### DevOps Center
Salesforce native: work items, Git, promotion. Native option when the bank won't add a vendor — still not a reason to skip Git discipline.

</details>

<details>
<summary>15. Apex & Triggers</summary>

- Deploy class + test together.
- Tests insert their own data; no `LIMIT 1` assumptions on org data.
- Bulkified — must handle 200 records, not just one.
- No trigger without coverage in production.
- Dependency order matters: deploy class B before class A that calls it.

</details>

<details>
<summary>16. Flows (Before/After Save)</summary>

- Before-save vs after-save matters: a flow built as after-save that should be before-save times out under volume.
- You don't have to author it, but don't deploy a flow you can't describe.
- Flow XML doesn't merge — one owner per release.
- Check active version after deploy; new version may be Draft.

</details>

<details>
<summary>17. Permission Sets vs Profiles</summary>

| | Profile | Permission Set |
|---|---------|----------------|
| Granularity | Coarse, dump of many permissions | Fine, per feature/persona |
| Merge behavior | Poor — conflicts easily | Better, if kept small |
| Best use | Baseline org-wide settings | Story/feature access, bundled via groups |

Coaching: story access goes in permission sets, not `Admin.profile`.

</details>

<details>
<summary>18. Record Types, Page Layouts, and Security model</summary>

- Record type needs business process + picklist values + layout assignment + visibility (profile or permission set) — deploy together.
- Layout file ≠ layout assignment.
- Classic page layout ≠ Lightning record page (FlexiPage).
- Security model: FLS, object permissions, sharing — verify in the diff before deploy.

</details>

<details>
<summary>19. Unlocked Packages / Managed Packages</summary>

| Kind | For | DevOps note |
|------|-----|-------------|
| Unlocked package | Your team, modular internal apps | Versioned, upgradeable, dependency list. Best for real boundaries (credit-application module), not "all of Sales Cloud." |
| Org-dependent unlocked package | Module still depending on unpackaged org metadata | Faster to adopt, harder to install elsewhere — say the limitation out loud. |
| Managed package (1GP/2GP) | ISV / hard IP boundary | You upgrade it; you don't edit its Apex in Git. Banks buy AppExchange products this way. |

Unpackaged metadata from Git is still the right default for a large existing bank org. Don't propose packaging the entire org on day one.

Dev Hub needed for 2GP + scratch orgs: Setup > Dev Hub. Unlocked packages don't require a namespace; managed usually do.

Commands (confirm flags with `--help`):
```
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```
Install only promoted (non-beta) versions into prod.

</details>

<details>
<summary>20. Exposure to Salesforce DX</summary>

- Modern CLI is `sf` (older `sfdx` still in runbooks; same family).
- DX project = folder of metadata XML + `sfdx-project.json`.
- Commands: `sf org login web`, `sf project retrieve start`, `sf project deploy start --dry-run`.
- Org Development Model and Salesforce DX Development Model (Trailhead) are the reference.

</details>

<details>
<summary>21. Experience in regulated or enterprise environments (banking, insurance, healthcare)</summary>

- Change control: ticket + window + backout + evidence.
- Segregation of duties.
- Data masking for sandboxes containing customer/PII data.
- Audit pack retention.
- No prod customer data in logs/tickets/slides.

</details>

<details>
<summary>22. Salesforce certifications — PD1, Advanced Admin, DevOps related certs</summary>

| Credential | Maps to | Link |
|------------|---------|------|
| Platform Developer I | PD1 the posting names; Apex, tests, platform model | trailhead.salesforce.com/credentials/platformdeveloperi |
| Platform App Builder | Objects, Flow, security metadata you move weekly | trailhead.salesforce.com/credentials/platformappbuilder |
| Advanced Admin | Posting names this; Salesforce renamed it Platform Administrator II | trailhead.salesforce.com/credentials/platformadministrator-ii |
| "Salesforce DevOps Engineer" cert | No official Salesforce one exists as of this writing. Copado/Gearset/AutoRabit offer vendor certificates — show tool time, don't replace PD1 | Vendor sites |

Study order: crash course + PD1 → this page's labs → Platform Administrator II topics overlapping releases (security, change, environments).

</details>

---

<details>
<summary>23. DevOps tools — practical usage and Gearset UI walkthrough</summary>

This section gives concrete technical examples for each tool, and exact Gearset UI locations for compare & deploy, backup, restore, and CI/CD.

### A. Salesforce CLI (`sf`) — the engine underneath every tool

Prerequisite: a Dev Hub + connected app with JWT, or a stored auth URL in CI secrets. Never `sf org login web` on a CI runner; never a password in the repo.

```bash
# Auth (JWT, CI-safe)
sf org login jwt --client-id $SF_CLIENT_ID --jwt-key-file server.key \
  --username $SF_CI_USERNAME --alias ci --instance-url https://login.salesforce.com

# Retrieve one metadata type from the trusted org
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev

# Inspect before committing
cat force-app/main/default/permissionsets/CB_Release_Reader.permissionset-meta.xml

# Dry-run deploy to the next org (no changes made)
sf project deploy start --dry-run --manifest manifest/package.xml \
  --test-level RunSpecifiedTests --tests CommercialBankingReleaseTest --target-org qa

# Real deploy
sf project deploy start --manifest manifest/package.xml --target-org qa

# Destructive changes (separate file)
sf project deploy start --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChanges.xml --target-org qa

# Apex tests
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 30 --target-org qa

# Package version (after Dev Hub + package exists)
sf package version create --package CB_Credit --installation-key-bypass \
  --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

### B. Gearset — UI walkthrough

Gearset's UI is organized around a few top areas. Button paths shift by edition/version; these are the canonical locations.

#### 1. Compare & Deploy (metadata promotion)
Path: **Dashboard → Compare & Deploy** (or top nav "Compare").

1. Choose **Source org** and **Target org** from your connected org list.
2. Select metadata types to compare (e.g., Apex Classes, Flows, Permission Sets, Custom Objects, Record Types, Page Layouts).
3. Run the comparison. Gearset shows a component-level diff: items in source only, target only, or different.
4. Review each difference side-by-side (XML diff viewer). Select components to include.
5. Click **Deploy**. Gearset builds a deployment package (internally a Metadata API deploy) and shows a deployment summary with job ID.
6. After completion, view **Deployment Status** for success/failure and any component errors.

Practical example: promote a new `CB_CreditApplication` Flow from Dev to QA.
- Source = Dev org, Target = QA org, metadata types = Flow + Custom Field + Permission Set.
- Run compare → select the flow, the field it references, and the permission set granting access → deploy → verify activation status in QA Setup > Flows.

#### 2. Org Browser
Path: **Org Browser** (left nav or top nav).

Use it to browse metadata in a single org without a comparison. Useful for:
- Verifying a component exists in the target before including it in a deploy.
- Checking the active version of a Flow.
- Confirming permission set assignments before a release.

#### 3. Backup
Path: **Backup** (top nav or "Org Backup & Restore").

1. Select the org to back up.
2. Configure backup schedule (daily/weekly) and retention.
3. Choose metadata + data scope (Gearset can back up metadata and, on applicable editions, records/data).
4. Run an on-demand backup or wait for the scheduled one.
5. View **Backup history**: each backup has a timestamp and status.
6. To restore: **Backup → Restore**, pick a backup date, select components, choose target org, run restore.

Practical example: recover an accidentally deleted Apex class in QA.
- Backup → Restore → select last night's QA backup → choose the deleted class → target = QA → restore.

#### 4. CI/CD (continuous integration)
Path: **CI/CD** (top nav).

1. Connect your Git repository (GitHub, Bitbucket, Azure DevOps, GitLab) via OAuth/app installation.
2. Create a pipeline: select source branch → target org → metadata filter → validation/test settings.
3. Configure triggers: on pull request, on merge to `main`/`release/*`, or scheduled.
4. Gearset runs a validation deploy to a scratch/sandbox org and reports pass/fail with the deployment ID.
5. For promotion, create a "deployment pipeline" linking Dev → QA → UAT → Prod with approval gates between stages.

#### 5. Comparison / diff review (pre-deploy gate)
Inside Compare & Deploy after running a comparison:
- **Differences tab**: component-level list.
- **Diff viewer**: side-by-side XML for each selected component — this is your "second person reads the diff" audit artifact.
- **Dependencies tab**: Gearset surfaces related components (e.g., selecting a Flow also suggests its custom fields and permission sets), reducing "missing dependency" failures.

### C. Copado — practical usage

Copado centers on **user stories** and **promotion pipelines**.

1. Create a user story linked to a Jira/Azure DevOps ticket.
2. Commit metadata from a sandbox to the story (Copado commits to Git behind the scenes).
3. Add the story to a user story / deployment pipeline (e.g., Dev → QA → UAT → Prod).
4. Run validation/deployment steps in the pipeline; each stage can require approvals.
5. Copado records commit → pipeline → deployment for audit.
6. Compliance Packs add segregation-of-duties enforcement and certified deployment steps.

Key concept: **promotion path** and **back-promotion** (moving fixes from higher envs back down) are explicit Copado operations, unlike raw CLI where you script them.

### D. AutoRabit — practical usage

AutoRabit combines CI/CD with data deployment.

1. Connect version control (Git) and orgs.
2. Create a build: select components from source branch/org.
3. Run CI build → automated test execution → deployment to target.
4. Data deployment module: move data (records) between orgs alongside metadata, with masking options.
5. Pipeline view shows promotion status across environments; rollback is a redeploy of a prior successful build version.

### E. DevOps Center (Salesforce native)

Path: Setup → search "DevOps Center" (must be enabled).

1. Create a **work item** linked to a Git branch/commit.
2. Use the built-in Git integration to commit promoted metadata from a sandbox.
3. Promote work items through stages (e.g., Dev → Test → Prod) with change sets under the hood.
4. View deployment history and rollback options within Setup.

Native option when the bank won't add a vendor — still requires Git discipline and does not replace the audit pack.

</details>

---

<details>
<summary>24. CI/CD pipeline on GitHub + Salesforce — architecture and best practices</summary>

### Reference architecture

```
Developer
   │  pushes feature/<ticket>
   ▼
GitHub (source of truth)
   │
   ├── Pull Request ─────┐
   │                     ▼
   │             GitHub Actions
   │             ├─ Auth (JWT / stored auth URL)
   │             ├─ sf project retrieve (CI org baseline)
   │             ├─ sf project deploy start --dry-run + tests
   │             └─ Report pass/fail + diff
   │                     │
   │             Approved (non-author reviewer)
   │                     ▼
   │             Merge → release/<date>
   │                     ▼
   │             GitHub Actions
   │             ├─ Deploy to QA (real deploy)
   │             ├─ Deploy to UAT (validation-only / real)
   │             ├─ Release manager promotes to Pre-Prod
   │             └─ Change window: Quick Deploy or fresh deploy to Prod
   │                     ▼
   │             Tag: release-2026-11-27
   │             Write deploy IDs to ticket
   │
   └── Hotfix branch (from main) ── same pipeline, smaller payload
```

### Sample GitHub Actions workflow

File: `.github/workflows/salesforce-release.yml`

```yaml
name: Salesforce Release CI/CD

on:
  push:
    branches: [release/*]
  pull_request:
    branches: [main, release/*]

permissions:
  contents: read
  id-token: write   # for OIDC/JWT auth if using connected app with OIDC

jobs:
  validate:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Install Salesforce CLI
        run: |
          npm install -g sfdx-cli || true  # prefer official sf installer in practice

      - name: Authenticate to CI org (JWT)
        run: |
          echo "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt --client-id ${{ secrets.SF_CONNECTED_APP_CLIENT_ID }} \
            --jwt-key-file server.key --username ${{ secrets.SF_CI_USERNAME }} \
            --alias ci --instance-url https://login.salesforce.com

      - name: Dry-run deploy + specified tests
        run: |
          sf project deploy start --dry-run \
            --manifest manifest/package.xml \
            --test-level RunSpecifiedTests \
            --tests CommercialBankingReleaseTest \
            --target-org ci \
            --json > deploy-result.json
          cat deploy-result.json | jq '.status'

      - name: Publish diff artifact (audit)
        uses: actions/upload-artifact@v4
        with:
          name: deploy-result
          path: deploy-result.json

  deploy-qa:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/heads/release/')
    steps:
      - uses: actions/checkout@v4
      - name: Authenticate to QA org
        run: |
          echo "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt --client-id ${{ secrets.SF_CONNECTED_APP_CLIENT_ID }} \
            --jwt-key-file server.key --username ${{ secrets.SF_QA_USERNAME }} \
            --alias qa --instance-url https://login.salesforce.com
      - name: Deploy to QA
        run: |
          sf project deploy start --manifest manifest/package.xml --target-org qa

  deploy-prod:
    needs: deploy-qa
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/release/*'
    steps:
      - uses: actions/checkout@v4
      - name: Authenticate to Prod (integration user)
        run: |
          echo "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt --client-id ${{ secrets.SF_CONNECTED_APP_CLIENT_ID }} \
            --jwt-key-file server.key --username ${{ secrets.SF_PROD_USERNAME }} \
            --alias prod --instance-url https://login.salesforce.com
      - name: Quick deploy or fresh deploy to Prod
        run: |
          # Prefer quick deploy if a recent validation exists and nothing changed;
          # otherwise a fresh deploy.
          sf project deploy start --manifest manifest/package.xml --target-org prod
      - name: Tag production
        run: |
          git config user.name "release-engineer"
          git config user.email "release-engineer@bank.example"
          git tag -a release-${{ github.run_id }} -m "Prod deploy ${{ github.run_id }}"
          git push origin release-${{ github.run_id }}
```

### Why this shape, per best practices

| Practice | Reason |
|----------|--------|
| Git is source of truth; prod is a target | Prevents "edit in Setup and forget" drift; every change reviewable |
| Dry-run on PR, real deploy after merge | Catches missing dependencies and test failures before the change window |
| Tests run on PR, not only in prod | 75% coverage gate enforced early; `RunSpecifiedTests` names coverage responsibility |
| Non-author approves PR | Segregation of duties; audit requirement |
| Deploy IDs + tag written to ticket | Audit pack; rollback target is the tag |
| JWT / stored auth URL, no passwords in repo | Security / compliance; integration user, not shared admin |
| Quick deploy inside window, fresh deploy if validation expired | Honest rehearsal; prod changes after validation invalidate quick deploy |
| Separate `destructiveChanges.xml` | Deletes are explicit, not side effects; recoverable |
| Sandboxes masked before broad login | Data privacy in regulated environments |
| One integration user deploys; a human approves | Structural segregation of duties |

### Pipeline stage definitions (mapped to JD)

- **Validate** — PR trigger → dry-run + tests → CI sandbox. Covers "CI/CD pipelines for Salesforce using Git based workflows" and "automated testing and validation."
- **Integrate** — merge to release branch → real deploy to QA. Covers multi-environment strategy.
- **Stage** — release manager → validation-only deploy → Pre-Prod. Covers scheduled releases and pre-prod dress rehearsal.
- **Release** — change window → quick deploy / fresh deploy → Prod → tag. Covers scheduled/hotfix/emergency deploys and audit.

</details>

---

<details>
<summary>25. Lab exercises (free Developer Edition orgs; never a bank org)</summary>

### Lab A — Retrieve, review, dry-run
1. Create two Developer Edition orgs; alias `dev` and `qa`.
2. In `dev`, create permission set `CB_Release_Reader` with read on Account.
3. `sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev`. Read the XML.
4. `sf project deploy start --dry-run --target-org qa`, then real deploy.
5. Change the permission set directly in `qa` Setup. Retrieve. Observe the diff — this is the "edited in prod" problem.
Done when the only path into `qa` is Git and you can explain the diff in one sentence.

### Lab B — Profile conflict, on purpose
1. Two branches, each adding a different field permission to the same profile XML. Merge → conflict.
2. Replace with two permission sets. Merge those (no conflict).
3. Write: why the profile conflicted, what a bad merge would grant, what you tell a developer asking to edit `Admin.profile` for one field.

### Lab C — Failing validation
1. Apex class referencing a second class you do not deploy. Dry-run → capture error.
2. Add missing class. Dry-run again.
3. Test querying `Account` without inserting. Run in empty org → fail. Fix test to insert the row.
Done when you map an error string to "missing dependency" vs "test depends on org data" without guessing.

### Lab D — Runbook
Fill the runbook template (Section 10 of the training page) for Lab A as if `qa` were production. Include a rollback tag. Habit, not perfection.

### Lab E — Sandbox + mask checklist
Write the checklist for a refresh ticket: sandbox name/type/why, next eligible refresh, template, fields to mask, who confirms mask complete, who may log in before confirmation, which integration endpoints point to non-prod first.

</details>

---

<details>
<summary>26. Interview drill answers (short form)</summary>

1. **Source of truth?** Git. Production is a deploy target. Setup-vs-Git disagreement is an incident.
2. **Change to prod walk:** feature branch → PR → dry-run + tests → merge to release branch → QA → UAT → prod validation before window → approval → quick deploy/fresh deploy → tag → ticket updated with both deploy IDs.
3. **Hotfix during open release?** Cut from `main`, merge back to `main` and the open release branch.
4. **Why profile deploys are risky:** profiles are a permission grab bag; two stories conflict; bad merge ships un-reviewed access. Prefer permission sets.
5. **Flow deployed but users see old screen:** new version likely not Active. Check Setup > Flows before redeploying.
6. **Validate vs quick deploy:** validate doesn't change the org; quick deploy applies an already-passed validation inside the platform window.
7. **Unlocked vs managed:** unlocked is yours and versioned (internal modules); managed is upgraded, not edited. Packaging the whole bank org day one is not a plan.
8. **Auditor hand-off:** ticket, diff, non-author approver, validation ID, prod deploy ID, test run, tag, and for Full sandboxes, mask-complete evidence.

</details>

---

*Source: cross-reference of Scotiabank Requisition 276046 and the Release Engineering Training page (built from that posting). Verify CLI flags and Gearset UI paths against your installed editions; button locations shift by vendor release.*
