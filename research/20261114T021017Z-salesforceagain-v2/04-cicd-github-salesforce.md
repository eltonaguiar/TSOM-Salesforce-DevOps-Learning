# 04 — CI/CD on GitHub + Salesforce (Best-Practice Pipeline)

> **Scope:** "Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows" + "Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab)" + "branching strategies" + "automated testing and validation" + "runbooks, rollback procedures."
> **Assumption:** GitHub Actions as the reference implementation. §10 maps the same stages to Azure DevOps and GitLab.

---

## 1. The pipeline in one picture

```text
feature/<ticket> ──PR──▶ release/<date> ──▶ main (prod)
      │                     │                  │
   validate.yml         deploy-uat.yml     release-prod.yml
   (dry-run + tests)    (real deploy)      (validate → approval → quick deploy)
      │                     │                  │
   CI sandbox            QA / UAT           Pre-Prod → Prod
```

**Two rules that do most of the work:**

1. **Nothing reaches a protected branch without a green validation.**
2. **Production is deployed from `main` only, inside a change window, by a pipeline with an approval gate — never by a human clicking in Setup.**

---

## 2. Branch → environment mapping

| Branch | Purpose | Deploys to | Trigger |
|---|---|---|---|
| `feature/<ticket>-slug` | Short-lived work | CI sandbox (validate only) | PR open/sync |
| `release/<YYYY-MM-DD>` | Release candidate | QA → UAT | Merge / manual |
| `main` | Mirror of production | Pre-Prod validate → Prod | Merge / manual with approval |
| `hotfix/<ticket>` | Prod defect | Prod (same gates, smaller payload) | Cut from `main`, manual with approval |

**Rules**

- Feature branches live **days**, not weeks — Salesforce XML does not merge well.
- A hotfix is cut from **`main`** (what production runs), then merged back to `main` and any open release branch.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the **change ticket ID**. That is the audit trail.

---

## 3. Authentication: the part that gets audited

<details>
<summary><strong>3.1 JWT bearer flow (recommended)</strong></summary>

A **Connected App** with a digital certificate, plus a dedicated **integration user**, plus JWT. The private key lives in GitHub Secrets; the pipeline authenticates without a password and without a browser.

**Setup once**

1. Create a **Connected App** (Setup > App Manager > New Connected App).
2. Enable OAuth; select **Use digital signatures**; upload the certificate.
3. Scopes: at minimum `api`, `refresh_token` (and `web` if needed).
4. Create/assign a dedicated **integration user** with a permission set that allows metadata deploy + Apex test. Not a human admin.
5. Pre-authorize the connected app for the integration user (or use the JWT `sub`).
6. Store the **consumer key**, **username**, **instance URL**, and **private key** as GitHub secrets/environment secrets.

**Login**

```bash
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file server.key \
  --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" \
  --alias ci
```

**Why JWT over username/password:** no stored password, no MFA bypass, revocable certificate, attributable to one integration identity.
</details>

<details>
<summary><strong>3.2 SFDX auth URL (simpler, still acceptable)</strong></summary>

```bash
echo "$SFDX_AUTH_URL" | sf org login sfdx-url --sfdx-url-stdin --alias ci
```

- Generated from an already-authenticated CLI session: `sf org display --verbose --json` → `sfdxAuthUrl`.
- Treat the auth URL as a **secret** (it contains a refresh token).
- Rotate it; scope it to a dedicated integration user.
- Prefer JWT for long-lived CI; auth URLs are convenient for short-lived or dev-only pipelines.
</details>

<details>
<summary><strong>3.3 Never do these</strong></summary>

- `sf org login web` on a runner (interactive, non-deterministic).
- Store a password, security token, or private key in the repo.
- Use a human admin's credentials.
- Give the integration user **System Administrator** when a scoped permission set suffices.
- Log the auth URL or token (`set -x` with secrets).
</details>

<details>
<summary><strong>3.4 Secrets layout</strong></summary>

Use **GitHub Environments** so production secrets are only available to jobs that target the production environment (and can require reviewers).

| Secret | Scope | Contents |
|---|---|---|
| `SF_CONSUMER_KEY` | repo/env | Connected App consumer key |
| `SF_USERNAME` | repo/env | Integration user username |
| `SF_INSTANCE_URL` | repo/env | `https://login.salesforce.com` or test.salesforce.com |
| `SF_JWT_KEY` | repo/env | Private key PEM |
| `SF_CI_ORG_ALIAS` | repo | Alias/username for the CI sandbox |
| `SF_UAT_ORG_ALIAS` | uat env | UAT alias |
| `SF_PROD_ORG_ALIAS` | production env | Prod alias |

> For sandboxes, the instance URL is typically `https://test.salesforce.com` for login, and the org-specific My Domain URL after auth.
</details>

---

## 4. Delta deploys (why and how)

<details>
<summary><strong>4.1 Why delta</strong></summary>

Full-repo deploys are slow, consume API limits, and can accidentally deploy unrelated in-flight work. A **delta** deploy sends only the components changed between two Git refs.

- Faster validations → more PRs validated per day.
- Fewer API calls → protects the 24 h allocation.
- Smaller blast radius → easier rollback reasoning.
- Better for monorepos and long histories.

Trade-off: delta tools can miss dependencies. Always deploy the generated `package.xml` **and** let the platform/tool resolve dependencies, then read failures.
</details>

<details>
<summary><strong>4.2 `sfdx-git-delta` (the common plugin)</strong></summary>

```bash
sf plugins install sfdx-git-delta

mkdir -p delta
sf sgd source delta \
  --from "origin/${{ github.base_ref }}" \
  --to "HEAD" \
  --output-dir delta \
  --generate-delta
```

Produces:

- `delta/package/package.xml`
- `delta/` source tree
- `delta/destructiveChanges/destructiveChanges.xml` (post-destructive)

Deploy the delta:

```bash
sf project deploy validate \
  --source-dir delta \
  --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
  --target-org ci \
  --test-level RunLocalTests \
  --wait 60
```

> `--post-destructive-changes` should be used only when the file exists. In CI, guard it.

**Flag drift warning:** plugin and CLI flags change between majors. Run `sf sgd source delta --help` and `sf project deploy validate --help` in the pipeline image before publishing a command.
</details>

---

## 5. Workflow: validate on every PR

`.github/workflows/validate.yml`

```yaml
name: Salesforce Validate

on:
  pull_request:
    branches: [main, 'release/**']
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: validate-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - name: Checkout (full history for delta)
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Salesforce CLI
        run: |
          npm install --global @salesforce/cli
          sf --version

      - name: Install delta plugin
        run: |
          echo y | sf plugins install sfdx-git-delta

      - name: Write JWT key
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key

      - name: Authenticate to CI org (JWT)
        run: |
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias ci
          sf org display --target-org ci

      - name: Build delta package
        run: |
          mkdir -p delta
          sf sgd source delta \
            --from "origin/${{ github.base_ref }}" \
            --to "HEAD" \
            --output-dir delta \
            --generate-delta

      - name: Validate delta (dry run, run local tests)
        run: |
          if [ ! -f delta/package/package.xml ]; then
            echo "No metadata changes; skipping validation."
            exit 0
          fi
          DESTRUCTIVE=""
          if [ -f delta/destructiveChanges/destructiveChanges.xml ]; then
            DESTRUCTIVE="--post-destructive-changes delta/destructiveChanges/destructiveChanges.xml"
          fi
          sf project deploy validate \
            --source-dir delta \
            $DESTRUCTIVE \
            --target-org ci \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Publish summary
        if: always()
        run: |
          echo "## Salesforce validation" >> "$GITHUB_STEP_SUMMARY"
          echo "Ref: \`${{ github.head_ref }}\` → \`${{ github.base_ref }}\`" >> "$GITHUB_STEP_SUMMARY"
          echo "Result: see the *Validate delta* step log." >> "$GITHUB_STEP_SUMMARY"

      - name: Cleanup key
        if: always()
        run: rm -f server.key
```

**Design notes**

- `fetch-depth: 0` is required for a correct merge-base delta.
- `cancel-in-progress: true` saves API budget on rapid pushes.
- `RunLocalTests` (not `RunAllTestsInOrg`) avoids running managed-package tests.
- The key is deleted even on failure.
- The PR comment/summary is the human-readable evidence link.

---

## 6. Workflow: deploy to UAT on merge to the release branch

`.github/workflows/deploy-uat.yml`

```yaml
name: Deploy to UAT

on:
  push:
    branches: ['release/**']

permissions:
  contents: read

concurrency:
  group: deploy-uat-${{ github.ref }}
  cancel-in-progress: false   # never cancel a deploy mid-flight

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    environment:
      name: uat
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI + delta
        run: |
          npm install --global @salesforce/cli
          echo y | sf plugins install sfdx-git-delta

      - name: Auth to UAT
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias uat

      - name: Build delta from previous commit
        run: |
          mkdir -p delta
          sf sgd source delta \
            --from "HEAD^" \
            --to "HEAD" \
            --output-dir delta \
            --generate-delta

      - name: Deploy to UAT
        run: |
          DESTRUCTIVE=""
          if [ -f delta/destructiveChanges/destructiveChanges.xml ]; then
            DESTRUCTIVE="--post-destructive-changes delta/destructiveChanges/destructiveChanges.xml"
          fi
          sf project deploy start \
            --source-dir delta \
            $DESTRUCTIVE \
            --target-org uat \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Cleanup
        if: always()
        run: rm -f server.key
```

> For UAT you often want a **full release-branch payload**, not a single-commit delta, because UAT must match the release candidate. Use `--source-dir force-app` or the release manifest in that case. Delta is right for feature/PR validation; the release candidate should be deployed as a coherent unit.

---

## 7. Workflow: production release with approval + quick deploy

`.github/workflows/release-prod.yml`

```yaml
name: Release to Production

on:
  workflow_dispatch:
    inputs:
      release_tag:
        description: 'Tag to deploy (e.g. release-2026-11-27)'
        required: true
      change_ticket:
        description: 'Change ticket ID'
        required: true

permissions:
  contents: read

concurrency:
  group: deploy-prod
  cancel-in-progress: false

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    environment:
      name: preprod
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.release_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Pre-Prod
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias preprod

      - name: Validate release against Pre-Prod
        id: validate
        run: |
          sf project deploy validate \
            --source-dir force-app \
            --target-org preprod \
            --test-level RunLocalTests \
            --wait 120 \
            --json > validate.json
          JOB_ID=$(jq -r '.result.id' validate.json)
          echo "job_id=$JOB_ID" >> "$GITHUB_OUTPUT"
          echo "Validated. Job: $JOB_ID"

      - name: Upload validation evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ inputs.change_ticket }}
          path: |
            validate.json
            server.key
          retention-days: 30

      - name: Cleanup key
        if: always()
        run: rm -f server.key

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 60
    environment:
      name: production        # configure required reviewers in repo settings
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.release_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Production
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod

      - name: Quick deploy the validated job
        run: |
          sf project deploy quick \
            --job-id "${{ needs.validate.outputs.job_id }}" \
            --target-org prod \
            --wait 60 \
            --verbose

      - name: Create release tag
        run: |
          git tag -a "deployed-$(date -u +%Y%m%dT%H%M%SZ)" -m "Prod deploy ${{ inputs.change_ticket }}"
          git push origin --tags

      - name: Cleanup key
        if: always()
        run: rm -f server.key
```

**Critical details**

- The **quick deploy is only honest if nothing relevant changed** in Pre-Prod/Prod since validation. If a hotfix landed, re-validate.
- Quick Deploy is valid for **10 days**; the release calendar must fit inside that.
- The `production` GitHub Environment must have **required reviewers** configured in Settings → Environments. That is the segregation-of-duties control.
- `needs.validate.outputs.job_id` requires `id: validate` and the `job_id` output — shown above.
- Tag **after** a successful deploy; the tag is the rollback target.
- If `sf project deploy quick` is unavailable in your CLI major, use `sf project deploy resume --job-id` or re-validate + deploy; run `--help`.

---

## 8. Gates and quality checks

<details>
<summary><strong>8.1 The gate table</strong></summary>

| Gate | Where | Blocks |
|---|---|---|
| Compile/validate | PR workflow | Merge |
| Apex tests (`RunLocalTests`) | PR + release validation | Merge / deploy |
| 75% coverage | Platform-enforced in prod | Prod deploy |
| Static analysis (PMD/CodeScan) | PR workflow (optional) | Merge (if configured) |
| Permission diff review | PR review + tool diff | Merge |
| Required reviewers | GitHub Environment `production` | Prod deploy |
| Change ticket present | Workflow input validation | Prod deploy |
| Rollback tag exists | Pre-release check | Prod deploy |
| Concurrency lock | `concurrency` group | Parallel prod deploys |
</details>

<details>
<summary><strong>8.2 Optional static analysis (PMD)</strong></summary>

```yaml
- name: Install PMD
  run: |
    curl -sSLo pmd.zip https://github.com/pmd/pmd/releases/latest/download/pmd-dist.zip
    unzip -q pmd.zip
- name: Run PMD on Apex
  run: |
    ./pmd-bin-*/bin/run.sh pmd \
      -d force-app \
      -R rulesets/apex/quickstart.xml \
      -f text
```

Use it to catch SOQL/DML-in-loop and sharing violations **before** review. Do not make it the only gate; it is not a substitute for tests.
</details>

<details>
<summary><strong>8.3 Coverage parsing</strong></summary>

```bash
sf apex run test --target-org ci --test-level RunLocalTests \
  --code-coverage --result-format json --wait 60 > test.json

jq '[.result.coverage.coverage[] | {name: .name, pct: .coveredPercent}] | sort_by(.pct) | .[0:10]' test.json
```

Fail the job if org-wide coverage drops below a threshold (e.g., 80% internal bar, above the 75% platform gate).
</details>

---

## 9. Rollback runbook

<details>
<summary><strong>9.1 Rollback workflow</strong></summary>

`.github/workflows/rollback.yml`

```yaml
name: Rollback Production

on:
  workflow_dispatch:
    inputs:
      target_tag:
        description: 'Last known-good tag (e.g. release-2026-11-20)'
        required: true
      incident_ticket:
        description: 'Incident/change ticket'
        required: true

permissions:
  contents: read

concurrency:
  group: deploy-prod
  cancel-in-progress: false

jobs:
  rollback:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.target_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Production
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod

      - name: Validate the rollback payload first
        run: |
          sf project deploy validate \
            --source-dir force-app \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 60

      - name: Deploy the last known-good tag
        run: |
          sf project deploy start \
            --source-dir force-app \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Cleanup
        if: always()
        run: rm -f server.key
```

</details>

<details>
<summary><strong>9.2 What rollback cannot do</strong></summary>

- **Undo data changes.** Metadata rollback ≠ data rollback. Restore data from a backup (Vault/Gearset/own tooling) or run a reviewed reverse script.
- **Undelete records** on a destructively deleted object.
- **Rescue a deleted field's data** after the recycle bin window.
- **Fix a managed-package upgrade** unless the vendor supports version rollback.

**The rule:** if you do not have a tag from the last good production deploy, you do not have a rollback. Fix that before the next release.
</details>

---

## 10. Same pipeline, other tools

<details>
<summary><strong>10.1 Azure DevOps</strong></summary>

- **Repos** for Git; **Pipelines** (YAML) for CI/CD.
- **Environments** + **Approvals and checks** replace GitHub Environments for SoD.
- **Variable groups** + Azure Key Vault replace GitHub Secrets.
- Stages: `Validate`, `DeployQA`, `DeployUAT`, `DeployProd` with `dependsOn`.
- Same `sf` CLI commands; same delta plugin.
</details>

<details>
<summary><strong>10.2 GitLab CI</strong></summary>

- `.gitlab-ci.yml` with `stages: [validate, deploy-qa, deploy-uat, deploy-prod]`.
- **Protected environments** + **Deploy approvals** for SoD.
- **CI/CD variables** (masked/protected) for secrets; or external secret manager.
- Same `sf` CLI commands; cache the CLI and plugins.
</details>

<details>
<summary><strong>10.3 Jenkins (legacy but common in banks)</strong></summary>

- Pipeline as code (`Jenkinsfile`), credentials binding, agents.
- Same `sf` CLI + delta; the hard part is secrets and agent hygiene.
- Common in regulated enterprises; document it even if you prefer GitHub Actions.
</details>

---

## 11. Anti-patterns (each one is an interview red flag)

| Anti-pattern | Why it fails |
|---|---|
| `sf org login web` in CI | Interactive, brittle, no audit identity |
| Password/security token in repo | Secret leak; MFA incompatibility |
| Deploying from a feature branch to prod | Bypasses release branch + review |
| `NoTestRun` in prod with Apex | Platform rejects; or ships untested |
| Full-repo deploy on every PR | API exhaustion; slow; deploys unrelated work |
| No `fetch-depth: 0` | Delta is wrong or empty |
| Cancel a deploy mid-flight | Partial state; inconsistent org |
| No concurrency lock | Two prod deploys race |
| No rollback tag | No rollback |
| Human clicks Setup in prod | Drift; no audit trail |
| Pipeline uses a human admin identity | No SoD; credential risk |
| Green deploy treated as "done" | Assignments/activation missed |

---

## 12. Runbook template (fill for every prod promotion)

```text
Change ticket:
Release tag:
Payload (source dir or manifest):
Source branch / commit:
Validation org / deploy id / time:
Tests run and coverage:
Prod deploy id / time:
Approver (not the author):
Post-deploy steps (assignments/activation/flags):
Rollback tag:
Rollback owner:
How we will know it worked (one query, one screen, one test):
Data changes (if any) and reverse plan:
```

---

## 13. Interview drills

1. **Walk a change to prod.** Feature branch → PR → validate (delta + tests) → merge to release → UAT deploy → Pre-Prod validate → approval → quick deploy → tag → ticket updated with both deploy IDs.
2. **Why delta deploys?** Speed, API budget, smaller blast radius; trade-off is dependency resolution.
3. **How does CI authenticate?** JWT via connected app + certificate + dedicated integration user; secrets in GitHub Environments.
4. **How do you enforce segregation of duties?** Required reviewers on the `production` environment; integration user deploys, a human approves; different identities.
5. **What is quick deploy and when is it invalid?** Applies a prior successful validation within 10 days; invalid if the payload or target changed.
6. **How do you roll back?** Redeploy the last known-good tag after validating; data restore is separate.
7. **What stops a bad profile merge?** Permission sets per feature, thin profile deltas, second reviewer reading the permission diff.
8. **How do you keep it portable across CI vendors?** The pipeline is just `sf` CLI + Git; the CI tool is a runner and an approval mechanism.
9. **What is your evidence pack?** Ticket, PR, reviewer, validation ID, test/coverage, prod deploy ID, approver, tag, post-deploy verification, rollback tag.

---

**Next:** `05-jd-term-by-term.md` — every requisition line decoded, with the configuration/setting variations behind each term.
