# Gearset click-paths — practical research (current UI shape)

**Merge target:** section 6.1 of the downstream page. Gearset is the tool most likely to be asked about by name, so this file is intentionally task-oriented.

**Caveat.** Gearset renames menu items between editions and releases. The task and the verification step are stable; the exact label is not. The current documentation groups the product into **My connections**, **Metadata deployments**, **Continuous delivery**, **Backup & archiving**, **Sandbox seeding & compliance**, **Problem analyzers**, **Observability**, **Automated testing**, and **Settings / Team management**. Add a "verify in your tenant" note to the page.

Sources checked 2026-11-14:
- Gearset docs home: <https://docs.gearset.com/en/>
- Compare and deploy collection: <https://docs.gearset.com/en/collections/10414029-compare-and-deploy-metadata>
- Continuous delivery collection: <https://docs.gearset.com/en/collections/10441562-continuous-delivery>
- Backup and archiving collection: <https://docs.gearset.com/en/collections/10435155-data-backup-and-archiving>
- Sandbox seeding and compliance collection: <https://docs.gearset.com/en/collections/10408207-sandbox-seeding-compliance>
- Problem analyzers collection: <https://docs.gearset.com/en/collections/10441556-problem-analyzers>

## 1. Before you compare anything

| Task | Where to go | What you click / enter | What to verify |
|---|---|---|---|
| Connect an org | **My connections** | Add org → authorize with the integration user → confirm API access | The user is dedicated, least-privilege, and not a personal admin login |
| Connect source control | **Settings → Source control** | Choose GitHub / GitLab / Bitbucket / Azure DevOps → authorize → select repo | The repo and branch are the ones the team treats as the source of truth |
| Set team permissions | **Settings / Team management** | Restrict who can deploy to production; require approvals if the edition supports it | Segregation of duties is structural, not a convention |
| Confirm edition features | **Settings / Subscription** | Check whether CI, pipelines, backup, archiving, and sandbox seeding are included | Do not promise a feature the bank has not licensed |

## 2. Metadata deployments — compare and deploy

The current docs call this collection **Compare and deploy metadata**; the left navigation is commonly **Metadata deployments**. Older material says **Compare and Deploy**. Treat them as the same surface.

### 2.1 Compare two orgs

1. Open **Metadata deployments** (Compare and deploy).
2. Set **Source** = the org you trust (usually Dev or the source-control branch).
3. Set **Target** = the org you are about to change (QA, UAT, Pre-Prod, Prod).
4. Click **Compare now**.
5. Filter by metadata type (Apex, Flow, permission set, layout, etc.). Use "show changes only" or the equivalent to hide unchanged components.
6. Expand a component to read the XML diff. This is the review step; do not skip it.
7. Select the components to deploy.
8. Click **Deploy selection** / **Deploy now**.
9. Choose the test level and whether this is a validate-only run (see **Validated packages** / the validation option if the edition exposes it).
10. Read the deployment summary. If it fails, open **Problem analyzers** before changing anything.

### 2.2 Compare a branch to an org (the CI-shaped comparison)

1. **Metadata deployments** → **Source** = source control → choose repo and branch.
2. **Target** = the org.
3. Compare now. This shows what the branch would change in that org.
4. Use this for a pre-merge sanity check, not as a substitute for the CI validation.

### 2.3 Compare an org to source control (drift detection)

1. **Source** = the org, **Target** = the branch/repo (or the reverse, depending on the UI's wording).
2. Compare. Components that exist in the org but not in Git are drift.
3. Do not "fix" drift by deploying the branch over the org without a review. Decide which side is correct and record the decision.

### 2.4 Validate and deploy later

The Compare and deploy collection includes **Validated packages**, **Draft deployments**, and **Cloning deployment packages**. The practical pattern is:

1. Validate the package against the target (no changes).
2. Keep the validated package / draft deployment.
3. Deploy it inside the window, if the validation is still valid.
4. If the payload or the target changed, re-validate.

Do not treat a stored validation as a permanent guarantee.

### 2.5 Deployment history and pull requests

The collection includes **Metadata deployment history** and **Create pull requests from "Deployment summary" page**. Use them to:

- Attach the deployment evidence to the ticket.
- Open a pull request for a change that was made in the UI, so the org change lands in Git.
- Reconcile drift instead of letting the org and Git diverge.

## 3. Continuous delivery — CI jobs and pipelines

Gearset's **Continuous delivery** collection covers **Pipelines**, **CI jobs**, **org monitoring**, and the **Gearset APIs**.

| Step | Where | What to do | Why |
|---|---|---|---|
| Create a CI job | **Continuous delivery → CI jobs** | Choose the repo, branch, and target org | The job is the repeatable gate |
| Choose the comparison | CI job settings | Source control branch → target org (or org → org) | You want the branch's changes, not a full-org compare |
| Add tests | CI job settings | Choose the test level or named tests | The gate must fail on a broken test |
| Choose the trigger | CI job settings | On commit, on pull request, or manual | PR validation is the earliest useful gate |
| Add notifications | CI job settings | Slack / email / GitHub status check | A failed validation must be visible on the PR |
| Separate validate from deploy | Two jobs or two actions | Validate on PR; deploy only on the release branch with approval | A PR should never change UAT or Prod |

**Pipelines.** Use **Continuous delivery → Pipelines** to define stages (QA → UAT → Pre-Prod → Prod), attach an org to each stage, and add approval gates. Promote the validated deployment; do not re-compare a different branch at Prod. The docs also cover destructive changes through a pipeline and the expanded branching model; those are the details to read if the bank uses a release-branch model.

**Org monitoring.** Use **Continuous delivery → Org monitoring** to detect metadata changes made outside Gearset. This is the "someone edited production in Setup" detector.

## 4. Backup and archiving

| Task | Where | What to click | What to verify |
|---|---|---|---|
| Take a backup | **Backup & archiving** (separately licensed; confirm edition) | Select org → **Back up now**, or set a schedule | The backup covers the metadata and data you are about to change; record the backup id |
| Compare a backup | Backup detail | **Compare** backup vs current org, or backup vs backup | This shows drift since the backup |
| Restore metadata | Backup detail | **Restore** → select components → restore to target | The docs include "Restoring metadata from a data backup job" |
| Restore data | **Backup & archiving** | Choose the data set and target | Data restore is a separate operation and may not be available in every edition |
| Archive data | **Backup & archiving → Data Archiving** | Configure the archive job | Archiving is not a backup substitute; confirm retention and access |

**Important correction.** Gearset **does not perform or schedule the Salesforce sandbox refresh itself**. It can help with **Backup & archiving** and **Sandbox seeding & compliance** around the refresh. Do not say "Gearset refreshes the sandbox" in an interview.

**Before a risky release:** take a backup, tag Git, and put both ids in the ticket. The Git tag is the rollback target for metadata; the backup is the additional safety net. Neither one restores deleted business records by itself.

## 5. Sandbox seeding and data masking

**Where:** **Sandbox seeding & compliance**.

| Task | Where | What you do | What to verify |
|---|---|---|---|
| Mask a Full sandbox | **Sandbox seeding & compliance → Data masking** | Choose the org, fields, and masking rules; run the in-place mask | Confirm completion before broad login |
| Seed a sandbox | **Sandbox seeding & compliance → Templates** | Choose a template, source, target, and objects/fields | Seeding is not masking; mask after seeding if the data is production-derived |
| Disable automation during seeding | **Sandbox seeding & compliance → Disabling rules, triggers and flows** | Use the documented toggles/process | Re-enable and verify after the seed |
| Refresh and mask best practice | **Sandbox seeding & compliance → Best practice – refreshing and masking a full copy sandbox** | Follow the documented order | The Salesforce refresh is a separate Setup action |

**Interview line.** "Gearset can mask and seed; Salesforce performs the sandbox refresh. Refresh is not done until masking and integration cut-over are done."

## 6. Problem analyzers

**Where:** the **Problem analyzers** panel on a comparison/deployment, or the Problem analyzers docs collection.

It surfaces issues such as:

- Missing dependencies.
- Deleted dependencies.
- Feature not enabled in the target.
- Changed dependencies.
- Master-detail relationship problems.
- Flow definitions being used to set the active state.
- Apex API version mismatch.
- Connected apps with a duplicate consumer key.
- Deleted active Flows.

**How to use it:** read the analyzer's explanation, confirm the missing component or setting in the target, add it to the payload or enable it, then re-run the comparison. Do not blindly accept an auto-fix; a human reviews what was added.

## 7. Monitoring and observability

| Task | Where | What you do |
|---|---|---|
| Detect direct org changes | **Continuous delivery → Org monitoring** | Turn on change tracking; route alerts to the release owner |
| Monitor errors and limits | **Observability** | Configure 24/7 error/limit monitoring where licensed |
| Audit a deployment | **Metadata deployment history** | Export the history and attach it to the ticket |

## 8. Practical scenarios

### 8.1 "It works in UAT, not in Prod"

1. Compare Prod (source) to UAT (target) or the branch to Prod.
2. Look for the Flow version, permission set, record type assignment, or setting that differs.
3. Fix it in Git or in the target configuration, not by copying from UAT in the UI.
4. Re-validate against Prod.

### 8.2 "Someone changed Prod directly"

1. Org monitoring alert or a compare of Prod vs the branch.
2. Review the diff.
3. If the change is wanted, commit it to Git through a PR; if not, redeploy the Git version.
4. Record the drift incident.

### 8.3 "The deploy failed and I do not know why"

1. Open **Problem analyzers** / the deployment error.
2. Identify the missing component or the failing test.
3. Add the dependency to the payload or fix the test.
4. Re-run the comparison/validation. Do not retry the identical deploy.

## 9. What Gearset does not replace

- Git as the source of truth.
- The `sf` CLI in a CI runner.
- A named human approver.
- A rollback tag.
- A Salesforce sandbox refresh.
- A data-masking policy (it can execute the mask; the policy is yours).
- A written runbook.

## 10. Interview line

"Gearset is a metadata deployment, continuous-delivery, backup, and sandbox-seeding layer over the Metadata API. I use it to compare orgs or branches, review the XML diff and problem analyzers, validate with tests, promote through approval gates, back up and restore, and mask sandbox data. I still keep Git as the source of truth and use the CLI in CI."

## 11. What to merge

**Merge:** sections 1–7 as a task table plus a short "what it does not replace" paragraph.

**Compress:** the practical scenarios into one example if the page is long.

**Do not merge:** exact menu labels without the "verify in your tenant" caveat, or the claim that Gearset refreshes the sandbox.
