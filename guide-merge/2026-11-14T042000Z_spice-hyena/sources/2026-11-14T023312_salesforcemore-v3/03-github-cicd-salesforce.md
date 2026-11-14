# A CI/CD pipeline on GitHub + Salesforce (and why)

## Stage model

```
Developer sandbox / scratch
        │  git push (feature/*)
        ▼
PR opened ──► PR VALIDATION (no org change)
   1. checkout (fetch-depth: 0)
   2. install sf + sfdx-git-delta + code analyzer
   3. compute delta vs base branch
   4. static analysis (PMD / Code Analyzer)
   5. `sf project deploy validate` + named tests
   6. report status check on the PR
        │  review approved + checks green → merge
        ▼
integration branch (qa) ──► DEPLOY TO QA (real deploy, RunLocalTests, smoke tests)
        │  release branch cut
        ▼
release/<date> ──► UAT deploy ──► business sign-off
        │
        ▼
PRE-PROD VALIDATE (against the org you are about to change, 24–48h before window)
   `sf project deploy validate --target-org prod`  → validated job id (≤10-day window)
        │  CAB approval + change window
        ▼
PROD QUICK DEPLOY (`sf project deploy quick --job-id …`) → tag `release-<date>` → audit pack
```

## Why each stage exists (best-practice rationale)

| Stage | Why it is a best practice |
|---|---|
| Git as single source of truth | Prevents org drift; every change is reviewable, revertable, attributable. "If it's not in Git, it doesn't exist." |
| PR validation (validate-only) | Catches compile errors, missing dependencies, and test failures **before** anything touches a shared org. Cheap, parallel, repeatable. |
| Delta deployment (`sfdx-git-delta`) | Avoids payload limits and slashes test runtime; deploys only what changed. |
| Static analysis | Catches SOQL-in-loops, CRUD/FLS gaps, and governor-limit landmines tests may not exercise. |
| Named tests on PR, `RunLocalTests` before release | Fast feedback on the PR; a broad honest gate before UAT/Pre-Prod. |
| Separate integration/QA branch | Keeps a stable, deployable integration line while feature work continues. |
| Release branch | Freezes scope; UAT deploys from it; hotfixes merge back into it. |
| Pre-prod validate before the window | A green Dev sandbox is not evidence. Validation must run **against the org you are about to change**, with real metadata and data shape. |
| Quick deploy inside the window | Reuses a passed validation to keep the maintenance window short and reduce change-window risk. |
| JWT auth + least-privilege integration user | No human admin credentials in CI; the integration user deploys but is not a shared login. |
| Branch protection + environment approvals | Segregation of duties: author ≠ approver ≠ deployer identity, enforced structurally. |
| Tag every production deploy | The tag is the rollback target and audit anchor. |
| Change ticket id in commit + PR | Traceability from code to change record — the first auditor question. |

## Branching model

```
main                         ← matches production
  hotfix/<ticket>            ← cut from main only
  release/2026-11-27         ← cut from main at freeze
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

Rules that matter more than the diagram:

- A hotfix is cut from `main`, because `main` is what production runs. It merges back to `main` **and**
  into any open release branch, or the next release resurrects the bug.
- Feature branches live days, not weeks. Salesforce XML (Flows, profiles) does not merge cleanly; long
  branches become "delete one side and hope."
- The release branch is what QA/UAT deploy. Developers do not deploy feature branches into UAT.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the change-ticket id. That is the audit trail, not style.

## Workflow A — PR validation (`[CLI: verified]` shape; pin action versions)

```yaml
name: Salesforce PR Validation
on:
  pull_request:
    branches: [main, 'release/*', uat, qa]
    paths: ['force-app/**', 'manifest/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - uses: actions/setup-node@v4
        with: { node-version: '20' }

      - name: Install Salesforce CLI + plugins
        run: |
          npm install -g @salesforce/cli
          echo y | sf plugins install sfdx-git-delta
          echo y | sf plugins install @salesforce/sfdx-scanner

      - name: Write JWT key
        run: |
          printf '%s' "${{ secrets.SF_JWT_PRIVATE_KEY }}" > server.key
          chmod 600 server.key

      - name: Authenticate (JWT)
        run: |
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_LOGIN_URL }}" \
            --alias ci-org --set-default

      - name: Compute delta
        run: sgt --to HEAD --from "origin/${{ github.base_ref }}" --output ./delta --generate-delta

      - name: Static analysis
        run: |
          if [ -d delta/force-app ]; then
            sf scanner run --target delta/force-app --engine pmd --severity-threshold 2
          else
            echo "No Apex/LWC changes"
          fi

      - name: Validate (no org change)
        run: |
          if [ -f delta/package/package.xml ]; then
            sf project deploy validate \
              --manifest delta/package/package.xml \
              --test-level RunLocalTests \
              --target-org ci-org --wait 60 --verbose
          else
            echo "No metadata changes"
          fi

      - name: Cleanup
        if: always()
        run: rm -f server.key
```

## Workflow B — Production quick deploy (`[CLI: verified]` shape)

```yaml
name: Salesforce Prod Quick Deploy
on:
  workflow_dispatch:
    inputs:
      job_id:        { required: true, type: string }
      change_ticket: { required: true, type: string }

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: Production          # approve here; named approvers ≠ commit author
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @salesforce/cli

      - name: Write JWT key
        run: |
          printf '%s' "${{ secrets.SF_PROD_JWT_PRIVATE_KEY }}" > prod.key
          chmod 600 prod.key

      - name: Authenticate (JWT)
        run: |
          sf org login jwt \
            --client-id "${{ secrets.SF_PROD_CONSUMER_KEY }}" \
            --jwt-key-file prod.key \
            --username "${{ secrets.SF_PROD_USERNAME }}" \
            --instance-url https://login.salesforce.com \
            --alias prod-org

      - name: Quick deploy
        run: |
          echo "Ticket: ${{ inputs.change_ticket }}"
          sf project deploy quick --job-id "${{ inputs.job_id }}" --target-org prod-org --wait 30

      - name: Tag release
        run: |
          git config user.name  "cb-devops-bot"
          git config user.email "cb-devops-bot@example.invalid"
          git tag -a "release-${{ inputs.change_ticket }}-$(date -u +%Y%m%d%H%M%S)" -m "${{ inputs.change_ticket }}"
          git push origin --tags

      - name: Cleanup
        if: always()
        run: rm -f prod.key
```

## Pipeline anti-patterns to call out in review

- `sf org login web` or a username/password on a runner.
- Deploying the whole repo on every change instead of a delta.
- Merging a PR with a red validation check ("we'll fix it in UAT").
- Quick-deploying a validation that has been invalidated by any later prod change.
- Manual Setup edits in UAT/Prod that never reach Git.
- One shared `Admin` integration user (violates SoD and audit).

## Authentication design (the part interviewers probe)

- **JWT bearer flow** with a connected app: consumer key + private key in the CI secret store, username of
  a dedicated integration user. The private key never lands in the repo; the job writes it, uses it, deletes it.
- **Integration user** has a narrow permission set that can deploy/retrieve but is not a human admin login.
- **Secret rotation** is a documented runbook: rotate the cert, update the connected app, update the CI secret,
  re-run a validation to prove the new credential works before the next release.
