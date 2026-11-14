# 04 — GitHub Actions + Salesforce CI/CD

> JD lines covered: R1 (design/implement/maintain CI/CD pipelines), R3 (scheduled/hotfix/emergency
> coordination), R4 (audit/security/compliance), Q4 (GitHub Actions, Azure DevOps, GitLab),
> Q6 (automated testing and validation).
>
> Every CLI flag below was read from the **Salesforce CLI plugin source**, not from memory — see
> `sources.md` §3. Where a flag does not exist, the doc says so.

---

## 1. Pipeline architecture

```
                    ┌──────────────────────┐
  pull_request ───▶ │  PR Validation        │  dry-run deploy + specified tests → CI sandbox
                    └──────────┬───────────┘
                               │ required status check
                               ▼
  push to main ────▶ ┌──────────────────────┐
                    │  QA deploy            │  real deploy → QA org
                    └──────────┬───────────┘
                               ▼
  push to release/* ─▶ ┌──────────────────────┐
                      │  UAT deploy           │  real deploy → UAT org
                      └──────────┬───────────┘
                                 ▼
  workflow_dispatch ─▶ ┌──────────────────────┐
   (or tag)           │  PROD: validate       │  sf project deploy validate → job id (10-day)
                      │  PROD: quick deploy   │  sf project deploy quick --job-id
                      └──────────┬───────────┘
                                 ▼
                        tag release-<date>
```

**Design rules that make this defensible to a bank:**

| Rule | Reason |
|---|---|
| PR validation is a **dry run**, never a real deploy to a shared org | Shared-org PR deploys cause the queue problem and contaminate the environment |
| The **same payload** is validated and deployed | A dry run of file A followed by a deploy of file B validates nothing |
| Tests run in **both** the PR and the prod validation | PR tests catch regressions early; prod validation proves the target org state |
| The prod job is **manual** (`workflow_dispatch`) or tag-triggered | A deploy should not fire because someone merged to `main` |
| `prod` is a **GitHub Environment** with required reviewers | The approving identity is recorded by the platform |
| The **concurrency group** serialises prod | Only one deployment runs at a time in Salesforce, and the queue is not FIFO (`02 §3.1`) |
| Every job publishes the **deployment id** as an artefact | The audit trail starts at the deployment id |
| The CLI version is **pinned** | A CLI release must not change deploy behaviour overnight |

---

## 2. Authentication

### 2.1 JWT bearer flow — the correct model for CI

**Why JWT and not a password or an auth URL:**

| Option | Verdict |
|---|---|
| Username + password | Never. Password policies, lockout policies, MFA, and the credentials live in the repo |
| `sf org login sfdx-url` with a stored refresh token | Legacy. The refresh token is a long-lived bearer secret; if the secret store leaks, the org is compromised until the token is revoked. Acceptable only if your security team signs off explicitly |
| **JWT bearer flow with a certificate** | **Recommended.** No password, no long-lived token, no human identity. The private key is the only secret |

### 2.2 The exact command

```bash
sf org login jwt \
  --username "$SF_USERNAME" \
  --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
  --client-id "$SF_CLIENT_ID" \
  --instance-url "$SF_INSTANCE_URL" \
  --alias org
```

**Verified flags** (`plugin-auth/src/commands/org/login/jwt.ts`):
`--username` (required, `-u`) · `--jwt-key-file` (required, `-f`) · `--client-id` (required, `-i`) ·
`--instance-url` (`-r`) · `--alias` (`-a`) · `--set-default` (`-s`) · `--set-default-dev-hub` (`-d`)
· `--no-prompt` (`-p`, hidden).

> **Correction — there is no `--client-secret` flag on `sf org login jwt`.** Some older runbooks
> show `--jwt-key` and `--client-secret`; neither exists in the current implementation. The flag is
> `--jwt-key-file`, and the authenticator is a **certificate**, not a secret. The old
> `force:auth:jwt:grant` alias still exists but is deprecated.

### 2.3 The Salesforce-side setup

1. **Create a digital certificate and private key** (OpenSSL, self-signed is fine for JWT).
2. **Create a Connected App** (or **External Client App** in newer orgs) with:
   - the certificate uploaded as the **Digital Certificate**,
   - the **consumer key** recorded as the client id,
   - OAuth scopes covering what the pipeline needs (`api`, `refresh_token`/`offline_access`, and
     `full` if you also move data),
   - the **Run As** user set to the integration user (and the user approved for the app).
3. **Create the integration user** with a **dedicated permission set** — not a human profile:
   - `API Enabled`
   - `Modify Metadata Through Metadata API Functions` **or** `Modify All Data`
   - `Customize Application` (Flow/LWC/custom metadata)
   - `Author Apex`, `Manage Flow`, `Manage Profiles and Permission Sets` as needed
   - `View Setup and Configuration` for read-only diagnostics
4. **Assign it to a profile** that permits login but grants nothing else. The user's own permissions
   should be a permission set, so revoking access is a metadata change, not a support ticket.
5. **Do not** give the integration user a session of its own beyond the permissions it needs.

### 2.4 Secret storage

| Secret | Contents | Scope |
|---|---|---|
| `SF_CLIENT_ID` | Connected App consumer key | Repository secret (not secret) |
| `SF_USERNAME` | Integration user username | Environment secret (per target org) |
| `SF_INSTANCE_URL` | `https://yourorg.my.salesforce.com` | Environment secret (per target org) |
| `SF_JWT_KEY_B64` | Base64 of the PEM private key | **Environment secret**, per target org |

**Materialise the key safely in the runner:**

```yaml
- name: Materialise JWT key
  run: |
    echo "${{ secrets.SF_JWT_KEY_B64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
    chmod 600 "$RUNNER_TEMP/jwt.pem"
```

**Never** write the key into the workspace (it would be picked up by `actions/upload-artifact`).
Use `$RUNNER_TEMP`.

### 2.5 OIDC — the honest answer

GitHub Actions can mint an OIDC token (`id-token: write`) and AWS/GCP/Azure can exchange it for
short-lived cloud credentials. **Salesforce does not document an equivalent token-exchange flow for
org authentication.** The supported non-interactive org auth model remains the JWT bearer flow with
a certificate.

If your bank requires short-lived credentials with no stored secret at all, the options are:

1. **A self-hosted runner** inside the bank's network with the certificate provisioned by the bank's
   PKI, with the key never leaving that host.
2. **A secrets broker** (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) that injects the
   key at run time — the secret is still a secret, but its storage and rotation are audited.
3. **A vendor deployment tool** whose own credential store is the bank's (Copado, AutoRABIT Vault,
   Gearset) — moves the problem, does not remove it.

**Say this in an interview:** "JWT with a certificate is the supported model. OIDC exchange is
standard in cloud, and Salesforce does not publish an equivalent for org auth, so the honest answer
is either a self-hosted runner with bank PKI or a brokered secret — not a long-lived refresh token
in a repo secret."

---

## 3. Repository layout

```
.
├── .github/
│   └── workflows/
│       ├── pr-validation.yml
│       ├── deploy-nonprod.yml
│       ├── prod-release.yml
│       └── _reusable-deploy.yml
├── .github/actions/sf-deploy/action.yml     # composite action
├── manifest/
│   ├── package.xml                          # the release payload
│   └── destructiveChanges.xml
├── sfdx-project.json
├── force-app/main/default/...
└── scripts/
    └── assert-coverage.sh
```

**`sfdx-project.json`** pins the source API version and package directories. `package.xml` pins
the API version used by the deploy. Both are release-control artefacts — a change to either is a
change to deploy behaviour and must be reviewed.

---

## 4. The workflows

### 4.1 PR validation — dry run + tests

```yaml
name: PR Validation

on:
  pull_request:
    branches: [main, 'release/**']
    types: [opened, synchronize, reopened]

permissions:
  contents: read

concurrency:
  group: pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true          # supersede stale runs on the same PR

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    permissions:
      contents: read
      id-token: write                # only if you add an OIDC-backed step
    environment: ci                  # secrets scoped to the CI environment

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Salesforce CLI (pinned)
        run: npm install -g @salesforce/cli@2.58.0

      - name: Cache CLI state
        uses: actions/cache@v4
        with:
          path: |
            ~/.sfdx
            ~/.sf
          key: sf-${{ runner.os }}-${{ hashFiles('sfdx-project.json', 'manifest/**') }}
          restore-keys: sf-${{ runner.os }}-

      - name: Materialise JWT key
        run: |
          echo "${{ secrets.SF_JWT_KEY_B64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
          chmod 600 "$RUNNER_TEMP/jwt.pem"

      - name: Authenticate (JWT bearer flow)
        run: |
          sf org login jwt \
            --username "${{ secrets.SF_USERNAME }}" \
            --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
            --client-id "${{ secrets.SF_CLIENT_ID }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias ci

      - name: Dry-run deploy to the CI sandbox
        run: |
          sf project deploy start \
            --dry-run \
            --manifest manifest/package.xml \
            --test-level RunLocalTests \
            --target-org ci \
            --wait 30 \
            --json > deploy-result.json

      - name: Publish deployment result
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pr-validation-deploy-result
          path: deploy-result.json
          if-no-files-found: warn
```

**Notes on this workflow:**

- `--dry-run` performs a `checkOnly` deployment: it compiles the payload against the target and runs
  the tests, and **changes nothing**.
- The CI sandbox should be **refreshed or reset on a schedule**; a stale sandbox is a false green.
- `cancel-in-progress: true` is safe for PR validation because it changes nothing in an org. **Do
  not** use it on a deploy job.
- `--json` gives a machine-readable result; parse it for the deployment id rather than scraping
  stdout.
- `timeout-minutes` is a real control: a deploy that hangs should fail, not occupy a runner.

### 4.2 Reusable deploy workflow

```yaml
# .github/workflows/_reusable-deploy.yml
name: Reusable Salesforce Deploy

on:
  workflow_call:
    inputs:
      target:
        type: string
        required: true
      manifest:
        type: string
        default: manifest/package.xml
      test-level:
        type: string
        default: RunLocalTests
      wait-minutes:
        type: number
        default: 30
    secrets:
      SF_CLIENT_ID:
        required: true
      SF_USERNAME:
        required: true
      SF_INSTANCE_URL:
        required: true
      SF_JWT_KEY_B64:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    environment: ${{ inputs.target }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @salesforce/cli@2.58.0
      - run: |
          echo "${{ secrets.SF_JWT_KEY_B64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
          chmod 600 "$RUNNER_TEMP/jwt.pem"
      - run: |
          sf org login jwt \
            --username "${{ secrets.SF_USERNAME }}" \
            --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
            --client-id "${{ secrets.SF_CLIENT_ID }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias org
      - run: |
          sf project deploy start \
            --manifest "${{ inputs.manifest }}" \
            --test-level "${{ inputs.test-level }}" \
            --target-org org \
            --wait "${{ inputs.wait-minutes }}" \
            --json > deploy-result.json
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: deploy-result-${{ inputs.target }}-${{ github.run_id }}
          path: deploy-result.json
```

**Critical detail:** `environment: ${{ inputs.target }}` means the **environment's** secrets and
**environment's** required reviewers apply. That is how the same workflow deploys to `qa`
automatically and to `prod` only after a named human approves — without two near-identical
workflow files.

### 4.3 Non-prod deployment (QA / UAT)

```yaml
name: Deploy Non-Prod

on:
  push:
    branches: ['release/**']
  workflow_dispatch:
    inputs:
      target:
        description: 'Target environment'
        type: choice
        options: [qa, uat]

permissions:
  contents: read

concurrency:
  group: deploy-${{ inputs.target || 'release' }}
  cancel-in-progress: false          # never cancel a running deploy

jobs:
  deploy:
    uses: ./.github/workflows/_reusable-deploy.yml
    with:
      target: ${{ inputs.target || 'qa' }}
      test-level: RunLocalTests
    secrets: inherit
```

> `secrets: inherit` passes the repository secrets to the called workflow. For tighter control,
> declare each secret explicitly in `workflow_call.secrets` and map them — the explicit form is
> better in a regulated environment because the contract is visible.

### 4.4 Production — validate then quick deploy

This is the pattern that keeps a change window short. Two jobs: **validate** (which runs the tests
and returns a job id valid for 10 days), then **quick deploy** (which applies the validated
deployment without re-running the tests).

```yaml
name: Production Release

on:
  workflow_dispatch:
    inputs:
      release-ticket:
        description: 'Change ticket id'
        required: true
      manifest:
        description: 'Manifest path'
        default: manifest/package.xml

permissions:
  contents: read

concurrency:
  group: deploy-prod
  cancel-in-progress: false

jobs:
  validate:
    name: Validate against production (checkOnly)
    runs-on: ubuntu-latest
    timeout-minutes: 90
    environment: prod-validate          # secrets only; no deploy permission yet
    outputs:
      job-id: ${{ steps.validate.outputs.job-id }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @salesforce/cli@2.58.0
      - run: |
          echo "${{ secrets.SF_JWT_KEY_B64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
          chmod 600 "$RUNNER_TEMP/jwt.pem"
      - run: |
          sf org login jwt \
            --username "${{ secrets.SF_USERNAME }}" \
            --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
            --client-id "${{ secrets.SF_CLIENT_ID }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod
      - id: validate
        name: Validate deployment (runs Apex tests, does not deploy)
        run: |
          sf project deploy validate \
            --manifest "${{ inputs.manifest }}" \
            --test-level RunLocalTests \
            --target-org prod \
            --wait 30 \
            --json > validate-result.json
          # job id is the field the CLI returns; confirm the exact key with --json
          jq -r '.jobId' validate-result.json >> "$GITHUB_OUTPUT"
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: prod-validation-result
          path: validate-result.json

  deploy:
    name: Quick deploy to production
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 45
    environment: prod                   # ← required reviewers live here
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @salesforce/cli@2.58.0
      - run: |
          echo "${{ secrets.SF_JWT_KEY_B64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
          chmod 600 "$RUNNER_TEMP/jwt.pem"
      - run: |
          sf org login jwt \
            --username "${{ secrets.SF_USERNAME }}" \
            --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
            --client-id "${{ secrets.SF_CLIENT_ID }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod
      - name: Quick deploy the validated deployment
        run: |
          sf project deploy quick \
            --job-id "${{ needs.validate.outputs.job-id }}" \
            --target-org prod \
            --wait 30 \
            --json > prod-deploy-result.json
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: prod-deploy-result
          path: prod-deploy-result.json
```

**Verified quick-deploy facts (from the CLI plugin messages):**

| Fact | Consequence |
|---|---|
| `sf project deploy quick` **skips running Apex tests** — they already ran during validation | The validation **must** have succeeded, and nothing may have changed in the target since |
| The validation job id is **valid for 10 days** from when the validation started | A stale validation cannot be quick-deployed |
| `--use-most-recent` only considers validations from the **past 3 days or less** | Use an explicit `--job-id` for anything older |
| "**This command doesn't support source-tracking.** The source you deploy overwrites the corresponding metadata in your org" | Quick deploy is not a merge. It is a replacement |
| "**Don't use this command on sandboxes** … By default, sandboxes don't run tests during a deploy. Use `sf project deploy start` instead" | Use `sf project deploy start --dry-run --test-level RunLocalTests` for sandbox validation |
| `sf project deploy validate` **requires** Apex tests; `NoTestRun` is not an option for it | The validation is meaningful by construction |

**Important:** `sf project deploy validate` **does not support source tracking** either, and for the
same reason — the source overwrites the corresponding metadata in the org. Source tracking is a
developer-loop feature (dev/sandbox), not a release feature.

**After a successful prod deploy, add the tag step:**

```yaml
      - name: Tag the release
        if: success()
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git tag -a "release-${{ inputs.release-ticket }}" -m "Deploy ${{ inputs.release-ticket }} to production"
          git push origin "release-${{ inputs.release-ticket }}"
```

Without the tag, you do not have a rollback target.

### 4.5 Composite action (optional but tidy)

```yaml
# .github/actions/sf-deploy/action.yml
name: 'Salesforce Deploy'
description: 'Authenticate with JWT and deploy a manifest to an org'
inputs:
  client-id:      { required: true }
  username:       { required: true }
  instance-url:   { required: true }
  jwt-key-b64:    { required: true }
  manifest:       { required: false, default: 'manifest/package.xml' }
  test-level:     { required: false, default: 'RunLocalTests' }
  target-alias:   { required: false, default: 'org' }
  dry-run:        { required: false, default: 'false' }
runs:
  using: composite
  steps:
    - shell: bash
      run: |
        echo "${{ inputs.jwt-key-b64 }}" | base64 -d > "$RUNNER_TEMP/jwt.pem"
        chmod 600 "$RUNNER_TEMP/jwt.pem"
        sf org login jwt \
          --username "${{ inputs.username }}" \
          --jwt-key-file "$RUNNER_TEMP/jwt.pem" \
          --client-id "${{ inputs.client-id }}" \
          --instance-url "${{ inputs.instance-url }}" \
          --alias "${{ inputs.target-alias }}"
    - shell: bash
      run: |
        set -euo pipefail
        ARGS=(--manifest "${{ inputs.manifest }}"
              --test-level "${{ inputs.test-level }}"
              --target-org "${{ inputs.target-alias }}"
              --wait 30 --json)
        if [ "${{ inputs.dry-run }}" = "true" ]; then ARGS+=(--dry-run); fi
        sf project deploy start "${ARGS[@]}" > deploy-result.json
```

---

## 5. GitHub repository configuration (the part that is not YAML)

| Setting | Where | Value |
|---|---|---|
| Environment `prod` | `Settings > Environments` | Required reviewers (1–2 named people, **not** the author), deployment branch rule, "prevent self-review" |
| Environment `prod-validate` | `Settings > Environments` | Secrets only; no reviewers needed |
| Environment `ci` / `qa` / `uat` | `Settings > Environments` | Environment-scoped secrets |
| Branch protection | `Settings > Branches > Branch protection rules` | Require PR; require the `PR Validation / validate` status check; require review; require conversation resolution; **do not allow bypassing** |
| Prevent force-push | Branch protection | On |
| Require signed commits | Branch protection | If bank policy demands |
| Secrets | `Settings > Secrets and variables > Actions` | Environment-scoped where possible |
| Dependabot / secret scanning | `Settings > Code security` | On; alerts on the org admin account are an incident |
| Actions permissions | `Settings > Actions > General` | Restrict to selected actions; pin third-party actions to a SHA, not a tag, for a regulated environment |

**Why "pin to SHA":** `@v4` is a mutable tag. In a bank, a compromised action tag is a supply-chain
entry into the prod deploy path. Pin the full commit SHA and update it via a reviewed PR.

---

## 6. Artefacts and the audit trail

Every deploy job should publish:

| Artefact | Contains | Retention |
|---|---|---|
| `deploy-result.json` | The CLI `--json` output: component list, deployment id, per-component errors, test results, coverage | GitHub artefact retention (set it; default is 90 days) — extend if policy requires |
| `validate-result.json` | The validation's job id and result | Same |
| The change ticket reference | In the workflow run name or a job output | GitHub run + the ticket system |
| The commit SHA | Automatic | Git |
| The release tag | Created by the deploy job | Git |

**Do not publish:** debug logs containing field values, test data dumps, org URLs that leak
environment topology, or the private key. Add a `.gitignore`-equivalent to the artefact upload
paths.

---

## 7. Mapping the same pipeline to Azure DevOps and GitLab

| Concept | GitHub Actions | Azure DevOps | GitLab |
|---|---|---|---|
| Workflow definition | `.github/workflows/*.yml` | `.azure-pipelines/*.yml` | `.gitlab-ci.yml` |
| PR validation | `on: pull_request` | `trigger: none` + `pr:` | `merge_request_event` |
| Environment + required reviewers | Environments → Required reviewers | **Approvals** on an Environment (classic) or **Deployment protection rules** (YAML pipelines) | **Protected environments** + approval rules on a branch |
| Secrets | Actions Secrets (environment-scoped) | Key Vault + variable groups | CI/CD variables (environment-scoped, protected) |
| Concurrency / serialisation | `concurrency: group` | `batch: true` on a stage, or an agent pool with max parallelism 1 | `resource_group` + `needs` |
| Reusable pipeline | `workflow_call` | Templates (`templates/*.yml`) | `include:` + `!reference` |
| Manual approval | Protected environment | Approval check | Protected environment approval |
| Pipeline as code trigger | `workflow_dispatch`, `release` | `resources: pipelines` or schedule | `when: manual` |

**The Salesforce-side configuration is identical in all three.** The platform mechanics — test
levels, coverage, payload ceilings, one-deploy-at-a-time — do not change with the CI product. That
is the single most useful thing to say in an interview when asked "GitHub Actions, Azure DevOps,
or GitLab":

> "I do not care which CI product we use. I care that a human cannot push to prod without a green
> validation, a named test run, and a ticket id — and that the pipeline publishes the deployment id
> so the change record is complete."

### 7.1 Which one for a bank

| Criterion | GitHub Actions | Azure DevOps | GitLab |
|---|---|---|---|
| Already in Azure AD / Entra ID governance | Weak — identities live outside | **Strong** — native Entra integration | Weak |
| Change-management integrations (ServiceNow, Jira, ADO boards) | Via API/webhooks | Native connectors | Via API/webhooks |
| Self-hosting of runners inside the bank network | Possible (self-hosted runners) | Possible (self-hosted pools) | Possible |
| Approval UX | Environments | Approvals / deployment protection | Protected environments |
| **Fit for a bank already on Azure** | Fine | **Best** | Fine |

---

## 8. Anti-patterns

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| `sf org login web` on a runner | Interactive, no session in CI | JWT bearer flow |
| Password in a repo secret | Password policy, lockout, MFA, and it is a human credential | Certificate + integration user |
| `--dry-run` in the PR, then deploy **different files** in prod | The validation proved nothing | Validate and deploy the identical manifest and commit |
| `--test-level NoTestRun` anywhere near prod | The production gate is "tests pass" | `RunLocalTests` for the validate step |
| `RunSpecifiedTests` with a test list nobody maintains | Coverage silently drops | `RunLocalTests` for the release gate; `RunRelevantTests` once it is out of Beta and approved |
| Deploying profiles wholesale | Unreviewed access changes | Permission sets; thin profile delta with a second reader |
| No tag after a prod deploy | No rollback target | Tag in the deploy job |
| `cancel-in-progress: true` on a deploy | Kills a half-finished deploy | `false` for any job that writes to an org |
| Multiple teams pushing prod at the same time | Only one deploy runs; the queue is not FIFO | Serialise with `concurrency` |
| Running the full local test suite in a sandbox that is never reset | Green on stale state | Refresh the CI sandbox on a schedule |
| Logging `sf` output with `--verbose` into an artefact | Debug output can contain field values | Redact; prefer `--json` and the deployment id |
| Trusting a stored `sfdx://` auth URL | Long-lived bearer token in a secret store | JWT certificate |

---

## 9. The complete checklist for "is this pipeline production-grade?"

**Correctness**
- [ ] PR validation is a dry run; the prod path is a validate + quick deploy
- [ ] The validated manifest and the deployed manifest are byte-identical
- [ ] The API version in `package.xml` and the CLI version are pinned
- [ ] The prod test level is `RunLocalTests` (or `RunRelevantTests` when approved)
- [ ] Coverage is checked per class/trigger, not just overall
- [ ] The payload is under the platform ceilings (`02 §3`)

**Security**
- [ ] JWT certificate auth; no password, no refresh token
- [ ] The private key lives in `$RUNNER_TEMP`, is `chmod 600`, and is never uploaded
- [ ] The integration user has a dedicated permission set
- [ ] The prod org restricts deployments to the runner's IP range
- [ ] Third-party actions are pinned to a commit SHA
- [ ] The `prod` environment has required reviewers and forbids self-approval

**Auditability**
- [ ] Commit message, branch, PR and tag all carry the ticket id
- [ ] The deployment id, validation id and test run id are published as artefacts
- [ ] Artefact retention is set longer than the audit retention requirement
- [ ] The release tag is created on success
- [ ] The rollback procedure is a documented forward deploy of the previous tag

**Reliability**
- [ ] `concurrency` serialises prod
- [ ] `timeout-minutes` is set on every job
- [ ] `cancel-in-progress` is `false` for any job that writes to an org
- [ ] The CI sandbox is refreshed on a schedule
- [ ] A failed deploy leaves the org in a known state (no partial metadata writes)

---

## 10. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| The exact JSON key for the deployment job id in `sf project deploy validate --json` | Not pinned here — the CLI's JSON shape is not documented as a stable contract | Run `sf project deploy validate --json` once in a sandbox and read the output; prefer `--job-id` passed explicitly if the CLI prints the id on stdout |
| Whether the current Salesforce CLI supports a GitHub Actions OIDC exchange for org auth | **No such flow is documented.** Treat as unavailable | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/> |
| `sfdx-actions/setup-sfdx` as the setup action | Repository last pushed **2022-12-15**; still uses the `sfdx` CLI and `sfdx-auth-url` | Installing the CLI with `npm install -g @salesforce/cli@<pinned>` directly is the current approach |
| The `@salesforce/cli` version pinned in the examples | Pin to a version you have tested; the examples use `2.58.0` as a placeholder | <https://www.npmjs.com/package/@salesforce/cli> |
| GitHub artefact retention maximum | Set per repository/organisation; the exact cap varies | `Settings > Artifacts` |
