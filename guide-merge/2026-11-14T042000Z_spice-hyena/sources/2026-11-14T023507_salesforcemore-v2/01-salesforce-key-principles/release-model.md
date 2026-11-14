# Release model — environments, branching, promotion, control gates

**Merge target:** sections 3, 4, 10, 11. This file is the reference model behind those sections.

## 1. Environment map

| Stage | Job | Usual sandbox | Who promotes | Gate |
|---|---|---|---|---|
| Dev | Build, unit test, early integration | Developer or Developer Pro; scratch org only for a package build | Developer via Git | Pull request review |
| QA | Automated validation, integration | Developer Pro or Partial Copy | Pipeline on merge | Green validation and named tests |
| UAT | Business acceptance | Partial Copy, or a masked Full | Release engineer from the release branch | Business sign-off |
| Pre-Prod | Dress rehearsal with prod-like metadata and volume | Full or recent Partial, refreshed close to the window | Release engineer | Validation-only deploy and release manager review |
| Prod | Customers | Production | Release engineer after approval | Named approver who is not the author; change window |

**Do not say "UAT is a scratch org."** A scratch org is an empty org created from a Dev Hub and a definition file. It will not have the bank's managed packages, SSO, named credentials, or licences unless someone encoded all of them. Scratch orgs are for package builds; sandboxes are the enterprise path.

## 2. Sandbox types

| Type | Metadata | Data | Best use |
|---|---|---|---|
| Developer | Yes | No | Isolated build and unit test |
| Developer Pro | Yes | No (more storage) | QA when rows are not needed |
| Partial Copy | Yes | A template sample | UAT when testers need realistic rows |
| Full | Yes | All production data | Pre-Prod, performance, and tests that depend on real shape |

**Refresh cadence.** Treat the interval as licence-dependent. Check Setup → Sandboxes for the next eligible refresh before committing to a date. A Full refresh is the slowest and the most sensitive.

**Refresh completion.** A refresh is not complete when the copy finishes. It is complete when:
1. Masking has run and someone has confirmed it.
2. Integration endpoints point at non-production.
3. Named credential secrets, external credentials, and certificates are present.
4. SSO has been tested.
5. Only the people named on the ticket can log in.

## 3. Branching model

```text
main                         ← mirrors production
  hotfix/<ticket>            ← cut from main only
  release/2026-11-27         ← cut from main at freeze
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

Rules:

- A hotfix is cut from `main` because `main` is what production is running. It merges back to `main` and into any open release branch. If it misses either, the next release resurrects the bug.
- A feature branch lives days, not weeks. Salesforce XML, especially Flows and profiles, does not merge. Long branches become manual conflict surgery.
- The release branch is what QA and UAT deploy. Developers do not deploy their feature branch into UAT.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the change-ticket id. That is the audit trail.

## 4. Promotion model

| Action | Trigger | What runs | Target |
|---|---|---|---|
| Validate PR | Pull request | Delta dry-run plus named Apex tests | CI sandbox |
| Integrate | Merge to release branch | Real deploy | QA |
| Stage | Release manager | Validation-only deploy | Pre-Prod, then Prod |
| Release | Change window, after approval | Quick deploy of the validated job, or a fresh deploy if the validation expired | Prod |
| Tag | Pipeline success | Annotated tag plus deploy id written to the ticket | Git |

**Key distinction.** A validation does not change the org. A quick deploy applies a validation that already succeeded, inside the platform window, so the change window stays short. If the payload changed or someone hotfixed production after the validation, re-validate.

## 5. Three release speeds

| Speed | When | Branch | Deploy bar |
|---|---|---|---|
| Scheduled | Release calendar | `release/<date>` | Full validation, UAT sign-off, change ticket, window |
| Hotfix | Production defect that cannot wait | `hotfix/<ticket>` from `main` | Same validation, smaller payload, still a ticket |
| Emergency | Active customer or regulatory harm | `hotfix/<ticket>` from `main` | A pre-written short path with a named approver and a validation deploy |

**Emergency is a shorter approval chain, not a skipped pipeline.** If the written path says one named approver and a validation deploy, that is the path at 2 a.m. as well.

## 6. Runbook template

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

## 7. Rollback model

Metadata does not roll back by itself. Rollback is a forward deploy of the last known-good tag, or a package install of the previous version.

| Situation | First move | Then |
|---|---|---|
| Bad Flow, previous version still in the org | Activate the previous Flow version | Redeploy the last good tag so Git matches the org |
| Bad Apex or configuration | Stop the bleeding (deactivate the automation if safe) | Validate the previous tag and deploy it |
| Destructive delete already ran | You cannot undelete records | Restore metadata from Git; data restore is a separate, ticketed path |
| Post-deploy data script already ran | Git revert will not undo the rows | The script needs its own reverse script, reviewed before the window |

## 8. Control gates checklist

- Branch protection requires a pull request, a review, and a green validation.
- Production environment requires a named reviewer who is not the author.
- The integration user is dedicated and least-privilege.
- Secrets are environment-scoped, not repository-wide, for production.
- The pipeline serializes deploys per org (concurrency group or lock).
- The release tag is created only after the smoke test passes.
- The runbook and audit pack are completed before the window closes.
