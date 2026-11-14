# 05 — Salesforce DevOps curriculum v1

Rebuilt from the guides' **actual section structure**, not from the previous `research_plan.md` (which was a
generic 4-week template with no Salesforce content).

**Why this differs from `forreviews/salesforceyetagain-v4`:** that folder's plan has 5 phases of "research"
and 0 modules of curriculum. This one has 8 modules, each with a terminal exercise and an evidence artifact —
the structure the guide itself uses ("Done when…").

---

## Design rules taken from the guide

1. **Every item ends in a "done when" test.** The guide never lists a topic without one. Neither does this.
2. **Labs before reading.** `labs-design.md` puts 4 labs before design considerations. The order is
   deliberate: you cannot design a Flow you have not built.
3. **Nothing is taught that the repo does not exercise.** The guide's §12 is about coaching patterns; a
   curriculum that teaches patterns the learner cannot practise in their own repo is decoration.
4. **Corrections are called out inline.** Where a widely-repeated figure is wrong (heap size), the module
   names the wrong number and the right one, with the source.

---

## Module 0 — Environment and vocabulary (half a day)

**Source:** Crash Course, "What Is Salesforce?" + "Navigation: Where Things Live"

| Topic | The one thing to remember |
|---|---|
| Platform, org, instance | An org is a tenant. Production is one org; dev is another. They do not share data |
| Objects / records / fields | Object = table. Record = row. Field = column |
| Standard vs custom | Custom objects and fields carry `__c`. That suffix is how you tell them apart in any payload |
| App Launcher vs Setup | App Launcher is where users work. Setup is the control room. Every admin task is a Setup path |
| Metadata vs data | Metadata is the schema and config (deploys). Data is the rows (migrates by load, never by deploy) |

**Done when:** you can say, without notes, which of these is metadata and which is data: a Flow, a
permission set, an Account record, a custom field, a validation rule, a page layout.

**Evidence:** a one-page table of 12 items, each labelled metadata or data.

---

## Module 1 — The data model and why it breaks deploys (1 day)

**Source:** Crash Course, "The Big Picture" → "Data Integrity & Relationships"; DevOps guide §2

| Topic | The one thing to remember |
|---|---|
| Lookup vs master-detail vs hierarchical | Master-detail is a real parent-child with cascade delete. Lookup is a soft pointer |
| Roll-up summaries | Only work on master-detail. If you need a roll-up and you have a lookup, you have a design decision to make |
| Record types + business processes | A record type depends on picklist values, a business process, a page layout assignment, and profile/permission-set visibility. Deploy all five together or it half-works |
| Custom metadata vs custom settings | Custom metadata is deployable configuration. Custom settings are data. Toggles belong in custom metadata |
| External IDs and unique fields | The only fields you can safely match on during a data load |

**Done when:** you can name the five things a record type deploy needs, from memory, and explain what
"deployed successfully but users cannot create that type" means.

**Evidence:** the 5-item list, plus a written explanation of the failure mode.

---

## Module 2 — Security model: profiles vs permission sets (1 day)

**Source:** Crash Course "Users, Profiles, Roles & Security"; User Management & Data guide §Profiles/Permission Sets; DevOps guide §7 (Profiles, Permission sets)

This is the module the DevOps guide calls out as the most common release-engineering failure.

| Topic | The one thing to remember |
|---|---|
| Profile | A grab bag: user permissions, object permissions, field permissions, layout assignments, record-type visibility. It is one big file. **It does not merge.** |
| Permission set | Fine-grained, additive, small. **It does merge** if you keep it small |
| Permission set group | Bundles permission sets for a job function. How you avoid one giant `CB_Admin` set |
| OWD → role hierarchy → sharing rules → manual sharing | The order of widening access. OWD is the floor; nothing restricts below it |
| Field-level security | Hide a field from a profile *or* a permission set. Not both, and not neither |
| `with sharing` / `without sharing` | Apex runs in the sharing context of the running user unless you say otherwise |

**The sentence to be able to say:** *"I will reject a story whose only access change is an edit to
`Admin.profile`. Ship a permission set for that persona instead."*

**Done when:** given a story "the new Credit Officer role needs read on Account and edit on
Credit_Application__c", you produce a permission set + permission set group, not a profile edit.

**Evidence:** the permission set XML and the group membership, committed to Git.

---

## Module 3 — Automation: Flow, and what still needs Apex (1 day)

**Source:** Crash Course "Automation: Flow, Process Builder, Workflow" + "When to Code vs When to Flow"

| Topic | The one thing to remember |
|---|---|
| Flow (record-triggered, before-save, after-save) | Before-save for same-record field updates (no DML, fast). After-save for anything touching other records |
| Flow XML does not merge | One owner per flow per release, or split into subflows |
| Flow version state | Deploy can leave the new version Draft or Active. Confirm which, in a sandbox, before promising prod behaviour |
| Process Builder / Workflow Rules | Retired-path features. Do not build new ones |
| Apex triggers | When Flow genuinely cannot do it: complex logic, callouts, recursion control |

**The sentence to be able to say:** *"A before-save Flow that should have been before-save and was built
as after-save will time out under volume."*

**Done when:** you can explain, for a given requirement, whether it is a before-save Flow, an after-save
Flow, or a trigger — and why.

---

## Module 4 — Governor limits (1 day, and do not trust the published page)

**Source:** Crash Course "Governor Limits" **with corrections** + `developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html`

The published crash course has **three wrong heap figures** (lines 802, 883, 896). I verified the correct
values against the official Apex Developer Guide. Learn these:

| Limit | Sync | Async | Verified value |
|---|---|---|---|
| **Total heap size** | **10 MB** | **25 MB** | Official governor-limits table: "Total heap size … 10 MB / 25 MB" |
| **CPU time** | 10,000 ms | 60,000 ms | same table |
| SOQL queries | 100 | 200 | Crash course — correct |
| DML rows | 10,000 | 10,000 | Crash course — correct |
| Callouts | 100 | 100 | Crash course — correct |

**Correction to memorise:** the crash course says heap "doubles" to 12 MB async. It does not double, and
12 MB is wrong. **10 MB sync → 25 MB async (2.5×), CPU 10,000 ms → 60,000 ms (6×).**

**The review question:** *"What happens when this runs on 200 records?"*

**Done when:** you can state the heap and CPU figures with the sync/async split, name the three places the
crash course is wrong, and explain why believing 12 MB would cause a production `LimitException` in a
Queueable job.

---

## Module 5 — Environments, sandboxes, and the masking gate (1 day)

**Source:** DevOps guide §3 (Environments and sandboxes)

The five stages, verbatim from the guide:

| Stage | For | Usual sandbox | Promoted by |
|---|---|---|---|
| Dev | Build and unit test | Developer / Developer Pro | Developer, via Git |
| QA | Automated validation, integration | Developer Pro or Partial Copy | Pipeline, on merge |
| UAT | Business testers | Partial Copy, or masked Full | Release engineer, from release branch |
| Pre-Prod | Dress rehearsal, prod-like metadata and volume | Full, or recent Partial | Release engineer |
| Prod | Customers | Production | Release engineer, after approval, in window |

Four sandbox types, in the order you will be asked: Developer (metadata, no data) → Developer Pro (metadata,
more room) → Partial Copy (metadata + template sample) → Full (metadata + all prod data).

**Scratch orgs are not sandboxes.** A scratch org is an empty org from a Dev Hub and a definition file.
Useful for a single package. A bad interview answer is "UAT is a scratch org."

**The masking rule:** a Full sandbox is not done when the copy finishes. It is done when masking has run
and access is limited to the people on the ticket. Mask email, phone, government id, account number, birth
date. A named person confirms mask-complete. Nobody outside the ticket logs in before that confirmation.

**Done when:** you can draw the five-stage path with the sandbox type for each, and say who promotes into
each one.

**Evidence:** the drawn path plus the refresh/mask checklist (Module 7's lab).

---

## Module 6 — Branching, CI/CD, and the four stages (2 days)

**Source:** DevOps guide §4, §5, §6

**Branching, verbatim:**

```
main                         ← matches production
  hotfix/<ticket>            ← cut from main only
  release/<date>             ← cut from main when the release freezes
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

Rules that matter more than the diagram:
- A hotfix is cut from `main`, merges back to `main` **and** into any open release branch. Otherwise the
  next release resurrects the bug.
- A feature branch lives days. Metadata XML does not merge.
- The release branch is what QA and UAT deploy. Developers do not deploy their own feature branch to UAT.
- **Tag production after a successful deploy.** That tag is the rollback target.

**The four CI stages:**

| Stage | Trigger | Runs | Target |
|---|---|---|---|
| Validate | Pull request | `sf project deploy start --dry-run` + the story's Apex tests | A CI sandbox, refreshed on a schedule |
| Integrate | Merge to release branch | Real deploy | QA |
| Stage | Release manager | Validation-only deploy | Pre-Prod, then Prod |
| Release | Change window, after approval | Quick deploy of the validated job, or a fresh deploy if validation expired | Prod |
| Tag | Pipeline success | Annotated tag + deploy id written to the ticket | Git |

**Authentication in CI:** JWT or a stored auth URL in the CI secret store. Never `sf org login web` on a
runner, never a password in the repo. The connected app, integration user, and that user's permission set
are part of the design. The integration user can deploy; it is not a shared human admin login.

**Test levels you must be able to say out loud:** `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`,
`RunAllTestsInOrg`. Production will not accept `NoTestRun` when the payload contains Apex.

**Done when:** you can describe the same four stages in GitHub Actions, Azure DevOps, or GitLab, and say
which auth method you would use and why.

---

## Module 7 — Labs (3 days)

**Source:** Labs & Design, Labs 1–4; DevOps guide Labs A–E

Do these in free Developer Edition orgs. Never against a bank org.

| Lab | Build | Done when |
|---|---|---|
| **A — Retrieve, review, dry-run** | Permission set `CB_Release_Reader` in `dev`, retrieve, read the XML, dry-run to `qa`, then real deploy. Then change it in `qa` Setup directly, retrieve, and look at the diff | The only path into `qa` is Git, and you can explain the diff in one sentence |
| **B — Profile conflict, on purpose** | Two branches each add a different field permission to the same profile XML. Merge. Watch it conflict. Throw it away, recreate as two permission sets, merge those | You can write three sentences: why the profile conflicted, what a bad merge would have granted, what you tell a dev who asks to edit `Admin.profile` for one field |
| **C — Failing validation** | An Apex class referencing a class you do not deploy. Dry-run, save the error. Add the class, dry-run again. Add a test that queries Account without inserting one, run it in an empty org, fix it | You can map an error string to "missing dependency" vs "test depends on org data" without guessing |
| **D — Runbook** | Fill the runbook template (see `06_salesforce_runbook_template.md`) for Lab A as if `qa` were production | You have a rollback tag even though the exercise is fake — the habit is the point |
| **E — Sandbox and mask checklist** | Write the refresh-ticket checklist for a Full sandbox | A stranger could run it without asking what "mask" means |

Plus the crash course's four build labs: custom object + Flow, Apex trigger + test, LWC, REST callout.

**Done when:** all five DevOps labs and all four build labs have a committed artifact.

---

## Module 8 — Release, hotfix, rollback, and the audit pack (1 day)

**Source:** DevOps guide §10, §11

Three speeds:

| Speed | When | Branch | Deploy bar |
|---|---|---|---|
| Scheduled | The release calendar | `release/<date>` | Full validation, UAT sign-off, change ticket, window |
| Hotfix | Prod defect, next release too late | `hotfix/<ticket>` from `main` | Same validation, smaller payload, still a ticket |
| Emergency | Active customer or regulatory harm | `hotfix/<ticket>` from `main` | Short path that is already written. Not "whoever is online clicks Setup" |

**Rollback is a forward deploy, not a revert:**

| Situation | First move | Then |
|---|---|---|
| Bad Flow, previous version still in org | Activate the previous Flow version | Redeploy the last good tag so Git matches the org |
| Bad Apex or config | Stop the bleeding (deactivate the automation if safe) | Validate the previous tag, deploy it |
| Destructive delete already ran | You cannot undelete records | Restore metadata from Git; data restore is a separate ticketed path |
| Post-deploy data script already ran | Git revert will not undo the rows | The script needs its own reverse script, reviewed before the window |

**The audit pack, every time:** change ticket id in commit and PR · diff a second person read (not the
author) · validation deploy id and prod deploy id · test run id and coverage number · named approver
different from the author · release tag · for a Full sandbox refresh, refresh time + mask-complete
confirmation + who may log in.

**The segregation-of-duties sentence:** *"The developer who wrote the Apex does not approve their own
production deploy. The integration user deploys. A human approves. Those are different identities."*

**Done when:** you can list the auditor's artifacts from memory, and you can say what a `git revert` does
not undo.

---

## Sequencing

```
Week 1   Modules 0-2   platform + data model + security      -> Labs 1, 2
Week 2   Modules 3-4   automation + governor limits          -> Lab 3
Week 3   Modules 5-6   environments + branching/CI           -> Labs A, B, C
Week 4   Modules 7-8   labs + release/hotfix/rollback        -> Labs D, E + audit pack
```

**Do not compress weeks 1–2.** The guide is explicit that the DevOps page assumes the crash course is not
fuzzy: *"Do the crash course first if Apex, Flow, profiles, and permission sets are still fuzzy."*

## What is deliberately not here

- **Exam-percentage tables.** No cited exam guide; publishing invented weights is the exact error the peer
  review caught in two bundles.
- **Vendor tool click-paths.** The guide is explicit that button paths differ by vendor and stay at the
  category level.
- **A "Salesforce DevOps Engineer" certification.** The guide states plainly: *"There is not an official one
  to list as if it existed."* The real credentials are PD1, Platform App Builder, and Platform Administrator II.
  Vendor certs (Copado, Gearset, AutoRABIT) "show tool time. They do not replace PD1."
- **An unverified "Development Lifecycle and Deployment Architect" mapping.** Two peer bundles assert this
  credential is the DevOps one. It may well be relevant, but it is not named in the DevOps guide and I did
  not verify it against the official credential page. It belongs in a follow-up, not in a curriculum.