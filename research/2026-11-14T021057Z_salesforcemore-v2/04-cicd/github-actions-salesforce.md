# GitHub Actions + Salesforce CI/CD pipeline

**Merge target:** sections 5 and 5.1 of the downstream page. The page already has a stage table; this file adds the runnable workflow and the reasoning.

## 1. The five jobs

| Job | Trigger | What it proves | Target |
|---|---|---|---|
| `validate-pr` | Pull request to a release branch | The proposed change compiles and tests pass in a disposable CI sandbox | CI sandbox |
| `validate-release` | Push to the release branch, or manual dispatch | The exact commit compiles and tests pass in the org you are about to change | QA / UAT / Pre-Prod / Prod |
| `deploy` | After `validate-release` | The validated payload can be applied | The same target |
| `smoke` (inside `deploy`) | After the quick deploy | The feature is alive, not just deployed | The same target |
| `tag` (inside `deploy`) | After a successful production deploy | There is a rollback target | Git |

The important separation: **validation does not change the org; deployment applies a validation that already passed.** If the payload changes after validation, re-validate.

## 2. Reference workflow

```yaml
name: salesforce-release

on:
  pull_request:
    branches: ["release/**"]
  push:
    branches: ["release/**"]
  workflow_dispatch:
    inputs:
      target:
        description: "Environment to validate and deploy"
        type: choice
        options: [qa, uat, preprod, prod]
        required: true

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: sf-${{ github.ref }}-${{ inputs.target || 'qa' }}
  cancel-in-progress: false

env:
  NODE_VERSION: "20"

jobs:
  validate-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias ci
          rm -f "$RUNNER_TEMP/server.key"
      - name: Build delta manifest
        run: |
          npx --yes sfdx-git-delta \
            --to HEAD \
            --from "origin/${{ github.base_ref }}" \
            --output delta \
            --generate-delta \
            --source force-app
      - name: Validate against the CI sandbox
        run: |
          sf project deploy start \
            --manifest delta/package/package.xml \
            --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
            --dry-run \
            --test-level RunLocalTests \
            --target-org ci \
            --wait 60 \
            --json | tee validation.json
      - name: Upload validation evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ github.run_id }}
          path: |
            validation.json
            delta/

  validate-release:
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    environment: ${{ inputs.target || 'qa' }}
    outputs:
      job_id: ${{ steps.validate.outputs.job_id }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT, environment-scoped secrets)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias target
          rm -f "$RUNNER_TEMP/server.key"
      - name: Build delta manifest
        run: |
          npx --yes sfdx-git-delta \
            --to HEAD \
            --from "origin/main" \
            --output delta \
            --generate-delta \
            --source force-app
      - name: Validate against the target
        id: validate
        run: |
          sf project deploy start \
            --manifest delta/package/package.xml \
            --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
            --dry-run \
            --test-level RunLocalTests \
            --target-org target \
            --wait 60 \
            --json | tee validation.json
          echo "job_id=$(jq -r '.result.id' validation.json)" >> "$GITHUB_OUTPUT"
      - name: Upload validation evidence
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ github.run_id }}
          path: |
            validation.json
            delta/

  deploy:
    needs: validate-release
    runs-on: ubuntu-latest
    environment: ${{ inputs.target || 'qa' }}
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT, environment-scoped secrets)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias target
          rm -f "$RUNNER_TEMP/server.key"
      - name: Quick deploy the validated job
        run: |
          sf project deploy quick \
            --job-id "${{ needs.validate-release.outputs.job_id }}" \
            --target-org target \
            --wait 60
      - name: Smoke test
        run: |
          sf apex run test \
            --test-level RunSpecifiedTests \
            --tests ReleaseSmokeTest \
            --target-org target \
            --wait 30
      - name: Tag the production release
        if: ${{ (inputs.target || 'qa') == 'prod' }}
        run: |
          git config user.name "salesforce-release-bot"
          git config user.email "salesforce-release-bot@users.noreply.github.com"
          git tag -a "release-$(date -u +%Y-%m-%d)-${{ github.run_number }}" \
            -m "Deployed ${{ github.sha }} to production"
          git push origin --tags
```

## 3. Why this shape

| Choice | Why it is there |
|---|---|
| Pull-request trigger | The earliest place to fail is the cheapest place to fix |
| CI sandbox as the PR target | PR validation never touches UAT or Prod |
| Delta manifest (`sfdx-git-delta`) | Keeps the payload under metadata ceilings and reduces blast radius |
| `--dry-run` with `RunLocalTests` | Proves compile and tests against the target without changing it; trade speed for honesty |
| Environment-scoped secrets | The prod runner cannot use QA credentials, and the PR runner cannot use prod credentials |
| Protected `prod` environment | Required reviewers pause the job; approval is structural, not a comment |
| Quick deploy | Applies the validated job inside the change window without paying the test runtime twice |
| Smoke test after deploy | Catches "deployed but broken" (inactive Flow, missing secret, wrong assignment) |
| Annotated tag | The rollback target and the audit anchor |
| Concurrency group | Two deploys to one org do not race; only one deployment runs at a time per org, and queued deployments are not guaranteed to run in submission order |
| Artifact upload | The validation result and delta are evidence for the ticket |
| Minimal `permissions` | A compromised workflow cannot write the repo by default |

## 4. What not to do

- Do not run `sf org login web` on a runner.
- Do not store a password, auth URL, or private key in the repo.
- Do not use a shared human admin login for CI.
- Do not deploy every commit to production.
- Do not use `NoTestRun` in production when the payload contains Apex.
- Do not use `--ignore-conflicts` in production.
- Do not let the author approve their own production deploy.
- Do not skip validation because "it is a small change."
- Do not rebuild the artifact from a different branch at production.
- Do not force-push a release branch that other people are deploying.

## 5. Trade-offs to mention in an interview

- `RunLocalTests` is slower than `RunSpecifiedTests` but catches more. Use it before the window; use named tests for the PR if the suite is too slow.
- `RunRelevantTests` (Beta, API 66.0+) is a fifth test level that runs only tests relevant to the payload. It is a good fit for Apex-heavy deployments where test time should scale with the payload, but do not use it to avoid a broad gate the bank's policy requires.
- A full-org delta from `origin/main` can be large on a long-lived release branch. Use the previous release tag as the base when the branch is long.
- The quick-deploy window is limited. If the validation expires or the payload changes, re-validate; do not force the quick deploy.
- GitHub Environments and required reviewers depend on the plan. If the bank uses Azure DevOps or GitLab, the same gates exist under different names.

## 6. What to merge

**Merge:** the five-job table, the YAML in a collapsible block, the "why" table, and the "what not to do" list.

**Compress:** the YAML if the page needs to stay short; keep the five-job table and the why table.

**Do not merge:** the workflow as a guaranteed drop-in for every repo. It is a reference; the team's org aliases, branch names, and test names will differ.
