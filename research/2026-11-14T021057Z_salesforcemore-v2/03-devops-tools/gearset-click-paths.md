# Gearset click-paths — practical research

**Merge target:** section 6.1 of the downstream page. Gearset is the tool most likely to be asked about by name, so this file is intentionally task-oriented.

**Caveat.** Gearset renames menu items and changes edition features. The task and the verification step are stable; the exact label is not. Add a "verify in your tenant" note to the page. The paths below are the common shape as of 2026-11-14.

## 1. Before you compare anything

| Task | Where to go | What you click / enter | What to verify |
|---|---|---|---|
| Connect an org | Connections (or Orgs) | Add org → authorize with the integration user → confirm API access | The user is dedicated, least-privilege, and not a personal admin login |
| Connect source control | Settings → Source control | Choose GitHub / GitLab / Bitbucket / Azure DevOps → authorize → select repo | The repo and branch are the ones the team treats as the source of truth |
| Set team permissions | Settings / Teams | Restrict who can deploy to production; require approvals if the edition supports it | Segregation of duties is structural, not a convention |
| Confirm edition features | Account / Subscription | Check whether CI, pipelines, backup, and data are included | Do not promise a feature the bank has not licensed |

## 2. Compare and deploy

### 2.1 Compare two orgs

1. Open **Compare and Deploy**.
2. Set **Source** = the org you trust (usually Dev or the source-control branch).
3. Set **Target** = the org you are about to change (QA, UAT, Pre-Prod, Prod).
4. Click **Compare now**.
5. Filter by metadata type (Apex, Flow, permission set, layout, etc.). Use "show changes only" or the equivalent to hide unchanged components.
6. Expand a component to read the XML diff. This is the review step; do not skip it.
7. Select the components to deploy.
8. Click **Deploy selection** / **Deploy now**.
9. Choose the test level and whether this is a validate-only run (if the edition exposes it).
10. Read the deployment summary. If it fails, open **Problem analysis** before changing anything.

### 2.2 Compare a branch to an org (the CI-shaped comparison)

1. **Compare and Deploy** → **Source** = source control → choose repo and branch.
2. **Target** = the org.
3. Compare now. This shows what the branch would change in that org.
4. Use this for a pre-merge sanity check, not as a substitute for the CI validation.

### 2.3 Compare an org to source control (drift detection)

1. **Source** = the org, **Target** = the branch/repo (or the reverse, depending on the UI's wording).
2. Compare. Components that exist in the org but not in Git are drift.
3. Do not "fix" drift by deploying the branch over the org without a review. Decide which side is correct and record the decision.

### 2.4 Validate only

If the edition exposes a **validate-only** or **validation** option in the deploy dialog, use it. It compiles the payload and runs tests without changing the target. If the edition does not expose it, create a CI job whose action is validate, or run `sf project deploy start --dry-run` in the pipeline.

## 3. Continuous integration

| Step | Where | What to do | Why |
|---|---|---|---|
| Create the job | **Continuous integration** → **Create CI job** | Choose the repo, branch, and target org | The job is the repeatable gate |
| Choose the comparison | CI job settings | Source control branch → target org (or org → org) | You want the branch's changes, not a full-org compare |
| Add tests | CI job settings | Choose the test level or named tests | The gate must fail on a broken test |
| Choose the trigger | CI job settings | On commit, on pull request, or manual | PR validation is the earliest useful gate |
| Add notifications | CI job settings | Slack / email / GitHub status check | A failed validation must be visible on the PR |
| Separate validate from deploy | Two jobs or two actions | Validate on PR; deploy only on the release branch with approval | A PR should never change UAT or Prod |

**Practical example.** A PR to `release/2026-11-27` triggers a validate job against the QA sandbox. The job posts a GitHub status check. The PR cannot merge until the check is green. Merge triggers a deploy job to QA. UAT and Prod are separate jobs with approval gates.

## 4. Deployment pipelines and approvals

1. Open **Deployment pipelines** → **Create pipeline**.
2. Add stages: QA → UAT → Pre-Prod → Prod.
3. Attach an org connection to each stage.
4. Add an approval gate between stages. The production approver must not be the author.
5. Promote the validated deployment through the stages. Do not re-compare a different branch at Prod.
6. Record the promotion id / deployment history in the ticket.

If the edition does not include pipelines, the same control lives in GitHub Environments or Azure DevOps approvals; Gearset is then the diff/deploy surface, not the approval system.

## 5. Backup and restore

| Task | Where | What to click | What to verify |
|---|---|---|---|
| Take a backup | **Backup** (add-on; confirm edition) | Select org → **Back up now**, or set a schedule | The backup covers the metadata you are about to change; record the backup id |
| Compare a backup | Backup detail | **Compare** backup vs current org, or backup vs backup | This shows drift since the backup |
| Restore metadata | Backup detail | **Restore** → select components → restore to target | A metadata restore is not a data restore |
| Restore data | Data / data backup (separate feature) | Choose the data set and target | Data restore is a separate, ticketed operation and may not be available in every edition |

**Before a risky release:** take a backup, tag Git, and put both ids in the ticket. The Git tag is the rollback target for metadata; the backup is the additional safety net. Neither one restores deleted business records by itself.

## 6. Data deployments

**Where:** **Data** → **Data deployments** (compare/deploy records) or **Data backup**.

**Use it for:** reference data, seed data, and small controlled data moves. **Do not use it for:** bulk customer data in a bank without approval, masking review, and a ticket. Data deployment is not a masking process.

## 7. Monitoring and drift

**Where:** **Monitoring** → **Change monitoring** / **Org monitoring**.

**Use it for:** an alert when metadata changes in an org outside the pipeline. This is the "someone edited production in Setup" detector.

**Response:** retrieve the change, review it, decide whether Git or the org is correct, then either commit the change or redeploy the Git version. Do not leave the org and Git diverged.

## 8. Deployment history and audit

**Where:** **Deployment history**, the CI job history, or the pipeline promotion history (label varies).

**What to capture for the ticket:**
- Who deployed, when, source, target.
- What components changed.
- Test results and coverage.
- The validation id and the production deploy id, if the tool exposes them.
- Any approval record.

Export or screenshot the history and attach it to the change ticket. This is evidence, not a nice-to-have.

## 9. Practical scenarios

### 9.1 "It works in UAT, not in Prod"

1. Compare Prod (source) to UAT (target) or the branch to Prod.
2. Look for the Flow version, permission set, record type assignment, or setting that differs.
3. Fix it in Git or in the target configuration, not by copying from UAT in the UI.
4. Re-validate against Prod.

### 9.2 "Someone changed Prod directly"

1. Monitoring alert or a compare of Prod vs the branch.
2. Review the diff.
3. If the change is wanted, commit it to Git through a PR; if not, redeploy the Git version.
4. Record the drift incident.

### 9.3 "The deploy failed and I do not know why"

1. Open **Problem analysis** / the deployment error.
2. Identify the missing component or the failing test.
3. Add the dependency to the payload or fix the test.
4. Re-run the comparison/validation. Do not retry the identical deploy.

## 10. What Gearset does not replace

- Git as the source of truth.
- The `sf` CLI in a CI runner.
- A named human approver.
- A rollback tag.
- A data-masking process.
- A written runbook.

## 11. Interview line

"Gearset is a diff, dependency, pipeline, and backup layer over the Metadata API. I use it to compare orgs or branches, review the XML diff, validate with tests, promote through approval gates, and keep a backup and audit trail. I still keep Git as the source of truth and use the CLI in CI."

## 12. What to merge

**Merge:** sections 1–8 as a task table plus a short "what it does not replace" paragraph.

**Compress:** the practical scenarios into one example if the page is long.

**Do not merge:** exact menu labels without the "verify in your tenant" caveat.
