# Term-by-term deep dives

**Merge target:** section 14 of the downstream page. Convert each `##` term into a collapsible `<details markdown="1">` block, or keep the headings if the page prefers an open glossary.

Shape for every entry: **Definition → Why the role cares → Concrete example → Failure mode → Interview line.**

---

## Git and metadata lifecycle

**Definition.** Git stores the metadata XML, the manifest or package directories, and the history of who changed what and why. Production is a deploy target, not the source of truth.

**Why the role cares.** The posting says "manage Salesforce metadata lifecycle using source control." Every change needs a commit, a branch, a review, and a tag. If someone changes production in Setup, the org and Git now disagree.

**Concrete example.** `main` mirrors production; `release/2026-11-27` is cut at freeze; `feature/CB-1234-invoice` is short-lived; `hotfix/CB-1299-null` is cut from `main`. Commit message: `CB-1234 add Invoice__c.Status__c validation rule`.

**Failure mode.** A developer edits production in Setup, "forgets to copy it later," and the next deploy reverts it. Or a long-lived branch accumulates Flow edits that cannot merge.

**Interview line.** "If Setup and Git disagree, that is an incident, not a workflow."

---

## Metadata deployments

**Definition.** A Metadata API call that creates, updates, or deletes configuration in a target org. The target compiles the payload, enforces dependencies, and runs tests.

**Why the role cares.** This is the core operation you own. You need to know what is in the payload, what the target has, what the target requires, and how to validate before you change it.

**Concrete example.**

```bash
sf project retrieve start --manifest manifest/package.xml --target-org dev
sf project deploy start --manifest manifest/package.xml --dry-run --target-org qa
sf project deploy start --manifest manifest/package.xml --target-org qa
```

**Failure mode.** Green in Dev, fails in QA because the payload references a field that exists only in Dev.

**Interview line.** "A deploy is a compile against the target, not a file copy."

---

## Salesforce limits

**Definition.** Per-transaction governor limits (SOQL, DML, heap, CPU, callouts) and org-wide allocations (API requests, async Apex, storage, concurrency). See `02-limits-constraints/governor-limits.md` and `other-limits-and-system-settings.md`.

**Why the role cares.** A deploy can be green and the feature can fail at volume or exhaust the org's API allocation during the release.

**Concrete example.** One SOQL for a collection, one DML for the list; test at 200 records; check Setup → Company Information → API Usage before the window.

**Failure mode.** SOQL/DML in a loop; a pipeline that retrieves the whole org and polls every second; an integration user that shares the production API pool.

**Interview line.** "I check the limit family and the org allocation before I retry or change the test level."

---

## Metadata dependencies

**Definition.** Parent/child references the target must satisfy: object before field, field before layout, record type before assignment, Apex class before trigger, permission set after the components it grants.

**Why the role cares.** Missing dependencies are the most common deploy failure.

**Concrete example.** Deploy object, field, record type, layout, layout assignment, and permission set in one payload. See `02-limits-constraints/dependencies-and-constraints.md`.

**Failure mode.** `invalid cross reference id`, `entity not found`, "no such column"; retrying the same payload without adding the parent.

**Interview line.** "Read the error, add the missing parent to the payload, re-validate against the same target."

---

## Deployment constraints

**Definition.** The things metadata cannot do: carry secrets, export private keys, enable a feature, move data, edit a managed package, or activate a Lightning page.

**Why the role cares.** A deploy can succeed and the feature still fails because the target is missing a switch, a secret, or an assignment.

**Concrete example.** Named credential metadata deploys, but the secret must be re-entered per org; a FlexiPage must be activated; a record type needs visibility.

**Failure mode.** "It deployed but nothing changed." See the constraints table in `02-limits-constraints/dependencies-and-constraints.md`.

**Interview line.** "I verify activation, assignment, secrets, and feature enablement after the deploy."

---

## CI/CD pipelines

**Definition.** Continuous integration validates every proposed change; continuous delivery/deployment promotes the same tested artifact with approvals.

**Why the role cares.** The posting names GitHub Actions, Azure DevOps, and GitLab. The vendor changes; the stages do not.

**Concrete example.** PR validates against a CI sandbox; merge validates the exact commit against QA; a protected environment approves Pre-Prod/Prod; the validated job quick-deploys; the commit is tagged. See `04-cicd/github-actions-salesforce.md`.

**Failure mode.** A pipeline that deploys every commit to production, or a pipeline with no validation.

**Interview line.** "A pipeline is a control: no human pushes to production without a green validation, a named test run, and a ticket id."

---

## Branching strategies

**Definition.** Feature branches for day-to-day work, a release branch for the frozen candidate, hotfix branches for urgent production fixes.

**Why the role cares.** Salesforce XML, especially Flows and profiles, does not merge well.

**Concrete example.** `main` mirrors production; a release branch is cut at freeze; a hotfix is cut from `main` and merged back to `main` and the open release branch.

**Failure mode.** A hotfix cut from the release branch never reaches `main`; the next release resurrects the bug.

**Interview line.** "Hotfix from `main`, merge back to `main` and the open release branch."

---

## Automated testing and validation

**Definition.** Validation proves the payload compiles and tests pass without changing the org. A real deploy changes it. A quick deploy applies a validation that already passed.

**Why the role cares.** Production rejects Apex without tests and 75% coverage. The validation that counts is against the target.

**Concrete example.**

```bash
sf project deploy start --dry-run --test-level RunSpecifiedTests \
  --tests CommercialBankingReleaseTest --target-org qa
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 30 --target-org qa
```

**Failure mode.** A test depends on org data and passes in Dev, fails in an empty QA sandbox.

**Test levels.** The Metadata API has five: `NoTestRun`, `RunSpecifiedTests`, `RunRelevantTests` (Beta, API 66.0+), `RunLocalTests`, `RunAllTestsInOrg`. The older four-level answer is incomplete.

**Interview line.** "Validate against the org you are about to change. Quick deploy is not a second validation."

---

## Gearset, Copado, AutoRABIT, or equivalent

**Definition.** DevOps platforms that provide metadata diff, dependency analysis, CI, promotion pipelines, backup, data deployment, monitoring, and audit on top of the Metadata API.

**Why the role cares.** The posting asks for hands-on experience. You need to know what the vendor adds and what still depends on Git and the CLI.

**Concrete example.** Gearset compare & deploy, CI job, pipeline, backup, monitoring; Copado user stories, promotions, quality gates; AutoRABIT CI, data loader, backup. See `03-devops-tools/`.

**Failure mode.** Treating the vendor UI as magic; a missing dependency or a bad test behaves the same.

**Interview line.** "They are a diff, dependency, pipeline, and backup layer over the Metadata API. They do not replace Git discipline."

---

## Apex and triggers

**Definition.** Apex is Salesforce's strongly typed language. A trigger runs on record events before or after insert, update, delete, or undelete.

**Why the role cares.** You deploy it, test it, and diagnose why it fails in the target. A trigger that is not bulkified can pass tests and fail the first real batch.

**Concrete example.** One trigger per object, a handler class, a test that inserts 200 records, one SOQL, one DML, a recursion guard.

**Failure mode.** SOQL/DML in a loop; multiple triggers on one object; recursion; tests that depend on org data.

**Interview line.** "I do not sign off on Apex I cannot describe at 200 records and 10,000 records."

---

## Flows (before/after save)

**Definition.** Before-save Flows run before the record is committed and are for fast field updates on the same record. After-save Flows run after the save and are for related records, Apex, email, and side effects. Before-save cannot do DML or callouts.

**Why the role cares.** Flow XML does not merge, and a deployed version can be inactive.

**Concrete example.** Before-save sets a priority field; after-save creates a task or calls Apex. Split large Flows into subflows.

**Failure mode.** After-save doing work a before-save should do; a new version deployed but not active; two stories editing one Flow.

**Interview line.** "Before-save for same-record field updates; after-save for side effects. I check whether the deployed version is active."

---

## Permission sets vs profiles

**Definition.** A profile is the baseline permission set, one per user. Permission sets are additive and a user can have many. Permission set groups bundle them.

**Why the role cares.** Profiles are a grab bag of access; two stories editing one profile conflict.

**Concrete example.** Create `CB_Invoice_User` with the object/field access and assign it; leave `Admin` alone.

**Failure mode.** A monolithic `CB_Admin` permission set; a permission set deployed without field-level security.

**Interview line.** "Profiles are the baseline; ship story access as small permission sets."

---

## Record types

**Definition.** A record type lets different users see different business processes, picklist values, and page layouts for the same object.

**Why the role cares.** A record type deploy is not one file; it depends on the object, picklist values, business process, layout assignment, and visibility.

**Concrete example.** Deploy the object, record type, picklist values, layout, assignment, and permission set in one payload; test as a user with only that permission set.

**Failure mode.** Deploys but users cannot create it because the business process, picklist value, assignment, or visibility is missing.

**Interview line.** "A record type is four things. I deploy them together or not at all."

---

## Page layouts

**Definition.** A classic page layout controls fields, related lists, and buttons. A Lightning record page (FlexiPage) is a different component with its own activation.

**Why the role cares.** The layout file is not the assignment; the Lightning page must be activated.

**Concrete example.** Deploy the layout plus the profile/permission-set and record-type assignment; activate the FlexiPage for the app and record type.

**Failure mode.** Layout deployed but not assigned; Lightning page active in Dev but not UAT.

**Interview line.** "The layout file is not the assignment. I test the page as a real user."

---

## Security model

**Definition.** OWD, role hierarchy, sharing rules, profiles, permission sets, field-level security, record types, guest access, and Apex sharing.

**Why the role cares.** A deploy can widen access without anyone noticing.

**Concrete example.** OWD Private + sharing rule + permission set; a test as a low-privilege user asserting the denied record is not visible.

**Failure mode.** A permission set grants more than intended; Apex runs in system mode and exposes records; a guest-user setting is loosened.

**Interview line.** "Least privilege, proven with a test as a real user."

---

## Troubleshooting deployment failures

**Definition.** A failure is a payload problem (missing dependency), a test problem (failure/coverage/data), or an environment problem (feature/secret/permission/limit).

**Why the role cares.** The posting names it explicitly; retrying or debugging in production is the wrong response.

**Concrete example.** Save the error and deploy id, identify the missing parent, add it, re-validate against the same target. See the method in `02-limits-constraints/dependencies-and-constraints.md`.

**Failure mode.** Retrying without changes, lowering the test level, or "trying it in production."

**Interview line.** "I reproduce in the target with a dry-run, fix the missing parent or the test, and re-validate."

---

## Platform Developer experience

**Definition.** Hands-on Apex, SOQL, triggers, LWC/Aura, Visualforce, APIs, async Apex, testing, debugging, CLI, and Git.

**Why the role cares.** A release engineer who cannot read Apex cannot diagnose the dependency, the limit, or the test.

**Concrete example.** Review a trigger story for one trigger per object, a handler, bulk collections, one SOQL, one DML, a recursion guard, a 200-record test.

**Failure mode.** Green deploy; feature fails at volume; nobody on the release side can read the stack trace.

**Interview line.** "I can read the code well enough to know what will break in the target and at volume."

---

## Unlocked packages

**Definition.** Versioned, upgradeable second-generation packages owned by your team. No namespace required; can be org-dependent.

**Why the role cares.** Packaging stops a large org from becoming one unreviewable folder.

**Concrete example.**

```bash
sf package version create --package CB_Credit \
  --installation-key-bypass --code-coverage --wait 30
sf package version promote --package 04tXXXXXXXXXXXX
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

**Failure mode.** Packaging too early or drawing the boundary in the wrong place; "all of Sales Cloud" is not a package.

**Interview line.** "Unlocked packages are for real module boundaries, not for packaging the whole org on day one."

---

## Managed packages

**Definition.** A packaged app with a namespace and IP protection, usually from an ISV or AppExchange. You upgrade it; you do not edit its Apex.

**Why the role cares.** A bank runs managed packages; a release can be blocked by a package upgrade or a missing dependency.

**Concrete example.** Read the release notes, upgrade in a sandbox, run your regression tests, then upgrade UAT and production; record the package version in the runbook.

**Failure mode.** Trying to modify a managed component; upgrading without testing the customizations.

**Interview line.** "You upgrade managed packages; you do not fork them. The package version is part of the release artifact."

---

## Salesforce DX

**Definition.** Source-driven development: a project folder, the `sf` CLI, `sfdx-project.json`, package directories, scratch orgs, source tracking.

**Why the role cares.** DX is the workflow behind modern pipelines.

**Concrete example.**

```text
my-project/
  sfdx-project.json
  force-app/main/default/
  manifest/package.xml
  .forceignore
```

**Failure mode.** Mixing org-driven and source-driven workflows; assuming a scratch org reproduces managed packages, SSO, and licences.

**Interview line.** "DX is the workflow; sandboxes are still the enterprise path."

---

## Regulated and enterprise environments

**Definition.** Environments with change advisory boards, segregation of duties, audit trails, data-residency rules, access reviews, and emergency change procedures.

**Why the role cares.** The deploy is the technical part; the audit pack is the job.

**Concrete example.** Ticket, reviewed diff, approver who is not the author, validation id, test run, production deploy id, tag, mask evidence.

**Failure mode.** A "small change" bypasses the pipeline; production data in a ticket; the author approves their own deploy.

**Interview line.** "Segregation of duties is structural: the integration user deploys, a human approves, and the evidence is retained."

---

## Sandbox strategy

**Definition.** Sandboxes are copies of production metadata and, depending on type, data. Developer/Developer Pro, Partial Copy, Full.

**Why the role cares.** The wrong type makes a test meaningless; an unmasked Full sandbox is a data incident.

**Concrete example.** Developer/Dev Pro for build; Partial Copy for UAT; Full for Pre-Prod. Refresh is complete only after masking, integration cut-over, and access control.

**Failure mode.** UAT on an empty Developer sandbox; a Full sandbox with broad logins; a refresh that breaks SSO/named credentials.

**Interview line.** "Refresh is not done until masking and integration cut-over are done."

---

## Audit, security, compliance

**Definition.** The evidence trail: ticket, approval, diff, test results, deploy ids, tag, access, and data-handling proof.

**Why the role cares.** The posting says "support audit and change management requirements."

**Concrete example.** An audit pack per release: ticket, PR with a second reviewer, validation id, test run and coverage, production deploy id, tag, approver, mask evidence.

**Failure mode.** Missing approver; author approves own deploy; deploy ids not recorded; PII in a debug log.

**Interview line.** "I can hand an auditor the ticket, the diff, the approver, the validation id, the production deploy id, the test run, the tag, and the mask evidence."

---

## DevOps-friendly design patterns

**Definition.** Design choices that make metadata small, modular, testable, and environment-independent.

**Why the role cares.** You are the person who rejects a story that will conflict with the next three.

**Concrete example.** Permission sets per persona; one Flow owner per release; tests create their own data; no hard-coded ids; named credentials; custom metadata toggles; bulkified Apex; no environment branches.

**Failure mode.** A story that edits `Admin.profile`, hard-codes a record type id, or creates a second trigger on the same object.

**Interview line.** "Design so the deploy is boring."

---

## Three release speeds

**Definition.** Scheduled releases follow the calendar and freeze; hotfixes address a production defect that cannot wait; emergency changes address active harm.

**Why the role cares.** The posting lists all three. The difference is the approval chain and scope, not whether the pipeline runs.

**Concrete example.** Scheduled: release branch, validation, UAT sign-off, window, deploy, tag. Hotfix: from `main`, same validation, smaller payload, merge back both ways. Emergency: a pre-written short path with one named approver and a validation deploy.

**Failure mode.** A hotfix from the release branch; an emergency change that skips validation; no rollback tag.

**Interview line.** "Emergency is a shorter approval chain, not a skipped pipeline."

---

## Runbook and rollback

**Definition.** A runbook is the written promotion sequence. Rollback is a forward deploy of the last known-good tag, or installing the previous package version.

**Why the role cares.** If you do not have a tag from the last good production deploy, you do not have a rollback.

**Concrete example.** Fill the template in section 10 for every promotion. For a bad Flow, activate the previous version first, then redeploy the last good tag. For a destructive delete, metadata restore is separate from data restore.

**Failure mode.** No tag; no reverse script; assuming `git revert` restores data; a "rollback" that only reverts the repo.

**Interview line.** "Rollback is a forward deploy of the last good tag. Git revert does not restore deleted records."

---

## Multi-environment strategy

**Definition.** A promotion path where the same artifact moves from Dev to QA to UAT to Pre-Prod to Prod, with one gate and one owner per stage.

**Why the role cares.** The posting names all five. The failure is usually environment drift or a skipped gate, not the code.

**Concrete example.** Dev: build; QA: automated validation; UAT: business sign-off; Pre-Prod: dress rehearsal; Prod: named approver and window. Promote the artifact, configure the target.

**Failure mode.** UAT is not prod-like; Pre-Prod is skipped; the artifact is rebuilt from a different branch at production.

**Interview line.** "One artifact, five targets, one gate per stage."

---

## Certifications (PD1, Advanced Admin, DevOps related)

**Definition.** PD1 is the Platform Developer I credential. Advanced Admin is now Platform Administrator II. There is no official Salesforce DevOps Engineer certification; vendor certificates exist.

**Why the role cares.** The posting names them; you should map the credential to the work, not collect badges.

**Concrete example.** Study order: crash course and PD1 material, then the labs, then Platform Administrator II topics that overlap releases. Add a vendor certificate after hands-on tool use.

**Failure mode.** Claiming a certification you do not have, or implying an official Salesforce DevOps certification exists.

**Interview line.** "PD1 plus Platform Administrator II plus hands-on pipeline evidence. The vendor certificates show tool time; they do not replace PD1."

---

## What to merge

**Merge:** all entries, but convert them to the page's existing collapsible style. Keep the five-part shape.

**Compress:** entries already covered in depth by section 13 (limits, dependencies, constraints) to a short recap with a link.

**Do not merge:** the longer entries verbatim if the page becomes a wall of text. The value is the definition + failure mode + interview line; the example can be shortened.
