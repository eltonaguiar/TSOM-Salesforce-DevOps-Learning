# 00 — Plan

## 1. Objective

Produce merge-ready research for the **Scotiabank DevOps Engineer (Salesforce)** requisition 276046,
targeting the published page
`https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/`.

The existing page is a good 12-section training track. This bundle does three things it does not do:

1. **Cross-reference** — proves, line by line, which JD bullet is covered and which is not.
2. **Deep dive** — expands every JD term into the settings, variations, commands and failure modes
   behind it.
3. **Verify** — replaces recalled UI labels and limit numbers with primary-source citations, and
   explicitly flags the places where the ecosystem's common vocabulary is out of date.

## 2. Constraints

- **No invented UI labels.** A wrong button name is a worse outcome than an admitted gap.
- **Everything must be teachable.** Each deep dive answers: where in the product do you go,
  what do you set, what breaks, how do you prove it.
- **Bank context.** Requisition 276046 is Commercial Banking Engineering, Toronto, regulated
  environment. Anything that weakens auditability or segregation of duties is called out.
- **Collapsible format.** The user asked for "deeper documentation into collapsible sections".
  The merge round should render each deep dive as `<details><summary>…</summary>…</details>` inside
  the existing page rather than creating a wall of prose.

## 3. JD → research artifact matrix

### 3.1 Responsibilities ("In this role, you will")

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

### 3.2 Qualifications ("Do you have the skills that will enable you to succeed")

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

## 4. Key Salesforce principles the research is anchored to

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

## 5. Method

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

## 6. Source policy and confidence rubric

| Tag | Meaning |
|---|---|
| `verified` | Primary source (official product docs, plugin source, official developer guide) states it directly. |
| `vendor-claim` | Vendor documentation states it; not independently confirmed in a live org. |
| `unverified` | Could not be confirmed. Recorded in the "Unverified" section with what would confirm it. |
| `correction` | A widely repeated claim that the primary source contradicts. |

**Rule applied throughout:** if a button label, product name, tier name or screen path could not
be found in current vendor documentation, the artifact says "not a current documented label" and
names the actual label instead. It never guesses.

## 7. Deliverables

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

## 8. Out of scope

- Writing the final merged page (the merge round owns that).
- Pricing/licensing negotiation advice.
- Any claim about what Scotiabank actually runs. The posting does not say; everything about their
  pipeline in this bundle is framed as "what a bank of this shape typically does", never as fact.
