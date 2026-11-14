# 01 — Job description × existing training page cross-reference

**Job:** DevOps Engineer (Salesforce), Scotiabank, Toronto. Requisition 276046.
**Job URL:** <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/>
**Existing page:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/>
**Page source:** `docs/salesforce/devops-engineer.md` (554 lines, commit `5bf3887` in the ServiceNow_Learning repo)

Verdict key:
**Covered** = the page answers the line at the right depth ·
**Thin** = the page names it but not deep enough for the line ·
**Gap** = the line is not materially addressed ·
**Correction** = the page says something the primary source contradicts.

> **Numbering.** `R1`–`R14` are the fourteen bullets under *"In this role, you will"*, in posting
> order. `Q1`–`Q14` are the fourteen bullets under *"Do you have the skills that will enable you to
> succeed"*, in posting order. The posting's eighth qualification bullet is a single bullet with
> four sub-items ("Good understanding of: Apex & Triggers / Flows / Permission Sets vs Profiles /
> Record Types, Page Layouts, and Security model"); those are labelled **Q8a–Q8d** here so the
> mapping stays one-to-one with the posting while keeping the sub-items addressable.
> *(Corrected 2026-11-14: an earlier draft of this file numbered the qualifications Q1–Q17,
> which over-counted the posting.)*

---

## Part 1 — Responsibilities ("In this role, you will")

| # | JD line | Page section | Verdict | What this bundle adds |
|---|---|---|---|---|
| R1 | Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows | §5 CI/CD | **Thin** | `04` — full GitHub Actions pipeline, JWT/OIDC auth, branch protection, environments, reusable workflows, concurrency, the validate→quick-deploy pattern. The page's §5 is a 4-stage table and a 3-line command pair. |
| R2 | Manage multi environment release strategies (Dev, QA, UAT, Pre Prod, Prod) | §3 Environments and sandboxes | **Covered** | `05 §2` adds the promotion gates, what "promotion" means in each tool, and which sandbox type supports which stage, plus the queueing constraint (`02 §3.1`) that makes parallel promotion unsafe. |
| R3 | Coordinate scheduled releases, hotfixes, emergency deployments | §10 Releases, hotfixes, rollback | **Thin** | `05 §3` adds the three speeds with branch topology, the branch-protection requirements GitHub enforces, the auto-reject/3-day approval rule in AutoRABIT, and Copado's scheduled-promotion exclusion from automations. |
| R4 | Ensure deployment activities follow audit, security, and compliance standards | §11 Banking change control | **Thin** | `05 §4` + `07 §7` — the artefacts an auditor asks for, and the org settings that either enforce or undermine them (deployment IP allowlist, audit trail retention, API usage notification, debug-log handling). |
| R5 | Manage Salesforce metadata lifecycle using source control (Git) | §1 Source of truth | **Covered** | `05 §1` adds the full lifecycle: retrieve → review → commit → validate → deploy → tag → rollback, plus source tracking behaviour and `.forceignore`. |
| R6 | Handle sandbox strategy (creation, refresh, data masking) | §3 Environments and sandboxes | **Thin** | `05 §5` + `03 §1.9` — sandbox **types** with their real constraints (Full = prod data; Partial = template; Developer = no data; scratch ≠ sandbox), the refresh→re-auth→re-sync→mask sequence, and the fact that **no vendor tool performs the Salesforce refresh for you**. |
| R7 | Resolve deployment conflicts: Profiles and Permission Sets | §7 Conflict clinic → Profiles | **Covered** | `05 §6.1` adds profile decomposition, permission set groups, and the exact permission-set model a deployment user needs. |
| R8 | Resolve deployment conflicts: Record Types & Page Layouts | §7 Conflict clinic → Record Types / Page Layouts | **Covered** | `05 §6.2` adds the "one payload" rule, the business-process dependency, and the Lightning record page (`FlexiPage`) vs classic layout distinction the page mentions but does not connect to deployment. |
| R9 | Resolve deployment conflicts: Flows, Apex, and dependencies | §7 Conflict clinic → Flows / Apex | **Thin** | `02 §4` is the real deep dive: the dependency table, the error-string→cause→fix map, the Master-Detail Recycle Bin destruction rule, and the 7,500-code-unit deployment ceiling. |
| R10 | Recommend best practices to reduce deployment failures and rework | §12 Design patterns | **Covered** | `05 §7` converts each pattern into a concrete policy with an owner and a measurable outcome. |
| R11 | Partner with Salesforce Developers, Admins, QA, and Platform teams | §What this role actually owns | **Thin** | `05 §8` defines the RACI and the handoff artefacts (a release note a QA lead can act on; a dependency list a developer can act on). |
| R12 | Provide guidance on DevOps friendly Salesforce design patterns | §12 Design patterns | **Covered** | `05 §9` extends to the pattern catalogue with the *deployability* consequence of each. |
| R13 | Document release processes, runbooks, and rollback procedures | §10 Runbook template | **Thin** | `05 §10` gives the runbook fields, who fills each, and the rollback decision tree (Flow version activation vs forward redeploy vs data restore). |
| R14 | Support audit and change management requirements | §11 Banking change control | **Thin** | `05 §4` + `06` — which certification evidence maps to which control, and how a change ticket, deploy id and test run assemble into an evidence pack. |

---

## Part 2 — Qualifications ("Do you have the skills that will enable you to succeed")

| # | JD line | Page section | Verdict | What this bundle adds |
|---|---|---|---|---|
| Q1 | Strong experience with Salesforce metadata deployments | §2 Metadata that breaks releases | **Thin** | `02 §3` — the actual deploy ceilings (≈39 MB compressed / ≈600 MB uncompressed / 10,000 files), one-deploy-at-a-time, the queue not being FIFO, the Deployment Status charts, and the permission the deploy identity needs. |
| Q2 | Experience with Git based source control | §4 Branching | **Covered** | `05 §1.4` adds the topology plus the GitHub branch-protection rules that make the topology real. |
| Q3 | **Understanding of Salesforce limits, metadata dependencies, and deployment constraints** | §2 (partial) | **Thin** | `02` is the dedicated artifact: governor limits per transaction and per org, platform allocations, payload limits, dependency map, deployment constraints, test levels. **This is the single biggest gap in the existing page.** |
| Q4 | Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab, etc.) | §5 CI/CD | **Thin** | `04` — complete YAML for GitHub Actions plus the Azure DevOps / GitLab equivalents, and the decision criteria for which one a regulated bank should pick. |
| Q5 | Understanding of branching strategies (feature, release, hotfix) | §4 Branching | **Covered** | `05 §1.4`, `05 §3` — adds the hotfix → release-branch back-merge rule and the tag-as-rollback-target discipline. |
| Q6 | Familiar with automated testing and validation concepts | §9 Tests and validation | **Thin** | `02 §5` — the **five** test levels (not four), the exact metadata-type list that forces a full local test run, per-class coverage semantics, and `checkOnly` restrictions. |
| Q7 | Hands on experience with Salesforce DevOps tools such as Gearset, Copado, AutoRABIT, or equivalent | §6 DevOps tools | **Thin** | `03` — per-vendor object model, navigation, click paths for compare/deploy/backup/masking/rollback, plan gates, and a list of stale names to avoid. The page has one table row per vendor. |
| Q8a | Good understanding of Apex & Triggers | §2 (mentions triggers) | **Thin** | `02 §1`, `02 §2` — trigger batch size 200 (2,000 for platform events/CDC), 16-level trigger stack, bulkification limits, and the deployment ceiling of 7,500 Apex code units. |
| Q8b | Flows (Before/After Save) | §7 Conflict clinic → Flows | **Covered** | `05 §6.3`, `05 §9` — before-save vs after-save deployment implications, the Draft/Active version trap, and why a before-save flow built as after-save fails under volume. |
| Q8c | Permission Sets vs Profiles | §7 Conflict clinic → Permission sets | **Covered** | `05 §6.1` — permission set groups as the bundling mechanism, and the exact deploy-user permission model. |
| Q8d | Record Types, Page Layouts, and Security model | §7 Conflict clinic | **Covered** | `05 §6.2` — the assignment chain (record type → business process → picklist values → layout → profile/permission set). |
| Q9 | Ability to troubleshoot deployment failures and dependency issues | §2 Metadata that breaks releases | **Thin** | `02 §6` — an ordered debugging procedure (get the id → read the error verbatim → classify by error class → reproduce with the CLI against the same org type → re-validate). |
| Q10 | Salesforce Platform Developer experience | throughout | **Covered** | `06 §1` — maps the JD's "Platform Developer" to the current **Salesforce Certified Platform Developer** credential and to the parts of PD1 that actually matter for release engineering. |
| Q11 | Experience with Unlocked Packages / Managed Packages | §8 Packages | **Covered** | `05 §11` — adds the 10,000-file limit, the 35,000-file 1GP ceiling, and the certified-namespace governor-limit interaction. |
| Q12 | Exposure to Salesforce DX | §1 Source of truth | **Covered** | `04 §2`, `05 §1` — `sfdx-project.json`, source tracking, scratch org vs sandbox, and the new `sf project` command family (including `sf project deploy validate` and `sf project deploy quick`, which the page does not mention). |
| Q13 | Experience in regulated or enterprise environments | §11 Banking change control | **Thin** | `05 §4`, `05 §10` — segregation of duties made structural, the evidence pack, and the "no customer data in a ticket or a slide" rule with the debug-log mechanism behind it. |
| Q14 | Salesforce certifications (PD1, Advanced Admin, DevOps related certs) | §Certifications | **Correction** | `06` — current credential names, the **Platform Administrator prerequisite** for Administrator II, and the fact that there is no Salesforce-branded DevOps certification, so "DevOps related certs" = vendor credentials (Gearset Academy, Copado Certified, AutoRABIT Academy ARM tracks). |

---

## Part 3 — Corrections the merge round must apply to the existing page

| Existing text | Problem | Corrected statement | Evidence |
|---|---|---|---|
| §5/§9: "the `--test-level` values … `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`" | Missing a fifth level that exists in the CLI and the API | Add `RunRelevantTests` (Beta): Salesforce selects the relevant tests from the payload; per-class/trigger 75% still applies; `@IsTest(critical=true)` and `@IsTest(testFor='…')` can force tests in | Salesforce CLI plugin messages (`flags.test-level.description`) + Metadata API guide |
| §5: "`sf project deploy start --dry-run --test-level RunSpecifiedTests --tests CommercialBankingReleaseTest`" | `--dry-run` and `--tests` together are fine, but the page implies dry-run is the only validation mode | `sf project deploy validate` is now a first-class command; `sf project deploy quick` is the quick-deploy path. Both should appear | `plugin-deploy-retrieve/src/commands/project/deploy/{start,validate,quick}.ts` |
| §6: the DevOps tools table lists Gearset/Copado/AutoRABIT as one row each with no object model | Cannot answer "where do I click" | Replace with per-vendor subsections (`03`) | Vendor docs, 2026-11-14 |
| §6: "Gearset — Compare and deploy, CI, backups on some editions" | Understates the backup product and omits that Gearset does **not** refresh sandboxes | Backups are the licensed `Data backup jobs` product (Standard/High frequency/Big Object tiers, 7-year record retention, indefinite metadata retention); the Salesforce refresh itself remains a Salesforce operation | Gearset docs |
| §6: "Change Sets — Setup UI … why they fail at this job's scale" | Accurate but incomplete for a bank | Add: change sets cannot satisfy segregation of duties because the deploying user is the approving identity; they have no audit artefact trail, no tag, no rollback target | Metadata API `deploy()` documentation |
| §9: "Salesforce requires 75% coverage as the production gate" | Imprecise | Coverage is computed **per class and trigger individually**, each needing ≥75%, under `RunSpecifiedTests` and `RunRelevantTests`; `RunLocalTests` has no per-class coverage requirement in the same sense | CLI plugin message text |
| §3: "Full copies contain customer data … Refresh is not done when the copy finishes" | Correct, but the page does not say who may log in before masking completes | Masking is a **gate**, not a courtesy: logins are restricted to the ticket's named people until mask-complete is confirmed, and integration endpoints must be repointed before any login | Gearset refresh best-practice + Vault masking config fields |
| §Certifications: "Salesforce renamed this credential to Platform Administrator II" | Missing the prerequisite | Administrator II requires **Salesforce Certified Platform Administrator** | Salesforce credential page |
| §10 rollback table: "Bad Flow, previous version still in the org → Activate the previous Flow version" | Correct but does not distinguish mitigation from rollback | Activating an older version is a **mitigation**; Git still holds the bad version. Rollback = forward-deploy the last good tag. Say both | — |
| `crash-course.md`: async heap "6× higher / 12 MB" | Wrong number | Async heap is **25 MB**; async CPU is **60,000 ms** | Apex Developer Guide, governor limits |

---

## Part 4 — What the existing page already does well (keep it)

The existing page's structure is sound and should not be rewritten. Specifically:

- The "You own / You partner on / You do not own alone" table is an excellent scope boundary — keep it
  and add the segregation-of-duties row.
- The failure-symptom table in §2 is good; `02 §4.1` extends it rather than replacing it.
- The branching diagram in §4 is correct. Add only the hotfix back-merge rule and the
  "feature branches live days, not weeks" consequence.
- The runbook template in §10 is the right shape. `05 §10` adds owners and the rollback decision tree.
- The quiz is well-formed. Add two questions: the 7,500-code-unit deployment ceiling and the
  one-deployment-at-a-time / non-FIFO queue rule.

---

## Part 5 — Proposed target structure for the merged page

Each new item is a `<details>` block so the page stays scannable — the user's explicit ask.

```
1. Source of truth                     (+ details: lifecycle end-to-end; source tracking; .forceignore)
2. Metadata that breaks releases        (+ details: error→cause→fix table; destructive changes;
                                                Master-Detail Recycle Bin rule)
2b. LIMITS, DEPENDENCIES AND CONSTRAINTS  (NEW, collapsible sub-blocks)
    2b.1 Governor limits — per transaction
    2b.2 Governor limits — per org / per 24 h
    2b.3 Platform allocations (API, storage)
    2b.4 Metadata API payload limits
    2b.5 Metadata dependency map
    2b.6 Deployment constraints (locking, queueing, permissions)
3. Environments and sandboxes           (+ details: sandbox type table; refresh→mask gate)
4. Branching                           (+ details: hotfix topology; GitHub protection rules)
5. CI/CD                                (+ details: GitHub Actions pipeline; auth; quick deploy;
                                                 Azure DevOps / GitLab equivalents)
6. DevOps tools                         (REWRITTEN as three vendor subsections, each collapsible)
6a. Gearset
6b. Copado
6c. AutoRABIT
6d. Choosing between them
7. Conflict clinic                      (+ details: profile decomposition; record-type chain; flow versions)
8. Packages                             (+ details: file-count limits; namespace governor limits)
9. Tests and validation                 (+ details: five test levels; the test-forcing metadata list)
10. Releases, hotfixes, rollback        (+ details: three speeds; runbook with owners; rollback tree)
11. Banking change control              (+ details: evidence pack; segregation of duties; org settings)
12. Design patterns you coach           (+ details: pattern → deployability consequence)
13. Certifications                       (+ details: current names; prerequisites; curricula; study order)
```
