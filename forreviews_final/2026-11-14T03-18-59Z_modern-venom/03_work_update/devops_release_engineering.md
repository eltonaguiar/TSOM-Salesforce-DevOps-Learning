# DevOps & Release Engineering — Research Notes

**Source:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/
**Source file:** `docs/salesforce/devops-engineer.md` (learning repo `main`, 554 lines)
**Supersedes:** the "⏳ Pending" row in `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/research_index.md`
**Date:** 2026-11-14

## What this track is for

A commercial-banking DevOps Engineer (Salesforce) role — Scotiabank requisition 276046. The posting is not
"write features"; it is "make Salesforce releases fast, safe, and auditable".

| You own | You partner on | You do not own alone |
|---------|----------------|----------------------|
| Git history of metadata | Apex, triggers, LWC | Business requirements |
| Pipeline: validate, test, deploy | Flow design | Production data fixes without a ticket |
| Dev / QA / UAT / Pre-Prod / Prod path | QA test evidence | Security exceptions |
| Sandbox create, refresh, mask | Admin config in a story | Approving your own prod change |
| Conflict resolution on deploy | Dependency design | Deciding the release scope |
| Runbooks, rollback, audit pack | Platform limits | Bypassing change control for a "small" deploy |

ELI5: developers build the furniture; you own the loading dock, the truck, the checklist, and the proof the
right furniture arrived in the right building.

## The 12 training items (work in order)

| # | Item | Done when |
|---|------|-----------|
| 1 | Source of truth | Retrieve one metadata type, commit it, dry-run deploy it to a second org |
| 2 | Metadata that breaks releases | Name the missing dependency without opening the org |
| 3 | Environments and sandboxes | Draw the path; say which sandbox type each stage uses and why a Full copy is masked |
| 4 | Branching | Say where a hotfix is cut from and which branches it merges back into |
| 5 | CI/CD | Describe the same four stages in GitHub Actions, Azure DevOps, or GitLab |
| 6 | DevOps tools | Say what the CLI does that a vendor UI does not replace |
| 7 | Conflict clinic | Have a fix for each of the six conflict classes, not just the symptom |
| 8 | Packages | Say when unpackaged source is still the right deploy |
| 9 | Tests and validation | Explain dry-run vs quick deploy vs a real prod deploy |
| 10 | Releases, hotfixes, rollback | Fill the runbook template from memory |
| 11 | Banking change control | List the artifacts an auditor asks for after a prod deploy |
| 12 | Design patterns you coach | Reject a story that edits `Admin.profile` for one field |

## 1. Source of truth

Production is not the source of truth. **Git is.** The org is a target you deploy to.

A Salesforce DX project is a folder of metadata XML plus `sfdx-project.json`. The modern CLI is `sf` (the old
`sfdx` binary still appears in older runbooks; same product family).

```bash
sf --version
sf org login web --alias dev --instance-url https://login.salesforce.com
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev
sf project deploy start --dry-run --target-org qa
```

Confirm flags with `sf project deploy start --help` before memorizing them — CLI flags move; the idea does not.

**Commit:** custom objects, fields, validation rules, Flows, Apex, LWC, permission sets, custom metadata, named
credentials **metadata** (not the secret); a manifest (`package.xml`) or a package directory.

**Do not commit:** profiles as the place business access lives; `.sfdx/`, org auth files, consumer secrets,
JWT private keys; retrieved junk (`*.profile` user lists, certificate bodies, sandbox-only endpoints).

**Destructive deletes** are a separate file, not a side effect of "it was not in the folder":

```bash
sf project deploy start \
  --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChanges.xml \
  --target-org qa
```

Use pre-destructive changes only when the delete must happen before the add (for example, a rename that would
collide). A delete in production is not undone by Git.

## 2. Metadata that breaks releases

Deploys are not file copies — the Metadata API compiles the payload against the target org.

| Failure you will see | Usual cause | Check first |
|----------------------|-------------|-------------|
| `no such column` / field does not exist | Flow, layout, formula, or Apex references a field not in the payload and not in the target | Add the field, or deploy to the org that already has it |
| `invalid cross reference id` | Record type, layout, or business process points at something missing | Deploy the parent in the same payload |
| `entity not found` / Apex dependency | Class A uses class B, B is not deployed | Deploy the dependency, or stop referencing it |
| Test failure only in prod/UAT | Test uses a profile, record type, or custom setting that exists in Dev and not the target | Make the test create its own data |
| Flow version deployed but users see the old one | New version is not active | Activate the version, or deploy the flow as Active |
| Coverage below 75% | Production gate | See tests |
| `CANNOT_MODIFY_MANAGED_OBJECT` | Tried to change a managed-package component | Configure around it, or upgrade the package — do not fork it in Git |

Governor limits still matter even if you are not writing the trigger. Your review question: **"what happens
when this runs on 200 records?"**

## 3. Environments and sandboxes

| Stage | What it is for | Usual sandbox | Who promotes into it |
|-------|----------------|---------------|----------------------|
| Dev | Build and unit test | Developer / Developer Pro; scratch orgs only if licenses and connected apps can be recreated | Developer, via Git |
| QA | Automated validation, integration | Developer Pro or Partial Copy | Pipeline, on merge |
| UAT | Business testers | Partial Copy, or a masked Full | Release engineer, from the release branch |
| Pre-Prod | Dress rehearsal against prod-like metadata and volume | Full or a recent Partial, refreshed close to the window | Release engineer |
| Prod | Customers | Production | Release engineer, after approval, inside the window |

**Scratch orgs are not sandboxes.** A scratch org is an empty org created from a Dev Hub and a definition
file. A bad answer in a bank interview is "UAT is a scratch org." Recommend scratch orgs for package builds;
recommend sandboxes for the path above.

| Sandbox type | Metadata | Data | Use it for |
|--------------|----------|------|------------|
| Developer | Yes | No | Isolated build |
| Developer Pro | Yes | No (more file/storage room) | QA when you do not need rows |
| Partial Copy | Yes | A template sample | UAT when testers need some rows, not all of prod |
| Full | Yes | All of prod | Pre-prod, performance, any test that depends on real shape |

Full copies contain customer data. In a bank that means SIN-adjacent identifiers, account numbers, emails,
phone numbers. **Refresh is not done when the copy finishes — it is done when masking has run and access is
limited to the people on the ticket.** Salesforce Data Mask is the product name to know; many banks also
mask with a vendor tool or a reviewed script.

| Task | Where |
|------|--------|
| List and refresh sandboxes | Setup > Sandboxes |
| Sandbox template (Partial Copy) | Setup > Sandboxes > Sandbox Templates |
| Allow inbound deploys | Setup > Deploy > Deployment Settings |
| See what is running | Setup > Deploy > Deployment Status |
| DevOps Center, if the org uses it | Setup, search "DevOps Center" (must be enabled) |
| Data Mask | App Launcher > Data Mask, after the managed package is installed |

Refresh cadence is license-limited; Full is the slowest. Do not promise a same-day Full refresh — check
Setup > Sandboxes for the next eligible refresh before committing a date.

## 4. Branching

```text
main                         ← matches production
  hotfix/<ticket>            ← cut from main only
  release/2026-11-27         ← cut from main when the release freezes
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

Rules that matter more than the diagram:

- A hotfix is cut from `main`, because `main` is what production is running. It merges back to `main` **and**
  into any open release branch, or the next release resurrects the bug.
- A feature branch lives days, not weeks. Salesforce XML (Flows, profiles) does not merge; long branches
  become "delete one side of the conflict and hope."
- The release branch is what QA and UAT deploy. Developers do not deploy their feature branch into UAT.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the change-ticket id. That is the audit trail, not a style preference.

## 5. CI/CD

Same pipeline in GitHub Actions, Azure DevOps, or GitLab — only the YAML header changes.

| Stage | Trigger | What it runs | Target |
|-------|---------|--------------|--------|
| Validate | Pull request | `sf project deploy start --dry-run` plus the story's Apex tests | A CI sandbox refreshed or reset on a schedule |
| Integrate | Merge to the release branch | Real deploy | QA |
| Stage | Release manager | Validation-only deploy | Pre-Prod, then Prod |
| Release | Change window, after approval | Quick deploy of the validated prod job, or a fresh deploy if the validation expired | Prod |
| Tag | Pipeline success | Annotated tag + deploy id written to the ticket | Git |

Authentication in CI is JWT or a stored auth URL in the CI secret store. It is never `sf org login web` on a
runner, and never a password in the repo. The connected app, the integration user, and the permission set on
that user are part of the design. **The integration user can deploy; it cannot be a shared human admin login.**

```bash
sf project deploy start --dry-run --test-level RunSpecifiedTests \
  --tests CommercialBankingReleaseTest --target-org ci

sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 30 --target-org qa
```

`--test-level` values to say out loud: `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`.
Production will not accept `NoTestRun` when the payload contains Apex.

Useful interview sentence: "I do not care which CI product we use. I care that a human cannot push to prod
without a green validation, a named test run, and a ticket id."

## 6. DevOps tools

| Tool | What it is | What you are expected to know |
|------|------------|-------------------------------|
| Salesforce CLI (`sf`) | The deploy/retrieve/test/package engine | Run a dry-run and read the failure. Every other tool is a UI over this or the Metadata API |
| DevOps Center | Salesforce product: work items, Git, promotion | Native option when the bank does not want another vendor; still not a reason to skip Git discipline |
| Gearset | Compare and deploy, CI, backups on some editions | Compare orgs, spot forgotten metadata, gate on tests |
| Copado | User stories, pipelines, compliance packs | Pipeline and promotion path, not just "we have Copado" |
| AutoRABIT | CI/CD and data tooling in the same category | Promotion path, back-promotion, where secrets live |
| Change Sets | Setup UI between related orgs | Why they fail at this job's scale: no reviewable diff, no hotfix branch, profile XML you cannot merge, no rollback tag |

Change Sets are the thing you can explain and then retire. This role's answer is CLI or a vendor UI that uses
the Metadata API, with Git in front of both.

## 7. Conflict clinic

The six the posting names. Learn the cause, not the click-path.

- **Profiles** — `Admin.profile-meta.xml` is a dump of user/object/field permissions, layout assignments, and
  record-type visibility. Two stories editing it will conflict, and a bad merge can grant or remove access
  you did not review. Coach: ship a permission set (or permission set group) per persona/feature; leave the
  profile alone. If a legacy org still deploys profiles, deploy a thin delta with a tool that supports profile
  decomposition, and require a second person to read the permission diff.
- **Permission sets** — smaller, but still a conflict if every story edits one giant `CB_Admin` set. Split by
  feature or persona; use permission set groups to bundle for a job function.
- **Record types** — a deploy fails, or "succeeds" and users still cannot use it, when the business process
  and picklist values, the page layout assignment, or the profile/permission-set visibility is missing.
  Deploy the record type, the layout, and the permission set that grants visibility in one payload.
- **Page layouts** — the layout file is not the assignment; assignment lives on the profile and the record
  type. Do not confuse a classic page layout with a Lightning record page (FlexiPage).
- **Flows** — Flow XML does not merge; two developers editing the same flow will lose one side. One owner per
  flow per release, or split into subflows. Know whether your deploy leaves the new version Draft or Active.
  Fast mitigation: activate the previous version in Setup > Flows — a mitigation, not a rollback of Git
  history; follow with a redeploy of the last good tag.
- **Apex and dependencies** — deploy the class and its test in the same payload. A test that queries
  `SELECT Id FROM Account LIMIT 1` and assumes a row exists will pass in Dev and fail in an empty QA sandbox.
  Tests create their own data.

## 8. Packages

| Kind | Who it is for | DevOps note |
|------|----------------|-------------|
| Unlocked package | Your own team, modular internal apps | Versioned, upgradeable, has a dependency list. Best fit when a boundary is real (a credit-application module, not "all of Sales Cloud") |
| Org-dependent unlocked package | A module that still depends on unpackaged metadata in that org | Faster to adopt, harder to install elsewhere — say that limitation out loud |
| Managed package (1GP or 2GP) | An ISV, or a hard IP boundary | You upgrade it; you do not edit its Apex in Git |

Unpackaged metadata deployed from Git is still the right default for a large existing commercial-banking org.
Packaging is how you stop that folder becoming one unreviewable tree. **Do not propose "package the entire
org" as the first move.**

You need a Dev Hub to create second-generation packages and scratch orgs (Setup > Dev Hub). Unlocked packages
do not require a namespace; managed packages usually have one.

```bash
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

The `04t` id is the package version you install. Promote that version before production. Do not install a beta
package version into prod.

## 9. Tests and validation

Three different actions — interviews collapse them; do not.

| Action | Changes the org? | Why you run it |
|--------|------------------|----------------|
| Validation / dry-run (`--dry-run`, or a validate-only job in Gearset/Copado) | No | Prove the payload compiles and tests pass against that org |
| Quick deploy | Yes | Promote a validation that already succeeded, inside Salesforce's quick-deploy window, so you do not pay the test runtime again during the change window |
| Real deploy | Yes | First deploy, or the validation expired, or the payload changed |

Quick deploy only works if nothing relevant changed since the validation. If someone hotfixed prod after your
validation, the quick deploy is no longer an honest rehearsal — re-validate.

Production rules you can say without notes:

- A payload with Apex must run tests.
- Salesforce requires **75% coverage** as the production gate.
- `RunSpecifiedTests` means you name the tests, and the Apex you are deploying has to be covered by those
  tests.
- `RunLocalTests` runs local tests and skips managed-package tests. It is the honest gate before a release,
  and it is slow — which is why you validate before the window, then quick-deploy inside it.
- A green Dev sandbox is not evidence. The validation that counts is against the org you are about to change.

## 10. Releases, hotfixes, rollback

| Speed | When | Branch | Deploy bar |
|-------|------|--------|------------|
| Scheduled | The release calendar | `release/<date>` | Full validation, UAT sign-off, change ticket, window |
| Hotfix | Prod defect, next release is too late | `hotfix/<ticket>` from `main` | Same validation, smaller payload, still a ticket |
| Emergency | Active customer or regulatory harm | `hotfix/<ticket>` from `main` | Short path that is already written — not "whoever is online clicks Setup" |

Emergency is a shorter approval chain, not a skipped pipeline.

### Runbook template

```text
Change ticket:
Release tag:
Payload (package directory or manifest):
Source branch / commit:
Validation org / deploy id / time:
Tests run and coverage:
Prod deploy id / time:
Approver (not the author):
Sandbox or feature flags to flip after deploy:
Rollback tag:
Rollback owner:
How we will know it worked (one query, one screen, one test):
```

### Rollback

Metadata does not roll back by itself. Rollback is a **forward deploy of the last known-good tag**, or a
package install of the previous version.

| Situation | First move | Then |
|-----------|------------|------|
| Bad Flow, previous version still in the org | Activate the previous Flow version | Redeploy the last good tag so Git matches the org |
| Bad Apex or config | Stop the bleeding (deactivate the automation if safe) | Validate the previous tag, deploy it |
| Destructive delete already ran | You cannot undelete records | Restore metadata from Git; data restore is a separate, ticketed path |
| Post-deploy data script already ran | Git revert will not undo the rows | The script needs its own reverse script, reviewed before the window |

If you do not have a tag from the last good prod deploy, you do not have a rollback. Fix that before the next
release.

## 11. Banking change control

Keep these, every time:

- Change ticket id in the commit and the pull request
- Diff a second person read (not the author)
- Validation deploy id and prod deploy id
- Test run id and coverage number
- Named approver, different from the person who wrote the change
- Release tag
- For a Full sandbox refresh: refresh time, mask-complete confirmation, who is allowed to log in

**Segregation of duties:** the developer who wrote the Apex does not approve their own production deploy. The
pipeline should make that structural, not cultural. The integration user deploys; a human approves. Those are
different identities.

Do not put production customer data in a slide, a debug log pasted into a ticket, or a sandbox that has not
been masked. Debug logs can contain field values — turn them off when the diagnosis is done.

This is the same discipline as the ServiceNow change path: a ticket, a window, a backout, evidence. The
metadata tool changes; the control does not.

## 12. Design patterns you have to coach

| Pattern | Why release engineering cares |
|---------|-------------------------------|
| Permission sets over profile edits | Profiles do not merge; permission sets do, if you keep them small |
| One flow owner per release, subflows for parallel work | Flow XML does not merge |
| Tests create their own data | Empty sandboxes and prod-like sandboxes behave the same |
| No hardcoded ids | The id in Dev is not the id in UAT — use custom metadata or a query |
| Named Credentials for callouts | Endpoints differ per sandbox; secrets never go in Git |
| Custom metadata / custom settings for toggles | Ship a feature dark and turn it on after deploy, without another deploy |
| Bulkified Apex | A deploy can be green and still fail the first real batch — ask the 200-record question |
| No environment-specific branches | `if (org.IsSandbox)` is a last resort; config belongs in the target, not a `uat` branch that can never merge |

## Labs

- **Lab A — Retrieve, review, dry-run.** Two Developer Edition orgs (`dev`, `qa`). Create a permission set
  `CB_Release_Reader` in `dev`; retrieve only that; dry-run deploy to `qa`; then change the permission set in
  `qa` Setup directly and retrieve to see the "someone edited prod in the UI" diff.
- **Lab B — Profile conflict, on purpose.** Two branches each add a different field permission to the same
  profile XML; merge; watch it conflict. Then recreate both as permission sets and merge those. Write three
  sentences: why the profile conflicted, what a bad merge would have granted, what you tell a developer who
  asks to edit `Admin` profile for one field.
- **Lab C — Failing validation.** Write an Apex class that references a second class you do not deploy;
  dry-run; save the error. Add the missing class; dry-run again. Add a test that queries `Account` without
  inserting one; run it in an empty org; fix the test to insert the row.
- **Lab D — Runbook.** Fill the runbook template for Lab A as if `qa` were production. Include a rollback tag
  even though the exercise is fake.
- **Lab E — Sandbox and mask checklist.** Write the checklist you would attach to a refresh ticket: sandbox
  name/type/why; next eligible refresh (looked up, not guessed); template name if Partial; fields to mask
  (email, phone, government id, account number, birth date); who confirms mask complete; who may log in before
  that confirmation (nobody outside the ticket); which integration endpoints must point at non-prod first.

## Interview drills (short answers)

1. **Where is the source of truth?** Git. Production is a deploy target. If Setup and Git disagree, that is an
   incident, not a workflow.
2. **Walk a change to prod.** Feature branch → pull request → dry-run with tests → merge to the release
   branch → QA deploy → UAT → prod validation before the window → approval → quick deploy or fresh deploy →
   tag → ticket updated with both deploy ids.
3. **Hotfix during an open release?** Cut from `main`, not the release branch. Merge back to `main` and to the
   open release branch.
4. **Why did this profile deploy fail or scare you?** Profiles are a grab bag of access; two stories conflict;
   a bad merge changes access you did not mean to ship. Prefer permission sets.
5. **Flow deploy succeeded but users see the old screen.** The new version is probably not the active version.
   Check that before you redeploy.
6. **Validate vs quick deploy?** Validate does not change the org. Quick deploy applies a validation that
   already passed, inside the platform window, so the change window stays short.
7. **Unlocked vs managed?** Unlocked is yours, versioned, for internal modules. Managed is something you
   upgrade and do not edit. Packaging the entire existing bank org on day one is not a plan.
8. **What do you hand an auditor?** Ticket, diff, approver who is not the author, validation id, prod deploy
   id, test run, tag, and for any Full sandbox, mask-complete evidence.

## Certifications

The posting names Platform Developer I, Advanced Admin, and "DevOps related certs."

| Credential | How it maps | Link |
|------------|-------------|------|
| Platform Developer I | The PD1 the posting names — Apex, tests, the platform model you deploy | trailhead.salesforce.com/credentials/platformdeveloperi |
| Platform App Builder | Metadata you move every week: objects, Flow, security | trailhead.salesforce.com/credentials/platformappbuilder |
| Advanced Admin | Salesforce renamed this credential to **Platform Administrator II**. Study the current exam guide and use both names in conversation | trailhead.salesforce.com/credentials/platformadministrator-ii |
| A Salesforce "DevOps Engineer" cert | There is not an official one. Copado, Gearset, and AutoRABIT offer their own certificates — they show tool time and do not replace PD1 | Vendor sites, after you have actually used the tool |

Study order for this role: crash course and PD1 material first, then this page's labs, then Platform
Administrator II topics that overlap releases (security, change, environments).

## Related pages

- Crash course — objects, security, Flow, Apex, governor limits
- Navigation breadcrumbs — Setup paths, including Deployment & DevOps
- Labs and design — first Flow, trigger, LWC, callout
- Users and data — profiles, permission sets, import, field-level security
