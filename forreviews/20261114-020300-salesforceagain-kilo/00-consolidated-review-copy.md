# For review — Salesforce DevOps Engineer research bundle (Scotiabank requisition 276046)

> **Unique file:** `forreviews/20261114-020300-salesforceagain-kilo/00-consolidated-review-copy.md`
> **Tracking subfolder:** `forreviews/20261114-020300-salesforceagain-kilo/` (this folder — all artifacts live here)
> **Worktree:** `salesforceagain`  ·  **Agent:** kilo  ·  **Research window:** 2026-11-14 02:03–02:33 UTC
> **Repository:** <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> (branch `main`)
> **Target page:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/>
> **Job:** <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> (Req. 276046)

This is a single consolidated review copy of the research bundle in
`forreviews/20261114-020300-salesforceagain-kilo/`. The split, per-topic source files sit beside it
in the same folder. The same content is also committed on branch
`research/salesforceagain-2026-11-14T020300Z` under
`research/2026-11-14T020300Z-kilo-salesforceagain/`.

---

## Contents

| Part | Artifact | Original file in the bundle |
|---|---|---|
| Part 0 | Bundle manifest, method, headline findings | `README.md` |
| Part I | Research plan — JD → artifact matrix, method, source policy | `00-plan.md` |
| Part II | Job description × existing training page cross-reference | `01-jd-crossreference.md` |
| Part III | Salesforce limits, metadata dependencies, deployment constraints | `02-limits-and-constraints.md` |
| Part IV | DevOps tools in practice — Gearset, Copado, AutoRABIT | `03-devops-tools-ui.md` |
| Part V | GitHub Actions + Salesforce CI/CD | `04-github-actions-salesforce-cicd.md` |
| Part VI | Term-by-term deep dive of every JD phrase | `05-jd-term-deep-dive.md` |
| Part VII | Certifications named in the posting and their curricula | `06-certifications-curriculum.md` |
| Part VIII | Org settings and system properties that change release behaviour | `07-system-properties-setup-paths.md` |
| Part IX | Cross-bundle delta and reconciliation | `08-cross-bundle-delta.md` |
| Part X | Sources — URL, access date, verification status | `sources.md` |

---

## Part 0 — Bundle manifest, method and headline findings

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/README.md`*


| Field | Value |
|---|---|
| Bundle | `2026-11-14T020300Z-kilo-salesforceagain` |
| Worktree | `salesforceagain` |
| Agent | kilo |
| Branch | `research/salesforceagain-2026-11-14T020300Z` (pushed to `origin`) |
| Sibling bundle | `2026-11-14T021057Z_salesforcemore-v2` on branch `research/salesforcemore-v2-2026-11-14T021057Z` |
| Research start | 2026-11-14T02:03:00Z |
| Job | DevOps Engineer (Salesforce), Scotiabank, Toronto — Requisition 276046 |
| Job URL | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| Downstream page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| Downstream repo | <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM> |
| Status | Complete — all 10 artifacts written and cross-checked against primary sources |
| Contains secrets / customer data | No |


### Objective

Produce merge-ready, primary-source-verified research that (a) cross-references every line of the
job description against the existing `devops-engineer` training page, (b) goes one level deeper
than that page on every term, configuration and setting, (c) gives a practical, click-path-level
tour of the three named DevOps tools, (d) specifies a production-grade GitHub Actions + Salesforce
pipeline, and (e) deep-dives Salesforce limits, metadata dependencies, deployment constraints and
system properties — the exact line the posting calls *"Understanding of Salesforce limits,
metadata dependencies, and deployment constraints"*.

### Method

1. Pulled the live job posting and the live published training page.
2. Read the current `devops-engineer.md` source in the ServiceNow_Learning worktree
   (`/home/eaguiar2015/wt-sf-devops`) to establish the baseline.
3. Harvested primary sources through a text-extraction proxy where the vendor site is
   client-rendered (`help.salesforce.com` is JS-only and cannot be scraped directly; the
   `developer.salesforce.com` and vendor documentation hosts work).
4. Cross-read the Salesforce CLI plugin source on GitHub so every flag, option and test-level
   description in this bundle is the actual implementation string, not recalled from memory.
5. Ran three parallel vendor-documentation research agents (Gearset; Copado + AutoRABIT;
   GitHub Actions + Salesforce CLI), each instructed to return only what its source documents and
   to flag anything unverified.
6. Cross-checked every limit number against the official Salesforce Apex Developer Guide and
   Metadata API Developer Guide.

### Headline findings

| # | Finding | Why it matters |
|---|---|---|
| 1 | Metadata API deploy ceiling is **≈39 MB compressed / ≈600 MB uncompressed**, with **10,000 files** for unlocked/2GP packages and **35,000** for AppExchange-reviewed 1GP. | The existing page never states a payload ceiling. A release that crosses it fails for a reason no error message explains. |
| 2 | **Only one deployment runs at a time per org.** Queued deployments are *not* executed in submission order. | The classic bank-release failure: three teams all queued "at 9am", and prod got the wrong one first. |
| 3 | The metadata type list that forces a full local test run is **explicit** (ApexClass, Flow, PermissionSet, Profile, CustomField, CustomObject, RecordType, …). A package of only Reports/Dashboards runs **zero** tests. | Lets the release engineer pick the test level deliberately instead of by habit. |
| 4 | `RunRelevantTests` (Beta) is a **fifth** test level, not four. It is the only one that scales test time to payload size. | The existing page says "four stages" and lists four test levels — out of date. |
| 5 | Gearset's current UI uses a **grouped left sidebar** (`My connections`, `Metadata deployments`, `Continuous delivery`, `Backup & archiving`, `Sandbox seeding`, `Settings`). `Work Rules`, `Plan & Deploy`, `Deploy only changed components`, `Invalidate cache` are **not current labels**. | The existing page lists Gearset/Copado/AutoRABIT as a single row of names. Anyone asked "where do I click for backup?" would have guessed. |
| 6 | Gearset **backups are data + metadata backups with a separately licensed product**, and Gearset does **not** perform or schedule the Salesforce sandbox refresh itself. | Directly corrects a likely interview answer of "Gearset refreshes the sandbox". |
| 7 | Copado's "Fundamentals" and "DevOps Center" tiers and "Copado Data Masking" **do not exist** in current documentation. Current branding is **Copado Essentials / Essentials Plus** (standalone SaaS) and **Agentia Pipeline / Agentia Pipeline Pro** (enterprise). | The posting names "Copado" generically; the name you say in the interview should be current. |
| 8 | AutoRABIT has **no** "Test Repository" product and no standalone "Data Masking" product. Data masking lives in **AutoRABIT Vault**; CI/CD is **AutoRABIT ARM**. | Same reason. |
| 9 | "Advanced Admin" is now **Salesforce Certified Platform Administrator II**, and it has a **hard prerequisite**: Salesforce Certified Platform Administrator. | Affects exam sequencing and the claim on a résumé. |
| 10 | There is **no Salesforce-branded "DevOps Engineer" certification.** "DevOps related certs" means vendor credentials: Gearset Academy Certification, Copado Certified, AutoRABIT Academy ARM tracks. | The existing page already hints at this; this bundle gives the exact current names and what each covers. |
| 11 | Gearset's deployment-user requirement is **`Modify All Data`** (or narrowly `Modify Metadata Through Metadata API Functions` with per-type coverage), **`API Enabled`**, and **`Customize Application`** for Flow/LWC/custom-metadata types. | The concrete answer to "what does the integration user need?". |

### Bundle map

| File | Contents |
|---|---|
| `00-plan.md` | Plan, JD → artifact matrix, source policy, confidence rubric. |
| `01-jd-crossreference.md` | Every JD bullet → current page section → coverage verdict → what this bundle adds. |
| `02-limits-and-constraints.md` | Governor limits, platform/org limits, Metadata API deploy limits, metadata dependencies, deployment constraints. |
| `03-devops-tools-ui.md` | Gearset / Copado / AutoRABIT click-path-level tour with plan gates and corrections. |
| `04-github-actions-salesforce-cicd.md` | Production GitHub Actions pipeline, auth, quick-deploy pattern, YAML. Flags verified against the CLI plugin source. |
| `05-jd-term-deep-dive.md` | Term-by-term deep dive: every JD phrase → settings, variations, failure modes. |
| `06-certifications-curriculum.md` | PD1, Platform Administrator II, vendor DevOps certs, curricula, study order. |
| `07-system-properties-setup-paths.md` | Org settings that change deploy/limit behaviour, with Setup paths. |
| `08-cross-bundle-delta.md` | How this bundle relates to sibling bundles; where this one is authoritative. |
| `sources.md` | All sources with access date and verification status. |

### Known corrections to the existing page

| Existing page says | Correction | Evidence |
|---|---|---|
| Four deployment test levels | Five — `RunRelevantTests` (Beta) exists | Salesforce CLI plugin messages + Metadata API guide |
| "Deployment Settings: Allow inbound deployments" only | The Deployment Settings surface also gates CLI deploys and IP-restricted deploys | `07-system-properties-setup-paths.md` |
| Gearset/Copado/AutoRABIT as one generic table row | Three different products with different object models, different plan gates, and several stale names in common use | `03-devops-tools-ui.md` |
| "Salesforce renamed Advanced Admin to Platform Administrator II" | Correct, but the page omits the **Platform Administrator prerequisite** | Salesforce credential page |
| Async heap "6x higher" in the crash course | Async heap is **25 MB** (not 12 MB); async CPU is **60,000 ms** | Apex Developer Guide, governor limits |

### How the merge round should use this bundle

1. Start from `01-jd-crossreference.md` — it is the map from posting to page section.
2. Lift `02`, `05`, `06`, `07` as **collapsible (`<details>`) deep-dive blocks** appended to the
   corresponding existing sections of `devops-engineer.md`.
3. Use `03` to replace the single-line "DevOps tools" table with per-vendor subsections.
4. Use `04` as the new section (or a companion page) for GitHub Actions.
5. Use `08-cross-bundle-delta.md` to resolve conflicts with the sibling bundle
   `2026-11-14T021057Z_salesforcemore-v2`.


## Part I — Research plan — JD → artifact matrix, method, source policy

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/00-plan.md`*


### 1. Objective

Produce merge-ready research for the **Scotiabank DevOps Engineer (Salesforce)** requisition 276046,
targeting the published page
`https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/`.

The existing page is a good 12-section training track. This bundle does three things it does not do:

1. **Cross-reference** — proves, line by line, which JD bullet is covered and which is not.
2. **Deep dive** — expands every JD term into the settings, variations, commands and failure modes
   behind it.
3. **Verify** — replaces recalled UI labels and limit numbers with primary-source citations, and
   explicitly flags the places where the ecosystem's common vocabulary is out of date.

### 2. Constraints

- **No invented UI labels.** A wrong button name is a worse outcome than an admitted gap.
- **Everything must be teachable.** Each deep dive answers: where in the product do you go,
  what do you set, what breaks, how do you prove it.
- **Bank context.** Requisition 276046 is Commercial Banking Engineering, Toronto, regulated
  environment. Anything that weakens auditability or segregation of duties is called out.
- **Collapsible format.** The user asked for "deeper documentation into collapsible sections".
  The merge round should render each deep dive as `<details><summary>…</summary>…</details>` inside
  the existing page rather than creating a wall of prose.

### 3. JD → research artifact matrix

#### 3.1 Responsibilities ("In this role, you will")

| # | JD line | Primary artifact | Supporting artifacts |
|---|---|---|---|
| R1 | Design, implement, maintain CI/CD pipelines for Salesforce using Git based workflows | `04` | `05` §1, `07` |
| R2 | Manage multi-environment release strategies (Dev, QA, UAT, Pre Prod, Prod) | `05` §2 | `03`, `02` §5 |
| R3 | Coordinate scheduled releases, hotfixes, emergency deployments | `05` §3 | `04` §6, `07` |
| R4 | Ensure deployment activities follow audit, security, compliance standards | `05` §4 | `06`, `07` §7 |
| R5 | Manage Salesforce metadata lifecycle using source control (Git) | `05` §1 | `02` §4, `07` §4 |
| R6 | Handle sandbox strategy (creation, refresh, data masking) | `05` §5 | `03` §7, `07` §6 |
| R7 | Resolve deployment conflicts: Profiles & Permission Sets | `05` §6.1 | `02` §3 |
| R8 | Resolve deployment conflicts: Record Types & Page Layouts | `05` §6.2 | `02` §3 |
| R9 | Resolve deployment conflicts: Flows, Apex, dependencies | `05` §6.3 | `02` §2, §4 |
| R10 | Recommend best practices to reduce deployment failures and rework | `05` §7 | `02` §6 |
| R11 | Partner with Salesforce Developers, Admins, QA, Platform teams | `05` §8 | `03` |
| R12 | Provide guidance on DevOps friendly Salesforce design patterns | `05` §9 | `02` §1 |
| R13 | Document release processes, runbooks, rollback procedures | `05` §10 | `04` §7 |
| R14 | Support audit and change management requirements | `05` §4, §10 | `07` §7 |

#### 3.2 Qualifications ("Do you have the skills that will enable you to succeed")

| # | JD line | Primary artifact |
|---|---|---|
| Q1 | Strong experience with Salesforce metadata deployments | `02`, `04` |
| Q2 | Experience with Git based source control | `05` §1 |
| Q3 | **Understanding of Salesforce limits, metadata dependencies, and deployment constraints** | `02` (dedicated artifact) |
| Q4 | Experience building/managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab) | `04` |
| Q5 | Understanding of branching strategies (feature, release, hotfix) | `05` §1.4, §3 |
| Q6 | Familiar with automated testing and validation concepts | `02` §3, `04` §4 |
| Q7 | Hands-on with Gearset, Copado, AutoRABIT, or equivalent | `03` |
| Q8 | Apex & Triggers | `02` §1, `05` §9 |
| Q9 | Flows (Before/After Save) | `05` §6.3, §9 |
| Q10 | Permission Sets vs Profiles | `05` §6.1 |
| Q11 | Record Types, Page Layouts, Security model | `05` §6.2 |
| Q12 | Troubleshoot deployment failures and dependency issues | `02` §6, `05` §6 |
| Q13 | Salesforce Platform Developer experience | `06` §1 |
| Q14 | Unlocked / Managed Packages | `05` §11 |
| Q15 | Exposure to Salesforce DX | `05` §1, `04` §2 |
| Q16 | Experience in regulated/enterprise environments | `05` §4, §10 |
| Q17 | Salesforce certifications (PD1, Advanced Admin, DevOps related certs) | `06` |

### 4. Key Salesforce principles the research is anchored to

These are the load-bearing ideas. Every artifact should be traceable to one of them.

| Principle | Consequence for the DevOps role |
|---|---|
| **Metadata API is a compiler, not a file copier.** | A deploy succeeds only if the payload is internally consistent *and* consistent with the target org. Dependency failures are the default failure mode, not the exception. |
| **One deployment at a time per org; queued order is not submission order.** | Concurrency between teams is a release-management problem, not a tooling problem. |
| **Tests are part of the deployment, and the test level is a policy decision.** | `NoTestRun` / `RunSpecifiedTests` / `RunLocalTests` / `RunAllTestsInOrg` / `RunRelevantTests` each change what "green" means. |
| **Coverage is per class/trigger, not overall.** | 75% overall can still mean one class at 0%. |
| **The platform is multitenant; every resource is rationed.** | Governor limits, API allocations, async daily caps and code-size ceilings are release constraints, not just runtime trivia. |
| **Metadata is code; it does not merge.** | Branching strategy must minimise the number of XML files two stories touch. |
| **Destructive changes are not undoable by Git.** | Deletions and data changes need their own rollback path and their own approval. |
| **Sandboxes carry production data.** | Masking is a release-control gate, not a courtesy. |
| **A deployment is an auditable event, not a click.** | Ticket, diff, validation id, prod id, test run, approver, tag. |
| **Rollback is a forward deploy.** | You need a tag of the last known-good state, or you do not have a rollback. |

### 5. Method

1. Fetch the live JD and the live published page; fetch the `devops-engineer.md` source from the
   ServiceNow_Learning worktree.
2. Where the vendor site is client-rendered, route through a text-extraction proxy. Record the
   proxy used in `sources.md` so the merge round can re-verify.
3. For the Salesforce CLI, read the **plugin source** on GitHub
   (`salesforcecli/plugin-deploy-retrieve`) instead of the docs — the messages file is the
   authoritative string for every flag description and test-level definition.
4. For vendor tools, run dedicated research agents against official vendor documentation, with an
   explicit instruction to list "not found" items rather than guess.
5. Cross-check every numeric limit against the official Salesforce Apex Developer Guide and
   Metadata API Developer Guide.

### 6. Source policy and confidence rubric

| Tag | Meaning |
|---|---|
| `verified` | Primary source (official product docs, plugin source, official developer guide) states it directly. |
| `vendor-claim` | Vendor documentation states it; not independently confirmed in a live org. |
| `unverified` | Could not be confirmed. Recorded in the "Unverified" section with what would confirm it. |
| `correction` | A widely repeated claim that the primary source contradicts. |

**Rule applied throughout:** if a button label, product name, tier name or screen path could not
be found in current vendor documentation, the artifact says "not a current documented label" and
names the actual label instead. It never guesses.

### 7. Deliverables

| Artifact | Done when |
|---|---|
| `01-jd-crossreference.md` | Every JD line has a verdict and a pointer. |
| `02-limits-and-constraints.md` | Limits, dependencies and constraints are sourced, not recalled. |
| `03-devops-tools-ui.md` | A reader can open Gearset/Copado/AutoRABIT and find the feature the JD asks for. |
| `04-github-actions-salesforce-cicd.md` | A copy-pasteable, correct workflow with the rationale per line. |
| `05-jd-term-deep-dive.md` | Every term has settings, variations, failure modes and a "say it like this" line. |
| `06-certifications-curriculum.md` | Current credential names, prerequisites, curricula, and study order. |
| `07-system-properties-setup-paths.md` | The org settings that change deploy behaviour, with Setup paths. |
| `08-cross-bundle-delta.md` | Conflicts with sibling bundles resolved, and this bundle's authority points listed. |
| `sources.md` | Every URL, with access date and confidence tag. |

### 8. Out of scope

- Writing the final merged page (the merge round owns that).
- Pricing/licensing negotiation advice.
- Any claim about what Scotiabank actually runs. The posting does not say; everything about their
  pipeline in this bundle is framed as "what a bank of this shape typically does", never as fact.


## Part II — Job description × existing training page cross-reference

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/01-jd-crossreference.md`*


**Job:** DevOps Engineer (Salesforce), Scotiabank, Toronto. Requisition 276046.
**Job URL:** <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/>
**Existing page:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/>
**Page source:** `docs/salesforce/devops-engineer.md` (554 lines, commit `5bf3887` in the ServiceNow_Learning repo)
Verdict key:
**Covered** = the page answers the line at the right depth ·
**Thin** = the page names it but not deep enough for the line ·
**Gap** = the line is not materially addressed ·
**Correction** = the page says something the primary source contradicts.
---


### Part 1 — Responsibilities ("In this role, you will")

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

### Part 2 — Qualifications ("Do you have the skills that will enable you to succeed")

| # | JD line | Page section | Verdict | What this bundle adds |
|---|---|---|---|---|
| Q1 | Strong experience with Salesforce metadata deployments | §2 Metadata that breaks releases | **Thin** | `02 §3` — the actual deploy ceilings (≈39 MB compressed / ≈600 MB uncompressed / 10,000 files), one-deploy-at-a-time, the queue not being FIFO, the Deployment Status charts, and the permission the deploy identity needs. |
| Q2 | Experience with Git based source control | §4 Branching | **Covered** | `05 §1.4` adds the topology plus the GitHub branch-protection rules that make the topology real. |
| Q3 | **Understanding of Salesforce limits, metadata dependencies, and deployment constraints** | §2 (partial) | **Thin** | `02` is the dedicated artifact: governor limits per transaction and per org, platform allocations, payload limits, dependency map, deployment constraints, test levels. **This is the single biggest gap in the existing page.** |
| Q4 | Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab, etc.) | §5 CI/CD | **Thin** | `04` — complete YAML for GitHub Actions plus the Azure DevOps / GitLab equivalents, and the decision criteria for which one a regulated bank should pick. |
| Q5 | Understanding of branching strategies (feature, release, hotfix) | §4 Branching | **Covered** | `05 §1.4`, `05 §3` — adds the hotfix → release-branch back-merge rule and the tag-as-rollback-target discipline. |
| Q6 | Familiar with automated testing and validation concepts | §9 Tests and validation | **Thin** | `02 §5` — the **five** test levels (not four), the exact metadata-type list that forces a full local test run, per-class coverage semantics, and `checkOnly` restrictions. |
| Q7 | Hands on experience with Salesforce DevOps tools such as Gearset, Copado, AutoRABIT, or equivalent | §6 DevOps tools | **Thin** | `03` — per-vendor object model, navigation, click paths for compare/deploy/backup/masking/rollback, plan gates, and a list of stale names to avoid. The page has one table row per vendor. |
| Q8 | Good understanding of Apex & Triggers | §2 (mentions triggers) | **Thin** | `02 §1`, `02 §2` — trigger batch size 200 (2,000 for platform events/CDC), 16-level trigger stack, bulkification limits, and the deployment ceiling of 7,500 Apex code units. |
| Q9 | Flows (Before/After Save) | §7 Conflict clinic → Flows | **Covered** | `05 §6.3`, `05 §9` — before-save vs after-save deployment implications, the Draft/Active version trap, and why a before-save flow built as after-save fails under volume. |
| Q10 | Permission Sets vs Profiles | §7 Conflict clinic → Permission sets | **Covered** | `05 §6.1` — permission set groups as the bundling mechanism, and the exact deploy-user permission model. |
| Q11 | Record Types, Page Layouts, and Security model | §7 Conflict clinic | **Covered** | `05 §6.2` — the assignment chain (record type → business process → picklist values → layout → profile/permission set). |
| Q12 | Ability to troubleshoot deployment failures and dependency issues | §2 Metadata that breaks releases | **Thin** | `02 §6` — an ordered debugging procedure (get the id → read the error verbatim → classify by error class → reproduce with the CLI against the same org type → re-validate). |
| Q13 | Salesforce Platform Developer experience | throughout | **Covered** | `06 §1` — maps the JD's "Platform Developer" to the current **Salesforce Certified Platform Developer** credential and to the parts of PD1 that actually matter for release engineering. |
| Q14 | Experience with Unlocked Packages / Managed Packages | §8 Packages | **Covered** | `05 §11` — adds the 10,000-file limit, the 35,000-file 1GP ceiling, and the certified-namespace governor-limit interaction. |
| Q15 | Exposure to Salesforce DX | §1 Source of truth | **Covered** | `04 §2`, `05 §1` — `sfdx-project.json`, source tracking, scratch org vs sandbox, and the new `sf project` command family (including `sf project deploy validate` and `sf project deploy quick`, which the page does not mention). |
| Q16 | Experience in regulated or enterprise environments | §11 Banking change control | **Thin** | `05 §4`, `05 §10` — segregation of duties made structural, the evidence pack, and the "no customer data in a ticket or a slide" rule with the debug-log mechanism behind it. |
| Q17 | Salesforce certifications (PD1, Advanced Admin, DevOps related certs) | §Certifications | **Correction** | `06` — current credential names, the **Platform Administrator prerequisite** for Administrator II, and the fact that there is no Salesforce-branded DevOps certification, so "DevOps related certs" = vendor credentials (Gearset Academy, Copado Certified, AutoRABIT Academy ARM tracks). |

---

### Part 3 — Corrections the merge round must apply to the existing page

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

### Part 4 — What the existing page already does well (keep it)

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

### Part 5 — Proposed target structure for the merged page

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


## Part III — Salesforce limits, metadata dependencies, deployment constraints

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/02-limits-and-constraints.md`*


> JD line covered: **"Understanding of Salesforce limits, metadata dependencies, and deployment
> constraints"** (Q3) and **"Strong experience with Salesforce metadata deployments"** (Q1).
>
> Every number below is taken from the official Salesforce Apex Developer Guide or Metadata API
> Developer Guide unless explicitly tagged otherwise. See `sources.md`.
---


### 1. Why a release engineer must know the limits

A deploy is a transaction against a shared, rationed platform. Three classes of limit decide
whether a release lands:

| Class | When it bites | Typical error |
|---|---|---|
| **Payload limits** (size, file count, one-deploy-at-a-time) | At deploy time | `Entity size limit exceeded`, `Deployment API` failure, a queued deploy that never starts |
| **Governor limits** (CPU, heap, SOQL/DML, callouts) | At runtime, under production volume | `System.LimitException: Too many SOQL queries: 101` |
| **Org allocations** (API calls/day, async executions/day, code size) | On a schedule, in bursts | `REQUEST_LIMIT_EXCEEDED`, `AsyncApexExecutions limit exceeded` |

The release engineer's job is to make the first class a *design* constraint, to gate the second
class before it reaches production, and to schedule around the third.

---

### 2. Governor limits (per Apex transaction)

**Source: Apex Developer Guide — Execution Governors and Limits.** `verified`

These limits count **per transaction**. For Batch Apex they reset for each execution of the
`execute` method. Scheduled Apex uses the *synchronous* limits even though it is asynchronous.

| Description | Synchronous | Asynchronous |
|---|---|---|
| Total SOQL queries issued | 100 | 200 |
| Total records retrieved by SOQL queries | 50,000 | 50,000 |
| Total records retrieved by `Database.getQueryLocator` | 10,000 | 10,000 |
| Total SOSL queries issued | 20 | 20 |
| Total records retrieved by a single SOSL query | 2,000 | 2,000 |
| Total DML statements issued | 150 | 150 |
| Total records processed by DML, `Approval.process`, `Database.emptyRecycleBin` | 10,000 | 10,000 |
| Stack depth for recursive trigger firing | 16 | 16 |
| Callouts (HTTP/web service) per transaction | 100 | 100 |
| Cumulative callout timeout | 120 s | 120 s |
| `future` methods per invocation | 50 | 0 in batch/future contexts; 50 in queueable |
| `System.enqueueJob` per transaction | 50 | 1 |
| `sendEmail` calls | 10 | 10 |
| **Total heap size** | **10 MB** | **25 MB** |
| **Maximum CPU time** | **10,000 ms** | **60,000 ms** |
| Maximum execution time per transaction | 10 min | 10 min |
| `EventBus.publish` (publish-immediately platform events) | 150 | 150 |
| Rows across all Apex cursors per transaction | 50 million | 50 million |
| `Cursor.fetch` calls per transaction | 100 | 100 |
| Rows across all Apex pagination cursors | 100,000 | 100,000 |
| Apex pagination cursor instances per transaction | 50 | 50 |
| Rows per page from an Apex pagination cursor | 2,000 | 2,000 |

#### 2.1 The rules that are easy to get wrong

| Rule | Detail | Release-engineering consequence |
|---|---|---|
| **Parent-child subqueries count as extra queries** | Each parent-child relationship subquery counts as an extra query; those query types have a limit of **3×** the top-level query limit (`Limits.getLimitAggregateQueries()`). Row counts contribute to the overall count. | A "one query" trigger with three child subqueries can blow the budget on its own. |
| **Custom metadata is exempt** | In a single transaction, custom metadata records can have **unlimited** SOQL queries. | Configuration-driven design does not consume the query budget. |
| **Dynamic SOQL still counts** | `Database.query`, `Database.countQuery`, `Database.getQueryLocator` and their `WithBinds` variants count against the SOQL limit. | "It's dynamic so it doesn't count" is false. |
| **DML counters include `System.runAs`**, `Approval.process`, `Database.setSavePoint`, `Database.rollback`, `EventBus.publish` (after-commit), `Database.emptyRecycleBin`, `Database.convertLead`. | | A `runAs` in a trigger framework is a DML statement. |
| **Heap and CPU are coupled** | Larger heap means more time spent on heap checks, so code near both limits is more likely to hit CPU first. | "It fits in heap" is not a durability argument. |
| **Exceptions are uncatchable** | Exceeding a limit raises an uncatchable `System.LimitException`. | There is no graceful degradation path inside the transaction. |
| **Limits apply per `testMethod`** | Each test method gets its own budget. | A bulk test that covers one case per method can hide a per-transaction blowout. |
| **Email services heap is 50 MB** | A separate ceiling for the email service path. | |

> **Correction to the existing crash course.** `crash-course.md` states the async heap as "6× higher"
> and "12 MB". The current official figure is **25 MB**, and async CPU is **60,000 ms**. This
> changes whether an async job is viable at all for a given design.

#### 2.2 Certified managed package namespace limits

Certified managed packages (those that passed AppExchange Security Review) get their own
per-transaction limits, *in addition to* the org's native limits.

| Description | Cumulative cross-namespace limit |
|---|---|
| SOQL queries | 1,100 |
| Records via `Database.getQueryLocator` | 110,000 |
| SOSL queries | 220 |
| DML statements | 1,650 |
| Callouts | 1,100 |
| `sendEmail` | 110 |

Heap, CPU, transaction execution time and namespace count are **shared**, not multiplied.
Non-certified packages get **no** separate limits — their usage counts against the org's totals.
`verified`

#### 2.3 Org-level limits (not per transaction)

| Description | Limit |
|---|---|
| Asynchronous Apex executions per 24 h (`DailyAsyncApexExecutions`) | **250,000** *or* applicable user licenses × 200, whichever is **greater** |
| Elastic async executions per 24 h (`DailyAsyncApexElasticExecutions`) | The org's daily async limit plus the lesser of the licensed daily limit or **2 million** |
| Apex cursor instances per 24 h | 10,000 |
| Cursor + pagination cursor rows per 24 h | 100 million |
| Apex pagination cursor instances per 24 h | 200,000 |
| Concurrent long-running transactions (>5 s) | Ratio of **100 licenses : 1** transaction; floor **10**, ceiling **50** |
| Apex classes scheduled concurrently | 100 (**5** in Developer Edition) |
| Batch Apex jobs in the flex queue in `Holding` | 100 |
| Batch Apex jobs queued or active concurrently | 5 |
| Batch Apex `start` method concurrent executions | 1 |
| Batch jobs submitted in a running test | 5 |
| Test classes queued per 24 h — production | greater of 500, or 10 × number of test classes |
| Test classes queued per 24 h — sandbox / Developer Edition | greater of 500, or 20 × number of test classes |

> **Why this belongs in a release document.** Batch Apex has **5 concurrent jobs**. A bank org with
> a nightly batch that fans out will silently queue behind itself. "Concurrent long-running
> transactions" is capped at 50 no matter how many licenses you buy past 5,000.

#### 2.4 Callout, query and code limits

| Description | Limit |
|---|---|
| Default callout timeout | 10 s |
| Max callout request or response size | 6 MB synchronous / 12 MB asynchronous (counts toward heap) |
| Max SOQL query runtime before cancellation | 120 s |
| **Max class and trigger code units in a single Apex deployment** | **7,500** |
| Apex trigger batch size | 200 (**2,000** for platform events and Change Data Capture) |
| For-loop list batch size | 200 |
| Records returned per Batch Apex `Database.QueryLocator` | 50 million |
| Max characters per class | 1,000,000 |
| Max characters per trigger | 1,000,000 |
| **Total Apex code in an org** | **6 MB** (10 MB in scratch orgs; raisable by Salesforce support) |
| Method size | 65,535 bytecode instructions |
| `MAX_DML_ROWS` in a single synchronous test | 450,000 rows (`Your runallTests is consuming too many DB resources`) |

> **The 7,500-unit deployment ceiling is the one people hit.** It is per *deployment*, not per
> package. A "small" change can fail with `Entity size limit exceeded` if the org is large and the
> tool expands dependencies. Split the release, or use the CLI's `--metadata` filter to deploy only
> what changed.

---

### 3. Metadata API deploy and retrieve limits

**Source: Metadata API Developer Guide — `deploy()` / `retrieve()`.** `verified`

> "Here are the deploy limits. Limits can change without notice."

| Feature | Limit |
|---|---|
| Maximum compressed `.zip` folder size | **≈39 MB** |
| Maximum uncompressed folder size | **≈600 MB** (629,145,600 bytes) |
| Maximum files in a first-generation managed package (1GP) | **35,000** — only if the package passed AppExchange Security Review |
| Maximum files in an unlocked or 2GP managed package | **10,000** |

Why 39 MB: Metadata API base64-encodes components *after* compression, and the encoded `.zip`
cannot exceed **50 MB**. Base64 adds roughly **22%**, so the compressed payload must be ≤ ≈39 MB.
Practical consequence: incompressible content (binary static resources, images) can exhaust the
39 MB compressed ceiling long before the 600 MB uncompressed ceiling.

> The existing training page gives **no payload ceiling at all**. A release engineer who does not
> know "≈39 MB compressed / 10,000 files" will learn it by hitting it during a change window.

#### 3.1 Deployment queueing — the constraint nobody writes down

From the same guide:

- You can initiate **multiple deployments**, but **only one deployment can run at a time**.
- The others sit in a queue under **Pending Deployments**.
- **Queued deployments are not necessarily executed in the order they were submitted.**
- To guarantee ordering, submit them one at a time after the previous one completes successfully.
- The deployment process **locks write access** to the resources being deployed until it completes.
  Changes made to locked resources or related items can result in errors.
- Salesforce recommends deploying during **off-peak** usage and limiting changes to the org while
  a deployment is in progress.

**Release-engineering translation:** three teams each queuing a prod deploy at 09:00 will not get
them applied in the order they submitted them. Gate prod promotions with a single serialised job
(GitHub Actions `concurrency`, a pipeline lock, a change-window calendar), not with "we asked people
to be polite".

#### 3.2 Deployment Status page

`Setup > Deploy > Deployment Status` (Quick Find: `Deployment Status`):

- Shows **real-time progress** of the current deployment.
- **Chart 1 — components:** how many components deployed out of total, and how many have errors.
- **Chart 2 — Apex tests:** how many tests have run out of total, how many errors, and the name of
  the currently running test.
- Deployments in progress or completed in the **last 30 days** are visible.
- `Cancel` is available while in progress or queued. The status becomes `Cancel Requested` until
  cancellation completes; a cancelled deployment is listed under **Failed**.

---

### 4. Metadata dependencies — what depends on what

A deploy is a **compile against the target org**, not a file copy. The payload must be internally
consistent and consistent with what already exists in the target.

#### 4.1 Error → root cause → fix

| Error / symptom | Root cause | Fix |
|---|---|---|
| `Invalid cross reference id` | A component points at something absent from the payload and absent from the target: record type referenced by a layout/business process, picklist values behind a record type, a class referenced by another class, a permission set assigned to a user that is not deploying | Deploy the parent **in the same payload**, or deploy to an org that already has it |
| `Entity not found` / compile error on Apex | The referenced class, trigger, interface or enum is not in the payload | Add the dependency; do not "try it in prod" |
| `no such column` / field does not exist | A Flow, layout, formula, validation rule or Apex references a field not in the payload and not in the target | Add the field, or deploy to the org that has it |
| `CANNOT_MODIFY_MANAGED_OBJECT` | Attempted to change a managed-package component | Configure around it, or upgrade the package. Never fork managed code into Git |
| `Field type change` failure (Master-Detail ↔ Lookup) | `checkOnly` (validation) does not support this field-type change | Validate by deploying to a **separate test sandbox**, not by `checkOnly` |
| Deployment succeeds but a record type is unusable | Business process, picklist values, layout assignment, or profile/permission-set visibility not deployed together | One payload: record type + layout + business process + permission set |
| Deployment succeeds but the user still sees the old Flow | The new Flow version was deployed **Draft** | Activate the version, or deploy the Flow as Active — verify what your tool does |
| Test passes in Dev, fails in UAT/Prod | The test depends on org data or org configuration that does not exist in the target (a profile, record type, custom setting, or an existing Account row) | Tests must create their own data |
| `Insufficient access OR no such type` | Deploying user lacks the permission for that metadata type | `Modify All Data` or `Modify Metadata Through Metadata API Functions` |

#### 4.2 The dependency rules that matter for package design

1. **Object first, then everything that points at it.** Custom object → fields → record types →
   validation rules → page layouts → Apex → Flows.
2. **Record type, layout and permission travel together.** The record type file is not the
   assignment; assignment lives on the profile and the record type.
3. **Apex class + its test + its dependencies in one payload.** A class that calls a class you
   forgot to retrieve fails to compile in the target.
4. **Flows do not merge.** One owner per Flow per release, or split into subflows.
5. **Profiles are a grab bag.** They do not merge. Two stories editing `Admin.profile` will
   conflict, and a bad merge silently grants or revokes access nobody reviewed.
6. **A deploy that adds a Master-Detail field** soft-deletes all detail records in the Recycle
   Bin before proceeding, and **permanently deletes them** during the deploy. They cannot be
   recovered. Same for a Lookup → Master-Detail conversion: detail records must reference a master
   or be soft-deleted, and a successful deploy permanently empties the Recycle Bin for those
   records.

#### 4.3 Destructive changes

| Rule | Detail |
|---|---|
| Deletions are a separate manifest | `destructiveChanges.xml`; the CLI exposes `--pre-destructive-changes` and `--post-destructive-changes` |
| Pre vs post | Pre-deletes run before additions (needed for renames that would collide); post-deletes run after. From API version **33.0**, both orders are supported. Earlier versions always deleted first. |
| Recycle Bin | By default deleted components go to the Recycle Bin. `--purge-on-delete` makes them immediately eligible for deletion instead (API 22.0+). |
| Git revert does not undo it | Rolling back a delete means **recreating** the metadata. Records on a deleted custom object are gone. A data restore is a separate, ticketed path (backup tool), not a Git operation. |
| Master-Detail caveat | See 4.2.6 — detail records are permanently deleted, not recycled. |

---

### 5. Test levels — the policy surface

**Source: Salesforce CLI plugin `deploy-retrieve` message definitions + Metadata API guide.** `verified`

There are **five**, not four. The existing page says four.

| Test level | Behaviour |
|---|---|
| `NoTestRun` | No tests run. Applies only to dev environments (sandbox, Developer Edition, trial). **This is the default for development environments.** |
| `RunSpecifiedTests` | Only the tests named with `--tests`. Coverage is computed **per class and trigger individually**, each needing **≥75%**. This differs from the overall coverage percentage. |
| `RunLocalTests` | All tests in the org **except** those from installed managed and unlocked packages. **This is the default for production deployments that contain Apex.** |
| `RunAllTestsInOrg` | All tests including managed packages. |
| `RunRelevantTests` *(Beta)* | Salesforce analyses the deployment payload and its dependencies and runs only the relevant tests. Each class/trigger in the payload still needs **≥75%** individually. Can be augmented with `@IsTest(critical=true)` (always runs) and `@IsTest(testFor='...')` (runs when the named class/trigger is new or changed). Requires explicit customer opt-in under Beta Services Terms. |

#### 5.1 Which metadata types force a test run

From the Metadata API guide — when no test level is specified:

> When deploying to production, **all local tests** are executed **if your deployment package contains
> Apex classes or triggers**. If your package doesn't contain Apex components, **no tests are run**.

From API version 33.0 and earlier, the trigger was broader: a package containing a **custom object**
ran all tests. From API 34.0, it does not.

**The full list of types that force all local tests to run:**

`ApexClass`, `ApexComponent`, `ApexPage`, `ApexTrigger`, `ArticleType`, `BaseSharingRule`,
`CriteriaBasedSharingRule`, `CustomField`, `CustomObject`, `DataCategoryGroup`, `Flow`,
`InstalledPackage`, `NamedFilter`, `OwnerSharingRule`, `PermissionSet`, `Profile`, `Queue`,
`RecordType`, `RemoteSiteSetting`, `Role`, `SharingReason`, `Territory`, `Validation Rules`,
`Workflow`

**Packages that run no tests by default:** `1 CustomApplication`; `100 Report + 40 Dashboard`
components.

**Packages that run all local tests:**

- `1 CustomField` component
- `1 ApexComponent` + `1 ApexClass`
- `5 CustomField` + `1 ApexPage`
- `100 Report` + `40 Dashboard` + `1 CustomField` ← the trap

**This is the single most useful table in this artifact for a release engineer.** A "reports-only"
release is safe and fast. A release that adds one field to an object with a Flow on it runs the
entire local test suite — which is often why a change window overruns.

#### 5.2 Validation (`checkOnly`) vs quick deploy

| Option | Changes the org? | Notes |
|---|---|---|
| `checkOnly` (validation) | **No** | Proves the payload compiles and tests pass against that org. Does not commit. |
| Quick deploy | Yes | Applies a previously successful validation without re-running the test runtime, inside Salesforce's quick-deploy window. |
| Full deploy | Yes | First deploy, or the validation expired, or the payload changed. |

**Quick deploy is only honest if nothing relevant changed in the target since the validation.** If a
hotfix landed in prod after you validated, your quick deploy is no longer a rehearsal of prod's
current state. Re-validate.

Also note: `checkOnly` **cannot** validate a Master-Detail ↔ Lookup field-type change. That
validation must be done by a full deploy to a separate test sandbox.

---

### 6. Platform and org allocations (not per transaction)

**Source: Salesforce App Limits Cheatsheet — API Request Limits and Allocations.** `verified`

| Org type | Concurrent inbound API requests lasting ≥20 s |
|---|---|
| Developer Edition / Trial | 5 |
| Production / Sandbox | 25 |

There is **no limit** on concurrent requests shorter than 20 seconds. Exceeding the concurrent limit
returns `REQUEST_LIMIT_EXCEEDED`; new requests are not processed until the count drops.

**24-hour total API allocations:**

| Edition | Per licence type per 24 h | Total per 24 h |
|---|---|---|
| Developer Edition | N/A | 15,000 |
| Enterprise / Professional with API | Salesforce 1,000; Salesforce Platform 1,000; Lightning Platform–One App 200; Partner Community 200; Lightning Platform Starter 200 per member (Enterprise); Lightning Platform Plus 1,000 per member (Enterprise) | 100,000 + (licences × per-licence calls) + purchased API Call Add-Ons |
| Unlimited / Performance | Salesforce 5,000; Salesforce Platform 5,000; Lightning Platform–One App 200; Lightning Platform Starter 200 per member; Lightning Platform Plus 5,000 per member | 100,000 + (licences × per-licence calls) + purchased API Call Add-Ons |
| Full Sandbox | N/A | 5,000,000 — **only** for Full sandboxes *not* created from a template; template-created sandboxes inherit the template's limits |

Other verified facts:

- REST/SOAP API timeout is **10 minutes**, except query calls (bounded by SOQL limits).
  `QUERY_TIMEOUT` / `REQUEST_RUNNING_TOO_LONG` on breach.
- Calls carrying a `DebuggingHeader` have a **separate** allocation of **1,000 calls per 24 h** and
  continue to work after the main allocation is exhausted.
- API calls made by certain Salesforce connected apps (for example the Salesforce mobile app) do
  **not** count.
- API calls made by **installed managed packages count** against the org limit.
- Monitor with: `Setup > System Overview` → **API Usage** section; **API Requests, Last 24 Hours**
  in Organization Detail; the `Sforce-Limit-Info` response header (REST); the REST `/limits`
  resource.
- Alert when approaching the cap: `Setup > Quick Find > API Usage Notifications`.
- Salesforce permits a limited overage after the daily limit is hit, to avoid blocking workflows.
  It applies only to paid orgs in active status — not trial, Developer Edition or sandboxes — and
  must not be relied on as a plan.

> **Release implication.** A CI pipeline that validates against a sandbox on every pull request
> burns API allocation on every PR. That is a scheduling decision, not a technical one.

---

### 7. Permissions the deploy identity needs

The client application must be logged in with **`Modify Metadata Through Metadata API Functions`**
or **`Modify All Data`**.

| Permission | Why |
|---|---|
| `Modify All Data` | Primary permission for metadata **and** data deployments |
| `Modify Metadata Through Metadata API Functions` | Narrower alternative — but the permission set must include the **specific permission for every metadata type deployed** |
| `API Enabled` | Required — the tool connects entirely through the API |
| `Customize Application` | Required for some Flow, LWC, app, custom-metadata and custom-setting deployments |
| Recommended | `View All Data`, `View Setup and Configuration`, `Author Apex`, `Manage Flow`, `Manage Profiles and Permission Sets`, `Manage Custom Permissions`, `View Roles and Role Hierarchy` |

**Practical trap:** choosing the narrow permission set is cheaper to approve through change
management and less risky, but every new metadata type you start deploying becomes a permission
change. For a bank, that trade-off is a decision to make deliberately, with a named owner and a
review cadence — not a default.

---

### 8. Debugging a failed deployment — the order to work in

1. **Get the deployment id.** `sf project deploy start` returns it; `Setup > Deploy > Deployment Status`
   lists the last 30 days with `View details` and the error text.
2. **Read the error verbatim.** Salesforce's messages are precise. Do not paraphrase them in the ticket.
3. **Classify it:**

| Error class | Signature | Where to look |
|---|---|---|
| Missing dependency | `Invalid cross reference id`, `entity not found`, `no such column` | The payload's `package.xml` and the target org's existing components |
| Permission | `Insufficient access OR no such type` | The deploy user's permission set |
| Managed package | `CANNOT_MODIFY_MANAGED_OBJECT` | Package version; upgrade path |
| Payload size | `Entity size limit exceeded` | Payload bytes vs ≈39 MB compressed; units vs 7,500 Apex code units |
| Test failure | `Test failure`, class-level failure | Test data assumptions; org data in the target |
| Field-type change | Master-Detail ↔ Lookup error | `checkOnly` cannot validate it — use a real sandbox deploy |
| Concurrency | Deployment sits in **Pending Deployments** | Another deploy is running; ordering is not guaranteed |
| Locked resource | Errors mentioning concurrent edits | A user changed a locked resource during the deploy |

4. **Reproduce locally with the CLI** using the same payload and the same API version, targeting
   the same org type. Gearset's own guidance is to reproduce a deployment error with the Salesforce
   CLI rather than guessing from the vendor UI.
5. **Re-validate after the fix** — do not jump straight to prod because the error was "obvious".

---

### 9. Unverified / open items

| Item | Status | What would confirm it |
|---|---|---|
| Exact per-org storage, file-size and Big Object ceilings | Not retrieved here (the Salesforce Help storage page is client-rendered) | The org's `Setup > System Overview` storage panel, or the current Salesforce App Limits Cheatsheet storage page |
| Whether the 39 MB / 600 MB / 10,000-file figures changed since retrieval (2026-11-14) | `verified` as of 2026-11-14, but the guide itself says "limits can change without notice" | Re-read the Metadata API Developer Guide before quoting in a customer document |
| Per-org custom limits (e.g. raised Apex code size, raised API allocation) | Org-specific, not published | `Setup > Company Information` and the Salesforce support case history |


## Part IV — DevOps tools in practice — Gearset, Copado, AutoRABIT

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/03-devops-tools-ui.md`*


> JD line covered: **"Hands on experience with Salesforce DevOps tools such as: Gearset, Copado,
> AutoRABIT, or equivalent"** (Q7).
>
> All navigation paths below were read from each vendor's current official documentation on
> **2026-11-14**. Where a label people commonly quote could **not** be found in current
> documentation, that is stated explicitly. Vendor UIs change; every path here is written so it can
> be re-verified from the linked article.
---


### 0. Premise corrections (read before quoting any of this)

| Commonly repeated claim | Current reality | Impact |
|---|---|---|
| "Gearset has tabs for Orgs / Pipelines / Deployments / Backups" | Gearset uses a **grouped left-hand navigation**: `My connections`, `Metadata deployments`, `Continuous delivery`, `Backup & archiving`, `Sandbox seeding`, `Settings` | The old mental map will not match the screen |
| "Gearset Work Rules" | Not a current label. The product name is **`Continuous Delivery Rules`** (Automation Platform Enterprise licence) | Name it correctly in an interview |
| "Gearset `Plan & Deploy`", "`Deploy only changed components`", "`Invalidate cache`", "`Single package`", "`Run deployment options`" | **None of these are current documented Gearset labels.** The real flow is `Compare and deploy` → select items → `Next` → `Pre-deployment summary` → `Validate deployment` / `Deploy now` | Do not say them |
| "Gearset compare tabs: Last deployed / Unmanaged / Components" | Current tabs are **`All items`, `New`, `Changed`, `Deleted`** plus a `Selected items` area. `Components` is an **expandable dependency-tree node**, not a tab | Do not say them |
| "Gearset Pipeline Job / Deployment Job" | Current job types are **`CI job`**, **`Deployment CI Job`** and **`Validation-only CI Job`** | Use these |
| "Gearset refreshes sandboxes" | **No.** Salesforce performs the refresh. Gearset handles re-authentication, branch sync, comparison and masking afterwards | Answering "Gearset refreshes the sandbox" is wrong |
| "Gearset backup is a feature toggle on the org" | Backups are a **separately licensed product** configured as `Data backup jobs` | — |
| "Copado Fundamentals / Copado DevOps Center" | Not current tier names. Current branding: **Copado Essentials** (Free / Basic / **Essentials Plus**) standalone SaaS, and **Agentia Pipeline** / **Agentia Pipeline Pro** (legacy docs: *Copado Deployer*, *Salesforce Metadata Pipelines*, *Salesforce Source Format Pipelines*) | Say the current name |
| "Copado Data Masking" | **No such product.** Copado has **Copado Data Deploy** / Data Sets / Data Templates | — |
| "AutoRABIT DevOps" / "AutoRABIT Test Repository" / "AutoRABIT Data Masking product" | Current: **AutoRABIT ARM** (CI/CD), **AutoRABIT Vault** (backup/recovery **and** data masking), **AutoRABIT CodeScan** (SAST), **AutoRABIT Guard** (security posture) | — |
| "AutoRABIT release calendar / change request object" | Not found. The real mechanisms are **Release Labels**, **Commit Labels**, **Merge Approvals**, and **Scheduled Deployments** (ARM New UI, feature-flagged) | — |

---

### 1. Gearset

#### 1.1 Navigation map (left sidebar)

| Group | Screen | URL |
|---|---|---|
| **My connections** | `Salesforce orgs` | `app.gearset.com/salesforce-connections` |
| | `Source control and services` | `app.gearset.com/linked-service-connections` |
| **Metadata deployments** | `Compare and deploy` | `app.gearset.com/configure` |
| | `Saved comparison pairs` | `app.gearset.com/configure-org-pairs` |
| | `Comparison history` | `app.gearset.com/deployments/comparison-history` |
| | `Deployment history` | `app.gearset.com/deployments/deployed` |
| | `Validated packages` | `app.gearset.com/deployments/validations` |
| **Continuous delivery** | `Pipelines` | `app.gearset.com/deployment-pipelines` |
| | `CI jobs` | `app.gearset.com/continuous-integration` |
| | `Change monitoring` | `app.gearset.com/change-alerts` |
| **Backup & archiving** | `Data backup jobs` | `app.gearset.com/data-backup-jobs` |
| **Sandbox seeding** | `Configure and deploy` | `app.gearset.com/configure-data` |
| **Data deployments** | `Data history` | `app.gearset.com/data-deployment-history` |
| **Settings** | `Settings`, `Team Security`, `Pipelines & CI jobs` | `app.gearset.com/account/team-security`, `…/account/pipelines-ci` |

There is **no single global Activity/History screen** — history is module-specific
(`Comparison history`, `Deployment history`, `Validated packages`, CI job run history,
`Data history`, backup `Job history`).

#### 1.2 Connecting an org

`My connections` → `Salesforce orgs` → `Add new org` → choose `Salesforce organization` → enter org
name and Salesforce username → authenticate. Sharing options: `Team member` or `Team owner`.
Row `Actions` menu → `Re-authorize`, `Remove connection`.

**Two Connected Apps.** Salesforce may show `Gearset` (OAuth connection/login) and `Gearset Deploy`
(deployment access). Connected Apps **cannot be installed through the Metadata API** — installation
is a manual Salesforce admin action. OAuth is 2.0 with PKCE; Gearset stores refresh tokens, rotates
them, applies a **30-day idle timeout**, and can enforce an **IP allowlist**.

**Deployment user permissions:** `Modify All Data` (or `Modify Metadata Through Metadata API
Functions` with per-type coverage), `API Enabled`, `Customize Application` (Flow/LWC/custom
metadata/settings), plus recommended `View All Data`, `View Setup and Configuration`, `Author Apex`,
`Manage Flow`, `Manage Profiles and Permission Sets`, `Manage Custom Permissions`, `View Roles and
Role Hierarchy`.

#### 1.3 Compare — the screen that replaces "diff two orgs by hand"

`Metadata deployments` → `Compare and deploy`.

1. `Choose comparison source location` — Salesforce organization, Git branch/repository, local
   files, or a Salesforce DX scratch org.
2. `Choose comparison target location` — Org-to-Org, Git-to-Org, Org-to-Git, Git-to-Git.
3. `COMPARISON FILTER` — built-in filters include `Default comparison`, `Basic comparison`,
   `All metadata`, `On-demand comparison`.
4. `Compare now`.

**Results tabs:** `All items`, `New`, `Changed`, `Deleted`; selected items move into
`Selected items`.

**Columns:** `Name`, `Metadata type`, `Changed on`, `Changed by`, `Difference type`
(`New`, `Changed`, `Deleted`, `No difference`).

**Filters:** search; metadata type; changed-on date; changed-by user; difference type; and a
`Compared types` tree on the left.

**`Components`** is an expandable dependency-tree group inside a result — it shows the
sub-components and dependencies of a component (e.g. the fields under a custom object).

#### 1.4 Deploy — the exact flow

`Compare and deploy` → tick the items → **`Next`** → Gearset runs **problem/dependency analysis**
and may propose package changes → **`Pre-deployment summary`** (source, target, change types, Apex
test level) → choose:

- **`Validate deployment`** — validates without deploying (the `checkOnly` equivalent).
- **`Deploy now`** — uploads the package and deploys.

**Apex test level** (in the pre-deployment summary and in CI job setup):
`No tests` · `Run specified tests` · `Run all local tests` · `Run all tests including managed
packages`.

`Deploy to target` is an action in **`Deployment history`** for a successful package — it is not
the button on the comparison summary.

#### 1.5 Deployment history, reports, rollback

`Metadata deployments` → `Deployment history`:

- filter by date / source / target; search
- `View details`, `View errors`, PDF report, package download, CSV deployment details
- **`Roll back`** — choose metadata to reverse. Gearset creates a **new rollback deployment**; it
  does not erase history. Metadata rollback needs Teams or Enterprise.
- `Clone package` — re-deploy the same package to another target.
- `Deploy to target` — promote a validated/successful package onward.

#### 1.6 CI jobs

`Continuous delivery` → `CI jobs` → `Add new deployment job…` (or a **Validation-only CI Job**).

| Control | Meaning |
|---|---|
| `Metadata filter` | Which metadata types are compared and deployed |
| Apex `Test level` | The five levels (see `02-limits-and-constraints.md` §5) |
| `Deploy deleted items` | Include deletions in the package |
| `Deploy permissions` | Excluded by default; turn on deliberately |
| `Delta CI` vs full sync | Delta runs an empty baseline first, then deploys only newer changes |
| `Validate pull requests against the source branch` | Creates a validation for PRs opened against the source branch |
| Static code-analysis ruleset | Violations can fail the validation |
| Problem Analyzer templates | Optional automatic fixes to the package |
| Outgoing webhook | Can trigger GitLab, Bitbucket or Azure DevOps after a successful run |

**Triggers:** `when the branch is updated` (recommended) or a `time interval` (e.g. 4-hour,
24-hour schedule). PR validation is enabled separately as above.

**`Deployment steps` and `Deployment steps library`** are the pre-/post-deployment checklist
features; step types are `Manual` and `Automatic`. There is **no verified arbitrary shell-command
"Build step"/"Custom step" UI** in current documentation.

#### 1.7 Pipelines

`Continuous delivery` → `Pipelines`.

- **Expanded branching model:** `+ Add` → `Add static environment` → `Create new` → environment
  name, source branch, target Salesforce org, CI job.
- **Gitflow model:** `Add environment` under `Integration`, `Release & Testing` or `Production`.
  Stage mapping: `Integration → develop`, `Release & Testing → release branch`,
  `Production → main`.
- Actions: `Create pull request`, `Promote changes`, `Commit more changes` (add/remove components
  from an in-flight change).
- **`Continuous Delivery Rules`** (`Edit details` → `Continuous delivery` → `Add rule`): per
  environment, enable/disable **forward promotion** and **back propagation**, with
  branch-protection and skip-test choices. Requires a team-shared pipeline and Automation Platform
  Enterprise.

**End-to-end:** developer commits → opens PR → validation-only CI job validates the PR →
promotion creates a PR / promotion branch → environment branch updated → webhook fires the
deployment CI job → compare → validate → deploy → promotion to the next environment →
back-propagation syncs earlier environments.

#### 1.8 Backups and restore (the "where do I click for backup" answer)

`Backup & archiving` → `Data backup jobs` → `Add new data backup job`.

**Tiers and limits:**

| Tier | Behaviour | Limit |
|---|---|---|
| `Standard` | Daily backups | Up to **2** Standard backup jobs; production and sandbox orgs |
| `High frequency` | Hourly backups | Up to **2** High frequency jobs; **max 10 objects**; licensed orgs only |
| `Big Object` | Higher limits incl. Big Objects | Enterprise licence |
| Team-shared backup connections | — | Backup Teams / Deployment Teams licences |
| `Metadata History` | Metadata snapshots and rollback | Backup Teams and Enterprise |

**What is captured:** metadata (subject to the job's metadata filter) **and** record data for
standard + selected custom objects. Files/attachments are supported through `ContentVersion`,
`ContentDocumentLink` and `Attachment`; some objects cannot be backed up due to Bulk API
restrictions. The **first run establishes the baseline**.

**Running and restoring:**

- `Back up now` on the job page → immediate run. `Job history` lists runs; `View changes` opens the
  changed / deleted / new record browser.
- **Restore records without dependencies:** `Job history` → `View changes` → object →
  `View records` → select IDs → `Restore from previous backup` → restoration plan → `Restore`.
- **Restore with dependencies:** select parent and dependent records; the plan shows dependencies
  before `Restore`.
- **Restore metadata from a snapshot:** `Job history` → snapshot date → `Use snapshot` → under
  `Metadata`, `Restore` → select changed metadata → normal deployment flow.
- **Metadata History rollback:** `Job history` → `Metadata History` → select date →
  `Roll back` → `Start rollback comparison`.

**Retention:** record data retained **7 years by default**; metadata snapshots and comparisons
retained **indefinitely**. Archiving is a separately configured licensed workflow with rules such
as `Archive data after`, `Delete after`, `Do not archive`.

#### 1.9 Data masking and sandbox seeding

- **In-place masking:** `Sandbox seeding` → `Configure and deploy` → `Configure in-place masking` →
  select target org → select objects and fields → `Automatically selected sensitive fields` (the
  default classification — Name, Email, Phone, Address, Description, SSN, Date of Birth and
  similar) → localisation → `Disable automations` and reactivation behaviour → `Mask data` /
  `Deploy data`.
- **Masking during seeding:** in `Configure sandbox seeding`, pick source org and objects, then
  `Configure masking`. Masking templates are reusable across seeding, in-place masking and data
  deployment.
- **Refresh sequence with Gearset in a pipeline:** (1) sync the pipeline environment branch →
  (2) run the Salesforce refresh → (3) re-authenticate the refreshed sandbox connection if needed →
  (4) compare the environment branch to the refreshed sandbox and redeploy in-flight changes →
  (5) apply in-place masking or seed/mask afterwards.

#### 1.10 GitHub integration

- GitHub / GitHub Enterprise: OAuth connection; repository integration via a **GitHub App**.
- GitHub App repository permissions: `Administration` (read), `Commit statuses` (read/write),
  `Contents` (read/write), `Deployments` (read/write), `Metadata` (read), `Pull requests`
  (read/write), plus Webhooks/Workflows access.
- **Required status check:** repository `Settings` → `Branches` → `Branch protection rules` →
  enable `Require status checks to pass before merging` → select the Gearset validation check.
- **Webhooks:** CI-job webhook (pooled URL, can trigger multiple CI jobs) and Pipeline webhook
  (pull-request events and propagation). Manual setup: CI-job page → job menu → `Webhook setup`.

#### 1.11 Other Gearset features worth naming

| Feature | Where | Note |
|---|---|---|
| `Change monitoring` | `Continuous delivery` → `Change monitoring` | Scheduled org scans detect metadata changes; can trigger alerts/webhooks |
| `Express Deploy` | Deployment mode | Open pilot — deploy without a separate pre-validation. Availability varies |
| Code-review enforcement | Pipeline settings | Require reviews, approvals and validation before promotion |
| Problem Analyzer | Deployment flow + CI job | Runs before deployment; may correct the package |

---

### 2. Copado

#### 2.1 Product lines and licences

| Product | Contents |
|---|---|
| **Copado Essentials** — Free | Up to 15 deployments/month, Knowledgebase support |
| **Copado Essentials** — Basic | Unlimited deployments; org comparison and change detection; fast deployments; full metadata support; team roles and collaboration |
| **Copado Essentials** — Essentials Plus | Adds **Release Pipelines & Work Items**, **Version Control & Backup**, **Automation & Continuous Integration** (custom CI jobs to back up, schedule, automate and validate deployments) |
| Enterprise | **Agentia Pipeline Pro** (SFDX CI/CD), **Agentia Pipeline** / Agentia Testing / Agentia AI Context Hub. Legacy docs: *Copado Deployer*, *Salesforce Metadata Pipelines (MFP)*, *Salesforce Source Format Pipelines (SFP)* |

**Licence types (Glossary of Terms):** *Copado User*, *Copado Plan* (planning records — user
stories, sprints, epics; Kanban, Sprint Wall, Work Manager), *Copado Branch Management*,
*Copado Compliance Hub*, *Copado Data Deploy*.

#### 2.2 Pipeline Manager

From the **Pipeline** record: `Manage Releases` → `Pipeline Manager` link. From the **App
Launcher**: search `Pipeline Manager` (renamed **MFP Pipeline Manager** in v24.22+).

**Environment status icons:** green check = last deployment succeeded; red cross = failed; pause =
waiting for a manual action; in-progress spinner; yellow warning = merge conflict to review.

**Drill-downs:** status icon → **Deployment Activity** (date, status, % completed/deployed, source
org, back-promotion flag; a paused deployment offers `Review Merge Conflict`). Right arrow →
**User Stories Ahead** (`Promote`, `Promote & Deploy`, `Validate Selections`). Left arrow →
**User Stories Behind** (`Back Promote`, `Back Promote & Deploy`, `Validate Selections`).

**Configure Pipeline:** `Pipeline Manager` → `Configure Pipeline`; per environment a **shield** icon
edits connection behaviour and a **+** adds a connection. Connection icons: infinity = automated,
clock = scheduled, hand = manual, arrows = direction. Actions: `Return to Pipeline`, `Variables`,
`View Pipeline Details`.

#### 2.3 Core objects (Glossary, verbatim in intent)

`Pipeline` (unidirectional flow of environments) · `User Story` (container for develop, commit,
promote, deploy) · `Environment` (an org or another cloud instance) · `Promotion` (container that
deploys one or more user stories between environments) · `Release` (groups user stories and tracks
the version after each deployment) · `Feature Branch` (created on user-story commit) ·
`Promotion Branch` (destination + promoted content) · `Credential` (connection between user and
environment) · `Git Snapshot` (org ↔ Git branch) · `Deployment Step` · `Job Template` / `Job Step` /
`Job Execution` · `Connection Behavior` (promotion/back-promotion behaviour, automation and quality
gates).

#### 2.4 Promotion flow

**Route A — one user story:** `User Stories` tab → select → check **`Promote and Deploy`**.

**Route B — bulk:**

1. Flag user stories `Ready to Promote`.
2. `Promotions` tab → `New`.
3. Choose the `Project` or `Release`.
4. Set `Source Environment` — destination environment and credentials auto-fill; a credential marked
   `Default Credential` is used regardless of owner.
5. `Available User Stories` → tick → `Add Selected User Stories`.
6. `Create Deployment` → **Deployment Details** pop-up: **test level**, optional
   **`Validation Only`** (becomes a `Check Only` step), optional `Attach Deployment File` →
   `Submit`.

**Route C — from Pipeline Manager:** right arrow → `User Stories Ahead` → `Promote` /
`Promote & Deploy`.

On submit Copado creates `promotion/{promotion-deployment}` from the destination branch, adds a
`Git Promotion` step and the user-story deployment tasks. On success the promotion branch merges
into the destination branch; a deployment name containing `tag=x.y.z` creates and pushes a tag.

**Limits:** max **8,000 files** per Copado-created commit or promotion; up to **10,000 files** for
manual-step or Git-repository deployments. Only a **Copado Admin** may add user stories to a
promotion targeting **Production**.

#### 2.5 Deployment steps and quality gates

`Deployments` tab → `New Deployment` → record types: **Metadata Deployment**, **Data Deployment**,
**Automation Template**, **Advanced (multi-step)**.

**Step types:** MetaData, Full Profiles, Full Permission Sets, Users, Translations, Data, Bulk
Data, Data Template, Delete MetaData, Custom Settings Deployment, Apex, Git MetaData, Manual Task,
URL Callout, Salesforce Flow, Function, External CI Jobs.

**Execution options:** `Deploy Outstanding` vs `Deploy All`; `Deploy Now` vs `Deploy Later`.

**Quality gates (Connection Behavior → Automations):**

| Gate | Step type | Behaviour |
|---|---|---|
| Apex Tests with Validation | Git Promotion | Runs `Git Promotion` with `Check Only`; you set the test level |
| Validation | Git Promotion | `Check Only`, test level `No Test Run` |
| Compliance Check | URL Callout | Scans metadata committed in the Git Promotion step against a Compliance Rule Group |
| Static Code Analysis | URL Callout | Scans against Static Code Analysis Settings |
| Automation | Automation | Runs a group of steps (External CI, Apex, Salesforce Flow) |
| Test | Test | Runs Copado Robotic Testing records attached to the user stories |
| Manual Approval / Manual Test / Pull Request | Manual Task | Pauses for a person |
| URL Callout | URL Callout | Executes an arbitrary URL callout |

**Connection Behavior fields:** `Promotion Execution` (Manual/Automated/Scheduled), `Promotion
Criteria`, `Execute promotions in parallel`, `Back-Promotion Execution` (Manual/Automated/
Scheduled/**Disabled**), `Back-Promotion Criteria`, `Execute back-promotions in parallel`,
`Scheduled Promotion US Group Size`, `Scheduled Back-Promotion US Group Size`, `User Story Status
After Promotion`, `Disable Environment Branch`. Automations apply to manual and automated
deployments — **not** scheduled promotions.

#### 2.6 Essentials Plus: Work Items and CI Jobs

`Account > Pipelines > Add Pipeline` → per environment: name + Salesforce org (+ optional Git org
and branch). `Work Items > New Work Item` — only **Title** and **Pipeline** are required; `Issue`
links Jira/Azure DevOps. On save you land on **Component Selection**. Actions: compare changes,
add components, share the deployment, comment, request **Approval**, run Robotic Testing, run
Static Code Analysis, `More > Back Promote`, rollback. On successful deployment of a stage the
Work Item **automatically advances**; `More > Go Back to Previous Stage` steps it back. Approvals
require a configured `Required approving reviews` count on the Pipeline and Owner/Team Lead roles.

**CI Jobs (Essentials Plus):** scheduled daily/weekly validations with coverage; scheduled
org → Git metadata backups; webhook-triggered Git-branch-to-org deploys; REST-API-triggered jobs
via **Outgoing Webhooks** (POST Request URL = Webhook URL, Essentials Plus username = Username,
API Token = Password).

#### 2.7 Compliance Hub

Objects: `Compliance Rule` (criteria applied during a scan), `Compliance rule criteria`,
`Compliance Rule Group` (assignable to an environment).

- **Active scan:** `Run Compliance Scan` button on a `Credential`, `User Story` or `Git Snapshot`.
- **Passive scan:** triggered automatically based on the environment's rule group and the
  `Compliance Scan Events` multi-picklist on the `Environment` record (values include `Commits`
  and `Deployments`).
- **Scheduled:** `Scheduled Jobs` → `New` → `Look up Copado Webhook` → `Run Compliance Scan on
  Credential` / `… on Git Snapshot`.
- Results: `Compliance Scan Results` tab of the `User Stories` page; available as a
  `Compliance Check` quality gate.

#### 2.8 Credentials and security

| Credential type | Notes |
|---|---|
| Governance Org Credentials | Required first — the org where Copado is installed |
| Pipeline Environment Credentials | dev/test/prod connections; inherit the authenticating user's permissions |
| Testing Credentials | Copado Explorer (read) and Copado Robotic Testing (dedicated) |

Create: App Launcher → `Credentials` → `New` → name, `Org Type` (e.g. `Custom Domain` for
`https://yourDomain`), `Disable Validation`, `Test Frequency`, `Default Credential`,
`Is Developer Hub Credential`. Authenticate: `Authenticate` → username+password or SSO → `Use
Custom Domain` → domain → `Continue`.

OAuth is used; usernames and passwords are not stored; tokens can be revoked. **Salesforce enforces
a 30-day refresh-token TTL** — an idle Copado credential expires and must be re-authenticated, with
no proactive warning. That is a real operational failure mode for a bank: a pipeline that worked in
March fails in April with an auth error during the change window.

#### 2.9 Validation and test levels

| Level | Behaviour |
|---|---|
| `Default` | Sandbox: no tests. Production: all local tests if the change set contains Apex classes or triggers. No Apex → no tests. |
| `Run Specified Tests` | Comma-separated class names; 75% coverage computed **per class/trigger individually** |
| `Run Local Tests` | All org tests except managed-package tests. Default for production with Apex |
| `Run All Tests in Org` | Includes managed packages |

Also: `Include Unit Test Code Coverage Result`; `Run Static Code Analysis for Selected Apex Classes`
(PMD, Classic and DX source formats). Trigger points: `Validate Changes` on a User Story;
`Validate Selections` on User Stories Ahead/Behind; the `Validation Only` checkbox in Deployment
Details; scheduled runs via CI Jobs.

---

### 3. AutoRABIT

#### 3.1 Product suite

| Product | Role |
|---|---|
| **AutoRABIT ARM** (Automated Release Management) | CI/CD — deployments, version control, pipelines, approvals, governance |
| **AutoRABIT Vault** | Data backup and recovery; **hosts data masking** |
| **AutoRABIT CodeScan** | Static code analysis |
| **AutoRABIT Guard** | Security posture management |
| **AutoRABIT Integral Zone** | MuleSoft API quality/governance |

**Two parallel ARM doc trees:** `/product-guides/arm/` (classic UI) and `/product-guides/arm-1/`
(**ARM New UI**). Several ARM-1 capabilities are feature-flagged — for example
`SCHEDULED_DEPLOYMENTS`. **Always establish which UI generation the customer runs before teaching
screen paths.**

**Licence classes:** `Standard User` (full access, includes Platform Owners/Admins) and
`Platform Integration User` (anything whose commit or action triggers an AutoRABIT job — view-only
permissions, but still consumes a licence; simultaneous Git pushes count individually).

#### 3.2 CI Job (classic ARM)

`Create New > New CI Job` → choose a tile: Deploy from **Version Control**; Build a Package from
**Salesforce**; Build a Package from **Version Control**; Deploy a Package from a **Salesforce Org**;
Deploy from Salesforce with **VC Backup**; Deploy from Version Control to a Salesforce Org; Deploy
from **SFDX Branch** to a Salesforce Org; Install an **Unlocked Package** from VC Branch.

Job screen sections: **Build**, **Deploy**, **Dependency Analyzer**, **Tests**, **Callout URL**,
**Notifications**, **Schedule**, then **Save** → redirected to **CI Job Results**.

**Build section:** VCS (GIT/SVN/TFS) → Repository → Branch → `Build Using` = `Baseline Revision`
or `Time Range`. Options: `Status Check API`, `Vlocity Build` (Pack Update / Pack Retry),
`Pull Request`, `Merge Request`, `Map ALM Project (e.g. Jira)`, `Trigger Build on commit`,
`Process commit revision via hook only`, `Incremental Build`, `Prepare Destructive Changes`,
`Run Static Analysis Report`. Packaging options: `Remove login IP Ranges`, `Remove System and User
Permissions`, `Exclude Metadata Types`.

**Tests section:** `Fetch Test Cases` from **Version Control** | **AccelQ** | **Provar**. VC path:
repository type, repository, branch, `Selenium Maven` or `Selenium Non-Maven`, `Test Case Root
Path`, `Execution Type`. Options: `Run Test even when the Deployment fails`, `Test Browsers`,
Provar path: `Test Cases Root Path` (the `.testproject` file), `Test Cases Execution Path`,
`Stop Deployment if Test cases fail to compile`.

**Schedule section:** `Daily`, `Weekly`, `No schedule`.

**CI Job List:** filters for `Group By`, `Job Name`, `Last Modified Date Range` (Last 7 days default;
14/30 days; 24 hours; `Custom Range`), and advanced filters for `Job Source Type` (Sandbox or
Version Control + repository + branch) and `Destination Org`. Row actions: `Info`, `Clone`, `Edit`
(prompts to abort an in-progress job), `Activate`/`Deactivate`, `Delete`. **A deactivated job** stops
scheduled builds, stops hook processing, clears queues, disables API triggers, and disables
Edit/Clone.

#### 3.3 Deployment

`Deployment` module → `New Deployment`. Fields: source org, destination org, deployment name,
`Deployment From` (10–14 methods, including `Release Label`), `Metadata Type(s)` (Entire Salesforce
Org / **Full Profiles** / **Full Permission Sets**), `Deployment Type` = `Selective Deployment` |
`Full Deployment`.

Optional `Metadata Filter` → `Retrieve Metadata` → tabs `Selected Items`, `Destructive Members` →
`Deploy` or `Compare Metadata & Deploy (recommended)` → `Diff` tab → `Deploy` → `Deployment
Settings` → `Deployment Summary` → **`Validate Deployment`**.

**Deployment Settings and Filters (verbatim from the docs):**

| Filter | Description |
|---|---|
| `Ignore warnings` | Metadata types that trigger warnings during retrieval will not fail the deployment |
| `Validate only` | Validates and saves the deployment label without executing it; usable later for a Quick Deploy |
| `Take backup` | Snapshots original metadata state to allow revert |
| `Ignore missing visibility settings (profiles)` | Keeps only common profile/permission-set settings between orgs |
| `Remove Login IP Ranges` | Removes IP ranges from profiles while deploying |
| `Remove System and User Permissions` | Removes user permissions from profiles while deploying |
| `Do not include 'Destructive members'` | Honours metadata types configured to skip |
| `Ignore installed components` | Excludes managed-package components from metadata.zip |
| `Fetch Wavexmd components` | Selects wavexmd files for the wave dashboard metadata type |

Also on that screen: `Apex Test Level`, `Static Code Analysis` (ApexPMD, Checkmarx, SonarQube,
CodeScan) with `SCA Mail Notifications`, `Search and Substitute` rules, `Fetch the Test Cases`,
`Deployment Notes`.

**Apex test levels:** `No Test Run` · `Run Specified Tests` (comma-separated; 75% per class/trigger)
· `Run Local Tests` (default for production) · `Run All Tests In Org` · `Run Tests Based On
Changes` · `User Salesforce Defaults` · `Run Relevant Tests`.

**CI-Job-only deployment options:** `Validate Only`, `Rollback`, `Ignore Missing Visibility
Settings, If Package Contains Profiles Or PermissionSets`, `Ignore Installed (Managed) components`,
`Ignore warnings`, `Do not include 'Skip members' during Deployment`, `Run Destructive Changes`
(pre/post), `Apply Search and Substitute Rules`, and an `On successful Deployment` group:
`Run Skuid Pages`, `Trigger another CI Job`, `Run Environment Provisioning Template`,
`Run DataLoader Process or Group`, `Run Merge Process` (up to 5 destination branches),
`Trigger Jenkins Job`, `Configure Parallel Processor`, `Set Sequence For Post Activities`.

#### 3.4 Release labels, scheduled deployments, approvals

**Release Labels:** `Version Control > Change Labels > Release Labels` → `Create Release Label`.
Fields: `Label Name`, `Description`, `Repository`, `Branch` (+ `Package Directory` for SFDX repos),
commit, `Label Type` = `Salesforce` | `Vlocity`, `No of Days` (30/60/90/120/180/365/**ALL**),
`Create package manifest for Deployment` → `Fetch Commit History` → select ≥2 revisions → `OK`.

**Release Labels Summary:** `Repository` dropdown; label name / last updated / branch; description;
package status (`Completed` | `Failed` | `Package Not Prepared` | `In-progress` | `Aborted`);
`View Dataset` (`JSON View` / `Tree View`); `Merge`; `Edit`; `Delete`; `Create Artifact` (only
enabled for orange/red labels).

**Scheduled Deployments (ARM New UI only, flag `SCHEDULED_DEPLOYMENTS`):** `Deployment > Create
Deployment` → source/destination/metadata → `Deployment Settings` → `Review & Deploy` → `Schedule`
→ date, time, time zone. The deployment appears in `Deployment History` with status `Scheduled`;
you can `Edit Schedule`, `Cancel Schedule` (leaves it as a draft) or `Deploy Now`.

**Approvals (L1/L2):** deployments pass through `L1 Approval Pending` and `L2 Approval Pending`.
Approvers see basic info, changed metadata, the approver list, comment history and the `SCA Report`
(SCA runs first and auto-rejects on failure). Actions: `Approve` (auto-deploys) or `Reject` with
comments. **Pending approvals auto-reject after 3 days**, **self-approval is impossible even for an
admin**, and deleting the target org auto-rejects pending approvals. Merge approvals live under
`Version Control > Merge Approvals`.

#### 3.5 Data masking (AutoRABIT Vault)

**Masking Rules (org level):** `Masking Rules` → `New Masking Rules` → `Select Orgs` →
`New Masking Rules` → complete the form → `Save` → `OK`. Rules are global to the org and selectable
during config creation; they can be cloned.

**Live Data Masking:** `Live Data Masking` → `JOB CONFIG` → `Salesforce Orgs` → `NEW CONFIG` →
`Object Info` (every selected object needs ≥1 rule) → `Masking Rules` icon → `NEW MASKING RULE` →
`Config Details` → `SAVE` or `SAVE & RUN`. Run from `JOB CONFIG` via the **Play** icon.

**Masking rule fields:** `Org Name`, `Rule Name`, `Select Object`, `Field Type` (date, double,
picklist, textarea, encryptedstring, url), `Masking Style` (e.g. `substitution`, `dateRange`),
`Masking Value`, `Add to Org "<ORG>" Masking Rules List` (global). **Local rules take precedence
over global rules.**

**Config Details:** `Org Name`, `Label`, `Batch Size`, `Email notification`, `Disable Workflows`,
`Disable Validation Rules`, `Disable Triggers`, `Disable Flows`, `Exclude Deleted Records`,
`Enable Serial Mode for Bulk API`.

**Rollback** is available from `JOB CONFIG`; deployed data is retained **7 days** then permanently
deleted. Every rollback appears in `JOB HISTORY` with `Job Type – Rollback`.

#### 3.6 Credentials and audit

`Admin > Credentials` → `Create Credential` (**Org Administrators only**). Types: `Username with
Password`, `SSH`, `HashiCorp Vault`, `SSH Certificate`, `Application Token` (Enterprise only — and
explicitly **not** supported for ARM CI Jobs). Scope: `Global` or `Private`.

Salesforce org registration via **OAuth** — self-hosted/dedicated uses a **Connected App** with
scopes `api`, `full`, `refresh_token/offline_access` and callback `https://<ARM access
URL>/oauth/_callback`; cloud deployments use the **External Client App (ECA)** flow.

**Reports module:** `Weekly Reports` for `EZ Merge`, `EZ Commits`, `Deployment`, `CI Build jobs`,
`Data Loader`. `Audit Report` → select org → from/to → `SEARCH` → `Download` (CSV; timestamps in
GMT). **Job Audit Report** (button on `CI Job Results`) downloads a **PDF** with a build list
(build number, timestamp, commit comments, author and approver) and per-build detail (commit IDs,
summaries, reviewer details, review dates, ALM IDs, differential revision details); filterable up
to **120 days**. CI job build reports are unavailable after **30 days**; SCA source content is
retained **90 days**.

**Deployment History** fields: `Deployment Label`, `Destination Sandbox`, `Last Created Date
Range`, `Last Iteration Status`, `Deployment Iterations`, `Async ID`, `Deployment Status`. Deployment
add-ons: `Promotion`, `Redeploy/Promote`, `Rollback`, `Abort`, `View Graph`, `SCA Report`,
`Test Results`, `Deployed Issues`, **`Quick Deploy`** (components validated successfully for the
target environment within the last **96 hours**).

---

### 4. The comparison that matters in an interview

| Question | Gearset | Copado | AutoRABIT |
|---|---|---|---|
| Core unit of work | CI job (Deployment / Validation-only) | User Story / Work Item | CI Job + Release Label |
| Pipeline model | Branch-centric, PR-based | Environment-centric with Connection Behaviours and quality gates | Repository + branch types (Development/Integration/QA/UAT/Production) |
| Where the gate lives | CI job configuration | Connection Behavior → Automations | Deployment Settings + CI Job sections |
| Where backups live | `Backup & archiving` → `Data backup jobs` (licensed) | Essentials Plus CI Jobs (metadata backup to Git) | Vault (data backup + masking) |
| Data masking | In-place masking / Sandbox Seeding | **No Copado product** (Data Deploy is different) | Vault → Live Data Masking |
| Rollback | `Deployment history` → `Roll back` | Deployment `Rollback` action | Deployment `Rollback` action; Vault rollback (7-day window) |
| Strongest asset | Backup + sandbox seeding + data | Compliance and governance | Data masking depth and release labelling |

**The answer to give:** *"I have used X in production; Y is what I would reach for if the bank's
control requirements were heavier. Underneath all three is the Metadata API and the CLI, and I do
not let a vendor UI become the only way I can deploy."* That last clause is the one that
distinguishes a release engineer from a tool operator.

---

### 5. Unverified / uncertain

| # | Item | Status |
|---|---|---|
| 1 | Exact OAuth scope strings for Gearset's Connected Apps | Not enumerated in current text docs — do not quote |
| 2 | A formal Gearset "Environment mapping" screen | Not found. Closest is Pipeline environment / static-environment configuration |
| 3 | A stable global Gearset top-level tab bar | The UI is a grouped sidebar; labels vary by rollout and licence tier |
| 4 | Arbitrary shell-command "Build step"/"Custom step" in Gearset | Not verified. Verified terms are `Deployment steps` and `Deployment steps library` |
| 5 | A Gearset "Reset sandbox" button | Not found — native refresh is a Salesforce operation |
| 6 | "Copado Fundamentals" / "Copado DevOps Center" tiers | Not found in current docs, pricing or product nav |
| 7 | "Copado Data Masking" | Not found; only Data Deploy / Data Sets / Data Templates |
| 8 | Copado "Deploy only if…" / "Freeze windows" labels | Not found; verified equivalents are Connection Behavior quality gates |
| 9 | Copado Work Item types (Feature/Bug/Task) and a "Blocked" status | Not found — only Title, Pipeline, Issue, Description, Start from are documented |
| 10 | A dedicated Copado "Releases" tab | The `Release` object is confirmed; a tab by that name was not located |
| 11 | Keypair authentication for Salesforce orgs in Copado | Not found — orgs authenticate via OAuth; SSH key pairs are documented for **Git** connections only |
| 12 | "AutoRABIT Test Repository" | Verified absent from the knowledge base index |
| 13 | "AutoRABIT DevOps" as a product name | Current name is AutoRABIT ARM |
| 14 | AutoRABIT "Max Batch Size" deployment option | Not found — `Batch Size` exists only in Vault → Live Data Masking → Config Details |
| 15 | AutoRABIT "Stages / Steps / Components" as classic ARM vocabulary | Classic ARM uses Build / Deploy / Dependency Analyzer / Tests / Callout URL / Notifications / Schedule. "Stage" appears only in ARM New UI Pipelines → Releases |
| 16 | Whether Copado Essentials pricing still matches the published matrix | Read from copado.com on 2026-11-14; re-check before quoting |


## Part V — GitHub Actions + Salesforce CI/CD

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/04-github-actions-salesforce-cicd.md`*


> JD lines covered: R1 (design/implement/maintain CI/CD pipelines), R3 (scheduled/hotfix/emergency
> coordination), R4 (audit/security/compliance), Q4 (GitHub Actions, Azure DevOps, GitLab),
> Q6 (automated testing and validation).
>
> Every CLI flag below was read from the **Salesforce CLI plugin source**, not from memory — see
> `sources.md` §3. Where a flag does not exist, the doc says so.
---


### 1. Pipeline architecture

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

### 2. Authentication

#### 2.1 JWT bearer flow — the correct model for CI

**Why JWT and not a password or an auth URL:**

| Option | Verdict |
|---|---|
| Username + password | Never. Password policies, lockout policies, MFA, and the credentials live in the repo |
| `sf org login sfdx-url` with a stored refresh token | Legacy. The refresh token is a long-lived bearer secret; if the secret store leaks, the org is compromised until the token is revoked. Acceptable only if your security team signs off explicitly |
| **JWT bearer flow with a certificate** | **Recommended.** No password, no long-lived token, no human identity. The private key is the only secret |

#### 2.2 The exact command

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

#### 2.3 The Salesforce-side setup

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

#### 2.4 Secret storage

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

#### 2.5 OIDC — the honest answer

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

### 3. Repository layout

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

### 4. The workflows

#### 4.1 PR validation — dry run + tests

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

#### 4.2 Reusable deploy workflow

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

#### 4.3 Non-prod deployment (QA / UAT)

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

#### 4.4 Production — validate then quick deploy

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

#### 4.5 Composite action (optional but tidy)

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

### 5. GitHub repository configuration (the part that is not YAML)

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

### 6. Artefacts and the audit trail

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

### 7. Mapping the same pipeline to Azure DevOps and GitLab

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

#### 7.1 Which one for a bank

| Criterion | GitHub Actions | Azure DevOps | GitLab |
|---|---|---|---|
| Already in Azure AD / Entra ID governance | Weak — identities live outside | **Strong** — native Entra integration | Weak |
| Change-management integrations (ServiceNow, Jira, ADO boards) | Via API/webhooks | Native connectors | Via API/webhooks |
| Self-hosting of runners inside the bank network | Possible (self-hosted runners) | Possible (self-hosted pools) | Possible |
| Approval UX | Environments | Approvals / deployment protection | Protected environments |
| **Fit for a bank already on Azure** | Fine | **Best** | Fine |

---

### 8. Anti-patterns

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

### 9. The complete checklist for "is this pipeline production-grade?"

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

### 10. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| The exact JSON key for the deployment job id in `sf project deploy validate --json` | Not pinned here — the CLI's JSON shape is not documented as a stable contract | Run `sf project deploy validate --json` once in a sandbox and read the output; prefer `--job-id` passed explicitly if the CLI prints the id on stdout |
| Whether the current Salesforce CLI supports a GitHub Actions OIDC exchange for org auth | **No such flow is documented.** Treat as unavailable | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/> |
| `sfdx-actions/setup-sfdx` as the setup action | Repository last pushed **2022-12-15**; still uses the `sfdx` CLI and `sfdx-auth-url` | Installing the CLI with `npm install -g @salesforce/cli@<pinned>` directly is the current approach |
| The `@salesforce/cli` version pinned in the examples | Pin to a version you have tested; the examples use `2.58.0` as a placeholder | <https://www.npmjs.com/package/@salesforce/cli> |
| GitHub artefact retention maximum | Set per repository/organisation; the exact cap varies | `Settings > Artifacts` |


## Part VI — Term-by-term deep dive of every JD phrase

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/05-jd-term-deep-dive.md`*


> Every JD phrase, with the **settings**, **variations**, **failure modes** and a one-line
> "say it like this" answer behind it. Numbers and platform behaviour come from `02`; vendor UI
> paths from `03`; pipeline mechanics from `04`.
---


### 1. "Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows"

**What it actually means:** a pipeline that moves *metadata*, not code, from a branch to an org,
and stops when the metadata is wrong. The pipeline is the enforcement point for every other
control in this job.

#### 1.1 The four knobs every Salesforce pipeline has

| Knob | Options | Where it lives |
|---|---|---|
| **Trigger** | PR open/update, push to branch, schedule, manual, pipeline event | GitHub Actions `on:` / Gearset CI-job trigger / Copado CI Job schedule / AutoRABIT Schedule section |
| **Payload** | source dir, manifest, metadata types, package directory | `--source-dir`, `--manifest`, `--metadata`, package.xml |
| **Test level** | `NoTestRun` / `RunSpecifiedTests` / `RunLocalTests` / `RunAllTestsInOrg` / `RunRelevantTests` | `--test-level` (+ `--tests`) |
| **Target** | org alias, target URL, environment | `--target-org`, GitHub `environment:` |

#### 1.2 What "maintain" means (the part people forget)

A pipeline is a **product with a support burden**:

- **Version pinning.** Pin the Salesforce CLI version (`npm i -g @salesforce/cli@2.x.x`) so a CLI
  release does not change your deploy behaviour overnight. Record the pin in the repo, not in a
  wiki.
- **API version pinning.** The `sfdx-project.json` `sourceApiVersion` and `package.xml` `version`
  control which API semantics apply. Behaviour changed at API 33.0/34.0 (destructive change
  ordering, test-triggering metadata types) and at 65.0 (deploy cancellation in `Finalizing
  Deploy`).
- **Secret rotation.** Connected-app certificates and client secrets expire. Salesforce refresh
  tokens expire after 30 days of inactivity — Copado documents this as a credential that
  "expires with no proactive warning".
- **Runner hygiene.** Cache `~/.sfdx` and `~/.sf` deliberately; a poisoned cache is a supply-chain
  problem.
- **Failure triage.** The pipeline must publish the **deployment id** as an artifact. Without it,
  the audit trail starts at "the pipeline went green".

#### 1.3 The pipeline that will actually pass a bank's architecture review

| Control | Implementation |
|---|---|
| No direct push to `main` | Branch protection, required PR, required status checks |
| Segregation of duties | The pipeline identity deploys; a **named human in a different identity** approves the `prod` environment |
| No credentials in the repo | JWT cert + secrets in the CI secret store; secrets scoped per environment |
| Immutable evidence | Deployment id, test run id, coverage %, commit SHA and tag written to the change ticket |
| Reversibility | Annotated tag on every prod deploy; rollback = forward deploy of the previous tag |
| Restricted network | Org-side deployment IP allowlist for prod |

#### 1.4 Say it like this

> "The pipeline is the only path into a non-dev org. Git is the source of truth, the org is a
> target, and the pipeline — not a person with Setup access — is what promotes. Every prod
> deployment carries a ticket, a validation id, a prod id, a test run, a coverage number, an
> approver who is not the author, and a tag."

---

### 2. "Manage multi environment release strategies (Dev, QA, UAT, Pre Prod, Prod)"

#### 2.1 The stage table with the one fact that matters per stage

| Stage | Purpose | Org type | The fact that matters |
|---|---|---|---|
| Dev | Build + unit test | Developer / Developer Pro / scratch | Scratch orgs are **not** sandboxes: no managed packages, SSO, named credentials or production licences unless recreated |
| QA | Automated validation, integration | Developer Pro / Partial Copy | CI burns **API allocation** here — schedule it, don't run it on every PR |
| UAT | Business testers | Partial Copy or masked Full | Testers need *some* rows; a Partial Copy from a template is cheaper and safer than a Full |
| Pre-Prod | Dress rehearsal | Full or recent Partial | The only stage where **volume and performance** are meaningful |
| Prod | Customers | Production | Only one deploy runs at a time; queue order is **not** submission order |

#### 2.2 Promotion strategies (the "variations")

| Strategy | How promotion works | Best when | Cost |
|---|---|---|---|
| **Forward-only (waterfall)** | Git is the only promotion path: deploy the same commit to each stage | Small team, strict audit | Slow; hotfixes need a separate path |
| **Forward + back-propagation** | After a prod change, the change is pushed back to earlier stages | Salesforce metadata genuinely diverges between stages | Two-way merge risk; needs a conflict policy |
| **Environment branching (release branches)** | Each stage has a branch; promotion = merge | Complex config, many parallel stories | Merge conflicts are constant |
| **Package promotion** | The same 2GP/unlocked package version is installed at each stage | You have already adopted packaging | Requires a package boundary and version discipline |
| **Delta / change detection** | Deploy only what differs from the target (Gearset Delta CI, CLI source tracking) | Large orgs, frequent deploys | Requires a trustworthy baseline |
| **Rebuild-from-source** | Each stage is rebuilt from `main` + release notes | Cleanest audit story | Slowest; loses stage-specific customisations |

> **The honest answer for a bank:** they will run **forward-only with a release branch**, plus
> **back-propagation only for genuine emergencies**, because bidirectional promotion in a regulated
> org creates an audit question ("which change is in prod now?") that is expensive to answer.

#### 2.3 Gate design per stage

| Gate | Implementation | Evidence produced |
|---|---|---|
| PR → Dev | Required status check: validation deploy + tests | CI run id, test result |
| Dev → QA | Merge to the release branch triggers a real deploy | Deployment id |
| QA → UAT | QA sign-off recorded against the release branch commit | Sign-off + deployment id |
| UAT → Pre-Prod | Full validation in Pre-Prod; performance/smoke | Validation id |
| Pre-Prod → Prod | `checkOnly` validation, then quick deploy or full deploy in the window | Validation id + prod id |

#### 2.4 Say it like this

> "Five stages, one promotion path, one direction of truth. The release branch is what QA and UAT
> deploy; developers never deploy their feature branch into UAT. Promotion is a deploy of the same
> commit, never a rebuild from someone's laptop."

---

### 3. "Coordinate scheduled releases, hotfixes, and emergency deployments"

#### 3.1 Three speeds, three branch topologies

| Speed | Trigger | Cut from | Merge back to | Approval |
|---|---|---|---|---|
| **Scheduled release** | Release calendar | `main` → `release/<date>` | `main` on close | Full: ticket + window + named approver |
| **Hotfix** | Production defect, next release too late | `main` → `hotfix/<ticket>` | `main` **and** every open release branch | Full, but smaller payload and shorter window |
| **Emergency** | Active customer or regulatory harm | `main` → `hotfix/<ticket>` | `main` + open release branches | **Shortened chain, same pipeline.** Emergency is a shorter approval path, not a skipped one. |

> **The rule that prevents the classic incident:** a hotfix cut from `main` and merged only back to
> `main` will be **resurrected** by the next release branch, which was cut before the fix. Merge
> the hotfix into every open release branch, or the bug comes back.

#### 3.2 Scheduled releases: the mechanics

- **Frequency.** Common bank pattern: one release train every 2–4 weeks, plus a weekly low-risk
  train for configuration-only changes.
- **Freeze.** A code/config freeze before the release branch is cut. Freeze mechanics belong in
  the branch-protection rules (no merges to `main` after freeze) and in the calendar, not in
  discipline.
- **Change ticket completeness.** The ticket must be in the release **before** the branch is cut.
  A ticket added after the cut either rides the train late (breaking the test matrix) or waits for
  the next one.
- **Payload assembly.** The release payload is the **diff between the last prod tag and the release
  branch tip**, not "whatever each developer merged". A diff-based payload makes the release
  auditable and makes the rollback payload computable.

#### 3.3 Hotfix: the runbook, in order

1. Announce in the change channel with the ticket id.
2. `git switch -c hotfix/<ticket> main`
3. Reproduce, fix, **test in a sandbox** (not in prod).
4. Open a PR into `main` with the ticket id in the commit message.
5. CI validates (dry-run + tests) against a CI sandbox.
6. Validate against prod (`checkOnly`) — the prod validation, not the sandbox one.
7. Obtain approval from the named approver (not the author).
8. Deploy in the window; capture the prod deployment id.
9. **Tag** `release-<date>-<ticket>`.
10. Merge the hotfix branch into `main` and every open release branch. **Do not skip this.**
11. Update the ticket with both deployment ids, the tag, the test run and the approver.
12. Verify with one query and one screen (define both in the ticket before you deploy).

#### 3.4 Emergency: what makes it different

| Dimension | Normal | Emergency |
|---|---|---|
| Branch | `hotfix/<ticket>` | Same |
| Pipeline | Full | Same |
| Approval | Named approver + window | **Pre-named on-call approver**, shorter SLA |
| Validation | `checkOnly` then deploy | `checkOnly` then deploy — **never skip validation** |
| Rollback | Tag + forward redeploy | Same, rehearsed |
| Documentation | Full evidence pack | Same — an emergency is audited **harder**, not less |

**The mistake:** treating "emergency" as licence to deploy from a laptop with a personal token.
Every emergency deploy that bypasses the pipeline creates the next emergency.

#### 3.5 Say it like this

> "Three speeds, one pipeline. Emergency changes to who approves and how fast — not to what gets
> validated. A hotfix is cut from main and merged back into main **and every open release branch**,
> because otherwise the next release resurrects the bug."

---

### 4. "Ensure deployment activities follow audit, security, and compliance standards"

#### 4.1 The evidence pack (what an auditor asks for)

| Item | Produced by | Where it lives |
|---|---|---|
| Change ticket id | Human | Commit message, PR title, branch name, tag annotation |
| Diff reviewed by a second person | PR review | PR record |
| Validation deployment id | `checkOnly` deploy | CI artifact + ticket |
| Production deployment id | Real deploy | CI artifact + ticket |
| Test run id + coverage % | `sf apex run test` / deploy | CI artifact |
| Named approver ≠ author | Environment protection rule | GitHub deployment record |
| Release tag | `git tag -a` annotated | Git |
| Approver identity | Human, different identity | Change record |
| Mask-complete confirmation (Full sandbox refresh) | Masking run | Refresh ticket |
| Logged-in-user list for a refreshed sandbox | Access list | Refresh ticket |

#### 4.2 Segregation of duties — make it structural

| Role | Identity | Can do | Cannot do |
|---|---|---|---|
| Author | Developer | Commit, open PR | Approve own change; deploy to prod |
| Reviewer | Second developer/admin | Approve PR | — |
| Release engineer | Pipeline service account | Deploy on approval | Approve own deployment |
| Approver | Named human, GitHub environment reviewer | Approve prod environment | Write the code |
| Platform owner | Salesforce admin | Manage org config | Approve changes they authored |

**Technical enforcement:**
- The GitHub **Environment** for `prod` has required reviewers → the approving identity is
  recorded by the platform, not claimed in a ticket.
- The Salesforce integration user **cannot** be a human's personal credential. It is a named
  integration user with a dedicated permission set.
- Branch protection requires the PR review and the CI check.

#### 4.3 Compliance controls that are org settings, not good intentions

See `07-system-properties-setup-paths.md` for the Setup paths. The ones that matter most:

| Setting | Why it matters for compliance |
|---|---|
| Deployment IP allowlist (prod) | Only the CI runner can deploy |
| API Usage Notifications | Early warning of runaway automation |
| Session timeout / IP relax | Limits for a stolen session |
| Password policies, lockout policy | Credential brute-force control |
| Audit trail retention | Determines how far back you can prove something |
| Debug log retention | Debug logs contain field values — a data-leak surface, not just a troubleshooting tool |
| Org-wide "Allow Users to View All Data" | Test and integration users should not see all data |
| API Enabled per profile | Least privilege for the integration user |

#### 4.4 Say it like this

> "I make segregation of duties structural rather than cultural: the pipeline identity deploys, a
> named human in a different identity approves, and the platform records both. Every prod deploy
> leaves a ticket, two deployment ids, a test run, a coverage number and a tag — and that pack is
> what I hand the auditor."

---

### 5. "Manage Salesforce metadata lifecycle using source control (Git)"

#### 5.1 The lifecycle, step by step

| Step | Command / action | Artefact |
|---|---|---|
| 1. Retrieve | `sf project retrieve start --metadata <Type:Name> --target-org <org> --output-dir <dir>` | XML in the working tree |
| 2. Review | `git diff` | Reviewable diff — **the whole point** |
| 3. Commit | `git commit -m "<TICKET> <description>"` | Traceable commit |
| 4. Validate | `sf project deploy start --dry-run --target-org <ci>` or `sf project deploy validate` | Validation deployment id |
| 5. Deploy | `sf project deploy start --target-org <target>` | Deployment id |
| 6. Tag | `git tag -a release-<date> -m "<ticket>"` | Rollback target |
| 7. Roll back | `git checkout <previous-tag>` then forward-deploy | New deployment id |

#### 5.2 What to commit and what never to commit

| Commit | Never commit |
|---|---|
| Custom objects, fields, validation rules | `.sfdx/`, `.sf/`, auth files |
| Flows, Apex, LWC, Aura, Visualforce | OAuth refresh tokens, JWT private keys, client secrets |
| Permission sets, permission set groups | Certificates, keystores |
| Custom metadata **definitions** (not secret **values**) | Sandbox-only endpoints hardcoded in code |
| Named credential **metadata** (not the secret) | Retrieved junk: profile user lists, full `*.profile` dumps |
| `package.xml` / `sfdx-project.json` | Production data, CSV exports, debug logs |

**Named Credentials are the pattern:** the *metadata* (endpoint, auth scheme) lives in Git; the
*secret* lives in the org's External Credentials / Secret Store. That is what makes the same
package deployable to five environments.

#### 5.3 Source tracking — what it does and when it helps

| Concept | Behaviour |
|---|---|
| Source tracking | Salesforce records which components came from which local files, so `sf project deploy start` can deploy **only what changed** |
| Where it is enabled by default | Scratch orgs and sandboxes. **Production orgs never allow source tracking.** |
| How to disable it | `sf org create scratch --no-track-source` / `sf org create sandbox --no-track-source` |
| What it buys you | Fast incremental deploys in dev; a "who edited this in the org" signal |
| What it costs you | In dev, a change made **in the org UI** silently exists only in the org until someone retrieves it. That is how "works in sandbox, vanishes in Git" happens. |

**Policy:** in dev and QA, either disable source tracking or run a scheduled "retrieve and diff"
job that reports org-side drift. In prod, source tracking is off, so **the only** way a prod
config change happens is a deploy — enforce that with a permission set, not a policy document.

#### 5.4 Branching topology (detailed)

```
main                    ← tag: matches production
├─ hotfix/<ticket>      ← cut from main; merges to main + every open release branch
└─ release/<date>       ← cut from main at freeze
   └─ feature/<ticket>  ← cut from release/<date>; short-lived
```

Rules:
- Feature branches live **days**, not weeks. Salesforce XML (Flows, profiles, layouts) does not
  merge; a long-lived branch becomes "keep one side and hope".
- The **release branch** is what QA and UAT deploy.
- Tag production after a successful deploy.
- Commit messages carry the change-ticket id. That is the audit trail.

**GitHub branch protection that makes this real:**

| Setting | Value |
|---|---|
| `Require a pull request before merging` | On; require review; dismiss stale reviews |
| `Require status checks to pass` | The validation check; require branches up to date |
| `Require conversation resolution` | On |
| `Require signed commits` | If the bank's policy demands it |
| `Do not allow bypassing the above settings` | On — this is the one that stops the "admin pushes straight to main" pattern |
| `Restrict who can push` | Release engineers only |

#### 5.5 Say it like this

> "Git is the source of truth; the org is a deploy target. If Setup and Git disagree, that is an
> incident, not a workflow. I retrieve, review the diff, commit with the ticket id, validate, deploy,
> tag. Production never allows source tracking, so in prod the only path in is a deploy."

---

### 6. "Handle sandbox strategy (creation, refresh, data masking)"

#### 6.1 Sandbox types (the table to memorise)

| Type | Metadata | Data | Use for | Licence constraint |
|---|---|---|---|---|
| **Developer** | Yes | No | Isolated build | Cheapest; smallest storage |
| **Developer Pro** | Yes | No | QA when you do not need rows | More file/storage room |
| **Partial Copy** | Yes | A template sample | UAT with some rows | Refreshes from a template you define |
| **Full** | Yes | **All of production** | Pre-prod, performance, volume | Slowest; **carries customer data** |
| **Scratch org** (not a sandbox) | From a definition file | No | Package builds, disposable CI | Needs a Dev Hub; no managed packages/SSO/licences unless recreated |

**The trap:** "UAT is a scratch org". In a commercial-banking org with managed packages, SSO, named
credentials and licences, a scratch org is not a substitute unless someone encoded all of it.

#### 6.2 Refresh constraints

| Constraint | Detail |
|---|---|
| Cadence | Licence-limited; refresh eligibility is visible in `Setup > Sandboxes` |
| Full refresh | Slowest; **do not promise a same-day Full refresh** in an interview |
| Partial refresh | Refreshes from a template, not from prod |
| Refresh destroys customisations | Any direct change made in the sandbox since the last refresh is lost — hence the "Git is the truth, sandbox is disposable" rule |
| In-flight work | Re-sync the environment branch and redeploy after a refresh |

#### 6.3 Data masking — the control, not the feature

| Step | Detail |
|---|---|
| 1 | Refresh the sandbox |
| 2 | **Restrict logins.** Until masking is confirmed, only the people named on the ticket may access it |
| 3 | Mask | Mask the fields that carry customer identity: name, email, phone, address, SSN/SIN, date of birth, account number, description/notes free text |
| 4 | Repoint integrations | Named credentials / endpoints must point at non-prod **before** anyone logs in |
| 5 | Confirm | Record mask-complete, time, who confirmed, and the access list in the refresh ticket |
| 6 | Audit | Treat the masked sandbox as containing production-shaped data — it still has real account structures, real values in unmasked fields, and real attachments |

**Which fields must be masked in a Canadian bank:** government identifiers (SIN), account and
card numbers, customer names, addresses, email, phone, date of birth, account balances,
transaction details, free-text notes and attachments. "Free text" is the one people forget —
`Description` and `Notes` fields are where PII hides.

#### 6.4 Tool support (detail in `03`)

- **Gearset:** `Sandbox seeding` → `Configure and deploy` → `Configure in-place masking`; default
  sensitive-field classification; masking templates reusable across seeding/in-place/data deploy.
- **AutoRABIT:** Vault → `Masking Rules` (global) and `Live Data Masking` (JOB CONFIG → NEW CONFIG
  → Object Info → rules); `Config Details` can disable workflows, validation rules, triggers and
  flows during masking; rollback window 7 days.
- **Salesforce:** Data Mask (App Launcher → Data Mask, after the managed package is installed) — not
  assumed in every org.
- **Copado:** **no masking product** (see `03 §2`). Data Deploy is a different thing.

#### 6.5 Say it like this

> "Sandboxes are disposable and Git is the truth, so a refresh destroys nothing important. A Full
> copy carries production data, so masking is a **gate**, not a chore: logins are restricted to the
> ticket's names until mask-complete is confirmed, endpoints are repointed before anyone connects,
> and the confirmation is in the refresh ticket."

---

### 7. "Resolve deployment conflicts"

#### 7.1 Profiles and Permission Sets

**Why profiles conflict:** `Admin.profile` is a single XML file containing object permissions,
field permissions, layout assignments, record-type visibility, user licence and **the user
assignment list**. Two stories touching it produce a textual conflict, and a bad manual merge can
silently grant or revoke access that nobody reviewed.

**The resolution pattern:**

1. Classify the change: *business access* (→ permission set) vs *profile-only setting* (layout
   assignment, login hours, user assignment) vs *licence*.
2. Business access becomes a **permission set per persona or per feature**, not a profile edit.
3. Where the bank still deploys profiles, deploy a **thin delta** with a tool that supports profile
   decomposition, and require a second reader on the permission diff. Never hand-merge a
   10,000-line profile.
4. Bundle for a job function with a **permission set group**.

**Permission set groups** are the modern answer: one group contains multiple permission sets,
assigned to users like a single object. The release-engineering benefit is that a feature's access
lands as one deployable unit.

**The deploy identity's permissions (also a conflict source):** a permission set granting
`Modify All Data` to the integration user is itself metadata. It must be deployed like everything
else, and reviewed like everything else.

**Failure mode to watch:** a profile deploy that strips a permission because the target's profile
had drifted (someone edited it in the UI). The diff that shows it is the artefact you need — that
is why profiles need a second reader.

#### 7.2 Record Types and Page Layouts

**The assignment chain — all of it must be in one payload:**

```
Custom Object
 └─ Record Type
     ├─ Business Process (picklist values it depends on)
     ├─ Picklist values on the status/Type field
     ├─ Page Layout (classic Layout assignment)
     ├─ Lightning Record Page (FlexiPage) for the app
     └─ Visibility: Profile or Permission Set (record type + layout assignment)
```

**Symptoms and causes:**

| Symptom | Cause | Fix |
|---|---|---|
| `Invalid cross reference id` on deploy | Business process or picklist values missing | Deploy the dependencies in the same payload |
| Deploy succeeds, users cannot create the record type | No layout assignment, or no record-type visibility on their profile/permission set | Deploy record type + layout + permission set together |
| Classic layout is right, the screen is wrong | The **Lightning record page** (`FlexiPage`) was never activated for the app | Deploy/activate the `FlexiPage`, and check app assignment |
| Users see the field but cannot edit it | Field-level security is not in the permission set | Add the field permission to the same permission set |
| The layout reverts after the next release | A profile in another release overwrote the layout assignment | Move the assignment to a permission set |

**The rule:** the record type, the layout, the business process and the permission set are **one
deployable unit**. "We deployed the record type on Monday and the permission set later" is exactly
how a release leaves a broken feature in production.

#### 7.3 Flows, Apex, and dependencies

**Flows:**

| Rule | Detail |
|---|---|
| Flow XML does not merge | Two developers editing the same flow will lose one side |
| One owner per flow per release | Or split into subflows and compose |
| Draft vs Active | A deploy can leave the new version **Draft** — users see the old behaviour and the deploy was "successful". Check what your tool does; verify in a sandbox |
| Fast mitigation | Activate the previous version in `Setup > Flows` — a **mitigation**, not a rollback |
| Before-save vs after-save | A before-save requirement built as after-save will time out under volume. A flow you cannot describe is a flow you should not deploy |
| Flow test coverage | The metadata type `Flow` is on the list that **forces all local tests to run** in a deployment |

**Apex:**

| Rule | Detail |
|---|---|
| Class + test + dependencies in one payload | A class calling a class you did not retrieve fails to compile in the target |
| Tests create their own data | `SELECT Id FROM Account LIMIT 1` and assume a row exists → passes in dev, fails in an empty QA sandbox |
| Coverage is per class/trigger | Each needs ≥75% under `RunSpecifiedTests` / `RunRelevantTests` |
| Bulkification is a release concern | A deploy can be green and the feature can still fall over on 200 records. The review question is "what happens when this runs on 200 records?" |
| Deployment ceiling | **7,500 class/trigger code units per deployment** |
| Trigger batch size | 200 (2,000 for platform events and CDC) |
| Recursion depth | 16 levels of trigger-firing recursion |
| 6 MB total Apex code in the org | 10 MB in scratch; raisable via support case |

**Dependency resolution order for a payload:** object → fields → record types → validation rules →
layouts → permission sets → Apex → Flows → approval processes → workflows.

#### 7.4 Say it like this

> "Profiles do not merge and a bad profile merge changes access nobody reviewed, so business access
> ships as permission sets. A record type, its layout, its business process and the permission set
> that grants visibility are one payload. Flow XML does not merge, so one flow owner per release.
> And the two questions I ask in every code review are: does the test create its own data, and
> what happens when this runs on 200 records?"

---

### 8. "Recommend best practices to reduce deployment failures and rework"

| Practice | Failure it prevents | How to enforce |
|---|---|---|
| One payload per release unit | Partial deployments that "succeed" but leave an unusable feature | Manifest/package per unit; CI validates the same payload |
| Thin profiles | Merge conflicts and unreviewed access changes | Permission sets; profile decomposition tool |
| Small permission sets | The same conflict in a different file | One permission set per persona/feature, not one `CB_Admin` |
| One flow owner per release | Lost XML | Release branch has a flow ownership register |
| Tests create their own data | Green in dev, red in UAT | CI runs against an empty sandbox at least once |
| No hardcoded IDs | Environment-specific bugs | Custom Metadata / Custom Settings |
| Named Credentials for callouts | Wrong endpoint in prod | Secret Store + per-org credentials |
| Config toggles in Custom Metadata | Redeploy to turn a feature on | Ship dark, enable after deploy |
| Bulkified Apex | Runtime failure after a green deploy | Code review + static analysis |
| One deployment at a time | Queue-order surprises | Serialise prod promotions |
| Validate before the window | Window overruns | `checkOnly` earlier in the day/week |
| Tag every prod deploy | No rollback target | `git tag -a` in the release job |
| Minimal payload | Deploy time and blast radius | Diff-based payloads, `--metadata` filters |

**The meta-practice:** *reduce the number of files two stories touch.* Every conflict is a file two
people edited. A monorepo of Salesforce XML will always conflict; the fix is structure, not
discipline.

---

### 9. "Partner with Salesforce Developers, Admins, QA, and Platform teams"

| Partner | What they need from you | What you need from them |
|---|---|---|
| **Developers** | A pipeline that fails fast with a readable error; a stable branch model; permission sets instead of profile asks | Tests that create their own data; no admin config inside a story |
| **Admins** | Permission sets they can assign; config-as-metadata; a change calendar | Admin changes captured in Git, not made directly in prod |
| **QA** | A deployment to test that they can identify by commit SHA; a known-good baseline | A test plan tied to the release; defect triage that names the component |
| **Platform teams** | A pipeline that respects network restrictions and API budgets | IP allowlists, runner network access, secret rotation |
| **Security / compliance** | Evidence packs; least-privilege deploy identities; no prod data outside prod | A named approver who is available in the window |

**The handoff artefact that matters:** a **release note per deploy** that a QA lead can act on
without reading the diff — ticket id, component list, feature flags flipped, what to test, what
changed for users, what to revert if it breaks.

---

### 10. "Provide guidance on DevOps friendly Salesforce design patterns"

| Pattern | Deployability consequence | Review rule |
|---|---|---|
| Permission sets over profile edits | Profiles do not merge | Reject a story whose only change is an `Admin.profile` field permission |
| One flow owner per release; subflows for parallel work | Flow XML does not merge | No two stories in the same flow |
| Tests create their own data | Empty and prod-like sandboxes behave the same | No `SELECT ... LIMIT 1` + assume |
| No hardcoded IDs | IDs differ per org | Custom Metadata / Custom Settings |
| Named Credentials for callouts | Endpoints differ per sandbox | No endpoint literals in code |
| Custom Metadata / Custom Settings for toggles | Ship dark, enable after deploy | A feature is never enabled by a deploy alone |
| Bulkified Apex | A green deploy can still fall over in production | "What happens at 200 records?" |
| No environment-specific branches | `if (org.IsSandbox)` branches never merge | Config in the target, not in the branch |
| Feature flags as Custom Metadata + Apex service | Rollback without a redeploy | Flag defaults false in prod |
| Unlocked packages for real module boundaries | Makes a boundary reviewable and upgradeable | Do not "package the whole org" on day one |
| Protected Custom Metadata | Prevents accidental deletion of config in an org | Mark config types as protected |

---

### 11. "Document release processes, runbooks, and rollback procedures"

#### 11.1 The runbook fields (expanded from the existing page's template)

| Field | Filled by | Notes |
|---|---|---|
| Change ticket | Requester | Must be in the release before the branch is cut |
| Release tag / source branch / commit SHA | Release engineer | The rollback anchor |
| Payload (package dir or manifest) | Release engineer | The exact artefact that was deployed |
| Validation org + validation deployment id + time | Pipeline | Evidence the payload compiles |
| Tests run and coverage % | Pipeline | Per class, not just overall |
| Prod deployment id + time | Pipeline | |
| Approver (not the author) | Named human | Enforced by the GitHub environment |
| Feature flags / config to flip after deploy | Developer | The post-deploy checklist |
| Sandbox or flags to restore | Release engineer | |
| Rollback tag | Release engineer | Must exist before the deploy starts |
| Rollback owner | Named human | Different from the deployer if possible |
| **Verification** (one query, one screen, one test) | QA | Written **before** the deploy |
| **Data scripts run and their reverse script** | Developer | A Git revert does not undo rows |

#### 11.2 Rollback decision tree

```
Deploy produced a bad state
├── Is the metadata still recoverable from a tag?
│   ├── Yes → forward-deploy the last good tag (a NEW deploy, recorded)
│   └── No  → you have no rollback. This is why tagging is mandatory.
├── Is it a Flow version problem and is the previous version still in the org?
│   └── Activate the previous version (MITIGATION) → then still forward-deploy the tag
├── Is it Apex / config?
│   └── Stop the bleeding (deactivate the automation if safe) → validate → deploy the tag
├── Did a destructive delete already run?
│   └── Metadata can be recreated from Git. RECORDS ON A DELETED OBJECT ARE GONE.
│       Data restore is a separate ticketed path (backup tool), not a Git revert.
└── Did a post-deploy data script run?
    └── Git revert does not undo rows. The script needs its own reviewed reverse script.
```

#### 11.3 Say it like this

> "Rollback is a forward deploy of the last known-good tag, not a magic button. So before a prod
> deploy I verify the tag exists, the payload is recorded, the reverse data script is reviewed, and
> the verification query and screen are written down — because during an incident nobody invents
> them."

---

### 12. "Support audit and change management requirements"

| Requirement | How release engineering satisfies it |
|---|---|
| Traceable change | Ticket id in commit, branch, PR, tag, deployment record |
| Separation of duties | Different identities for author, deployer, approver |
| Reproducibility | The exact payload artefact + commit SHA + API version stored |
| Evidence of validation | Validation deployment id, test run id, coverage |
| Change control | Named approver, window, calendar, freeze rules |
| Emergency procedure | A written, rehearsed path — not improvisation |
| Retention | Org audit trail retention; Git repository retention; backup retention (7 years for records in Gearset, indefinite for metadata snapshots) |
| No data leakage | No prod data in tickets, slides, debug logs, or unmasked sandboxes |
| Periodic access review | The deploy identity's permissions reviewed on a cadence |
| Evidence that the change was tested | Test results tied to the deployed commit |

**What the release engineer supplies to the change-management system:** the ticket, the plan, the
impact assessment (which orgs, which components, which users), the rollback plan, the test
evidence, and the post-implementation verification.

---

### 13. "Experience with Unlocked Packages / Managed Packages"

| Kind | Who owns it | Deploy mechanism | Release-engineering notes |
|---|---|---|---|
| **Unlocked package** | Your team | `sf package version create` → `sf package install` | Versioned, upgradeable, has a dependency list. Best when a boundary is real (a credit-application module), not "all of Sales Cloud". **10,000-file ceiling** |
| **Org-dependent unlocked package** | Your team, but coupled to unpackaged metadata in the org | Same | Faster to adopt, harder to install elsewhere. Say the limitation out loud |
| **2GP managed package** | ISV or a hard IP boundary | `sf package install` with a `04t` version id | You **upgrade** it; you do not edit its Apex in Git |
| **1GP managed package** | Legacy ISV | Same | 35,000-file ceiling, only if AppExchange Security Review passed |

**The commands:**

```
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

The `04t` id is the package version. Promote that version before production. **Never install a beta
package version into prod.**

**Certified managed package namespaces get their own governor limits** (plus a cumulative
cross-namespace ceiling of 1,100 SOQL / 1,650 DML). An unlocked package does **not** — its usage
counts against the org's limits. That is a capacity-planning fact, not trivia.

**Practical position:** unpackaged metadata deployed from Git is still the right default for a large
existing commercial-banking org. Packaging is how you stop the folder becoming one unreviewable
tree. "Package the entire org on day one" is not a plan.

---

### 14. "Exposure to Salesforce DX"

| DX concept | What it gives you | Release-engineering use |
|---|---|---|
| `sfdx-project.json` | Package directories, source API version, namespace | The project's contract |
| `package.xml` (manifest) | Explicit component list | The deployable unit; makes the payload reviewable |
| `sfdx-project` / `force-app` layout | Metadata in source format | What every deploy tool expects |
| Source tracking | Org ↔ file provenance | Incremental deploys in dev; **off in prod** |
| Scratch orgs | Disposable org from a definition file | CI test target; package builds |
| `sf org login jwt` | Non-interactive auth with a certificate | The CI auth model |
| `sf project deploy preview` | Shows what *would* be deployed and deleted, plus conflicts | Pre-deploy diff without a deploy |
| `sf project deploy validate` | Validation-only deploy | The `checkOnly` equivalent as a first-class command |
| `sf project deploy quick` | Quick deploy from a validation | The fast path into the window |
| `sf project run` | Source-tracking-aware run | Not used for deploys |

**CLI commands a release engineer should know cold:**

```
sf org login jwt --client-id <id> --client-secret <secret> --username <u> --jwt-key <cert> --instance-url <url> --alias <name>
sf project retrieve start --metadata <Type:Name> --target-org <org> --output-dir <dir>
sf project deploy preview --target-org <org>
sf project deploy validate --manifest package.xml --test-level RunLocalTests --target-org <org> --wait 30
sf project deploy start --manifest package.xml --target-org <org> --wait 30
sf project deploy quick --job-id <id> --target-org <org> --wait 30
sf apex run test --test-level RunLocalTests --code-coverage --result-format human --wait 30 --target-org <org>
sf data query --query "SELECT Id FROM Account LIMIT 1" --target-org <org>
```

---

### 15. "Experience in regulated or enterprise environments (banking, insurance, healthcare)"

| Regulatory pressure | Release-engineering consequence |
|---|---|
| Change control | Every deploy traces to an approved ticket; freeze windows; emergency procedure documented |
| Segregation of duties | Structural identities, not policy |
| Data protection | Masking as a gate; no prod data in lower environments; no debug logs in tickets |
| Evidence retention | Git, CI artifacts and org audit trail retained per policy; record backups 7 years where the vendor supports it |
| Least privilege | Deploy identity with a narrow permission set; quarterly review |
| Availability | Deploy off-peak; never deploy during a business-critical batch window |
| Vendor/third-party risk | Managed packages upgraded on a controlled cadence, not opportunistically |
| Reproducibility | Exact payload, API version and CLI version pinned |

**What is different in a bank from a commercial org:** the change window, the named approver, the
masking gate, the evidence pack, and the fact that an emergency still goes through the pipeline.

---

### 16. "Good understanding of Apex & Triggers" / "Salesforce Platform Developer experience"

What the release engineer needs from Apex, even if they do not write it:

| Concept | Release relevance |
|---|---|
| Triggers | Order of execution; before/after; recursion (16 levels); bulkification; trigger batch size 200 |
| Governor limits | The production capacity model — `02 §2` |
| Test coverage | Per class/trigger ≥75%; tests create their own data |
| Deployment | Class + test + dependencies in one payload; 7,500 code-unit ceiling |
| Async | 250,000 async executions/day floor; 5 concurrent batch jobs; 60,000 ms async CPU |
| Managed package Apex | You cannot edit it; you upgrade it |
| LWC / Aura | Bundle metadata; `Customize Application` permission needed to deploy |
| Integration | Named Credentials; callout timeout 10 s; 6 MB/12 MB payload ceiling; 100 callouts per transaction |

**The review questions a release engineer asks** (and should be able to ask out loud):

1. "What happens when this runs on 200 records?"
2. "Does this test create its own data?"
3. "What does this trigger do when it fires recursively?"
4. "Which metadata types does this deployment touch, and do any of them force a full local test run?"
5. "What is the rollback if this behaves differently in production?"

---

### 17. Quick reference — the "say it like this" answers, collected

1. **Where is the source of truth?** Git. Production is a deploy target. If Setup and Git disagree,
   that is an incident, not a workflow.
2. **Walk a change to prod.** Feature branch → PR with ticket id → CI validation → merge to the
   release branch → QA → UAT → `checkOnly` against prod → approval → quick deploy or full deploy →
   tag → ticket updated with both deployment ids.
3. **Hotfix during an open release?** Cut from `main`; merge back to `main` **and** the open
   release branch.
4. **Why did this profile deploy scare you?** Profiles are a grab bag of access; two stories
   conflict; a bad merge changes access nobody reviewed. Prefer permission sets.
5. **Flow deployed but users see the old screen.** The new version is probably not active. Check
   that before redeploying.
6. **Validate vs quick deploy?** Validate changes nothing. Quick deploy applies a validation that
   already passed, inside the window — and is only honest if nothing changed in the target since.
7. **Unlocked vs managed?** Unlocked is yours and versioned. Managed is something you upgrade.
8. **What do you hand an auditor?** Ticket, reviewed diff, approver who is not the author,
   validation id, prod id, test run, coverage, tag — and mask-complete evidence for any Full
   sandbox refresh.
9. **What is the deployment payload ceiling?** ≈39 MB compressed (base64 payload ≤50 MB),
   ≈600 MB uncompressed, 10,000 files for unlocked/2GP packages.
10. **Why does only one deploy run at a time?** Because queued deployments are not guaranteed to
    run in submission order. Serialise prod promotions.
11. **What are the test levels?** Five, not four: `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`,
    `RunAllTestsInOrg`, `RunRelevantTests` (Beta).
12. **Which packages force all local tests to run?** Anything containing Apex, Flow, PermissionSet,
    Profile, CustomField, CustomObject, RecordType, Validation Rule, Workflow, and 20 other types.
    A reports-only package runs zero tests.
13. **Which credential do I give the pipeline?** A named integration user with `API Enabled`,
    `Modify Metadata Through Metadata API Functions` (per-type) or `Modify All Data`, plus
    `Customize Application` for Flow/LWC/custom metadata. Never a human's password.


## Part VII — Certifications named in the posting and their curricula

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/06-certifications-curriculum.md`*


> JD line covered: **"Salesforce certifications (PD1, Advanced Admin, DevOps related certs)"** (Q17).
>
> Credential names and prerequisites read from the official Salesforce credential pages on
> **2026-11-14**. Vendor certification details read from each vendor's own training/academy
> pages.
---


### 1. What the posting is actually asking for

| Posting phrase | Current credential | Prerequisite | Notes |
|---|---|---|---|
| **PD1** | **Salesforce Certified Platform Developer** (exam `Plat-Dev-201`) | — | The posting's "PD1". Trailhead calls it "Platform Developer"; the exam id retains `Plat-Dev-201` |
| **Advanced Admin** | **Salesforce Certified Platform Administrator II** (exam `Plat-Admn-301`) | **Salesforce Certified Platform Administrator** — this is a hard prerequisite, not a recommendation | Salesforce renamed "Advanced Administrator" to "Platform Administrator II". The existing training page says the rename but omits the prerequisite |
| **DevOps related certs** | **No Salesforce-branded DevOps certification exists.** These are vendor credentials | Per vendor | Say the vendor names explicitly; do not imply a Salesforce DevOps cert exists |
| *(implied but unnamed)* | **Salesforce Certified Platform App Builder** | — | Directly relevant: declarative metadata is what a release engineer deploys most often. The existing page mentions it as a study option |

#### 1.1 The naming trap

The posting was written before the renames. In an interview:

- Say "**Platform Administrator II**" (and note it is the credential formerly called Advanced
  Administrator) — not "Advanced Admin".
- Say "**Salesforce Certified Platform Developer**" — not "Developer I" without the "Platform".
- Do **not** say "Salesforce DevOps Engineer certification". It does not exist.

#### 1.2 The prerequisite changes your sequencing

| If you have | You are eligible for | You still need for this role |
|---|---|---|
| Nothing | Platform Administrator → Platform Administrator II → Platform Developer | Vendor DevOps cert, and the hands-on release engineering evidence |
| Platform App Builder | Platform Administrator → Administrator II; Platform Developer | Same |
| Platform Developer only | Platform Administrator → Administrator II (separate track) | Same |
| Administrator II only | Platform Developer (no prerequisite) | Same |

**Practical sequencing for this posting:** Platform App Builder (fastest, covers the declarative
metadata you deploy daily) → Platform Administrator (needed for Administrator II) → Platform
Administrator II → Platform Developer (PD1). Vendor DevOps certification in parallel or after.

---

### 2. Salesforce Certified Platform Developer (PD1) — curriculum

**Purpose:** "Certified Platform Developers understand how to develop and deploy custom business
logic and custom interfaces using the programmatic capabilities of the Lightning Platform."

**How it maps to the JD:** PD1 covers the *content* a release engineer deploys. It does **not** cover
Git, CI/CD, environments, releases, rollback, or audit. Those come from the vendor certs and from
the job itself. A PD1-only candidate is strong on Apex and weak on releases.

**Curriculum (official study-guide trail modules):**

| Domain | What it covers | Release-engineering relevance |
|---|---|---|
| **Apex Basics** | Variables, operators, classes, triggers, unit tests, execution order, debugging | You review this code every day. Test discipline = deployment gate discipline |
| **Apex and the Salesforce Platform** | Apex in the platform: objects, SOQL/SOSL, DML, collections, governor limits, sObjects | The limits are your capacity model (`02 §2`) |
| **Apex Testing** | Test classes, `testMethod`, `SeeAllData`, setup/teardown, coverage, running tests | **Directly maps to the deployment test level and the 75% per-class rule** |
| **Object Manager** | Objects, fields, validation rules, record types, page layouts, compact layouts | The metadata you deploy most often; the record-type/layout dependency chain |
| **Security** | Profiles, permission sets, permission set groups, OWD, roles, sharing, field-level security | The conflict clinic (`05 §7.1`, `05 §7.2`) |
| **Data Model and Management** | Data modelling, relationships, validation/duplicate rules, import/export | Data masking and data design (`05 §6`) |
| **Workflow and Process Automation** | Workflow, Flow, Process Builder, approval processes | The Flow version trap and the before/after-save distinction |
| **Debug and Deployment** | Debug logs, trace flags, deployment options, the deployment process, change sets | **The most directly relevant module for this role** |
| **Platform Cache** | Session, org and platform cache | Performance in Pre-Prod; cache invalidation after a deploy |

**Study order for this posting:** Debug and Deployment → Apex Testing → Security → Object Manager →
Apex and the Salesforce Platform → the rest. Do not start at Apex Basics if you already write Apex.

**Exam mechanics:** 60 questions, 60 minutes, 65% pass mark, no negative marking, **retake
attempts are limited** — confirm the current attempt allowance on the exam page before booking.

---

### 3. Salesforce Certified Platform Administrator II — curriculum

**Purpose:** "seasoned Salesforce Administrators who can harness the power of advanced features and
functionality."

**Prerequisite:** Salesforce Certified Platform Administrator.

**Curriculum domains (official study-guide trail modules):**

| Domain | Release-engineering relevance |
|---|---|
| **Configuration and Setup** | Org settings: deployment settings, session/password/lockout policies, system properties (`07`) |
| **Object Manager and Data Management** | The metadata surface you deploy and retrieve |
| **Security and Access** | Permission sets/groups, sharing, the deploy identity's permissions (`07 §4`) |
| **Setup and Maintenance** | Sandboxes, refresh, templates, releases, change management (`07 §3`) |
| **Service and Support** | Case handling and support; escalation paths |
| **Productivity / App Builder depth** | Flow, approval processes, the automation you deploy |

**Why it matters for this role:** the release engineer is the person who *configures the org so
that releases are safe*. Administrator II is the exam for that configuration vocabulary. In an
interview, "I set the deployment IP allowlist, I govern the integration user's permissions, I own
the sandbox refresh and masking checklist" is an Administrator II answer.

---

### 4. Salesforce Certified Platform App Builder — curriculum

**Purpose:** "design, build, and deploy custom applications using the declarative customization
capabilities of the Salesforce Platform."

| Domain | Relevance |
|---|---|
| **Object and Field Design** | Custom objects, fields, validation rules |
| **Security** | Profiles, permission sets, sharing — the declarative half of the conflict clinic |
| **Flow** | Before/after-save flows, record-triggered flows, the version trap |
| **Page Layouts and UI** | Layouts, Lightning record pages, the record-type → layout assignment chain |
| **App Design and Customisation** | Apps, tabs, Lightning pages, sharing |
| **Data and Analytics** | Reports, dashboards, data import/export |
| **Packaging and Deployment** | Unlocked packages, deployment options, change sets — **directly on the JD** |

**This is the fastest high-value credential for a release engineer**, because most of what a
release engineer reviews, retrieves and deploys is declarative metadata, and the exam already
contains a packaging-and-deployment domain.

---

### 5. Other credentials worth naming in an interview

| Credential | Why it is worth mentioning |
|---|---|
| **Salesforce Certified Architect — Associate / Professional** | Systems design: environments, integration, identity. Speaks directly to "DevOps friendly design patterns" and platform boundaries (the unlocked-package decision) |
| **Salesforce Certified Identity and Access Management Designer** | The deploy identity, connected apps, certificate-based auth, secret management — the exact controls a regulated bank will probe |
| **Salesforce Certified Marketing / Sales Cloud / Service Cloud Consultant** | Domain credibility in Commercial Banking (Sales Cloud is the likely core) |

---

### 6. "DevOps related certs" — the vendor credentials

#### 6.1 Gearset Academy Certification

| Attribute | Detail |
|---|---|
| Provider | Gearset, delivered through **DevOps Launchpad** |
| Audience | Admins, developers, architects and release managers |
| Coverage | The full Salesforce DevOps lifecycle: **deployments, automation, backup**, plus version control, CI/CD, release management, sandbox seeding, CPQ and Salesforce backup strategies |
| Format | Guided modules with practical work in the app; a practical certification |
| Link | <https://devopslaunchpad.com/courses/gearset-academy-certification/> |
| Fit for this JD | **Strongest** match: the JD explicitly names Gearset first, and the certification's scope (compare, deploy, pipeline, backup, masking) is the JD's scope |

#### 6.2 Copado Certified

| Attribute | Detail |
|---|---|
| Provider | Copado |
| Entry point | Copado Success certification guides (<https://success.copado.com/s/certification-guides>) and credential validation (<https://success.copado.com/s/validate-credentials>) |
| Scope | Pipelines, user stories, promotions, deployments, compliance, Copado Robotic Testing |
| Caution | The enterprise product naming changed (**Agentia Pipeline / Agentia Pipeline Pro**). A certification earned years ago may refer to `Copado Deployer` or the Metadata Pipelines product. Check the current certification catalogue rather than naming a tier from memory |
| Fit for this JD | Strong for the governance half: compliance rules, quality gates, promotion and back-promotion |

#### 6.3 AutoRABIT Academy

| Attribute | Detail |
|---|---|
| Provider | AutoRABIT |
| Entry point | <https://academy.autorabit.com/> — publishes an **ARM Core Track**, ARM Professional/Admin certification tracks, and a **Tier One ARM Certification Exam** |
| Scope | ARM (CI/CD, pipelines, approvals, release labels), Vault (backup, data masking), CodeScan (SAST) |
| Caution | Confirm which UI generation the curriculum targets — **ARM classic vs ARM New UI** have different screens and different feature flags |
| Fit for this JD | Strong for the data half: masking and backup are a named JD responsibility, and AutoRABIT is deepest there |

#### 6.4 How to answer "do you have a DevOps certification?"

> "There is no Salesforce-branded DevOps certification. On the Salesforce side I hold Platform
> Developer and Platform Administrator II, because the content I release is Apex, Flow, security and
> deployment settings. On the tooling side I hold the vendor credential — [Gearset Academy / Copado
> Certified / AutoRABIT ARM] — because that is where the pipeline, compliance and masking product
> knowledge lives. What I would not do is list a tool cert and imply it covers release engineering;
> the runbooks, the rollback model and the audit pack are what I actually bring."

---

### 7. Which credentials matter for which interview question

| Interview question | Credential that helps most | Why |
|---|---|---|
| "Explain the deployment test level and coverage rules" | PD1 (Apex Testing) + Debug and Deployment module | It is literally the exam content |
| "How do you resolve a profile conflict?" | PD1 (Security) + App Builder (Security) | Profiles, permission sets, permission set groups |
| "What org settings govern deployment?" | Administrator II (Setup and Maintenance, Configuration and Setup) | Deployment settings, session policies, sandboxes |
| "How do you design package boundaries?" | App Builder (Packaging and Deployment) + Architect Associate | Unlocked packages, dependency boundaries |
| "How do you authenticate a pipeline?" | Identity and Access Management Designer | Connected apps, certificates, secrets, scopes |
| "Which tool would you pick for masking and backup?" | AutoRABIT ARM/Vault cert | It is the product knowledge |
| "How do you prove a release was controlled?" | Administrator II + the vendor compliance features | Compliance rules, quality gates, evidence |

---

### 8. Certification-maintenance reality

Salesforce credentials require **maintenance** to stay active — a periodic exam or a set of
Trailhead units. Two practical consequences:

1. **A certification you let lapse is a claim you should not make.** Check the maintenance status
   on the Salesforce credential verification page before putting it on a résumé.
2. **The material changes.** The Deployment Settings and DevOps Center surfaces change. If the
   certification is recent but the org is old, or vice versa, trust the org.

---

### 9. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| Exact current exam-question count, duration, pass mark and retake allowance for PD1 / Administrator II | Not re-verified on the exam page (the exam pages are behind the Trailhead Academy app) | The exam page linked from each credential page: <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201> and `.../exam-platform-admin2---Plat-Admn-301` |
| Exact per-domain weightings for the PD1 and Administrator II exam outlines | The Trailhead study-guide trails render client-side; the weights were not retrievable as text | Open the study-guide trail in a browser: <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> and `.../platform-administrator-certification-study-guide` |
| Current Copado certification catalogue names | The certification-guide index is behind a Salesforce Knowledge render | <https://success.copado.com/s/certification-guides> |
| Current AutoRABIT ARM certification track names | The academy site is a dynamic storefront | <https://academy.autorabit.com/> |
| Whether a "Salesforce Certified Release Manager" credential exists | **Not found** in the credential catalogue; no evidence of such a credential | <https://trailhead.salesforce.com/credentials> |


## Part VIII — Org settings and system properties that change release behaviour

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/07-system-properties-setup-paths.md`*


> JD lines covered: R4 (audit/security/compliance), R6 (sandbox strategy), Q3 (limits and
> deployment constraints), and the "configuration/setting/variation" requirement behind every
> term in the posting.
>
> **Accuracy rule applied here.** Setup **paths** are stable and match the repository's existing
> `navigation-breadcrumbs.md`. Exact **field labels inside a settings page** vary by Salesforce
> release, edition and whether a feature (DevOps Center, Data Mask) is installed — where that is
> true, the row says so and tells you how to find the setting. Behaviour that is verified against
> the Metadata API Developer Guide or vendor documentation is marked `verified`.
---


### 1. The DevOps Setup surface — path reference

| Task | Path |
|---|---|
| Sandboxes | `Setup > Sandboxes` |
| Sandbox templates (Partial Copy source) | `Setup > Sandboxes > Sandbox Templates` |
| Deployment settings (inbound deploy gate) | `Setup > Deploy > Deployment Settings` |
| Deployment status / last 30 days of deploys | `Setup > Deploy > Deployment Status` |
| Deployed components | `Setup > Deploy > Deployed Components` |
| Change sets (legacy) | `Setup > Deploy > Change Sets` |
| Apex test execution | `Setup > Apex Test Execution` |
| Custom metadata types (incl. Protected flag) | `Setup > Custom Metadata Types` |
| Custom settings | `Setup > Custom Settings` |
| Named credentials | `Setup > Named Credentials` |
| External credentials / secret store | `Setup > External Credentials` |
| Connected apps / external client apps | `Setup > App Manager > Connected Apps` (or `External Client Apps`) |
| Debug logs | `Setup > Debug Logs` |
| Apex jobs | `Setup > Apex Jobs` |
| Scheduled jobs | `Setup > Scheduled Jobs` |
| Users, permissions, "view all data" | `Setup > Users > Users` |
| Permission sets / groups | `Setup > Permission Sets`, `Setup > Permission Set Groups` |
| Profiles | `Setup > Profiles` |
| Session settings | `Setup > Session Settings` |
| Password policies | `Setup > Password Policies` |
| Lockout policies | `Setup > Lockout Policies` |
| System properties | `Setup > System > System Properties` |
| Org system overview / API usage | `Setup > System Overview` |
| Data import / export | `Setup > Data > Data Import Wizard`, `Setup > Data > Export` |
| Salesforce backups (native) | `Setup > Data > Backups` |
| DevOps Center (if enabled) | `Setup`, Quick Find `DevOps Center` |
| Data Mask (if installed) | App Launcher → `Data Mask` |

> **Search, don't browse.** Salesforce Setup's Quick Find is the fastest route. Most of the rows
> above are one search away, and the search term is also what you should write in a runbook.

---

### 2. Deployment and CI settings — `Setup > Deploy > Deployment Settings`

This is the single page that decides **whether a pipeline can deploy into an org at all**.

| Setting | Effect | Release-engineering note |
|---|---|---|
| **Allow inbound deployments** | Master switch for Metadata API deployments into the org | If off, every pipeline fails with an auth/deploy error that does not name the cause. **Check this first when a pipeline that worked yesterday fails today on a new org.** |
| **Enable Salesforce CLI deploys** | Allows `sf project deploy start` (the CLI-specific deploy path) as opposed to raw Metadata API calls | Some orgs have the CLI path separately gated from the API path. `verified` that these are distinct controls; the exact field name varies by release |
| **Restrict deployments to specific IP ranges** | Only traffic from the listed CIDRs may deploy | This is how a bank enforces "only the CI runner deploys to prod". Combine with the runner's static egress IP. Verify the current field name in your org — the setting has been renamed across releases |
| **Deployment history retention** | Deployments in progress or completed in the **last 30 days** are visible in `Setup > Deploy > Deployment Status` | `verified` (Metadata API Developer Guide). If your audit needs 7 years of deployment evidence, Salesforce's 30-day view is **not** enough — you must export the CI artefacts yourself |

**Variations and traps**

| Variation | Trap |
|---|---|
| Inbound deployments disabled | "Invalid session id"/"deploy not permitted" style errors with no mention of the switch |
| CLI deploys disabled but API deploys enabled | `sf project deploy start` fails while the vendor tool's Metadata API path succeeds — and vice versa |
| IP allowlist set, but the runner uses a NAT or an egress proxy | Deploys intermittently fail from a different runner pool. The fix is the network config, not the retry |
| Allowlist set to a corporate CIDR rather than the CI runner's | A human on the corporate network can deploy. This quietly destroys segregation of duties |

**Audit implication:** record the Deployment Settings values in the org's configuration baseline and
review them on the same cadence as the deploy identity's permissions. A setting change here is a
control change and belongs in the change process.

---

### 3. Sandbox settings

| Setting / path | Effect | Note |
|---|---|---|
| `Setup > Sandboxes` | Lists every sandbox, its type, its refresh history and the **next eligible refresh** | The page is the source of truth for refresh cadence — do not quote a cadence from memory |
| `Setup > Sandboxes > Sandbox Templates` | Defines the data set copied into a **Partial Copy** | A template is the difference between a Partial Copy that is useful and one that leaks. Review the template the way you review a data masking rule |
| Sandbox refresh permissions | Who may request a refresh | For a bank, refresh should be a **ticketed, named-person** operation. Some orgs restrict refresh to admins so that a casual "refresh my sandbox" cannot create an unmasked production copy |
| Refresh notifications | Salesforce emails on refresh completion | Use it as the trigger for the masking step — do not rely on a human noticing the email |
| Sandbox naming convention | E.g. `CB-DEV-01`, `CB-UAT-02` | Naming is how the pipeline maps a target. If `target-org` aliases and Salesforce sandbox names drift, the pipeline deploys to the wrong org. Make the alias derivation mechanical |

**Refresh variations**

| Variation | Behaviour |
|---|---|
| Developer / Developer Pro | No data; fast; can be refreshed often (licence-limited) |
| Partial Copy | Data from the **template**, not from production; template is the privacy control |
| Full | **All production data and metadata**; slowest; carries the masking obligation |
| Scratch org | Created from a definition file on a Dev Hub; **not a sandbox**; disposable |

---

### 4. User, permission and identity settings that gate deployments

| Setting | Why a release engineer cares |
|---|---|
| `Modify All Data` on the integration user | The broad metadata + data deploy permission. Narrowest acceptable alternative is `Modify Metadata Through Metadata API Functions` **plus** per-type permissions for everything you deploy |
| `API Enabled` | Without it the identity cannot connect at all |
| `Customize Application` | Required to deploy some Flow, LWC, app, custom-metadata and custom-setting components |
| `Author Apex`, `Manage Flow`, `Manage Profiles and Permission Sets` | Recommended for the deploy identity so it can deploy the metadata types the bank actually uses |
| "Allow Users to View All Data" (org-wide) | A QA or integration user with this sees everything, including unmasked customer data. In a bank, this should be off and granted per-user through a permission set, if at all |
| `Setup > Users` → user lifecycle | Deactivate, never delete. A deleted user referenced by an approval process or an assignment breaks a deploy with `Invalid cross reference id` |
| Permission set groups | The bundling unit for a persona's access. Deploy them like any other component |
| Session settings (timeout, IP relax) | A CI token that is idle too long gets invalidated mid-release — keep the timeout compatible with your longest test run |
| Password policies / lockout policies | A shared human credential that trips the lockout policy fails a deploy. This is exactly why the pipeline uses a certificate, not a password |

---

### 5. Security and compliance settings

| Setting | Control it supports |
|---|---|
| `Setup > Session Settings` | Session timeout, IP relax, "Require secure URL" |
| `Setup > Password Policies` | Credential hygiene for human admins |
| `Setup > Lockout Policies` | Brute-force protection — and a deploy-failure cause if a shared account locks itself out |
| `Setup > IP Relax` (login IP ranges) | Where the bank restricts human logins by network |
| Connected App / External Client App policies | Token lifetime, scopes, IP relax for the deploy identity |
| `Setup > System > System Properties` | The org-wide switches; **the exact list varies by edition and release** — use Quick Find for the specific property rather than a remembered menu path |
| Audit trail / field history retention | Determines how far back "who changed this" can be answered. If your retention policy is 7 years, org field history will not cover it — externalise it |
| `Setup > System Overview` → API Usage | Monitoring; feeds the API budget decision in `02 §6` |

**The debug-log data leak.** Debug logs contain field values, query text and sometimes payload.
In a bank, a debug log pasted into a ticket is a **data incident** if it contains customer data.
Practices: capture logs only in a masked sandbox; set log retention short; scrub before attaching;
prefer the "trace flag + deployment id" pair over a full log.

---

### 6. Apex, limits and platform settings that change deploy behaviour

| Setting / limit | Where | Effect on a release |
|---|---|---|
| Concurrent Apex limit per org | `Setup > Apex Settings` (org-wide) | Caps parallel long-running transactions (10–50 depending on licences). A nightly batch + a release validation compete for the same pool |
| Concurrent Apex limit per user | `Setup > Apex Settings` | The integration user running tests counts against it |
| Apex CPU time limit | Apex settings / org limit | Determines whether a test run is killed mid-deploy |
| Total Apex code in the org (6 MB; 10 MB scratch) | Org limit; raisable via support case | The 6 MB ceiling is an **org-level** constraint on how much custom code a bank can accumulate — a release-engineering concern over years, not days |
| 7,500 class/trigger code units per deployment | Platform limit | The per-deploy ceiling that bites large orgs |
| Async executions per 24 h | Org limit (`DailyAsyncApexExecutions`) | A release that triggers a lot of async work can exhaust the day's budget |
| Batch Apex concurrent jobs (5) | Platform limit | A release that enqueues many batches will queue behind itself |
| API request allocation per 24 h | `Setup > System Overview`; `API Usage Notifications` | CI validation burns it. If the org is API-constrained, validate on a schedule, not per PR |
| `API Usage Notifications` | `Setup`, Quick Find `API Usage Notifications` | Alert a named owner before a release, not after |

---

### 7. Logging, tracing and observability settings

| Setting | Use |
|---|---|
| `Setup > Debug Logs` | Retrieve logs for a failed test/deploy. **Set a short retention; logs contain field values** |
| `Setup > Trace Flags` | Narrow diagnostic flags (e.g. Apex, workflow) to reproduce a production issue in a masked sandbox — **never** enable a trace flag at high verbosity in production during business hours |
| `Setup > Apex Test Execution` | The org-side record of a test run; the second source of test evidence alongside CI |
| `Setup > Apex Jobs` / `Setup > Scheduled Jobs` | Confirm an async job actually ran after a deploy — a common "deployed but nothing happened" cause |
| `Setup > Platform Events` / `Setup > Event Monitoring` | Verify event-driven integrations consumed the post-deploy events |
| Salesforce Setup → **API Usage** | Delivery of the post-deploy integration calls |

**The "deployed but nothing happened" checklist** — run this after every prod deploy that involves
automation:

1. Is the Flow version **Active**? (Draft is the default for some deploy tools.)
2. Did the permission set actually assign the user? (Deploy succeeded; assignment may be missing.)
3. Is the feature flag in Custom Metadata still off? (A deliberate dark launch — check it was turned on.)
4. Did the async job run? (`Setup > Apex Jobs` / `Scheduled Jobs`)
5. Did the integration endpoint point at prod? (Named Credential, not a literal URL.)
6. Is the record type visible on the user's profile/permission set?

---

### 8. Metadata and configuration settings that make releases portable

| Setting / pattern | Effect |
|---|---|
| **Custom Metadata types marked Protected** | Prevents accidental deletion of config in an org — and prevents a "delete everything I did not retrieve" deploy from removing your toggles |
| **Custom Settings (hierarchy or list)** | Org-level configuration that can differ per sandbox without a code branch |
| **Custom Metadata for feature flags** | Ship dark; flip after deploy; roll back without a redeploy |
| **Named Credential metadata** | Endpoint + auth scheme live in Git; the secret lives in the org's secret store. This is what makes one package deploy to five environments |
| **External Credentials / Secret Store** | Where the secret actually lives; not in Git |
| **Protected Custom Metadata and destructive changes** | If a type is protected, a destructive change that deletes it fails the deploy instead of silently removing config |

**The anti-pattern to name in an interview:** a hardcoded endpoint or an `if (org.IsSandbox)`
branch in Apex. It creates an environment-specific branch that can never merge, and it puts a
production URL in Git.

---

### 9. Feature gates that change the release model

| Feature | Where | Effect if enabled |
|---|---|---|
| **DevOps Center** (Salesforce-native) | `Setup`, Quick Find `DevOps Center` | Work items, Git integration and promotion inside Salesforce. Native alternative to a vendor tool; does not remove the need for Git discipline |
| **Data Mask** | App Launcher → `Data Mask` | Native sandbox masking. Not installed in every org |
| **Salesforce Native Backups** | `Setup > Data > Backups` | Native metadata backup; complement to a vendor backup product |
| **Approval Processes** | `Setup > Approval Processes` | A metadata type that **forces all local tests** in a production deployment |
| **Enhanced Field Security / Field History** | `Setup > Object Manager` | Affects what a retrieve returns, and therefore what a retrieve-all would overwrite |
| **Sandbox templates** | `Setup > Sandboxes > Sandbox Templates` | The data privacy control for Partial Copy sandboxes |
| **Flow / Process Builder retirement** | `Setup > Flows`, `Setup > Process Builder` | A legacy automation still in an org is metadata you must keep deploying. Migrate deliberately, not during a release |
| **Source tracking** | Cannot be turned on in production | This is why prod config changes must go through Git |

---

### 10. Settings matrix by JD term

| JD term | Settings that implement it | Who owns them |
|---|---|---|
| CI/CD pipelines using Git workflows | `Setup > Deploy > Deployment Settings` (inbound + CLI + IP allowlist); GitHub branch protection; GitHub Environment required reviewers | Release engineer + platform team |
| Multi-environment release strategies | `Setup > Sandboxes`; sandbox naming and aliases; per-environment GitHub Environments | Release engineer |
| Scheduled releases / hotfixes / emergency | GitHub `schedule` trigger; Environment deployment rules; freeze via branch protection; change calendar | Release manager |
| Audit / security / compliance | IP allowlist; deploy identity permissions; audit trail retention; debug log retention; API usage notifications; session/password/lockout policies | Platform + security |
| Metadata lifecycle in Git | `.gitignore` for auth files; `sfdx-project.json` source API version; `package.xml`; source-tracking policy | Developers + release engineer |
| Sandbox creation / refresh / masking | `Setup > Sandboxes`; Sandbox Templates; refresh permissions; Data Mask or a vendor masking product | Release engineer + data protection |
| Deployment conflicts (profiles / permission sets) | Permission set groups; profile decomposition tooling; `Manage Profiles and Permission Sets` on the deploy identity | Salesforce admin |
| Deployment conflicts (record types / layouts) | `Setup > Object Manager` assignment rules; app assignment for Lightning record pages | Salesforce admin |
| Flows / Apex / dependencies | Apex settings (CPU, concurrency); test level; `Setup > Apex Test Execution`; 7,500-unit deployment ceiling | Developers + release engineer |
| Reducing failures / rework | `Setup > Apex Test Execution`; `Setup > Debug Logs`; `Setup > Trace Flags`; CI gates | Release engineer |
| Unlocked / managed packages | Dev Hub (`Setup > Dev Hub`); package namespace; `sfdx-project.json` `packageDirectories` | Developers + architect |
| Regulated environment | Everything in §5, plus the evidence pack in `05 §4` | Compliance |
| DevOps-friendly design patterns | Protected Custom Metadata; Custom Metadata flags; Named Credentials; Custom Settings per sandbox | Developers + architect |
| Runbooks and rollback | Release tags; CI artefact retention; `Setup > Deploy > Deployment Status` (30-day view — export to CI for longer) | Release engineer |

---

### 11. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| Exact field label for the deployment IP allowlist in the current Salesforce release | Renamed across releases | `Setup > Deploy > Deployment Settings` in the target org |
| Exact contents of `Setup > System > System Properties` in each edition | Org-dependent | Quick Find the property name in the org |
| Whether `Allow inbound deployments` and `Enable Salesforce CLI deploys` are one setting or two in the current release | Behaviour differs by org vintage | Inspect the Deployment Settings page in a non-prod org |
| Exact refresh cadence limits by licence | Not retrieved; the Salesforce Help sandbox page is client-rendered | `Setup > Sandboxes` in the org — it shows the next eligible refresh |
| Native Salesforce backup retention and scope | Not retrieved | `Setup > Data > Backups` |


## Part IX — Cross-bundle delta and reconciliation

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/08-cross-bundle-delta.md`*


**For the merge round.** This bundle is one of two independent research drops for Scotiabank
requisition 276046. This file records the overlap, who is authoritative where, and what to do
about the one genuine divergence.
| Field | Value |
|---|---|
| This bundle | `research/2026-11-14T020300Z-kilo-salesforceagain/` |
| Worktree | `salesforceagain` |
| Sibling bundle | `research/2026-11-14T021057Z_salesforcemore-v2/` |
| Sibling worktree | `salesforcemore-v2` |
| Both started | 2026-11-14 (UTC) |
| Downstream target | `docs/salesforce/devops-engineer.md` in the ServiceNow_Learning repo |
The sibling bundle already wrote a reconciliation file against this bundle's early README
(`08-cross-bundle-notes.md` in that bundle). **We agree on all eight headline corrections** — the
deploy ceilings, the one-deploy-at-a-time/non-FIFO queue, the five test levels, the Gearset UI
shape and backup product, the Copado and AutoRABIT product renames, and the Platform
Administrator II prerequisite. No reconciliation conflict remains on those.
---


### 1. Where this bundle is the better source

| # | Content only this bundle has | Why it wins | Where to lift it |
|---|---|---|---|
| 1 | **The complete list of metadata types that force all local tests to run** — `ApexClass`, `ApexComponent`, `ApexPage`, `ApexTrigger`, `ArticleType`, `BaseSharingRule`, `CriteriaBasedSharingRule`, `CustomField`, `CustomObject`, `DataCategoryGroup`, `Flow`, `InstalledPackage`, `NamedFilter`, `OwnerSharingRule`, `PermissionSet`, `Profile`, `Queue`, `RecordType`, `RemoteSiteSetting`, `Role`, `SharingReason`, `Territory`, `Validation Rules`, `Workflow` — plus the worked examples (1 `CustomField` forces a full run; 100 Reports + 40 Dashboards does not) | It is the single most actionable fact in the posting's test-and-validation area, and it is quoted verbatim from the Metadata API Developer Guide. The sibling bundle has the five test levels but not the type list | `02-limits-and-constraints.md` §5.1 |
| 2 | **CLI flags verified against the plugin source, not the docs** — `sf org login jwt` uses `--jwt-key-file` and has **no `--client-secret`**; `sf org login jwt` has aliases `force:auth:jwt:grant` / `auth:jwt:grant` (deprecated) | Several widely copied runbooks show `--jwt-key` and `--client-secret`; neither exists in the current implementation. Publishing the wrong flag is a broken pipeline for the reader | `04-github-actions-salesforce-cicd.md` §2.2 |
| 3 | **`sf project deploy validate` semantics** — it **requires** Apex tests (`NoTestRun` is not an option); it **does not support source tracking**; the CLI explicitly says **"Don't use this command on sandboxes"** and directs you to `sf project deploy start --dry-run --test-level RunLocalTests` for sandbox validation | This is the validate/quick-deploy pattern the posting implies, and the sandbox/prod split is a common source of broken pipelines | `04` §4.4 |
| 4 | **`sf project deploy quick` semantics** — the validation job id is **valid for 10 days**; `--use-most-recent` only considers validations from the **past 3 days or less**; it skips Apex tests; it does not support source tracking; it is not intended for sandboxes | These are the exact rules that decide whether a quick deploy is legitimate | `04` §4.4 |
| 5 | **`sf apex run test` flag set** — `--output-dir`, `--class-names`, `--suite-names`, `--result-format` with values `human` / `tap` / `junit` / `json`, `--detailed-coverage`, `--synchronous`, `--poll-interval`, `--wait` | Needed to wire a real JUnit/coverage artefact into a CI pipeline | `04` §4.1 |
| 6 | **`checkOnly` cannot validate a Master-Detail ↔ Lookup field-type change**; a deploy that adds a Master-Detail field soft-deletes all detail records in the Recycle Bin and **permanently deletes them during the deploy**; a Lookup→Master-Detail conversion requires detail records to reference a master or be soft-deleted, and a successful deploy **permanently empties the Recycle Bin** | A destructive, non-recoverable data behaviour that belongs on a release-engineering page, and which a Git revert cannot undo | `02` §4.2 and §4.3 |
| 7 | **Deployment Status page mechanics** — two live charts (components processed; Apex tests run, with the currently running test named), cancellation semantics including `Finalizing Deploy` on API 65.0+, and a **30-day** deployment history window | Directly supports the audit-evidence discussion: Salesforce's own view is only 30 days, so a 7-year retention policy requires exporting CI artefacts | `02` §3.2, `07` §2 |
| 8 | **The negative-result lists** — 16 numbered "not a current documented label" findings for Gearset, Copado and AutoRABIT (`Work Rules`, `Plan & Deploy`, `Deploy only changed components`, `Invalidate cache`, `Last deployed`/`Unmanaged` as compare tabs, `Pipeline Job`/`Deployment Job`, `Reset sandbox`, Copado `Fundamentals`/`DevOps Center`/`Data Masking`, Copado Work Item types and "Blocked" status, AutoRABIT `Test Repository`, AutoRABIT `Max Batch Size`, ARM "Stages/Steps/Components" vocabulary, and more) | The most valuable training artefact in the bundle, because it stops the page from teaching wrong labels and stops the reader from asserting them in an interview. The sibling bundle has the corrections but not the exhaustive negative list | `03` §0 and §5 |
| 9 | **Specific retention/expiry numbers that are release blockers** — Copado credentials expire after **30 days** of inactivity (Salesforce refresh-token TTL) with no proactive warning; AutoRABIT pending approvals **auto-reject after 3 days** and **self-approval is impossible even for an admin**; AutoRABIT CI build reports are unavailable after **30 days** and SCA source after **90 days**; AutoRABIT Quick Deploy uses components validated in the last **96 hours**; Gearset record data is retained **7 years** with metadata retained indefinitely; AutoRABIT masking rollback data is retained **7 days** | These are the numbers a release engineer must put in a runbook | `03` §2.8, §2.9, §3.4, §3.5, §3.6, §1.8 |
| 10 | **Copado's per-commit/promotion file ceilings** — 8,000 files for a Copado-created commit or promotion, 10,000 for manual-step or Git-repository deployments; and **only a Copado Admin** may add user stories to a promotion targeting production | A concrete gate a release engineer can be asked about | `03` §2.4 |
| 11 | **The 7,500 class-and-trigger code units per Apex deployment ceiling**, alongside the 6 MB org-wide Apex code ceiling and the 10 MB scratch ceiling | The per-deployment ceiling is the one that bites large orgs and is absent from most training material | `02` §2.4 |
| 12 | **AutoRABIT masking precedence** — local masking rules take precedence over global rules; `Config Details` can disable workflows, validation rules, triggers and flows during masking | Operationally important when a masking run fails on an automation | `03` §3.5 |
| 13 | **A full org-settings catalogue mapped to JD lines** — `Setup > Deploy > Deployment Settings` (inbound deploy gate, CLI deploy gate, deployment IP allowlist, 30-day history), sandbox templates as a privacy control, debug logs as a **data-leak surface** in a bank, the "deployed but nothing happened" post-deploy checklist, and a settings-matrix by JD term | The sibling bundle covers system settings more briefly; this bundle indexes them against the posting so nothing is orphaned | `07` |

---

### 2. Where the sibling bundle is the better source

| # | Content in the sibling bundle | Why it wins | Where to lift it |
|---|---|---|---|
| 1 | `01-salesforce-key-principles/principles.md` and `release-model.md` | The user explicitly asked for "planning best on Salesforce key principles". The sibling bundle has this as a standalone, well-argued artifact; this bundle only has the principle table inside `00-plan.md` §4 | Use the sibling's principles as the framing layer; this bundle's `00-plan.md` §4 is a compact fallback |
| 2 | Folder-per-topic organisation with an explicit **"Merge target"** line on every file | This bundle is flat-file. The "Merge target" annotation tells the merge round exactly which downstream section each artefact feeds, which removes guesswork | Adopt the annotation convention in the merged page |
| 3 | `07-merge/merge-map.md` and `content-gaps.md` | The sibling bundle already produced a merge map and a gap list. Do not duplicate that work | Use theirs as the merge plan; this bundle's `01-jd-crossreference.md` is the supporting evidence |
| 4 | `02-limits-constraints/inspection-and-drills.md` | A practical "where do I look" companion (UI paths + CLI/code) plus interview drills. This bundle has the limits but fewer inspection drills | Merge both; the sibling's drills are the more usable form for a student |
| 5 | `03-devops-tools/gearset-click-paths.md` lists a **more granular Gearset navigation grouping** (adding *Problem analyzers*, *Observability*, *Automated testing*, *Sandbox seeding & compliance*, *Settings / Team management*) | See the divergence below | Use theirs as the navigation list; use this bundle's article-level citations |
| 6 | `05-certifications/certification-landscape.md` and `vendor-and-study-plan.md` | The sibling bundle separates the landscape from the curriculum and adds a study plan; this bundle combines them | Use theirs for the study plan; this bundle adds the **prerequisite chain** and the exam-domain mapping |
| 7 | `06-term-deep-dives/term-index.md` and `term-entries.md` | A one-entry-per-term format with interview lines. This bundle's `05` covers the same ground with more configuration depth per term | Use the sibling's index format, this bundle's depth |

---

### 3. The one genuine divergence — Gearset navigation grouping

| Bundle | Navigation groups |
|---|---|
| This bundle (`03` §1.1) | `My connections` · `Metadata deployments` · `Continuous delivery` · `Backup & archiving` · `Sandbox seeding` · `Data deployments` · `Settings` |
| Sibling bundle | `My connections` · `Metadata deployments` · `Continuous delivery` · `Backup & archiving` · `Sandbox seeding & compliance` · `Problem analyzers` · `Observability` · `Automated testing` · `Settings / Team management` |

**Neither is wrong; they are different resolutions of the same doc set.** The sibling's list comes
from the Gearset **documentation collections index**; this bundle's list comes from the individual
articles' navigation and the screens those articles describe (there is a separate `Data history`
screen under data deployments, which the sibling's grouping folds elsewhere).

**Resolution for the merged page:** do not publish a single rigid sidebar as *the* Gearset UI.
Publish the **task → screen** mapping (which both bundles agree on and which is what a learner
needs), and note that the left sidebar is grouped and that group names vary by rollout and licence
tier. A task-to-screen table is stable; a screenshot of a sidebar is not.

---

### 4. Suggested merge order

1. **Framing** — sibling `01-salesforce-key-principles/*` (principles + release model).
2. **Structure** — sibling `07-merge/merge-map.md` (which section takes what).
3. **Depth, in page order** — this bundle's `01` (JD cross-reference) drives the order; then
   `02` (limits) → `03` (tools) → `04` (CI/CD) → `05` (terms) → `06` (certs) → `07` (settings).
4. **Sibling extras** — `inspection-and-drills.md` after the limits section;
   `certification-landscape.md` + `vendor-and-study-plan.md` after the certifications section;
   `term-index.md` alongside `05`.
5. **Formatting** — wrap every deep dive in `<details><summary>…</summary>…</details>` and keep
   the existing page's section numbering intact so existing links still resolve.
6. **Corrections** — apply the correction table in this bundle's `01` §3 and the sibling's
   `08-cross-bundle-notes.md` §2 together; they do not conflict.

---

### 5. Conflicts requiring a human decision

| # | Question | Why it needs a decision |
|---|---|---|
| 1 | Does the published page get a **companion page** (`devops-engineer-deep`) or do all of this get folded into `devops-engineer.md` as collapsible blocks? | The merged content is several times the current page length. The user asked for "deeper documentation into collapsible sections", which suggests folding in — but a companion page keeps the original scannable and is easier to maintain |
| 2 | Should the **sub-agent research** be published, or distilled into prose? | The negative-result lists (`03` §5) are valuable but read like an audit. Publishing them under a `<details>` "Naming traps and stale labels" heading preserves their value without cluttering the page |
| 3 | Is the **exam-domain weighting** table published at all? | Neither bundle could retrieve the current weights (the Trailhead study-guide trails are client-rendered). Publishing unverified weights would be a mistake. **Recommendation: publish the domain names, not the percentages**, and link the study guide |
| 4 | Do the **Copado prices** stay in? | Vendor pricing changes; it is not needed for the posting. **Recommendation: drop the prices, keep the edition-feature matrix** |
| 5 | Should the Gearset **navigation grouping** be published as a sidebar diagram? | See §3. **Recommendation: no diagram; publish the task → screen table instead** |


## Part X — Sources — URL, access date, verification status

*Source artifact: `research/2026-11-14T020300Z-kilo-salesforceagain/sources.md`*


All URLs accessed **2026-11-14 (UTC)** unless stated. Confidence tags follow `00-plan.md` §6.
---


### 1. Job and target page

| # | Source | Type | Confidence |
|---|---|---|---|
| S1 | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> — Requisition 276046, DevOps Engineer (Salesforce), Commercial Banking Engineering, Toronto | Primary | `verified` |
| S2 | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> — published training page | Primary | `verified` |
| S3 | `docs/salesforce/devops-engineer.md` (554 lines, commit `5bf3887`) read from the ServiceNow_Learning worktree `/home/eaguiar2015/wt-sf-devops` | Primary (source) | `verified` |
| S4 | `docs/salesforce/navigation-breadcrumbs.md` — Setup path conventions used by this repo | Primary (source) | `verified` |
| S5 | `docs/salesforce/crash-course.md` — source of the async-heap correction | Primary (source) | `verified` |
| S6 | <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM> — repository that publishes the target page | Primary | `verified` |
| S7 | <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> — this research repository | Primary | `verified` |

---

### 2. Salesforce platform documentation

Fetched through the `r.jina.ai` text-extraction proxy, because `help.salesforce.com` is a
client-rendered application that cannot be scraped as static text. The underlying Salesforce URLs
are listed so the merge round can re-verify in a browser.

| # | Source | Used for | Confidence |
|---|---|---|---|
| S10 | <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm> → *Execution Governors and Limits* | All governor limits, per-transaction and per-org; callout/query/code limits; certified-package namespace limits | `verified` |
| S11 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm> → *Deploying Metadata Using the Metadata API* | Deploy payload ceilings (≈39 MB / ≈600 MB / 10,000 / 35,000 files); one-deploy-at-a-time and non-FIFO queue; Deployment Status charts; 30-day history; cancellation semantics; `checkOnly`; destructive changes; required permissions | `verified` |
| S12 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_retrieve.htm> | Retrieve limits; Big Object index requirement | `verified` |
| S13 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_running_tests.htm> → *Running Tests in a Deployment* | The exact metadata-type list that forces all local tests to run; API 33.0/34.0 behaviour change | `verified` |
| S14 | <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_run_relevant_tests.htm> → *Run Relevant Apex Tests in a Deployment (Beta)* | `RunRelevantTests`; `@IsTest(critical=true)`; `@IsTest(testFor='…')`; per-class 75% | `verified` |
| S15 | <https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm> → *API Request Limits and Allocations* | Concurrent and 24-hour API allocations; timeout; `DebuggingHeader` allocation; managed-package calls counting; monitoring surfaces; overage policy | `verified` |
| S16 | <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> — Quick Deploy | Referenced for the quick-deploy concept | **Not retrievable** — client-rendered. Quick-deploy behaviour is instead sourced from S11 + S14 + the CLI source in §3 |
| S17 | <https://help.salesforce.com/s/articleView?id=sf.deploy_sandboxes_parent.htm&type=5> — Sandboxes | Referenced | **Not retrievable** — client-rendered. Sandbox facts are sourced from S1/S2 reasoning and `03` vendor behaviour; per-org refresh cadence must be read from `Setup > Sandboxes` |
| S18 | <https://help.salesforce.com/s/articleView?id=sf.overview_limits.htm&type=5> — Limits overview | Referenced | **Not retrievable** — client-rendered |

---

### 3. Salesforce CLI — plugin source used as the authoritative flag reference

Reading the plugin implementation (not the docs page) means every flag name and description below
is the literal string the CLI uses.

| # | Source | Used for | Confidence |
|---|---|---|---|
| S20 | <https://github.com/salesforcecli/plugin-deploy-retrieve> — `messages/deploy.metadata.md` | Exact `--test-level` semantics for all five levels; `--pre-destructive-changes` / `--post-destructive-changes`; `--purge-on-delete`; `--metadata` / `--source-dir` / `--manifest` / `--single-package` / `--metadata-dir`; the "Metadata components are deployed in source format by default" note; the "production orgs never allow source tracking" note | `verified` |
| S21 | Same repo — `messages/commonFlags.md` | `--tests` syntax (repeat the flag, or space-separated, quote names with spaces) | `verified` |
| S22 | Same repo — `src/commands/project/deploy/start.ts`, `validate.ts`, `quick.ts`, `preview.ts`, `report.ts`, `cancel.ts`, `resume.ts` | The existence and flag sets of `sf project deploy validate`, `sf project deploy quick`, `sf project deploy preview`, `sf project deploy report`, `sf project deploy cancel`, `sf project deploy resume` | `verified` |
| S23 | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/guide/project-deploy-start.html> | Referenced for the CLI guide | **403** — Salesforce blocks automated access; S20–S22 used instead |
| S24 | <https://developer.salesforce.com/docs/platform/salesforce-cli-plugin/guide/project-deploy-quick.html> | Referenced for quick deploy | **403** — as S23 |

---

### 4. Salesforce certifications

| # | Source | Used for | Confidence |
|---|---|---|---|
| S30 | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Credential name "Salesforce Certified Platform Developer"; exam `Plat-Dev-201`; study trail and trailmix links | `verified` |
| S31 | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Credential name "Salesforce Certified Platform Administrator II"; exam `Plat-Admn-301`; **prerequisite: Platform Administrator** | `verified` |
| S32 | <https://trailhead.salesforce.com/credentials/administratoroverview> | The certification landscape by role; absence of a Salesforce DevOps credential | `verified` |
| S33 | <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> | PD1 study-guide trail (module structure) | `verified` for the trail; **exact exam-domain weightings not retrievable** (client-rendered) |
| S34 | <https://trailhead.salesforce.com/content/learn/trails/platform-administrator-certification-study-guide> | Administrator II study-guide trail | `verified` for the trail; weightings not retrievable |
| S35 | <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201> | PD1 exam page (referenced; live exam parameters unverified) | `vendor-claim` / unverified content |
| S36 | <https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301> | Administrator II exam page (referenced) | `vendor-claim` / unverified content |

---

### 5. Gearset

| # | Source | Used for | Confidence |
|---|---|---|---|
| S40 | <https://docs.gearset.com/en/articles/16666562-setting-your-homepage-in-gearset> | Grouped left-navigation structure | `verified` |
| S41 | <https://docs.gearset.com/en/articles/618755-managing-salesforce-org-connections> | Adding, authorising and removing org connections; sharing | `verified` |
| S42 | <https://docs.gearset.com/en/articles/2707810-why-does-gearset-have-two-connected-apps> | Two Connected Apps (`Gearset`, `Gearset Deploy`); manual install requirement | `verified` |
| S43 | <https://docs.gearset.com/en/articles/2288760-what-oauth-version-does-gearset-use> | OAuth 2.0 + PKCE; refresh-token rotation; 30-day idle timeout; IP allowlist | `vendor-claim` |
| S44 | <https://docs.gearset.com/en/articles/16012727-deployment-user-in-salesforce-permission-checklist> | Deployment-user permission checklist | `verified` |
| S45 | <https://docs.gearset.com/en/articles/9155775-running-your-first-comparison> | Compare flow; source/target locations; comparison filters; `Compare now` | `verified` |
| S46 | <https://docs.gearset.com/en/articles/619012-configuring-comparisons> and <https://docs.gearset.com/en/articles/8870853-default-comparison-metadata-filter> | `COMPARISON FILTER` and built-in filters | `verified` |
| S47 | <https://docs.gearset.com/en/articles/595002-exploring-comparison-results> | Result tabs `All items`/`New`/`Changed`/`Deleted`; `Selected items`; table columns; difference types; filters | `verified` |
| S48 | <https://docs.gearset.com/en/articles/3154487-where-are-subcomponents-and-their-dependencies-displayed-in-the-comparison-results> | `Components` as a dependency-tree node, not a tab | `verified` |
| S49 | <https://docs.gearset.com/en/articles/595095-running-your-first-deployment> | `Next` → problem analysis → `Pre-deployment summary` → `Validate deployment` / `Deploy now` | `verified` |
| S50 | <https://docs.gearset.com/en/articles/1376067-setting-apex-test-levels> | The four Gearset Apex test-level options | `verified` |
| S51 | <https://docs.gearset.com/en/articles/625054-metadata-deployment-history> | Deployment history actions: `View details`, `View errors`, PDF report, package download, CSV, `Roll back`, `Clone package`, `Deploy to target` | `verified` |
| S52 | <https://docs.gearset.com/en/articles/625156-validated-packages> | Validation history and `View errors` | `verified` |
| S53 | <https://docs.gearset.com/en/articles/8333138-setting-up-your-first-ci-job-in-gearset> | CI job options: metadata filter, test level, `Deploy deleted items`, `Deploy permissions`, Delta CI, PR validation, SA ruleset, Problem Analyzer, outgoing webhook | `verified` |
| S54 | <https://docs.gearset.com/en/articles/8345280-validation-only-ci-jobs> | `Validation-only CI Job` | `verified` |
| S55 | <https://docs.gearset.com/en/articles/8345275-managing-and-viewing-your-ci-jobs> | CI job history, `View comparison`, `View job performance` | `verified` |
| S56 | <https://docs.gearset.com/en/articles/6115277-an-introduction-to-gearset-pipelines> | Pipeline concept | `verified` |
| S57 | <https://docs.gearset.com/en/articles/12460112-creating-ci-jobs-in-gearset-pipelines> | `Add static environment` / `Create new` — environment, branch, target org, CI job | `verified` |
| S58 | <https://docs.gearset.com/en/articles/12928379-adding-environments-to-a-gitflow-pipeline> and <https://docs.gearset.com/en/articles/14151578-the-gitflow-branching-strategy-in-pipelines> | Gitflow stage → branch mapping | `verified` |
| S59 | <https://docs.gearset.com/en/articles/12656100-getting-started-with-continuous-delivery-rules-in-gearset-pipelines> | `Continuous Delivery Rules`; forward promotion; back propagation; Automation Platform Enterprise | `verified` |
| S60 | <https://docs.gearset.com/en/articles/9859659-pre-and-post-deployment-steps-in-gearset-pipelines> and <https://docs.gearset.com/en/articles/10718514-deployment-steps-library-in-gearset-pipelines> | `Deployment steps`; `Deployment steps library`; `Manual` / `Automatic` step types | `verified` |
| S61 | <https://docs.gearset.com/en/articles/9965863-integrating-with-github-or-github-enterprise-through-a-github-app> | GitHub App repository permissions | `verified` |
| S62 | <https://docs.gearset.com/en/articles/2437757-managing-status-check-rules-in-github> | Required status check setup in GitHub branch protection | `verified` |
| S63 | <https://docs.gearset.com/en/articles/8548816-ci-job-and-pipeline-webhooks> | CI-job and pipeline webhooks; manual trigger | `verified` |
| S64 | <https://docs.gearset.com/en/articles/11496146-running-and-managing-your-backup-job> | Backup tiers (Standard, High frequency, Big Object); 7-year record retention; indefinite metadata retention; `Back up now`; `Job history`; `View changes` | `verified` |
| S65 | <https://docs.gearset.com/en/articles/3277396-creating-your-first-data-backup-job> | Backup job creation flow and first-run baseline | `verified` |
| S66 | <https://docs.gearset.com/en/articles/8425850-what-data-is-backed-up-in-each-run> | Metadata + record data capture | `verified` |
| S67 | <https://docs.gearset.com/en/articles/9311061-what-binary-data-files-or-attachments-are-supported> | `ContentVersion`, `ContentDocumentLink`, `Attachment` support; Bulk API restrictions | `verified` |
| S68 | <https://docs.gearset.com/en/articles/3456807-restoring-deleted-records-without-dependencies> | Restore flow: `Job history` → `View changes` → `View records` → `Restore from previous backup` | `verified` |
| S69 | <https://docs.gearset.com/en/articles/8065268-data-restoration-using-gearset> | Restore with dependencies | `verified` |
| S70 | <https://docs.gearset.com/en/articles/3457045-restoring-metadata-from-a-data-backup-job> | Metadata restore from snapshot; Metadata History rollback | `verified` |
| S71 | <https://docs.gearset.com/en/articles/10147094-how-to-configure-retention-rules-for-your-archived-data> | Archive rules (`Archive data after`, `Delete after`, `Do not archive`) | `verified` |
| S72 | <https://docs.gearset.com/en/articles/10471254-running-your-first-in-place-masking> | In-place masking flow; `Automatically selected sensitive fields`; `Disable automations` | `verified` |
| S73 | <https://docs.gearset.com/en/articles/14737732-what-fields-are-selected-for-masking-by-default> | Default masked fields | `verified` |
| S74 | <https://docs.gearset.com/en/articles/13112693-running-your-first-sandbox-seeding-job> and <https://docs.gearset.com/en/articles/2529785-using-templates-for-sandbox-seeding-compliance> | Sandbox seeding + `Configure masking`; template reuse | `verified` |
| S75 | <https://docs.gearset.com/en/articles/10256103-how-do-i-refresh-a-sandbox-in-my-pipeline> and <https://docs.gearset.com/en/articles/11838948-best-practice-refreshing-and-masking-a-full-copy-sandbox> | The refresh → re-auth → re-sync → redeploy → mask sequence; **Gearset does not perform the refresh** | `verified` |
| S76 | <https://docs.gearset.com/en/articles/604536-org-monitoring-automating-org-change-tracking-and-metadata-backup> | `Change monitoring` | `verified` |
| S77 | <https://docs.gearset.com/en/articles/14134763-how-to-replicate-deployment-errors-using-salesforce-cli> and <https://docs.gearset.com/en/articles/14134708-how-to-replicate-retrieval-issues-using-salesforce-cli> | Salesforce CLI as the troubleshooting/reproduction tool, not a per-org setting | `verified` |
| S78 | <https://docs.gearset.com/en/articles/13938209-what-is-express-deploy> | `Express Deploy` as an open-pilot deployment mode | `vendor-claim` |
| S79 | <https://docs.gearset.com/en/articles/6170088-enforcing-code-review-before-promotion> | Code-review enforcement in pipelines | `verified` |
| S80 | <https://docs.gearset.com/en/articles/5069914-delta-ci> | Delta CI baseline behaviour | `verified` |
| S81 | <https://docs.gearset.com/en/articles/10473502-configuring-gearset-permissions> and <https://docs.gearset.com/en/articles/8989748-gearset-backup-restore-user-permissions> | Team Security; backup/restore permissions; plan gates | `verified` |

---

### 6. Copado

| # | Source | Used for | Confidence |
|---|---|---|---|
| S90 | <https://www.copado.com/copado-essentials> | Essentials Free / Basic / Essentials Plus edition matrix and prices | `vendor-claim` (prices as at 2026-11-14) |
| S91 | <https://docs.copado.com/home/en-us/> | Current publication set: Agentia Pipeline Pro, Agentia Testing, Agentia AI Context Hub, Salesforce Metadata Pipelines (legacy) | `verified` |
| S92 | <https://docs.copado.com/articles/copado-ci-cd-publication/glossary-of-terms> | Object definitions (Pipeline, User Story, Environment, Promotion, Release, Feature/Promotion Branch, Credential, Git Snapshot, Deployment Step, Job Template/Step/Execution, Connection Behavior) and licence types | `verified` |
| S93 | <https://docs.copado.com/articles/copado-ci-cd-publication/pipeline-page> and <https://docs.copado.com/articles/copado-ci-cd-publication/pipeline-configuration> | Pipeline Manager navigation; status icons; drill-downs; `Configure Pipeline` | `verified` |
| S94 | <https://docs.copado.com/articles/copado-ci-cd-publication/how-to-create-a-promotion> and <https://docs.copado.com/articles/copado-ci-cd-publication/promotion-overview> | Promotion routes; `Ready to Promote`; `Add Selected User Stories`; `Create Deployment`; `Deployment Details`; promotion-branch naming; `tag=x.y.z`; 8,000/10,000 file limits; Copado Admin rule for production | `verified` |
| S95 | <https://docs.copado.com/articles/copado-ci-cd-publication/deployment-steps1> | The full deployment-step type list | `verified` |
| S96 | <https://docs.copado.com/articles/copado-ci-cd-publication/deployment-execution-options> | `Deploy Outstanding` vs `Deploy All`; `Deploy Now` vs `Deploy Later` | `verified` |
| S97 | <https://docs.copado.com/articles/copado-ci-cd-publication/creating-a-deployment> | Deployment record types; `Attach Deployment Files`; Advanced (multi-step) | `verified` |
| S98 | <https://docs.copado.com/articles/copado-ci-cd-publication/quality-gates-in-copado-continuous-delivery> | The quality-gate table (Apex Tests with Validation, Validation, Compliance Check, Static Code Analysis, Automation, Test, Manual Approval/Test/PR, URL Callout) | `verified` |
| S99 | <https://docs.copado.com/articles/copado-ci-cd-publication/connection-behaviors> | Connection Behavior fields; automation scope; CDC and API-key prerequisites | `verified` |
| S100 | <https://docs.copado.com/articles/copado-ci-cd-publication/copado-compliance-hub> and <https://docs.copado.com/articles/copado-ci-cd-publication/compliance-scan-and-scan-results> | Compliance objects; active and passive scans; `Compliance Scan Events`; scheduled scans; results tab | `verified` |
| S101 | <https://docs.copado.com/articles/source-format-pipelines-publication/credential-overview> and <https://docs.copado.com/articles/source-format-pipelines-publication/how-to-create-a-credential> | Credential types; creation fields; OAuth/SSO authentication; the 30-day refresh-token TTL | `verified` |
| S102 | <https://docs.copado.com/articles/copado-pipelines-publication/copado-branching-strategy> | The five Copado branching mechanics | `verified` |
| S103 | <https://docs.essentials.copado.com/en/articles/4719394-using-work-items> | Work Item fields and actions; automatic stage progression; `Go Back to Previous Stage` | `verified` |
| S104 | <https://docs.essentials.copado.com/en/articles/6887394-approval-process-with-copado-essentials-plus> | Required approving reviews; approver roles | `verified` |
| S105 | <https://docs.essentials.copado.com/en/articles/6828447-ci-jobs-overview> | Essentials Plus CI Jobs (scheduled validation, metadata backups, webhook deploys, outgoing webhooks) | `verified` |
| S106 | <https://docs.essentials.copado.com/en/articles/5742593-essentials-plus-edition-setup-guide> | Pipeline setup; org connection; integration user recommendation; Git branching behaviour | `verified` |
| S107 | <https://docs.essentials.copado.com/en/articles/7861656-validations-with-copado-essentials> | Validation and test levels; coverage; SA | `verified` |
| S108 | <https://docs.copado.com/articles/copado-ci-cd-publication/copado-pipelines-publication/reference-articles> and `.../creating-a-deployment` | Deployment Activity, Work Items list, `Attach Deployment File` producing `Deploy-{deploymentJobId}.zip` | `verified` |
| S109 | <https://success.copado.com/s/certification-guides> | Copado certification entry point | `vendor-claim` |

---

### 7. AutoRABIT

| # | Source | Used for | Confidence |
|---|---|---|---|
| S120 | <https://www.autorabit.com/products/automated-release-management-ci-cd/> | ARM as the CI/CD product | `vendor-claim` |
| S121 | <https://www.autorabit.com/products/vault-data-backup-recovery/> | Vault as backup/recovery and the home of data masking | `vendor-claim` |
| S122 | <https://knowledgebase.autorabit.com/fundamentals/faq/autorabit-platform-user-definitions> | Standard User vs Platform Integration User licence classes | `verified` |
| S123 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/automation-and-ci/create-a-new-ci-job/deploy-from-version-control-to-a-salesforce-org> | CI Job creation, all sections, all options | `verified` |
| S124 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/automation-and-ci/ci-job-list> | CI Job List filters and row actions; deactivated-job behaviour | `verified` |
| S125 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/dashboard-and-pipelines/pipelines> | Classic ARM Pipeline screen; branch types | `verified` |
| S126 | <https://knowledgebase.autorabit.com/product-guides/arm-1/arm-features/dashboard-and-pipelines/pipelines> and `.../most-recent-runs/release-pipeline-run-details` | ARM New UI `Pipelines → Releases`; stage cards; logs; `Deployment report` / `Deployment logs` | `verified` |
| S127 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/create-and-deploy-changes-in-autorabit> | Deployment creation; `Deployment From`; `Selective` vs `Full`; compare-metadata-and-deploy flow | `verified` |
| S128 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/apex-unit-tests> | Apex test levels; `Run Tests Based On Changes`; `Run Relevant Tests` | `verified` |
| S129 | <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/masking-rules> | Masking Rules (global) and cloning | `verified` |
| S130 | <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/live-data-masking> | Live Data Masking flow; masking-rule fields; `Config Details`; local vs global precedence; rollback retention (7 days) | `verified` |
| S131 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/version-control/change-labels/release-labels> | Release Labels; `Label Type`; `No of Days`; `Create package manifest`; delta metadata types | `verified` |
| S132 | <https://knowledgebase.autorabit.com/product-guides/arm-1/arm-features/deployment/schedule-a-deployment> | Scheduled Deployments (feature flag `SCHEDULED_DEPLOYMENTS`); `Edit`/`Cancel`/`Deploy Now` | `verified` |
| S133 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/monitor-deployments> | Deployment History; promotion/redeploy/rollback/abort; `Quick Deploy` within 96 hours | `verified` |
| S134 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-administration/user-management/arm-credential-manager> | Credential Manager types and scope; Org Administrators only | `verified` |
| S135 | <https://knowledgebase.autorabit.com/product-guides/arm/registration/salesforce-org/salesforce-authentication-using-oauth> | OAuth registration, Connected App scopes and callback, ECA flow | `verified` |
| S136 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/reports/reports-overview> and `.../audit-report` | Weekly reports; Audit Report (CSV, GMT); Job Audit Report PDF; retention windows | `verified` |
| S137 | <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/reports/deployment-reports` | Deployment report set; code coverage warning; `Audit Log` categories | `verified` |
| S138 | <https://knowledgebase.autorabit.com/llms.txt> | Knowledge-base index; used to confirm the **absence** of a "Test Repository" product | `verified` (negative result) |
| S139 | <https://academy.autorabit.com/?sfwd-courses=arm-core-track> and <https://academy.autorabit.com/?product=admin-certification> | ARM Academy tracks | `vendor-claim` |

---

### 8. Gearset Academy certification

| # | Source | Used for | Confidence |
|---|---|---|---|
| S140 | <https://devopslaunchpad.com/courses/gearset-academy-certification/> | Gearset Academy Certification: audience, lifecycle coverage (deployments, automation, backup, version control, CI/CD, release management, sandbox seeding, restore) | `vendor-claim` |
| S141 | <https://docs.gearset.com/en/articles/8825457-gearset-onboarding-training-courses> and <https://docs.gearset.com/en/articles/4497508-what-is-devops-launchpad> | Training relationship between Gearset and DevOps Launchpad | `vendor-claim` |

---

### 9. Method notes

| Note | Detail |
|---|---|
| **Proxy** | `r.jina.ai` was used to convert client-rendered Salesforce and vendor pages to text. It changes presentation, not content; every citation above points at the canonical source URL, not the proxy URL. |
| **Why the Salesforce CLI source was preferred over the docs page** | `developer.salesforce.com` returned **403** to automated requests during this research. The `salesforcecli/plugin-deploy-retrieve` repository is the implementation, and its `messages/*.md` files are the literal user-facing strings — a stronger source than the rendered docs page. |
| **Negative results** | Where a UI label could not be found, the artifact says so. This is deliberate: "not a current documented label" is a finding, silence would be a gap. The main negative results are listed in `03 §5`. |
| **Vendor pricing** | Copado Essentials prices were read from copado.com on 2026-11-14 and are subject to change. Re-verify before quoting. |
| **Not consulted** | Any local Salesforce org, any live vendor tenant, and any internal Scotiabank material. Every statement about what a bank "typically" does is framed as such. |
