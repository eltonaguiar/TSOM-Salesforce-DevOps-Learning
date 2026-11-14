# Salesforce DevOps Research — Consolidated Review Copy

| Field | Value |
|---|---|
| **Worktree / agent** | `salesforcemore-v2` (Kilo) |
| **Consolidated (UTC)** | 2026-11-14T02:35:07Z |
| **Source run folder** | `research/2026-11-14T021057Z_salesforcemore-v2/` (PR #2) |
| **Target role** | DevOps Engineer (Salesforce), Scotiabank requisition 276046 |
| **Merge target** | `docs/salesforce/devops-engineer/` on the published ServiceNow/Salesforce training site, plus sibling Salesforce guides |
| **Status** | Round 1 research — ready for review/merge |
| **Contains secrets / customer data** | No |

This is a single-file review copy of the round-1 research run. The canonical, split version with per-file provenance lives in the source run folder and [PR #2](https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning/pull/2). Sections below are the original files, concatenated in reading order.

## Contents

1. Bundle manifest
2. Plan and method
3. Salesforce key principles
4. Release model
5. Apex governor limits
6. Other limits, system settings, and org properties
7. Metadata dependencies and deployment constraints
8. Limits inspection and interview drills
9. DevOps tool landscape
10. Gearset click-paths
11. Copado, AutoRABIT, DevOps Center, Change Sets, and CLI
12. GitHub Actions + Salesforce CI/CD
13. Auth, secrets, environments, and approvals
14. Azure DevOps and GitLab equivalents
15. Certification landscape
16. Salesforce credential curricula
17. Vendor certifications and study plan
18. Term index
19. Term-by-term deep dives
20. Merge map
21. Content gaps and recommendations
22. Cross-bundle notes and reconciliation
23. Sources
24. Job description and requirement mapping

## Review notes — verified corrections in this copy

- **Metadata API deploy ceiling:** approximately **39 MB compressed** (the base64-encoded request cannot exceed 50 MB) / approximately **600 MB uncompressed**; **10,000 files** for an unlocked or second-generation managed package, **35,000** for an AppExchange-reviewed first-generation managed package. Source: Metadata API `deploy()` reference.
- **Test levels:** there are **five**, not four: `NoTestRun`, `RunSpecifiedTests`, `RunRelevantTests` (Beta, API 66.0+), `RunLocalTests`, `RunAllTestsInOrg`.
- **Deployment queue:** only one deployment runs at a time per org; queued deployments are not guaranteed to execute in submission order. Submit in order one at a time when order matters.
- **Gearset:** the current documentation groups the product into My connections, Metadata deployments, Continuous delivery, Backup & archiving, Sandbox seeding & compliance, Problem analyzers, Observability, and Settings. Gearset does **not** perform or schedule the Salesforce sandbox refresh.
- **Copado / AutoRABIT:** current product names are Copado CI/CD, Copado Essentials, Agentia, Robotic Testing; AutoRABIT ARM, Vault, CodeScan, Guard. Older generic module names are not current branding.
- **Certifications:** PD1 is current; Advanced Administrator is now **Platform Administrator II** with **Platform Administrator** as a prerequisite; there is no official Salesforce DevOps Engineer certification.
- **Caveats:** vendor UI labels drift by edition; certification weights are intentionally omitted pending the current official exam guide; platform limits can change without notice.
- **Safety:** no secrets, org auth files, consumer keys, certificates, customer data, or invented bank policy.

---

<!-- ===== begin: README.md ===== -->

# Research bundle — Salesforce DevOps Engineer (Scotiabank 276046)

| Field | Value |
|---|---|
| Bundle | `2026-11-14T021057Z_salesforcemore-v2` |
| Worktree | `salesforcemore-v2` |
| Agent | kilo |
| Research date | 2026-11-14 |
| Job | DevOps Engineer (Salesforce), Scotiabank, Toronto, Requisition 276046 |
| Job URL | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| Downstream page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| Status | Research complete for merge round 2; no secrets or customer data included |

## What this bundle is

This is a structured research package, not the final page. It is designed so a second agent can merge the material into the existing DevOps training page without re-researching it.

The research is split into small files so the merge agent can accept, reject, or rewrite each unit independently. Every file starts with a "merge target" line naming the section of the downstream page it belongs to.

## How to read the bundle

| Folder | What it contains | Merge disposition |
|---|---|---|
| `00-source-log/` | Job description, source URLs, access date, confidence notes | Reference only; do not paste wholesale into the page |
| `01-salesforce-key-principles/` | The platform principles that justify the release model | Merge as framing / "why" material |
| `02-limits-constraints/` | Governor limits, org/platform limits, system settings, metadata dependencies, deployment constraints, inspection and drills | Merge into section 13 of the page; highest priority |
| `03-devops-tools/` | Tool landscape; Gearset, Copado, AutoRABIT, DevOps Center click-paths; Change Sets vs CLI | Merge into sections 6 and 6.1 |
| `04-cicd/` | GitHub Actions + Salesforce pipeline, JWT auth, environments, secrets, Azure/GitLab equivalents | Merge into sections 5 and 5.1 |
| `05-certifications/` | Certification landscape, Salesforce credential curricula, vendor certificates, study plan | Merge into the Certifications section and section 14 |
| `06-term-deep-dives/` | Term index and term entries for every posting line | Merge into section 14 |
| `07-merge/` | Merge map and content-gap recommendations | Instructions for the merge agent, not page content |
| `08-cross-bundle-notes.md` | Reconciliation with the sibling `2026-11-14T020300Z-kilo-salesforceagain` bundle and verified corrections | Read before merging; do not paste into the page |

## What is safe to merge as-is

- The limits tables, dependency tables, constraints tables, and the CLI/UI inspection table in `02-limits-constraints/`.
- The GitHub Actions workflow and the "why this shape" notes in `04-cicd/`.
- The tool click-path tables in `03-devops-tools/`, with the caveat that vendor labels drift.
- The certification landscape and study plan, with the "verify current exam guide" note intact.

## What needs a human decision before merge

- **Vendor click-paths.** Gearset, Copado, AutoRABIT, and DevOps Center change menu labels between editions. Keep the "verify in your tenant" caveat. Never present a click-path as guaranteed for every edition.
- **Exact limits.** The Apex governor table is taken from the current Salesforce limits page; platform limits and metadata payload ceilings change. Keep the "verify current release" note.
- **Certification exam weights.** Do not publish percentages from memory. Use the topic domains and official study-guide links; let the merge agent add current weights only from the official exam guide PDF.
- **Bank-specific process.** The Scotiabank change-control specifics are not public. The research describes a defensible regulated-environment pattern, not Scotiabank's internal procedure.

## What must not be merged

- Any credential, org auth file, JWT key, consumer secret, or customer data. None is included.
- Any claim that a vendor UI path is universal across editions.
- Any claim that a Salesforce "DevOps Engineer" certification officially exists. It does not; the page must say so.
- Any invented Scotiabank policy, approver name, tool licence, or environment name.

## Confidence summary

| Area | Confidence | Why |
|---|---|---|
| Apex governor limits | High | Official Salesforce limits page, checked 2026-11-14 |
| Metadata dependency behaviour | High | Documented Metadata API behaviour and repeated field experience |
| Deployment constraints | High | Documented platform behaviour |
| GitHub Actions + Salesforce pattern | High on mechanics; medium on bank-specific approval flow | Mechanics are standard; the approval flow is a design choice |
| Gearset click-paths | Medium | Public docs and UI conventions; labels vary by edition |
| Copado / AutoRABIT / DevOps Center click-paths | Medium | Category-level accuracy; edition-specific labels must be verified |
| Certification curricula | Medium | Official credential pages and study-guide titles; current exam weights need the official exam guide |
| Scotiabank internal process | Low / not public | Not asserted; the bundle describes a regulated-environment pattern |

## Next action

Give this folder to the merge agent with `07-merge/merge-map.md`. The merge agent should update the downstream page, keep the collapsible `<details>` structure, and preserve the "verify at time of use" caveats.

<!-- ===== end: README.md ===== -->

---

<!-- ===== begin: PLAN.md ===== -->

# PLAN — structured research approach

## 1. Objective

Produce a merge-ready research package for the Salesforce DevOps Engineer (Scotiabank requisition 276046) training page, with emphasis on:

1. Salesforce key principles and the release-engineering model they justify.
2. Governor limits, other platform/org limits, system settings and org properties, metadata dependencies, and deployment constraints.
3. Practical, technical use of each DevOps tool, including Gearset UI click-paths for compare/deploy, backup, CI, pipelines, monitoring, and audit.
4. A GitHub Actions + Salesforce CI/CD pipeline and the reasons behind each design choice.
5. Research on the certifications named in the posting (PD1, Advanced Admin / Platform Administrator II, and "DevOps related certs") and their curricula.
6. A term-by-term deep dive for every line in the posting.

## 2. Method

### 2.1 Source hierarchy

1. **Official Salesforce documentation** — Metadata API, Apex limits, sandbox docs, deployment docs, credential pages.
2. **Official vendor documentation** — Gearset docs, Copado docs, AutoRABIT docs, Salesforce DevOps Center help.
3. **Reputable secondary sources** — Trailhead study guides, vendor academies, well-known DevOps write-ups. Used only when the first two are inaccessible, and labelled as secondary.
4. **Job posting** — treated as the scope contract. Every bullet is mapped to a research file.

### 2.2 Work sequence

1. Capture the posting and split it into atomic requirements.
2. Map each requirement to a page section and a research file.
3. Research the "why" first (principles), then the "what" (limits, dependencies, constraints), then the "how" (tools, pipeline, click-paths).
4. Write each unit with: definition, why the role cares, concrete example, failure mode, interview line.
5. Mark every fact that can change with a verify-at-time-of-use note.
6. Produce the merge map so a second agent can integrate without guessing.

### 2.3 Quality bar

- No invented UI paths presented as universal.
- No certification percentages without the current official exam guide.
- No secrets, customer data, or org auth files.
- Every claim that matters to an interview has a concrete example or command.
- Every table has a "what to do" column, not just a definition.

## 3. Salesforce key principles used as the spine

These are the principles the downstream page should keep repeating. They explain why the release model looks the way it does.

| Principle | What it means for release engineering | Where it appears |
|---|---|---|
| **Git is the source of truth** | The org is a deploy target. Setup edits that are not in Git are drift. | `01-salesforce-key-principles/`, `06-term-deep-dives/` |
| **A deploy is a compile against the target** | The Metadata API resolves dependencies in the payload and enforces the target's tests and limits. | `02-limits-constraints/dependencies.md` |
| **Promote one artifact** | Build/validate once, promote the same commit or package version through environments. | `04-cicd/`, `06-term-deep-dives/` |
| **Least privilege and segregation of duties** | The integration user deploys; a human approves; the author does not approve their own change. | `04-cicd/auth-secrets-environments.md`, `06-term-deep-dives/` |
| **Environment parity, not environment branches** | Configure the target; do not fork the codebase per environment. | `01-salesforce-key-principles/` |
| **Test against the org you will change** | A green Dev test is not evidence for UAT or Prod. | `02-limits-constraints/`, `04-cicd/` |
| **Bulkify by default** | A deploy can be green and the feature can fail at 200 or 10,000 records. | `02-limits-constraints/governor-limits.md` |
| **Make metadata modular** | Permission sets, packages, subflows, and custom metadata reduce conflicts. | `01-salesforce-key-principles/`, `06-term-deep-dives/` |
| **Design for reversibility** | A tag, a previous package version, and a Flow-version mitigation are part of the design. | `06-term-deep-dives/` |
| **Mask before you share** | A Full sandbox is a customer-data copy until masking completes. | `06-term-deep-dives/`, `02-limits-constraints/system-settings.md` |
| **Evidence is part of the deploy** | Ticket, diff, approval, deploy ids, test results, tag, mask confirmation. | `06-term-deep-dives/`, `04-cicd/` |
| **Observability after deploy** | A deploy is not done until the smoke test, the API usage check, and the business check pass. | `04-cicd/`, `02-limits-constraints/inspection-and-drills.md` |

## 4. Research questions

### Limits and constraints

- Which Apex governor limits are per transaction, which are per org, and which are per 24 hours?
- What is the difference between a governor limit and an org allocation?
- Which "system properties" (feature enablement, settings, secrets, certificates, SSO, email deliverability) are not normal metadata?
- Which metadata dependencies cause the common deploy errors, and what is the deploy order?
- Which constraints cannot be solved by a deploy at all (data, secrets, managed packages, feature switches)?

### Tools

- What does each vendor layer add over the Metadata API and the `sf` CLI?
- Where in Gearset do you compare, deploy, validate, run CI, build a pipeline, back up, restore, monitor drift, and read the audit history?
- What are the equivalent paths in Copado, AutoRABIT, and DevOps Center?
- When is a Change Set still acceptable, and why is it not the answer at this scale?

### CI/CD

- What are the minimum jobs in a Salesforce pipeline, and what does each one prove?
- How does JWT authentication work, and where do the secrets live?
- Why is a quick deploy not the same as a validation?
- How do GitHub Environments, required reviewers, branch protection, and environment-scoped secrets implement segregation of duties?
- What changes when the same pipeline runs in Azure DevOps or GitLab?

### Certifications

- Which credentials does the posting actually name, and what are their current official names?
- What does each exam cover, and which domains overlap release engineering?
- Is there an official Salesforce DevOps certification? (No.)
- Which vendor certificates are worth listing, and what do they prove?
- What is a realistic study order for this role?

## 5. Deliverables

| File | Purpose |
|---|---|
| `00-source-log/SOURCES.md` | Source URLs, access date, confidence |
| `00-source-log/job-description.md` | Posting captured and split into requirements |
| `01-salesforce-key-principles/principles.md` | The principles spine |
| `01-salesforce-key-principles/release-model.md` | Environments, branching, promotion, control gates |
| `02-limits-constraints/governor-limits.md` | Apex governor limits and bulkification |
| `02-limits-constraints/other-limits-and-system-settings.md` | Org/platform limits and system properties |
| `02-limits-constraints/dependencies-and-constraints.md` | Metadata dependencies and deployment constraints |
| `02-limits-constraints/inspection-and-drills.md` | UI/CLI inspection and interview drills |
| `03-devops-tools/tool-landscape.md` | Tool comparison and selection |
| `03-devops-tools/gearset-click-paths.md` | Gearset practical click-paths |
| `03-devops-tools/copado-autorabit-devopscenter.md` | The other tools and Change Sets |
| `04-cicd/github-actions-salesforce.md` | Pipeline stages, YAML, why |
| `04-cicd/auth-secrets-environments.md` | JWT, secrets, environments, approvals |
| `04-cicd/other-ci-platforms.md` | Azure DevOps and GitLab mapping |
| `05-certifications/certification-landscape.md` | What the posting names and what exists |
| `05-certifications/salesforce-credentials.md` | PD1, App Builder, Admin, Admin II curricula |
| `05-certifications/vendor-and-study-plan.md` | Vendor certs and study plan |
| `06-term-deep-dives/term-index.md` | Every posting term mapped to a file |
| `06-term-deep-dives/term-entries.md` | Term-by-term deep dives |
| `07-merge/merge-map.md` | File → page section mapping |
| `07-merge/content-gaps.md` | What the current page lacks and what to change |
| `08-cross-bundle-notes.md` | Reconciliation with the sibling `salesforceagain` bundle and verified corrections |

## 6. Open questions for the merge agent

1. Does the downstream page want full click-paths, or a compact table plus a caveat? The research provides both a table and detail so the merge agent can choose.
2. Should the certification section keep exact exam weights? Recommendation: no, unless the current official exam guide PDF is fetched and cited. Use domains and study-guide links.
3. Should the GitHub Actions YAML be inline on the page or linked? Recommendation: inline in a collapsible block, with a short "why" table outside it.
4. Should the page mention Scotiabank by name in the body? Recommendation: only in the header and the JD matrix. The body should describe a regulated-bank pattern, not an internal procedure.
5. Should vendor click-paths be labelled with a "last verified" date? Recommendation: yes, with the research date and a "labels drift" warning.

## 7. Acceptance criteria

- Every posting bullet has a mapped research unit.
- Every limits table has a source and a verify note.
- Every tool has a practical example and a failure mode.
- The pipeline has a runnable YAML and a "why" explanation.
- The certification research distinguishes official Salesforce credentials from vendor certificates.
- The merge map is sufficient for a second agent to integrate without re-reading the whole bundle.
- No secrets, customer data, or invented bank policy.

<!-- ===== end: PLAN.md ===== -->

---

<!-- ===== begin: 01-salesforce-key-principles/principles.md ===== -->

# Salesforce key principles for release engineering

**Merge target:** framing material for the page intro and section 12 (design patterns). Keep each principle short; the value is the release-engineering consequence, not the definition.

## 1. Git is the source of truth; the org is a deploy target

**Principle.** Every metadata change has a commit, a branch, a review, and a tag. Production is a target, not a workspace.

**Release consequence.** If Setup and Git disagree, the pipeline cannot tell which state is intended. Treat the difference as drift: retrieve it, review it, decide which side is correct, and record the decision.

**Anti-pattern.** "I changed it in production, I will copy it to Git later." Later never comes, and the next deploy silently reverts the change.

**Interview line.** "If Setup and Git disagree, that is an incident, not a workflow."

## 2. A deploy is a compile against the target

**Principle.** The Metadata API validates the payload against the target org. It resolves dependencies inside the payload, enforces the target's tests, and fails if the target cannot satisfy a reference.

**Release consequence.** Validate against the org you are about to change. A green deploy to Dev is not evidence for UAT or Prod.

**Anti-pattern.** "It worked in Dev" as a release argument.

**Interview line.** "A deploy is a compile against the target, not a file copy."

## 3. Promote one artifact

**Principle.** Build or validate once, then promote the same commit or package version through the environments. Do not rebuild from a different branch at each stage.

**Release consequence.** The artifact has an id: a commit SHA, a validation job id, a package version `04t...`, and a release tag. The runbook records it.

**Anti-pattern.** Rebuilding the release from a `uat` branch that no longer matches the release branch.

**Interview line.** "One artifact, many targets. The artifact is promoted; the environment is configured."

## 4. Least privilege and segregation of duties

**Principle.** The identity that deploys is not the identity that approves. The integration user has the minimum permissions to deploy; a human approves the production change.

**Release consequence.** The pipeline uses JWT auth with a dedicated integration user. Production has a protected environment with required reviewers. The author is not the approver.

**Anti-pattern.** A shared admin login in a CI secret, or the developer approving their own production deploy.

**Interview line.** "The integration user deploys, a human approves, and they are different identities."

## 5. Environment parity, not environment branches

**Principle.** Environments differ by configuration and data, not by forked code. The same metadata should work in every stage.

**Release consequence.** Put environment-specific values in named credentials, custom metadata, custom settings, or the target's configuration. Do not create a `uat` branch that can never merge.

**Anti-pattern.** `if (org.IsSandbox)` scattered through Apex, or a branch per environment.

**Interview line.** "Configure the target; do not fork the codebase."

## 6. Test against the org you will change

**Principle.** A test proves behaviour in the org where it ran. A Developer sandbox and production are different orgs with different data, features, and limits.

**Release consequence.** The validation that counts is a dry-run against the target. Production requires passing tests and 75% coverage when the payload contains Apex.

**Anti-pattern.** A 75% coverage result in Dev used as the production gate.

**Interview line.** "Validate against the target, not against the branch."

## 7. Bulkify by default

**Principle.** Apex and Flows run on collections, not single records. One SOQL for the collection, one DML for the list, no callouts in a loop.

**Release consequence.** A deploy can be green and the feature can fail at 200 or 10,000 records. Review asks: "What happens on 200 records? What happens on 10,000?"

**Anti-pattern.** SOQL or DML inside a loop.

**Interview line.** "A green unit test is not bulk evidence."

## 8. Make metadata modular

**Principle.** Small, single-purpose metadata merges and deploys better than monoliths. Permission sets per persona, subflows for parallel work, packages for real module boundaries, custom metadata for configuration.

**Release consequence.** Two stories do not collide in one 10,000-line profile or one Flow. The deploy payload is reviewable.

**Anti-pattern.** One `CB_Admin` permission set, one giant Flow, one profile edited by every story.

**Interview line.** "Design so the deploy is boring."

## 9. Design for reversibility

**Principle.** Metadata does not roll back by itself. Reversibility is a forward deploy of the last known-good tag, a previous package version, or a Flow-version activation.

**Release consequence.** Tag every successful production deploy. Keep the previous package version. Write the rollback owner into the runbook. Know that destructive deletes and data scripts are not undone by Git.

**Anti-pattern.** No tag, no previous version, and a verbal "we will figure it out."

**Interview line.** "If you do not have a tag from the last good production deploy, you do not have a rollback."

## 10. Mask before you share

**Principle.** A Full sandbox is a copy of production customer data. It is not safe for broad access until masking has run and access is limited.

**Release consequence.** A refresh is not complete when the copy finishes; it is complete when masking, integration cut-over, and access control are complete. Record who confirmed the mask.

**Anti-pattern.** An unmasked Full sandbox with broad logins; production data pasted into a ticket or a debug log.

**Interview line.** "Refresh is not done until masking and integration cut-over are done."

## 11. Evidence is part of the deploy

**Principle.** A regulated release needs proof: ticket, reviewed diff, approver, validation id, test results, production deploy id, tag, and mask evidence.

**Release consequence.** The pipeline writes the ids somewhere durable. The runbook is filled per release, not reconstructed after an incident.

**Anti-pattern.** "We deployed it and it worked" with no deploy id or approver.

**Interview line.** "The deploy is technical; the audit pack is the job."

## 12. Observability after deploy

**Principle.** A deploy is not done when the API returns success. It is done when the smoke test, the API usage check, and the business check pass.

**Release consequence.** Run a named smoke test, check Setup → Company Information → API Usage, and confirm the user-facing behaviour. Record the result in the runbook.

**Anti-pattern.** Declaring success because the deployment status says "Succeeded" while the Flow version is inactive or the named credential secret is missing.

**Interview line.** "Green deploy is not green feature. I verify activation, assignment, secrets, and a real user."

## How these principles land on the page

- Use principles 1–3 to open the page and justify the pipeline.
- Use principles 4, 11, 12 in the banking change-control section.
- Use principles 5, 8, 10 in the design-patterns and sandbox sections.
- Use principles 6, 7 in the tests/limits sections.
- Use principle 9 in the rollback section.
- Put the one-line interview answers in section 14.

<!-- ===== end: 01-salesforce-key-principles/principles.md ===== -->

---

<!-- ===== begin: 01-salesforce-key-principles/release-model.md ===== -->

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

<!-- ===== end: 01-salesforce-key-principles/release-model.md ===== -->

---

<!-- ===== begin: 02-limits-constraints/governor-limits.md ===== -->

# Apex governor limits — deep dive

**Merge target:** section 13.1 of the downstream page (new "Limits" section). This is the highest-priority research file for the posting's "understanding of Salesforce limits" requirement.

**Source:** [Apex execution governors and limits](https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html), accessed 2026-11-14. Verify the exact number in the current release before quoting it in an interview or a runbook.

## 1. What a governor limit is

A governor limit is a per-transaction ceiling enforced by the Apex runtime. It exists because Salesforce is multi-tenant: one runaway transaction must not monopolise shared resources. When you cross a limit, the runtime throws an uncatchable `System.LimitException`. You cannot `try/catch` your way out of it, and you cannot raise it with a support ticket.

A limit is not the same as an **org allocation**. The daily API request pool, the daily asynchronous Apex allocation, storage, and concurrent long-running requests are shared by the whole org. A limit is per transaction; an allocation is per org per day or per licence.

## 2. The per-transaction table

| Limit | Synchronous | Asynchronous |
|---|---:|---:|
| Total SOQL queries issued | 100 | 200 |
| Records retrieved by SOQL | 50,000 | 50,000 |
| Records retrieved by `Database.getQueryLocator` | 10,000 | 10,000 |
| Total SOSL queries issued | 20 | 20 |
| Records retrieved by a single SOSL query | 2,000 | 2,000 |
| Total DML statements issued | 150 | 150 |
| Records processed by DML, `Approval.process`, or `emptyRecycleBin` | 10,000 | 10,000 |
| Recursive trigger stack depth | 16 | 16 |
| Callouts (HTTP requests or web service calls) per transaction | 100 | 100 |
| Cumulative callout timeout | 120 seconds | 120 seconds |
| Methods with the `@future` annotation per invocation | 50 | 0 in batch/future contexts; 50 in Queueable |
| Apex jobs added with `System.enqueueJob` | 50 | 1 |
| `sendEmail` methods | 10 | 10 |
| Heap size | 10 MB | 25 MB (email services 50 MB) |
| CPU time on Salesforce servers | 10,000 ms | 60,000 ms |
| Maximum execution time per transaction | 10 minutes | 10 minutes |
| Push notification method calls | 10 | 10 |
| Push notifications per method call | 2,000 | 2,000 |
| `EventBus.publish` calls for immediately published platform events | 150 | 150 |
| Rows across all Apex cursors per transaction | 50 million | 50 million |
| `Cursor.fetch` calls per transaction | 100 | 100 |
| Rows across all Apex pagination cursors per transaction | 100,000 | 100,000 |
| Apex pagination cursor instances per transaction | 50 | 50 |
| Rows retrieved per page from a pagination cursor | 2,000 | 2,000 |

## 3. What the footnotes mean in practice

- **SOQL subqueries count.** A parent-child relationship subquery counts as an extra query. The subquery limit is three times the top-level limit. Row counts from subqueries contribute to the overall row count. Custom metadata queries are exempt from the SOQL query limit, but do not use that as an excuse to query in a loop.
- **These count as DML statements:** `Approval.process`, `Database.convertLead`, `Database.emptyRecycleBin`, `Database.rollback`, `Database.setSavePoint`, insert, update, upsert, delete, undelete, merge, `EventBus.publish` for after-commit events, and `System.runAs`.
- **Recursive triggers get a tighter stack.** A recursive trigger fires a new Apex invocation, which is more expensive than a recursive call in one invocation. The stack depth limit is 16.
- **Certified managed packages can get their own limits.** Certified AppExchange packages get a separate per-namespace allowance for most per-transaction limits; non-certified packages share the org's limits. Heap, CPU, transaction time, and namespace count are shared.
- **Scheduled Apex uses synchronous limits** even though it runs asynchronously.

## 4. Org-wide and 24-hour limits that surprise release engineers

| Limit | Value / shape | Why it matters to a release |
|---|---|---|
| Daily asynchronous Apex executions | `max(250,000, applicable licences × 200)` | A nightly batch plus a release's tests and queueables share it |
| Async elastic executions | Daily limit plus up to 2 million extra, throttled | Elastic is not a guarantee; do not design to it |
| Apex cursor instances | 10,000 per 24 hours | Cursor-based integrations can exhaust it |
| New cursor + pagination rows | 100 million per 24 hours | Large data jobs can hit it |
| Pagination cursor instances | 200,000 per 24 hours | Same |
| Concurrent long-running synchronous transactions (>5 s) | 10–50, based on licences, 100 licences per one concurrent transaction | Two simultaneous big deploys or data jobs can hit it |
| Concurrent scheduled Apex classes | 100 (5 in Developer Edition) | A release that schedules jobs can collide |
| Batch Apex jobs in flex queue `Holding` | 100 | Queue floods delay the release |
| Batch Apex jobs queued or active | 5 | Batch-heavy releases queue |
| Concurrent batch `start` methods | 1 | Start is serialized |
| Batch jobs submitted in a running test | 5 | Tests that submit batches are limited |
| Test classes queued per 24 h (production) | `max(500, 10 × test classes)` | A huge test suite can hit the queue |
| Test classes queued per 24 h (sandbox/DE) | `max(500, 20 × test classes)` | Same |

## 5. The bulkification failure

### 5.1 The bad pattern

```apex
// One SOQL and one DML per record. Passes on 1 record, dies on 200.
for (Account a : accounts) {
    Contact c = [SELECT Id FROM Contact WHERE AccountId = :a.Id LIMIT 1];
    c.Description = 'Reviewed';
    update c;
}
```

### 5.2 The good pattern

```apex
// One SOQL for the collection, one DML for the list.
Map<Id, Contact> contactsByAccount = new Map<Id, Contact>();
for (Contact c : [SELECT Id, AccountId FROM Contact WHERE AccountId IN :accounts]) {
    contactsByAccount.put(c.AccountId, c);
}

List<Contact> toUpdate = new List<Contact>();
for (Account a : accounts) {
    Contact c = contactsByAccount.get(a.Id);
    if (c != null) {
        c.Description = 'Reviewed';
        toUpdate.add(c);
    }
}
update toUpdate;
```

### 5.3 The review questions

1. **What happens on 200 records?** One trigger invocation, collections, one SOQL, one DML.
2. **What happens on 10,000 records?** Batch or Queueable, not a synchronous trigger.
3. **What happens if the callout is slow or down?** 100 callouts and 120 seconds cumulative; do not put HTTP in a loop.
4. **What happens if the same record is updated twice?** Recursion guard or a static flag.
5. **What happens when the test runs in an empty sandbox?** The test creates its own data.

## 6. Reading the limits at runtime

```apex
System.debug('SOQL  ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug('DML   ' + Limits.getDmlStatements() + '/' + Limits.getLimitDmlStatements());
System.debug('Rows  ' + Limits.getDmlRows() + '/' + Limits.getLimitDmlRows());
System.debug('Heap  ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
System.debug('CPU   ' + Limits.getCpuTime() + '/' + Limits.getLimitCpuTime());
System.debug('Calls ' + Limits.getCallouts() + '/' + Limits.getLimitCallouts());
```

Use this in long-running code to fail early with a useful message, not in production as a substitute for bulkification.

## 7. Test behaviour

- Limits apply individually to each test method.
- `Test.startTest()` gives the code inside a fresh set of limits. Use it so test data setup does not consume the code's budget.
- Batch Apex resets limits for each `execute` call.
- A test that inserts 200 records is the minimum proof of bulk safety. A test that queries `LIMIT 1` and assumes a row exists proves nothing about an empty sandbox.
- Tests that submit batch jobs are limited to 5 batch jobs in a running test.

## 8. Limit-aware design rules

- One SOQL for a collection; one DML for a list.
- No SOQL, DML, or HTTP callout inside a loop.
- Prefer before-save Flow or a before trigger for same-record field updates; do not use after-save to do work a before-save could do.
- Use Queueable for chaining and callouts; use Batch for volume; use Platform Events for decoupling.
- Do not chain Queueables past the async `enqueueJob` limit (1 per async transaction).
- Stub callouts with `HttpCalloutMock`; never call a live endpoint in a test.
- Keep heap in mind: large collections, JSON serialization, and string concatenation can hit CPU during heap checks.
- Test at 200 and 10,000 records.

## 9. Interview drills

1. **"What happens on 200 records?"** One trigger invocation, collections, one SOQL, one DML, no callouts in the loop.
2. **"A batch fails at 5,000 records but the unit tests pass."** Check CPU, heap, SOQL/DML inside `execute`, callout limits, and the daily async allocation.
3. **"The pipeline user gets `REQUEST_LIMIT_EXCEEDED` during a release."** Check API Usage, identify the consumer, stop retrying, move to a delta/off-peak window, use a dedicated CI user.
4. **"A trigger has 80% coverage but production rejects the deploy."** Coverage is per org for the deployed Apex; a managed package or an untested branch can pull the org below 75%. Run the real test level against the target.
5. **"A test passes in Dev and fails in QA."** The test depends on org data or a feature that exists only in Dev. Make the test create its own data.
6. **"A Flow times out under volume."** It is doing after-save work a before-save should do, querying per record, or launching too many interviews. Split it or move the bulk work to Apex/Queueable.

## 10. What to merge and what to leave out

**Merge:** the per-transaction table, the org-wide table, the bad/good Apex example, the review questions, the runtime `Limits` snippet, and the interview drills.

**Leave out or compress:** cursor and pagination rows unless the page has space; cross-namespace managed-package limits can be a short note. Do not turn the page into a copy of the Salesforce limits page.

<!-- ===== end: 02-limits-constraints/governor-limits.md ===== -->

---

<!-- ===== begin: 02-limits-constraints/other-limits-and-system-settings.md ===== -->

# Other limits, system settings, and org properties

**Merge target:** section 13.2 and 13.3 of the downstream page. This file covers the limits that are not per-transaction, and the per-org switches that a metadata deploy does not carry.

## 1. The five limit families

| Family | Scope | Example | Where it shows up |
|---|---|---|---|
| Apex governor limits | One transaction | 100 SOQL, 150 DML, 10 MB heap | Runtime `System.LimitException`; see `governor-limits.md` |
| Org/platform allocations | Whole org, often per 24 hours | API requests, async Apex, storage, concurrent long-running transactions | Pipeline or integration gets 403 / `REQUEST_LIMIT_EXCEEDED` |
| Metadata/deploy ceilings | One deploy/retrieve | Component count, payload size, test runtime | Large release fails or times out |
| Feature/configuration caps | Whole org | Custom objects, fields, permission sets, flows, validation rules | A story cannot add the component it needs |
| System settings / org properties | Whole org | Feature enablement, SSO, named credentials, certificates, email deliverability | Deploy succeeds, feature/auth fails |

## 2. API request limits

**What they are.** Every REST, SOAP, Bulk, and Metadata API request consumes the org's daily API allocation. The allocation depends on edition, licence types, and user count. The integration user does not get a separate unlimited bucket.

**Why a release engineer cares.** A pipeline that retrieves the whole org, runs a full test suite, and polls a deploy every second can consume a meaningful slice of the day's API calls. If the pipeline shares a user with production integrations, a busy release day becomes an integration outage.

**How to inspect.** Setup → Company Information → API Usage shows the last 24 hours and the allocation. The CLI can show org limits with `sf org list limits` and `sf limits api display` (confirm the command in your CLI version).

**How to stay under it.**
- Use delta manifests (`sfdx-git-delta`) instead of full retrieves.
- Use `--wait` on deploy/test commands instead of a tight poll loop.
- Schedule nightly validation off-peak.
- Use a dedicated integration user for CI.
- Cache what does not change.
- Split very large test suites; do not run `RunAllTestsInOrg` on every commit.

## 3. Metadata and deploy ceilings

Salesforce caps what one deploy or retrieve can contain. The current Metadata API `deploy()` reference lists:

- **Maximum compressed `.zip` size:** approximately **39 MB**. Metadata API base64-encodes the zip; the encoded result cannot exceed 50 MB, and base64 adds roughly 22%, so the compressed payload must stay under about 39 MB.
- **Maximum uncompressed folder size:** approximately **600 MB** (629,145,600 bytes), depending on the files' compression ratio.
- **Maximum files:** **10,000** for an unlocked or second-generation managed package; **35,000** for a first-generation managed package that passed AppExchange Security Review.

Source: [Metadata API `deploy()`](https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html), accessed 2026-11-14. Limits can change without notice; re-check before you quote them in an interview or a runbook.

**Why it matters.** A full-org retrieve or deploy is the classic way to hit the ceiling. It is also the classic way to make a release unreviewable. Delta manifests, package directories, and split payloads are the design response.

**Related constraints:**
- Test runtime: a large `RunLocalTests` can take a long time. Validate before the window and quick-deploy inside it.
- Coverage: production requires 75% when the payload contains Apex.
- API version: the target must support the source API version.
- Destructive changes: they are a separate manifest, not a side effect of absence.

## 4. Storage and data limits

Setup → Company Information → Storage shows data and file storage. Sandboxes have their own storage; a Developer sandbox cannot hold production-scale data. Tests and data loads consume storage. A full copy of production data into a sandbox is a licence, cost, and privacy decision, not just a technical one.

## 5. Concurrency limits

- **Only one deployment runs at a time per org.** You can submit multiple deployments, but the others remain in a queue. Queued deployments are **not necessarily executed in the order they were submitted**. To control the order, submit them one at a time after the previous deployment completes successfully. (Source: Metadata API `deploy()` reference.)
- Long-running synchronous transactions over 5 seconds: 10–50 concurrent, based on licences.
- Batch Apex: 5 concurrent jobs, 1 concurrent `start`, 100 holding in the flex queue.
- Deployments are long-running operations. Two deploys to one org can queue or conflict; serialize per org with a CI concurrency group or a deployment lock.

## 6. Email and Flow limits

- `sendEmail` is limited to 10 calls per transaction; org-wide daily email limits apply.
- Sandboxes often block email. Do not use email as a test signal; stub it.
- Flow has its own interview, scheduled-run, and version-history limits. A Flow that queries per record is still a limit problem even if the limit is not an Apex governor.

## 7. Custom object, field, and permission-set caps

Editions allocate maximum custom objects, fields, tabs, apps, and permission sets. A story can be valid metadata and still be blocked by the org's allocation. Check the edition allocation and the current usage before you promise a field. Permission-set sprawl is a design problem, not a platform cap you can ignore.

## 8. "System properties" — the per-org switches

In this research, "system properties" means the per-org settings that behave like platform switches: feature enablement, org preferences, endpoints, certificates, and secrets. They are not business data, and many do not travel cleanly in a metadata deploy.

| Setting / property | Setup path | Deployable like metadata? | Release consequence |
|---|---|---|---|
| Feature enablement: Person Accounts, Multi-Currency, CPQ, Field Service, Shield, Revenue Cloud, Sites, Omni-Channel | Feature Settings / Company Information / product settings | Usually an org switch, not a file | Dependent metadata fails or does nothing until the feature is enabled and licensed in the target |
| Company Information: org id, locale, time zone, default currency | Company Information | Org-specific | Never copy production's org id or locale into a sandbox |
| System Settings | Settings → System Settings | Some `*Settings` metadata types | Org-wide behaviour; review the diff, do not deploy blind |
| Apex Settings | Apex Settings | `ApexSettings` where supported | Debug-log retention and other behaviour differ by environment |
| Session Settings | Session Settings | `SessionSettings` | Timeout/caching changes can log users out or weaken security |
| Password and login policies | Security → Password Policies; Login IP Ranges | Some deployable, some org-specific | Do not weaken production policy to make a CI runner work; allowlist the runner |
| Connected Apps / External Client Apps | App Manager | Metadata plus per-org consumer key, secret, certificate | The consumer key is per org; the JWT certificate must be uploaded per org |
| Named Credentials / External Credentials | Named Credentials | Endpoint metadata; the secret is not retrieved | The callout works in Dev and fails in UAT because the secret/principal is missing |
| Remote Site Settings | Remote Site Settings | `RemoteSiteSetting` | Often org-specific; a missing entry blocks a callout at runtime |
| Certificates and Keys | Certificate and Key Management | Public certificate only; private key is not exported | JWT auth and mutual TLS fail until the private key is imported per org |
| Email Deliverability | Email Deliverability | Org setting, not normal metadata | Sandboxes often block email; choose the test setting deliberately |
| SSO / SAML | Single Sign-On Settings | Metadata plus IdP certificate | Sandbox IdP differs; test login before inviting UAT users |
| Sites / Digital Experiences / Guest User | Sites / Digital Experiences | Metadata plus per-org configuration | Guest-user access is a security review item |
| Sharing Settings / OWD | Sharing Settings | Object `sharingModel` plus `SharingRules` metadata | A deploy can widen data access; prove it with a real low-privilege user |
| API version / feature compatibility | Apex Classes; Company Information; project config | Project setting, not a deploy file | Align `sourceApiVersion` with the target |

## 9. Pre-flight checklist for a target org

1. Is the feature licensed and enabled?
2. Are the settings metadata types compatible with the target?
3. Are the named credential secrets, external credentials, and certificates present?
4. Are endpoints pointed at non-production systems?
5. Is email deliverability set for the test (and not sending to customers)?
6. Has SSO been tested with a real sandbox user?
7. Does the integration/deploy user have the right permissions (API Enabled, the deploy permissions, Author Apex where needed)?
8. Is the target API version supported?

If you cannot answer these before the window, you have a configuration risk, not a code risk.

## 10. What to merge

**Merge:** the five-family table, the API-usage caution, the metadata ceiling with the verify note, the system-settings table, and the pre-flight checklist.

**Compress:** the storage/flow/custom-object sections into a short table unless the page needs every category.

**Do not merge:** any exact API allocation number, because it is edition/licence-specific. Point to Setup → Company Information → API Usage instead.

<!-- ===== end: 02-limits-constraints/other-limits-and-system-settings.md ===== -->

---

<!-- ===== begin: 02-limits-constraints/dependencies-and-constraints.md ===== -->

# Metadata dependencies and deployment constraints

**Merge target:** section 13.4 and 13.5 of the downstream page, plus section 2 (failure table) and section 7 (conflict clinic). This is the research backing the posting's "metadata dependencies and deployment constraints" requirement.

## 1. The mental model

The Metadata API resolves dependencies **inside the payload**. It does not invent a parent that is missing from both the payload and the target. If a child references a parent the target does not have, the deploy fails with an error such as `invalid cross reference id`, `entity not found`, or "no such column."

A deploy is therefore a graph problem, not a file-copy problem.

## 2. Dependency graph

| Child component | Depends on | Typical error if parent is missing |
|---|---|---|
| Custom field | Custom or standard object | `no such column` / "field does not exist" |
| Validation rule | The fields it references | `no such column` |
| Record type | Object, business process, picklist values | `invalid cross reference id` |
| Page layout | Object, fields, related lists, record types | `invalid cross reference id` |
| Layout assignment | Profile or permission set + record type | Deploy succeeds; users see the wrong page |
| Permission set | Objects, fields, Apex classes, Flows, tabs, custom permissions | `entity not found` / missing component |
| Apex class | Other classes, custom objects/fields, metadata types | Compile failure in the target |
| Trigger | Handler class, object | Compile failure / `entity not found` |
| Flow | Objects, fields, Apex classes, subflows, custom metadata | Flow deploys but fails at runtime |
| LWC | Static resources, Apex controllers, custom labels | Component fails to load |
| FlexiPage (Lightning page) | Components, objects, fields | Page deploys but is not the active page |
| Custom metadata type | Records and references | `entity not found` |
| Named credential | External credential, auth provider, certificate | Callout fails at runtime |
| Connected app | Certificate, OAuth scopes | Login/auth fails |
| Unlocked/managed package | Its dependency versions | Install fails on a missing dependency |
| Sharing rule | Object, roles, groups | Rule deploys but does not grant the expected access |
| Queue / routing | Object, users, roles | Records route to the wrong place |

## 3. The rules that prevent most failures

1. **Deploy parent and child in the same payload when both are new.** Object + field + record type + layout + permission set is one reviewable unit. Do not deploy the object on Monday and the permission set "later."
2. **`package.xml` is a list, not a promise of order.** The API orders by metadata type internally, but an absent dependency is still absent.
3. **A dry-run against the target is the only honest dependency test.** A green deploy to Dev says nothing about UAT.
4. **Read the component name in the error and search the repo for the reference.** Add the missing parent; do not retry the same payload.
5. **Vendor dependency analysis is a suggestion, not an approval.** Gearset's problem analysis and Copado's dependency view can surface the missing component; a human reviews what was added.
6. **Do not use "ignore conflicts" in production.** It hides a real divergence between Git and the org.

## 4. A manifest that ships the whole record-type story

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <types>
    <members>Invoice__c</members>
    <name>CustomObject</name>
  </types>
  <types>
    <members>Invoice__c.Status__c</members>
    <name>CustomField</name>
  </types>
  <types>
    <members>Invoice__c.Invoice_Layout</members>
    <name>Layout</name>
  </types>
  <types>
    <members>CB_Invoice_User</members>
    <name>PermissionSet</name>
  </types>
  <version>60.0</version>
</Package>
```

Use your project's API version, not the one in the example. The point is the shape: parent, child, assignment, and access in one reviewable unit.

## 5. Deployment constraints

These are the things a deploy cannot fix by including another component.

| Constraint | What it means | What you do instead |
|---|---|---|
| Feature not enabled in target | The metadata is valid but the target cannot accept or use it | Enable and license the feature first; re-validate |
| Secret is not metadata | Named credential passwords, private keys, and some connected-app values are not retrieved | Re-enter per org, use external credentials, or a secret manager; never commit them |
| Certificate private key is not exported | You can deploy the public cert, not the private key | Import the private key per org; test JWT auth |
| Managed package component is read-only | You cannot edit its Apex or metadata in Git | Configure around it, extend it, or upgrade the package |
| Profile is a monolith | Two stories editing the same profile conflict; a bad merge changes access | Ship permission sets; decompose profiles with a tool; require a second reviewer |
| Flow XML does not merge | Two developers on one Flow lose work | One owner per Flow per release; split into subflows |
| Destructive changes are separate | Deleting metadata is not "it was absent from the folder" | Use `destructiveChanges.xml`; accept that records on a deleted object are gone |
| Tests and 75% coverage | Production rejects Apex without passing tests and coverage | Run `RunLocalTests` or named tests; fix the tests, do not lower the bar |
| API version mismatch | The target may not support the source API version | Align `sourceApiVersion`; validate before the window |
| Record type assignment | The record type file is not the assignment | Deploy layout assignment and visibility in the same payload |
| Lightning page activation | A FlexiPage can deploy and still not be the active page | Activate it for the app/record type in the target |
| Named credentials / remote sites / certs | Endpoints and trust are per org | Configure per sandbox; include it in the pre-flight checklist |
| Data is not metadata | Records, attachments, and customer data do not ride in a metadata deploy | Use a data migration/seed process; mask and ticket it |
| Change Sets only work between related orgs | No Git diff, no CLI, no rollback | Use the CLI or a vendor pipeline with Git in front |
| Sandbox refresh overwrites | A refresh replaces metadata and data | Re-deploy from Git and re-run masking after refresh |
| Deploy user permissions | The integration user needs API access and deploy permissions | Use a dedicated user with a least-privilege deploy permission set |
| Concurrent deploys | Two deploys to one org can conflict or queue unpredictably; only one deployment runs at a time, and queued deployments are not guaranteed to run in submission order | Serialize per org with a concurrency group or deployment lock; submit in order one at a time |
| Hard-coded ids | The id in Dev is not the id in UAT | Use custom metadata, custom settings, or a query by developer name |
| `NoTestRun` in production | Rejected when the payload contains Apex | Use `RunSpecifiedTests` or `RunLocalTests` |
| "Ignore conflicts" | Hides a real divergence between Git and the org | Do not use it in production; fix the source of truth |

## 6. Destructive changes

A delete is a separate manifest:

```bash
sf project deploy start \
  --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChanges.xml \
  --target-org qa
```

Use pre-destructive changes only when the delete must happen before the add (for example, a rename that would collide). A delete in production is not undone by Git. Rollback of a delete means recreating the metadata, and any records that lived on a deleted object are gone.

## 7. Test levels — five, not four

The Metadata API `TestLevel` enum has five values. The older four-level answer is incomplete.

| Level | What it runs | When to use |
|---|---|---|
| `NoTestRun` | No tests | Development environments only; rejected in production when the payload contains Apex |
| `RunSpecifiedTests` | Only the tests you name | Fast, targeted validation; each deployed class/trigger must be covered to 75% by those tests |
| `RunRelevantTests` (Beta) | Only tests relevant to the deployment payload, identified from the payload and its dependencies | API version 66.0+; Apex-heavy deployments where you want test time to scale with the payload; annotate test classes for fine-grained control |
| `RunLocalTests` | All tests in the org except managed/unlocked package tests | The default for production deployments that include Apex; slower but honest |
| `RunAllTestsInOrg` | All tests, including managed-package tests | Rarely; very slow and usually not necessary for a release |

Source: [Metadata API `deploy()`](https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html) and the [Salesforce CLI deploy messages](https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md), accessed 2026-11-14.

**Interview line.** "There are five test levels. `RunRelevantTests` is the Beta level that runs tests relevant to the payload on API 66.0+. I still use `RunLocalTests` when I need the broadest honest gate before production."

## 8. Troubleshooting method

```text
1. Save the full error and the deploy id.
2. Identify the component and the missing reference.
3. Search the repo for the reference; is the parent in the payload?
4. Add the parent to the same payload, or deploy the parent first.
5. Re-run the dry-run against the same target.
6. If a test failed, read the stack trace; do not change the test level to hide it.
7. If coverage failed, find the uncovered lines.
8. If it is a managed package, stop; upgrade or configure around it.
9. Only then change code.
```

## 9. Error-to-fix quick table

| Error | First check | Fix |
|---|---|---|
| `no such column` / field does not exist | Is the field in the payload? Is it in the target? | Add the field or deploy the object+field first |
| `invalid cross reference id` | Record type, layout, or business process parent | Add the parent to the same payload |
| `entity not found` | Apex/Flow dependency or missing metadata type | Deploy the dependency or remove the reference |
| Test failure only in UAT/Prod | Test uses org data, a profile, a record type, or a setting that exists only in Dev | Make the test create its own data; use the target's test level |
| Coverage below 75% | Untested branches, managed package exclusion | Add meaningful tests; do not lower the bar |
| `CANNOT_MODIFY_MANAGED_OBJECT` | You tried to change a managed component | Configure around it or upgrade the package |
| Deploy succeeds but Flow is old | New version is not active | Activate the version or deploy as active |
| Record type deploys but users cannot create | Missing business process, picklist value, layout assignment, or visibility | Deploy all four together |
| Layout deploys but page is wrong | Layout not assigned; Lightning page not activated | Deploy the assignment and activate the page |
| Callout works in Dev, fails in UAT | Missing named credential secret, external credential, certificate, remote site, or endpoint | Configure per org |
| `REQUEST_LIMIT_EXCEEDED` | API usage, async queue, or concurrency | Check Setup → Company Information → API Usage; reduce/serialize/off-peak |

## 10. What to merge

**Merge:** the dependency graph, the six rules, the record-type manifest, the constraints table, the destructive-change warning, the troubleshooting method, and the error-to-fix table.

**Compress:** the full graph if the page is already long; keep the rows that match the posting (profiles, permission sets, record types, layouts, Flows, Apex).

**Do not merge:** any claim that a specific vendor's dependency analysis is authoritative. It is a suggestion.

<!-- ===== end: 02-limits-constraints/dependencies-and-constraints.md ===== -->

---

<!-- ===== begin: 02-limits-constraints/inspection-and-drills.md ===== -->

# Inspecting limits and drilling the limits story

**Merge target:** section 13.6 and 13.7 of the downstream page. This file is the practical "where do I look?" companion to the limits tables.

## 1. UI and CLI inspection map

| What you need | UI path | CLI / code |
|---|---|---|
| API usage and allocation | Setup → Company Information → API Usage | `sf org list limits`; `sf limits api display` |
| Storage | Setup → Company Information → Storage | `sf org list limits` |
| Apex jobs / batch queue | Setup → Apex Jobs; Setup → Background Jobs | Job listing varies by CLI version |
| Test results and coverage | Setup → Apex Test Execution | `sf apex run test --code-coverage --result-format human --wait 30` |
| Deploy status and id | Setup → Deploy → Deployment Status | `sf project deploy report --job-id <id>` |
| Debug logs | Setup → Debug Logs | `sf apex tail log`; `sf apex get log` |
| Org identity and instance | Setup → Company Information | `sf org display --target-org <alias>` |
| Runtime counters | Debug log / `Limits` class | `Limits.getQueries()`, `getDmlStatements()`, `getHeapSize()`, `getCpuTime()` |

## 2. Useful command set

```bash
# Who am I connected to?
sf org display --target-org uat

# What does the org say about its limits?
sf org list limits --target-org uat
sf limits api display --target-org uat

# Run the honest test gate and capture coverage
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 60 --target-org uat

# On API 66.0+, the Beta level runs only tests relevant to the payload
sf project deploy start --manifest manifest/package.xml \
  --test-level RunRelevantTests --target-org uat --wait 60

# What happened to that validation/deploy?
sf project deploy report --job-id <job-id> --target-org uat

# Preview what a deploy would do
sf project deploy preview --manifest manifest/package.xml --target-org uat
```

CLI flags move. Confirm with `sf <command> --help` before you put a command in a runbook.

## 3. Limit-aware design checklist

- [ ] One SOQL for a collection, one DML for a list.
- [ ] No SOQL, DML, or HTTP callout in a loop.
- [ ] Before-save Flow for same-record field updates; after-save for side effects.
- [ ] Queueable for chaining/callouts; Batch for volume; Platform Events for decoupling.
- [ ] No Queueable chaining past the async `enqueueJob` limit.
- [ ] `HttpCalloutMock` in tests; no live endpoint.
- [ ] Test at 200 and 10,000 records.
- [ ] `Test.startTest()` around the code under test.
- [ ] `Limits` checks in long-running code to fail early.
- [ ] API usage checked before a release.
- [ ] Deploys serialized per org.
- [ ] Delta payload, not full-org.

## 4. Interview drills (limits and constraints)

1. **"What happens on 200 records?"** One trigger invocation, collections, one SOQL, one DML, no callouts in the loop.
2. **"A batch fails at 5,000 records but the unit tests pass."** Check CPU, heap, SOQL/DML inside `execute`, callout limits, and the daily async allocation.
3. **"The pipeline user gets `REQUEST_LIMIT_EXCEEDED` during a release."** Check API Usage, identify the consumer, stop retrying, move to a delta/off-peak window, use a dedicated CI user.
4. **"The deploy fails at the component limit."** Split the payload or use delta/package deployments; do not open a support ticket first.
5. **"The deploy is green but the feature is broken."** Check feature enablement, named credential secret, certificate, remote site, record type assignment, Lightning page activation, and Flow version.
6. **"A record type deploys and users cannot create it."** Missing business process/picklist values, missing layout assignment, or missing profile/permission-set visibility.
7. **"A Flow deploys and users see the old screen."** The new version is not active.
8. **"A callout works in Dev and fails in UAT."** Named credential secret, external credential, certificate, remote site setting, or endpoint.
9. **"Why is a 75% coverage result in Dev not enough?"** Coverage is per org; the target's tests and the target's package context decide whether production accepts the deploy.
10. **"What does a Git revert not undo?"** Data changes, destructive deletes, activated Flow versions, and any post-deploy script that already ran.
11. **"Name the five test levels."** `NoTestRun`, `RunSpecifiedTests`, `RunRelevantTests` (Beta, API 66.0+), `RunLocalTests`, `RunAllTestsInOrg`.
12. **"Two teams submit deployments at 9 a.m. Which one runs first?"** Only one deployment runs at a time per org; queued deployments are not guaranteed to run in submission order. Serialize or submit one at a time.

## 5. What to merge

**Merge:** the inspection map, the useful command set (with the `--help` caveat), the checklist, and drills 1–8.

**Compress:** drills 9–10 if the page already covers them in the tests and rollback sections.

**Do not merge:** command flags without a "confirm with `--help`" note. CLI syntax changes more often than the concepts.

<!-- ===== end: 02-limits-constraints/inspection-and-drills.md ===== -->

---

<!-- ===== begin: 03-devops-tools/tool-landscape.md ===== -->

# DevOps tool landscape

**Merge target:** section 6 and 6.1 of the downstream page. This file explains what each tool is, what it adds over the Metadata API, and when to choose it.

## 1. The layer cake

```text
Business process: ticket, approval, change window, evidence
        ↑
Vendor platform: Gearset / Copado / AutoRABIT / DevOps Center
  - diff, dependency analysis, CI job, pipeline, approval gate,
    backup, data deployment, monitoring, audit history
        ↑
Salesforce CLI (sf) and Metadata API
  - retrieve, deploy, validate, test, package, report
        ↑
Git + CI runner (GitHub Actions, Azure DevOps, GitLab)
  - source of truth, branch protection, secrets, environments
        ↑
Salesforce orgs: Dev, QA, UAT, Pre-Prod, Prod
```

Every vendor tool is a UI and automation layer over the Metadata API. None of them replaces Git discipline, a test gate, or a rollback tag.

## 2. Tool-by-tool summary

| Tool | What it is | What it adds | What it does not replace |
|---|---|---|---|
| Salesforce CLI (`sf`) | The deploy/retrieve/test/package engine | Scriptability, CI integration, exact control over payload and flags | Git, approvals, a UI for admins |
| DevOps Center | Native Salesforce work items, Git, pipelines | No extra vendor; work-item traceability; native promotion | Vendor-grade dependency analysis, data tooling, backup |
| Gearset | Metadata deployments, continuous delivery (CI jobs, pipelines, org monitoring), backup & archiving, sandbox seeding & compliance, problem analyzers | Org/branch diff, dependency hints, CI jobs, approval pipelines, backup/restore, masking/seeding, monitoring | Git as source of truth; the CLI in CI; the Salesforce sandbox refresh itself |
| Copado | Copado CI/CD (enterprise), Copado Essentials (small teams), Agentia (AI layer), Robotic Testing | Release management, approvals, quality gates, audit evidence | Git hygiene; the Metadata API |
| AutoRABIT | ARM (CI/CD), Vault (backup/restore), CodeScan (static analysis), Guard (security posture) | CI/CD, data backup/restore, static analysis, security/compliance | Git hygiene; the Metadata API |
| Change Sets | Setup UI between related orgs | Nothing that scales | Diff, CLI, rollback, branch model, audit-grade evidence |

## 3. Selection matrix

| Situation | Best fit | Why |
|---|---|---|
| Large bank, multi-vendor, audit-heavy, existing Gearset | Gearset metadata deployments + continuous delivery + backup & archiving, with GitHub Actions for the gate | Strong diff and problem analyzers; CI status checks; backup/restore; sandbox seeding/masking; audit history |
| Copado already licensed and release management is the priority | Copado CI/CD or Essentials + Git | User stories, promotions, quality gates, compliance evidence |
| AutoRABIT already licensed, data tooling is needed | AutoRABIT CI + data loader + backup | CI, data, backup, monitoring in one platform |
| No vendor budget, small team, strong CLI skills | `sf` CLI + GitHub Actions | Lowest cost, full control, but you build the UI and the audit pack |
| Native-only mandate | DevOps Center | No extra vendor; work items and pipelines; still needs Git discipline |
| Legacy org with no pipeline | Change Sets only as a documented exception | Fast for a tiny fix; not a release process |

## 4. What interviewers listen for

They are not checking whether you memorized a menu. They are checking whether you understand the division of responsibility:

- **Git** is the source of truth.
- **The CLI/Metadata API** performs the operation.
- **The vendor tool** makes the operation reviewable and repeatable.
- **The CI runner** enforces the gate.
- **The human** approves the production change.
- **The tag and the evidence** make it reversible and auditable.

A good answer: "Gearset and Copado are diff and pipeline layers over the Metadata API. I still keep Git as the source of truth, use the CLI in CI, and treat the vendor UI as the place where a human reviews the diff and promotes the change."

## 5. What to merge

**Merge:** the layer cake, the tool summary table, the selection matrix, and the division-of-responsibility answer.

**Compress:** the selection matrix if the page is short; keep the "vendor tool does not replace Git" line.

<!-- ===== end: 03-devops-tools/tool-landscape.md ===== -->

---

<!-- ===== begin: 03-devops-tools/gearset-click-paths.md ===== -->

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

<!-- ===== end: 03-devops-tools/gearset-click-paths.md ===== -->

---

<!-- ===== begin: 03-devops-tools/copado-autorabit-devopscenter.md ===== -->

# Copado, AutoRABIT, DevOps Center, Change Sets, and the CLI

**Merge target:** section 6.1 of the downstream page. The goal is practical familiarity, not a vendor manual.

**Caveat.** These platforms rename modules between releases and editions. The task and the verification step are stable; the labels are not.

## 1. Copado

### 1.1 What it is

A release-management platform built around user stories, pipelines, promotions, deployment steps, quality gates, and audit evidence. Current product branding includes **Copado CI/CD** for enterprise teams, **Copado Essentials** for smaller teams, **Agentia** as the AI layer, **Copado Robotic Testing**, and the **Copado AI Platform**. "Copado Fundamentals" and a Copado "DevOps Center" tier are not current product names; do not use them in an interview.

### 1.2 Practical click-paths (Copado CI/CD)

| Task | Where (common shape) | What you do | What to verify |
|---|---|---|---|
| Create a pipeline | Copado app → Pipelines / Pipeline setup | Define stages: Dev → QA → UAT → Prod; attach orgs | Each stage has one owner and one gate |
| Create a user story | Copado → User Stories | Create a story, link the ticket, attach commits/metadata | The story is the unit of promotion, not a loose commit |
| Commit changes | VS Code / Copado extension or Git | Commit with the story id | The story and the commit agree |
| Validate | Story or pipeline action | Run the validation/deployment step to the target | Tests run; failures block promotion |
| Promote | Pipeline / promotion | Move the story to the next stage; approve at the gate | The approver is not the author |
| Quality gate | Pipeline step / quality gate config | Static analysis, coverage, peer review | The gate is enforced, not advisory |
| Deploy | Promotion action | Execute the deployment steps | Destructive changes and tests are explicit steps |
| Audit | Deployment history / story history | Export the promotion evidence | Ticket, approver, deploy id, test result, timestamp |
| Backup (if licensed) | Copado backup module | Take a backup before the risky step | Backup id recorded in the ticket |

**Copado Essentials** is the simpler standalone product. It may not expose the same enterprise pipeline objects; verify which product the bank actually licenses before you promise a specific workflow.

### 1.3 What it does not replace

Git hygiene, a real test suite, a rollback tag, or a human who reads the diff. Copado makes the process visible; it does not make a bad payload safe.

### 1.4 Interview line

"Copado models the release process: user story, pipeline, promotion, quality gate, deployment, audit. The underlying operation is still Metadata API, and Git is still the source of truth."

## 2. AutoRABIT

### 2.1 What it is

A Salesforce DevOps platform with four current product areas:

| Product | What it does |
|---|---|
| **AutoRABIT ARM** | CI/CD, deployments, version control, testing, sandbox management |
| **AutoRABIT Vault** | Backup/restore, data integrity, archiving; data masking capabilities may sit in Vault or a related module—verify the edition |
| **AutoRABIT CodeScan** | Static code analysis and code quality |
| **AutoRABIT Guard** | Security posture, policy enforcement, misconfiguration detection |

Older material may describe a generic "CI Jobs / Deployment / Data Loader / Backup / Monitoring / Release" module list. Treat that as category-level, not as current product naming.

### 2.2 Practical click-paths

| Task | Where (common shape) | What you do | What to verify |
|---|---|---|---|
| CI job | ARM → CI Jobs / CI | Connect Git repo and branch; choose target org; choose validate or deploy; add tests | The job fails on a test failure |
| Deployment | ARM → Deployment | Compare metadata between orgs/branches; deploy; keep a history | The diff is reviewed, not blindly deployed |
| Data | Vault / data tooling | Seed or migrate records | Data is masked/approved; not bulk customer data without a ticket |
| Backup | Vault → Backup & Restore | Back up metadata/data before a risky release | Backup id and restore path are recorded |
| Monitoring | ARM / Guard | Detect drift and security/compliance issues | Alerts route to the release owner |
| Static analysis | CodeScan | Scan the branch for quality/security findings | The gate is configured and enforced |

### 2.3 Interview line

"AutoRABIT ARM is the CI/CD layer; Vault is backup/restore and data; CodeScan is static analysis; Guard is security posture. The questions are always the promotion path, the back-promotion, and where the secrets live."

## 3. DevOps Center

### 3.1 What it is

Salesforce's native work-item and pipeline product. It connects a Git repo and orgs, tracks work items, and promotes changes through pipeline stages. It is the option when the bank does not want another vendor.

### 3.2 Practical click-paths

| Task | Where | What you do | What to verify |
|---|---|---|---|
| Enable | Setup → search "DevOps Center" | Enable and connect Git/orgs | The connected app and repo permissions are correct |
| Create a pipeline | Setup → DevOps Center → Pipelines | Define stages and orgs | Each stage maps to a real sandbox |
| Create a work item | App Launcher → DevOps Center → Work Items | Create a story/bug, associate changes | The work item is the traceable unit |
| Commit and deploy | VS Code / DevOps Center | Commit with the work item; promote | The commit and work item agree |
| Promote | Work item / pipeline | Move to the next stage; approve | The approver is not the author |
| Audit | Work item history / deployment history | Capture the evidence | Ticket, deploy id, test result |

### 3.3 Limitations to say out loud

DevOps Center is native and improving, but it is not a full replacement for a mature vendor platform's dependency analysis, data tooling, and backup. It still requires branch discipline, tests, and a rollback tag.

### 3.4 Interview line

"DevOps Center is the native option: work items, Git, pipelines, promotion. It does not remove the need for Git discipline or a test gate."

## 4. Change Sets

### 4.1 What they are

A Setup UI mechanism for moving metadata between related orgs. Outbound change set → upload → inbound change set → validate → deploy.

### 4.2 Click-path

1. Source org: Setup → Deploy → Outbound Change Sets → New.
2. Add components manually.
3. Upload to the target org.
4. Target org: Setup → Deploy → Inbound Change Sets → select → Validate → Deploy.

### 4.3 Why they fail at this scale

- No reviewable Git diff.
- No CLI/API automation.
- No dependency analysis; you add components by hand.
- No branch, feature, or hotfix model.
- No rollback tag.
- Profile and permission-set XML conflicts are manual.
- Weak audit evidence compared with a pipeline.
- Only between related orgs.

### 4.4 When a Change Set is still acceptable

A tiny emergency fix in an org that has no pipeline, with a ticket, a validation, a named approver, and a follow-up to backfill Git. In a regulated bank, expect the written procedure to forbid it or to require an exception.

### 4.5 Interview line

"Change Sets are the thing I can explain and then retire. They have no diff, no branch model, and no rollback tag. The answer is the CLI or a vendor pipeline with Git in front."

## 5. Salesforce CLI practical set

```bash
# Auth (interactive for a developer machine; JWT in CI)
sf org login web --alias dev
sf org login jwt --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file server.key --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" --alias ci

# Retrieve and inspect
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev
sf project deploy preview --manifest manifest/package.xml --target-org qa

# Validate and deploy
sf project deploy start --manifest manifest/package.xml --dry-run \
  --test-level RunSpecifiedTests --tests CB_Release_Test --target-org qa
sf project deploy start --manifest manifest/package.xml --target-org qa

# Status and quick deploy
sf project deploy report --job-id <job-id> --target-org qa
sf project deploy quick --job-id <job-id> --target-org prod

# Tests
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 30 --target-org qa

# Packages
sf package version create --package CB_Credit --installation-key-bypass \
  --code-coverage --wait 30
sf package version promote --package 04tXXXXXXXXXXXX
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

Flags move. Confirm with `sf <command> --help` before putting a command in a runbook.

## 6. What to merge

**Merge:** the Copado and DevOps Center task tables, the Change Sets "why fail" list, and the CLI set.

**Compress:** AutoRABIT if the page is short; keep the category-level answer.

**Do not merge:** edition-specific module names as if universal. Keep the caveat.

<!-- ===== end: 03-devops-tools/copado-autorabit-devopscenter.md ===== -->

---

<!-- ===== begin: 04-cicd/github-actions-salesforce.md ===== -->

# GitHub Actions + Salesforce CI/CD pipeline

**Merge target:** sections 5 and 5.1 of the downstream page. The page already has a stage table; this file adds the runnable workflow and the reasoning.

## 1. The five jobs

| Job | Trigger | What it proves | Target |
|---|---|---|---|
| `validate-pr` | Pull request to a release branch | The proposed change compiles and tests pass in a disposable CI sandbox | CI sandbox |
| `validate-release` | Push to the release branch, or manual dispatch | The exact commit compiles and tests pass in the org you are about to change | QA / UAT / Pre-Prod / Prod |
| `deploy` | After `validate-release` | The validated payload can be applied | The same target |
| `smoke` (inside `deploy`) | After the quick deploy | The feature is alive, not just deployed | The same target |
| `tag` (inside `deploy`) | After a successful production deploy | There is a rollback target | Git |

The important separation: **validation does not change the org; deployment applies a validation that already passed.** If the payload changes after validation, re-validate.

## 2. Reference workflow

```yaml
name: salesforce-release

on:
  pull_request:
    branches: ["release/**"]
  push:
    branches: ["release/**"]
  workflow_dispatch:
    inputs:
      target:
        description: "Environment to validate and deploy"
        type: choice
        options: [qa, uat, preprod, prod]
        required: true

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: sf-${{ github.ref }}-${{ inputs.target || 'qa' }}
  cancel-in-progress: false

env:
  NODE_VERSION: "20"

jobs:
  validate-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias ci
          rm -f "$RUNNER_TEMP/server.key"
      - name: Build delta manifest
        run: |
          npx --yes sfdx-git-delta \
            --to HEAD \
            --from "origin/${{ github.base_ref }}" \
            --output delta \
            --generate-delta \
            --source force-app
      - name: Validate against the CI sandbox
        run: |
          sf project deploy start \
            --manifest delta/package/package.xml \
            --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
            --dry-run \
            --test-level RunLocalTests \
            --target-org ci \
            --wait 60 \
            --json | tee validation.json
      - name: Upload validation evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ github.run_id }}
          path: |
            validation.json
            delta/

  validate-release:
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    environment: ${{ inputs.target || 'qa' }}
    outputs:
      job_id: ${{ steps.validate.outputs.job_id }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT, environment-scoped secrets)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias target
          rm -f "$RUNNER_TEMP/server.key"
      - name: Build delta manifest
        run: |
          npx --yes sfdx-git-delta \
            --to HEAD \
            --from "origin/main" \
            --output delta \
            --generate-delta \
            --source force-app
      - name: Validate against the target
        id: validate
        run: |
          sf project deploy start \
            --manifest delta/package/package.xml \
            --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
            --dry-run \
            --test-level RunLocalTests \
            --target-org target \
            --wait 60 \
            --json | tee validation.json
          echo "job_id=$(jq -r '.result.id' validation.json)" >> "$GITHUB_OUTPUT"
      - name: Upload validation evidence
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ github.run_id }}
          path: |
            validation.json
            delta/

  deploy:
    needs: validate-release
    runs-on: ubuntu-latest
    environment: ${{ inputs.target || 'qa' }}
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - name: Install Salesforce CLI
        run: npm install --global @salesforce/cli
      - name: Authenticate (JWT, environment-scoped secrets)
        env:
          SF_CONSUMER_KEY: ${{ secrets.SF_CONSUMER_KEY }}
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_INSTANCE_URL: ${{ secrets.SF_INSTANCE_URL }}
          SF_JWT_KEY: ${{ secrets.SF_JWT_KEY }}
        run: |
          printf '%s' "$SF_JWT_KEY" > "$RUNNER_TEMP/server.key"
          sf org login jwt \
            --client-id "$SF_CONSUMER_KEY" \
            --jwt-key-file "$RUNNER_TEMP/server.key" \
            --username "$SF_USERNAME" \
            --instance-url "$SF_INSTANCE_URL" \
            --alias target
          rm -f "$RUNNER_TEMP/server.key"
      - name: Quick deploy the validated job
        run: |
          sf project deploy quick \
            --job-id "${{ needs.validate-release.outputs.job_id }}" \
            --target-org target \
            --wait 60
      - name: Smoke test
        run: |
          sf apex run test \
            --test-level RunSpecifiedTests \
            --tests ReleaseSmokeTest \
            --target-org target \
            --wait 30
      - name: Tag the production release
        if: ${{ (inputs.target || 'qa') == 'prod' }}
        run: |
          git config user.name "salesforce-release-bot"
          git config user.email "salesforce-release-bot@users.noreply.github.com"
          git tag -a "release-$(date -u +%Y-%m-%d)-${{ github.run_number }}" \
            -m "Deployed ${{ github.sha }} to production"
          git push origin --tags
```

## 3. Why this shape

| Choice | Why it is there |
|---|---|
| Pull-request trigger | The earliest place to fail is the cheapest place to fix |
| CI sandbox as the PR target | PR validation never touches UAT or Prod |
| Delta manifest (`sfdx-git-delta`) | Keeps the payload under metadata ceilings and reduces blast radius |
| `--dry-run` with `RunLocalTests` | Proves compile and tests against the target without changing it; trade speed for honesty |
| Environment-scoped secrets | The prod runner cannot use QA credentials, and the PR runner cannot use prod credentials |
| Protected `prod` environment | Required reviewers pause the job; approval is structural, not a comment |
| Quick deploy | Applies the validated job inside the change window without paying the test runtime twice |
| Smoke test after deploy | Catches "deployed but broken" (inactive Flow, missing secret, wrong assignment) |
| Annotated tag | The rollback target and the audit anchor |
| Concurrency group | Two deploys to one org do not race; only one deployment runs at a time per org, and queued deployments are not guaranteed to run in submission order |
| Artifact upload | The validation result and delta are evidence for the ticket |
| Minimal `permissions` | A compromised workflow cannot write the repo by default |

## 4. What not to do

- Do not run `sf org login web` on a runner.
- Do not store a password, auth URL, or private key in the repo.
- Do not use a shared human admin login for CI.
- Do not deploy every commit to production.
- Do not use `NoTestRun` in production when the payload contains Apex.
- Do not use `--ignore-conflicts` in production.
- Do not let the author approve their own production deploy.
- Do not skip validation because "it is a small change."
- Do not rebuild the artifact from a different branch at production.
- Do not force-push a release branch that other people are deploying.

## 5. Trade-offs to mention in an interview

- `RunLocalTests` is slower than `RunSpecifiedTests` but catches more. Use it before the window; use named tests for the PR if the suite is too slow.
- `RunRelevantTests` (Beta, API 66.0+) is a fifth test level that runs only tests relevant to the payload. It is a good fit for Apex-heavy deployments where test time should scale with the payload, but do not use it to avoid a broad gate the bank's policy requires.
- A full-org delta from `origin/main` can be large on a long-lived release branch. Use the previous release tag as the base when the branch is long.
- The quick-deploy window is limited. If the validation expires or the payload changes, re-validate; do not force the quick deploy.
- GitHub Environments and required reviewers depend on the plan. If the bank uses Azure DevOps or GitLab, the same gates exist under different names.

## 6. What to merge

**Merge:** the five-job table, the YAML in a collapsible block, the "why" table, and the "what not to do" list.

**Compress:** the YAML if the page needs to stay short; keep the five-job table and the why table.

**Do not merge:** the workflow as a guaranteed drop-in for every repo. It is a reference; the team's org aliases, branch names, and test names will differ.

<!-- ===== end: 04-cicd/github-actions-salesforce.md ===== -->

---

<!-- ===== begin: 04-cicd/auth-secrets-environments.md ===== -->

# Authentication, secrets, environments, and approvals

**Merge target:** sections 5.1 and 11 of the downstream page. This file is the "how the pipeline proves who is allowed to do what" research.

## 1. Authentication: JWT bearer flow

The standard CI pattern is the OAuth 2.0 JWT bearer flow:

1. Create a Connected App (or External Client App, depending on the org's release).
2. Enable OAuth settings and **Use digital signatures**.
3. Upload the public certificate.
4. Grant the `api` scope (and the scopes the integration needs).
5. Create a dedicated integration user with a least-privilege deploy permission set.
6. Pre-authorize the Connected App for that user (for example, "Admin approved users are pre-authorized" plus a permission set).
7. Generate an RSA key pair. Store the private key in the CI secret store. Upload the certificate to the Connected App.
8. In CI, run `sf org login jwt` with the consumer key, username, private key, and instance URL.

```bash
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file "$RUNNER_TEMP/server.key" \
  --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" \
  --alias target
```

The runner writes the key to a temporary file and deletes it after login. The key is never committed and is never printed.

## 2. The integration user

| Property | Rule |
|---|---|
| Identity | Dedicated, not a human's admin login |
| Permissions | Least privilege: API Enabled plus the deploy permissions the pipeline needs (often Modify All Data for Metadata API deploys; confirm the bank's approved set) |
| Password | Not used for JWT; the certificate is the credential |
| Rotation | The certificate/key pair has an owner and a rotation date |
| Monitoring | The user's API usage and login history are reviewed |
| Scope | One user per environment (or a tightly controlled shared CI identity with environment isolation) |
| Approval | The user cannot approve changes; approval is a human action |

## 3. Secrets

| Secret | Scope | What it is | Rotation |
|---|---|---|---|
| `SF_CONSUMER_KEY` | Repo or environment | Connected App consumer key | When the app is rotated |
| `SF_USERNAME` | Environment | Integration username | When the user changes |
| `SF_INSTANCE_URL` | Environment | `https://login.salesforce.com` or `https://test.salesforce.com` | Rarely |
| `SF_JWT_KEY` | Environment | PEM private key | On a schedule and on suspected exposure |
| `SF_CLIENT_SECRET` | Do not use with JWT | Not needed for the JWT bearer flow | — |

**Rules:**
- Production secrets are environment-scoped, not repository-wide.
- Development/QA secrets do not grant production access.
- Do not echo secrets. Mask them in logs.
- Rotate on a schedule and immediately after any suspected exposure.
- Do not put secrets in a pull request, an issue, a screenshot, or a debug log.

## 4. GitHub Environments and approvals

**Settings → Environments → `prod`:**

| Control | Setting | Why |
|---|---|---|
| Required reviewers | Named release managers | A human approves the production deploy |
| Prevent self-review | Enabled if available | The author is not the approver |
| Deployment branches | Only the release branch or a tag | A feature branch cannot deploy to prod |
| Environment secrets | Prod-only `SF_*` values | The QA runner cannot read prod credentials |
| Wait timer | Optional | Adds a pause after approval for a final check |

The `environment:` key in the workflow is what makes the approval gate real:

```yaml
jobs:
  deploy:
    environment: ${{ inputs.target || 'qa' }}
```

For production, the job pauses before it runs until the required reviewer approves. That is the structural segregation of duties.

## 5. Branch protection

**Settings → Branches → Branch protection rules** for `main` and `release/**`:

- Require a pull request before merging.
- Require at least one approval (two for production-bound branches if the bank requires it).
- Dismiss stale approvals when new commits are pushed.
- Require status checks to pass, including the CI validation job.
- Require conversation resolution.
- Restrict who can push.
- Include administrators, if the bank's policy allows.
- Add `CODEOWNERS` for `force-app/**`, `manifest/**`, and `.github/workflows/**`.

## 6. Segregation of duties

| Action | Who |
|---|---|
| Write the Apex or Flow | Developer |
| Review the diff | A second person, not the author |
| Run the validation | Pipeline / integration user |
| Approve the production deploy | Named release manager, not the author |
| Execute the deploy | Pipeline / integration user |
| Verify the business result | QA or business owner |
| Retain the evidence | Release engineer |

If the same person can author, approve, and deploy, the control is cultural, not structural. The pipeline should make it impossible.

## 7. Common authentication failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `invalid_grant` / `user hasn't approved this consumer` | The Connected App is not pre-authorized for the integration user | Pre-authorize the app or assign the permission set |
| `invalid_client_id` | Wrong consumer key for the environment | Use the environment-scoped secret |
| `invalid_grant` / `expired access/refresh token` | Wrong instance URL or user | Check `SF_INSTANCE_URL` and `SF_USERNAME` |
| `INVALID_SESSION_ID` | The key/cert pair does not match | Re-upload the certificate, rotate the key |
| Login works, deploy fails with permission error | The integration user lacks a deploy permission | Assign the approved deploy permission set |
| Callout works in Dev, fails in CI | Named credential secret/cert missing in the target | Configure per-org secrets and certificates |

## 8. What to merge

**Merge:** the JWT flow, the integration-user table, the secrets table, the environment/approval table, the branch-protection list, and the segregation-of-duties table.

**Compress:** the failure table if the page is long; keep the first four rows.

**Do not merge:** a specific permission-set name, consumer key, org id, or certificate. None is included, and none should be.

<!-- ===== end: 04-cicd/auth-secrets-environments.md ===== -->

---

<!-- ===== begin: 04-cicd/other-ci-platforms.md ===== -->

# Azure DevOps and GitLab equivalents

**Merge target:** section 5 of the downstream page, as a "same stages, different syntax" subsection. The posting names GitHub Actions, Azure DevOps, and GitLab, so the page should show that the design is vendor-neutral.

## 1. Concept mapping

| Concept | GitHub Actions | Azure DevOps | GitLab CI/CD |
|---|---|---|---|
| Pipeline definition | Workflow YAML | Pipeline YAML | `.gitlab-ci.yml` |
| Trigger | `on:` | `trigger:` / PR policy | `rules:` / `only:` |
| Job runner | `runs-on` | `pool` | `tags` / runners |
| Secret store | Actions secrets / environment secrets | Variable groups / Key Vault | CI/CD variables (protected, masked) |
| Approval gate | Environment required reviewers | Environment approvals and checks | Protected environment + manual job |
| Branch gate | Branch protection + required checks | Branch policy + build validation | Protected branch + MR approvals |
| Artifact | `actions/upload-artifact` | Pipeline artifact | `artifacts:` |
| Status on PR | Checks API | Branch policy status | MR pipeline status |
| Concurrency | `concurrency:` | `lockBehavior` / demands | `resource_group` |

## 2. Azure DevOps sketch

```yaml
trigger:
  branches:
    include: [release/*]

pr:
  branches:
    include: [release/*]

variables:
  - group: salesforce-ci

stages:
  - stage: Validate
    jobs:
      - job: ValidatePR
        pool: { vmImage: ubuntu-latest }
        steps:
          - checkout: self
            fetchDepth: 0
          - task: NodeTool@0
            inputs: { versionSpec: '20.x' }
          - script: npm install --global @salesforce/cli
          - script: |
              printf '%s' "$(SF_JWT_KEY)" > "$(Agent.TempDirectory)/server.key"
              sf org login jwt --client-id "$(SF_CONSUMER_KEY)" \
                --jwt-key-file "$(Agent.TempDirectory)/server.key" \
                --username "$(SF_USERNAME)" \
                --instance-url "$(SF_INSTANCE_URL)" --alias ci
              rm -f "$(Agent.TempDirectory)/server.key"
          - script: |
              npx --yes sfdx-git-delta --to HEAD --from "origin/$(System.PullRequest.TargetBranch)" \
                --output delta --generate-delta --source force-app
          - script: |
              sf project deploy start --manifest delta/package/package.xml \
                --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
                --dry-run --test-level RunLocalTests --target-org ci --wait 60

  - stage: DeployProd
    dependsOn: Validate
    condition: succeeded()
    jobs:
      - deployment: DeployProd
        environment: 'salesforce-prod'   # configure approvals/checks
        pool: { vmImage: ubuntu-latest }
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Auth, quick deploy the validated job, smoke test, tag"
```

Azure DevOps approvals live on the **environment** (Pipelines → Environments → Approvals and checks). Branch policies provide the PR validation gate.

## 3. GitLab sketch

```yaml
stages: [validate, deploy]

variables:
  SF_CLI: "@salesforce/cli"

validate:
  stage: validate
  image: node:20
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - npm install --global $SF_CLI
    - printf '%s' "$SF_JWT_KEY" > server.key
    - sf org login jwt --client-id "$SF_CONSUMER_KEY" --jwt-key-file server.key
        --username "$SF_USERNAME" --instance-url "$SF_INSTANCE_URL" --alias ci
    - rm -f server.key
    - npx --yes sfdx-git-delta --to HEAD --from "origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
        --output delta --generate-delta --source force-app
    - sf project deploy start --manifest delta/package/package.xml
        --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml
        --dry-run --test-level RunLocalTests --target-org ci --wait 60
  artifacts:
    when: always
    paths: [delta/, validation.json]

deploy_prod:
  stage: deploy
  image: node:20
  environment:
    name: salesforce-prod
    action: prepare
  rules:
    - if: $CI_COMMIT_BRANCH =~ /^release\//
      when: manual
  script:
    - echo "Auth, quick deploy the validated job, smoke test, tag"
```

GitLab approvals live on **Settings → CI/CD → Protected environments** and merge request approval rules. A manual job is not an approval by itself; pair it with a protected environment.

## 4. Design invariants

These do not change with the vendor:

1. PR validation targets a disposable CI sandbox.
2. The release validation targets the org you will change.
3. Production requires a human approver who is not the author.
4. Secrets are environment-scoped and never in the repo.
5. The artifact is promoted; it is not rebuilt per environment.
6. A tag is created after a successful production deploy.
7. The pipeline serializes deploys per org.

## 5. Interview line

"I do not care which CI product we use. The stages are the same: validate against the target, gate production on a human approval, promote the same artifact, and tag the release. Only the YAML header, the secret store, and the approval UI change."

## 6. What to merge

**Merge:** the concept mapping and the design invariants.

**Optional:** one short Azure DevOps or GitLab sketch, depending on the page's audience. Do not include all three full pipelines; the page will become a CI manual.

<!-- ===== end: 04-cicd/other-ci-platforms.md ===== -->

---

<!-- ===== begin: 05-certifications/certification-landscape.md ===== -->

# Certification landscape — what the posting names and what actually exists

**Merge target:** the page's Certifications section and the term-by-term entry for Q14. This file corrects the two common interview mistakes: treating "Advanced Admin" as the current name, and implying an official Salesforce DevOps Engineer certification exists.

## 1. What the posting says

> Salesforce certifications (PD1, Advanced Admin, DevOps related certs)

That is three different things:

1. **PD1** — Salesforce Certified Platform Developer I. A real, current Salesforce credential.
2. **Advanced Admin** — the former name of **Salesforce Certified Platform Administrator II**. A real, current credential under a new name.
3. **"DevOps related certs"** — a category, not a specific Salesforce credential. There is no official Salesforce Certified DevOps Engineer exam. Vendor certificates exist (Gearset, Copado, AutoRABIT), and Salesforce's architect/developer credentials cover parts of the lifecycle, but the posting is using a loose category.

## 2. Current Salesforce credentials that map to this role

| Credential | Current name | Why it maps | Official page |
|---|---|---|---|
| Platform Developer I (PD1) | Salesforce Certified Platform Developer I | Apex, triggers, testing, deployment tools, the platform model you deploy | <https://trailhead.salesforce.com/credentials/platformdeveloperi> |
| Platform App Builder | Salesforce Certified Platform App Builder | Objects, fields, security, automation, UI, app deployment — the metadata you move every week | <https://trailhead.salesforce.com/credentials/platformappbuilder> |
| Administrator (foundation) | Salesforce Certified Platform Administrator | The baseline admin model: configuration, security, data, automation | <https://trailhead.salesforce.com/credentials/platformadministrator> |
| Advanced Administrator | Salesforce Certified Platform Administrator II | Advanced security, objects, automation, data, environment management and deployment | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> |
| Platform Developer II | Salesforce Certified Platform Developer II | Advanced Apex, integration, performance, lifecycle; useful but not named in the posting | <https://trailhead.salesforce.com/credentials/platformdeveloperii> |

**Naming note.** Use both names in conversation: "Advanced Administrator, now called Platform Administrator II." That shows you are current and that you know the history.

## 3. What does not exist

- **Salesforce Certified DevOps Engineer.** Not an official Salesforce credential as of 2026-11-14. Do not claim it.
- **A single "Salesforce DevOps" exam** covering Gearset/Copado/AutoRABIT. Salesforce does not certify third-party tools.
- **A vendor certificate that replaces PD1.** Vendor certificates show tool familiarity; they do not prove Apex or platform fundamentals.

## 4. What "DevOps related certs" can reasonably mean

| Category | Examples | What it proves | Caveat |
|---|---|---|---|
| Salesforce developer/architect credentials | PD1, PD2, Application Architect, System Architect, Technical Architect | Platform depth, including deployment and integration | Not DevOps-specific |
| Gearset / DevOps Launchpad | Salesforce DevOps Fundamentals, CI/CD for Salesforce, DevOps Leadership, Salesforce Backup, Gearset Academy | DevOps concepts and Gearset tool use | Free tracks; verify the current catalogue |
| Copado | Copado Academy / Copado certification program | Copado pipeline and release-management use | Offerings and URLs change; verify with Copado |
| AutoRABIT | AutoRABIT Academy / certification program | AutoRABIT CI, deployment, data, backup | Verify current programme; product packaging varies |

**Rule for the page:** list vendor certificates as "tool time," not as a substitute for PD1. Keep the "verify current offering" caveat.

## 5. Mapping to the posting

| Posting phrase | Best interpretation | What to say in an interview |
|---|---|---|
| PD1 | Platform Developer I | "I have PD1-level Apex, testing, and deployment-tool knowledge." |
| Advanced Admin | Platform Administrator II | "Advanced Administrator is now Platform Administrator II; I know the advanced security, automation, and environment-management domains." |
| DevOps related certs | Vendor + Salesforce developer/architect credentials | "There is no official Salesforce DevOps Engineer cert. I have hands-on pipeline evidence plus a vendor certificate or PD1/architect material." |

## 6. What to merge

**Merge:** the three-part interpretation, the current-name table, the "what does not exist" list, and the mapping table.

**Do not merge:** any claim that a specific vendor certification is required, or that an official Salesforce DevOps certification exists.

<!-- ===== end: 05-certifications/certification-landscape.md ===== -->

---

<!-- ===== begin: 05-certifications/salesforce-credentials.md ===== -->

# Salesforce credential curricula

**Merge target:** the Certifications section of the downstream page. This is the research behind the study order and the "what does the exam actually cover?" answer.

**Caveat.** Salesforce updates exam guides with each release. The domain names below are the stable structure; the weights and the exact topic list change. Fetch the current official exam guide PDF before you publish a percentage. Do not study from exam dumps.

## 1. Salesforce Certified Platform Developer I (PD1)

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperi>
**Study trail:** <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide>

### 1.1 What the credential is for

The PD1 is the developer foundation: Apex, triggers, SOQL/SOSL, testing, the UI layer, and the debug/deployment tools. It is the credential the posting names explicitly.

### 1.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Salesforce Fundamentals | Platform architecture, multi-tenancy, the data model, the MVC pattern, the development lifecycle | Explains why governor limits exist and why metadata is compiled against the target |
| Data Modeling and Management | Objects, fields, relationships, schema design, SOQL/SOSL, DML | The metadata you deploy; the queries that hit limits |
| Process Automation and Logic | Apex classes, triggers, interfaces, asynchronous Apex, exception handling, order of execution | The bulkification and dependency risks you review |
| User Interface | Lightning components, Visualforce, Lightning Web Components, page layouts | The UI metadata that deploys and the activation that does not |
| Testing | Test classes, assertions, test data, coverage, `Test.startTest()` | The production gate and the reason a green Dev test is not enough |
| Debug and Deployment Tools | Debug logs, checkpoints, the Developer Console, the CLI, change sets, Metadata API | The daily tools of this role |

### 1.3 Study emphasis for this role

- Trigger order of execution and recursion.
- Bulkification at 200 and 10,000 records.
- Writing tests that create their own data.
- `sf` CLI retrieve/deploy/test.
- Reading a deploy error and mapping it to a missing dependency.

### 1.4 Exam logistics (verify current)

- Register through Trailhead Academy / Salesforce Credentialing.
- Typical format: about 60 questions, about 105 minutes, multiple choice and multiple select.
- Passing score varies by exam; use the current exam guide.
- Plan for maintenance modules each release cycle.

## 2. Salesforce Certified Platform App Builder

**Official page:** <https://trailhead.salesforce.com/credentials/platformappbuilder>
**Study trail:** <https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-platform-app-builder-certification>

### 2.1 What the credential is for

Declarative application design: objects, fields, security, automation, UI, and app deployment. It is the best certificate for the metadata a DevOps engineer moves every week.

### 2.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Salesforce Fundamentals | Platform capabilities, the app model, the declarative vs programmatic boundary | Explains what can be built without code and what must be deployed |
| Data Modeling and Management | Objects, fields, relationships, schema, data quality | The parent/child dependencies that break deploys |
| Security | Profiles, permission sets, OWD, role hierarchy, sharing, field-level security | The access diff you must review before production |
| Business Logic and Process Automation | Validation rules, Flow, approval processes, formula fields | The automation that does not merge and the Flow activation trap |
| User Interface | Lightning apps, pages, layouts, record types, Dynamic Forms | The layout/assignment/page-activation distinction |
| App Deployment | Change sets, packages, the deployment lifecycle | The transition from declarative build to release engineering |

### 2.3 Study emphasis for this role

- Permission sets vs profiles.
- Record types, page layouts, and Lightning page activation.
- Flow before-save vs after-save.
- Deployment options and their limits.

## 3. Salesforce Certified Platform Administrator

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator>

### 3.1 What the credential is for

The baseline administrator credential: configuration, security, data, automation, and the standard applications. Platform Administrator II requires it (per the credential page).

### 3.2 Curriculum domains

| Domain | What it covers |
|---|---|
| Configuration and Setup | Org settings, company information, UI settings, app configuration |
| Object Manager and Lightning App Builder | Objects, fields, page layouts, Lightning pages, record types |
| Sales and Marketing Applications | Leads, opportunities, campaigns, products, price books |
| Service and Support Applications | Cases, queues, entitlements, service contracts, knowledge |
| Productivity and Collaboration | Activities, Chatter, groups, files |
| Data and Analytics Management | Import/export, data quality, reports, dashboards |
| Automation | Validation rules, Flow, approval processes, escalation rules |
| Security and Access | Profiles, permission sets, roles, OWD, sharing rules, login policies |

### 3.3 Study emphasis for this role

- Security and access (the permission diff).
- Automation (the Flow/validation-rule conflicts).
- Data management (the data-vs-metadata boundary).
- Configuration and setup (the org properties that do not deploy).

## 4. Salesforce Certified Platform Administrator II (formerly Advanced Administrator)

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
**Prerequisite:** Salesforce Certified Platform Administrator.

### 4.1 What the credential is for

Advanced administration: complex security, objects and fields, automation, data management, analytics, and environment management/deployment. It is the closest Salesforce credential to release engineering.

### 4.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Security and Access | Advanced sharing, restriction rules, permission set groups, login policies, session settings | The access changes that a deploy can widen |
| Objects and Fields | Complex schema, relationships, field-level security, record types | The dependency graph |
| Automation | Advanced Flow, approvals, escalation, order of execution | The automation that does not merge and the bulk failures |
| Data Management | Data import/export, duplicate management, data quality, large data volumes | The data-vs-metadata boundary and masking |
| Analytics | Reports, dashboards, reporting snapshots | Usually out of scope for releases, but part of the admin model |
| Environment Management and Deployment | Sandboxes, change sets, packages, deployment tools, release management | The posting's core |
| Sales and Marketing Applications | Advanced sales configuration | Domain context |
| Service and Support Applications | Advanced service configuration | Domain context |
| Productivity and Collaboration | Advanced collaboration features | Domain context |

### 4.3 Study emphasis for this role

- Environment management and deployment (the direct overlap).
- Advanced security (the permission diff).
- Advanced automation (the conflict clinic).
- Sandboxes and data management (refresh and masking).

## 5. Platform Developer II (optional, not named)

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperii>

PD2 goes deeper into Apex, integration, performance, and the development lifecycle. It is not required by the posting, but it is the natural next step for a developer-heavy DevOps engineer. Mention it as optional.

## 6. What the exams do not cover

- Gearset, Copado, or AutoRABIT UI.
- A specific bank's change-management process.
- GitHub Actions or Azure DevOps YAML.
- Data masking product operations.

Those come from hands-on labs and vendor training, not the Salesforce exams. The page should say so.

## 7. What to merge

**Merge:** the domain tables, the "study emphasis" bullets, and the "what the exams do not cover" note.

**Do not merge:** exact question counts, time limits, or passing scores without the current official exam guide. Use "typically" and link the official page.

<!-- ===== end: 05-certifications/salesforce-credentials.md ===== -->

---

<!-- ===== begin: 05-certifications/vendor-and-study-plan.md ===== -->

# Vendor certifications and a study plan

**Merge target:** the Certifications section and the study-order paragraph. This file answers "what should I actually study, in what order, and what counts as evidence?"

## 1. Vendor certification landscape

| Programme | Tracks / credentials | Cost | What it proves | Caveat |
|---|---|---|---|---|
| DevOps Launchpad (Gearset) | Salesforce DevOps Fundamentals; CI/CD for Salesforce; Salesforce DevOps Leadership; Salesforce Backup; **Gearset Academy Certification** | Free | DevOps concepts and Gearset tool use | Catalogue and certificate names can change; verify on the site |
| Copado | **Copado Certified** / Copado Academy tracks | Varies | Copado pipeline, promotion, release management | The public certification URL returned 404 on 2026-11-14; verify the current name with Copado |
| AutoRABIT | **AutoRABIT Academy ARM tracks** (and related product tracks) | Varies | AutoRABIT ARM CI/CD, deployment, data, backup | Product packaging and programme names vary by edition |
| Salesforce developer/architect | PD1, PD2, Application Architect, System Architect, Technical Architect | Paid exams | Platform depth | None is a DevOps-specific credential |

**DevOps Launchpad link:** <https://devopslaunchpad.com/>

The useful, vendor-neutral tracks for this role are **Fundamentals** and **CI/CD**. The **Backup** track is directly relevant to the sandbox/backup questions. **Gearset Academy** is the tool-specific one.

## 2. What to study first

The posting is a DevOps role, not a pure developer role, so the order is:

1. **Platform fundamentals** — objects, fields, relationships, security, automation, the metadata model. If these are fuzzy, the rest is memorization. Use the crash course page and the Platform App Builder/Administrator material.
2. **PD1-level Apex** — triggers, bulkification, testing, order of execution, debug/deployment tools. You need to read code, not write a framework.
3. **Metadata API and the CLI** — retrieve, deploy, validate, test, report, packages. This is the daily tool.
4. **Git and branching** — feature/release/hotfix, pull requests, tags, conflict resolution.
5. **CI/CD** — the five-job pipeline, JWT auth, environment approvals, evidence.
6. **Limits, dependencies, constraints** — the section 13 material. This is the interview differentiator.
7. **Vendor tool** — one of Gearset/Copado/AutoRABIT, hands-on. Learn compare/deploy, CI, pipeline, backup, monitoring, audit.
8. **Regulated-environment controls** — segregation of duties, masking, change windows, emergency path, audit pack.

## 3. A 10-week plan

| Week | Focus | Evidence you can show |
|---|---|---|
| 1 | Platform fundamentals: objects, fields, relationships, security model | A data model diagram and a permission matrix |
| 2 | Automation: validation rules, Flow before/after save, order of execution | A before-save Flow and an after-save Flow, with a test plan |
| 3 | Apex: triggers, handler pattern, bulkification, recursion | A trigger + handler + test that inserts 200 records |
| 4 | Testing and limits | A test class with coverage and a bulk test; a debug log showing `Limits` output |
| 5 | Metadata API and CLI | A retrieve, a dry-run, a real deploy, a destructive change manifest |
| 6 | Git and branching | A repo with `main`, `release/*`, `feature/*`, `hotfix/*`, PR templates, tags |
| 7 | CI/CD | A GitHub Actions workflow that validates a PR and quick-deploys a validated job |
| 8 | Vendor tool | A Gearset/Copado/AutoRABIT compare, validation, pipeline, and backup screenshot (no customer data) |
| 9 | Limits/dependencies/constraints deep dive | A failure lab: missing dependency, profile conflict, inactive Flow, missing named credential |
| 10 | Regulated release simulation | A filled runbook, an audit pack, a rollback rehearsal, a mock interview |

## 4. Portfolio evidence that beats a certificate list

- A public or sanitized repo with a Salesforce DX project, a manifest, and a pipeline.
- A test class that proves bulk safety (200 records, one SOQL, one DML).
- A before/after Flow pair with a written explanation of why each is before/after.
- A permission-set design that avoids profile edits.
- A deployment runbook and a rollback plan for a fake release.
- A one-page "limits and dependencies" cheat sheet you wrote yourself.
- A vendor-tool walkthrough with screenshots from a free trial or Developer org (no customer data).

## 5. How to talk about certifications in the interview

- "I have PD1-level Apex and testing knowledge" is stronger than "I am studying for PD1" if you can show the lab.
- "Advanced Administrator is now Platform Administrator II" shows you are current.
- "There is no official Salesforce DevOps certification; I have hands-on pipeline evidence plus vendor tool time" is the honest, senior answer.
- Do not list a certificate you do not hold. Do not imply a vendor certificate is a Salesforce credential.

## 6. What to merge

**Merge:** the vendor table (with the caveat), the study order, the 10-week plan, and the portfolio evidence list.

**Compress:** the 10-week plan into a 6-step study order if the page is short.

**Do not merge:** specific prices, pass rates, or certificate names that are not verified on the vendor site at merge time.

<!-- ===== end: 05-certifications/vendor-and-study-plan.md ===== -->

---

<!-- ===== begin: 06-term-deep-dives/term-index.md ===== -->

# Term index — every posting line mapped

**Merge target:** section 14 of the downstream page (term-by-term deep dive). Use this index to check coverage; use `term-entries.md` for the content.

## Responsibilities

| # | Term / posting line | Research unit | Page section |
|---|---|---|---|
| R1 | CI/CD pipelines using Git-based workflows | `04-cicd/`, entry "CI/CD pipelines" | 5, 5.1, 14 |
| R2 | Multi-environment release strategy (Dev, QA, UAT, Pre-Prod, Prod) | `01-salesforce-key-principles/release-model.md`, entry "Multi-environment strategy" | 3, 14 |
| R3 | Scheduled releases, hotfixes, emergency deployments | `01-salesforce-key-principles/release-model.md`, entry "Three release speeds" | 4, 10, 14 |
| R4 | Audit, security, compliance | entry "Audit, security, compliance" | 11, 14 |
| R5 | Metadata lifecycle using source control (Git) | `01-salesforce-key-principles/principles.md`, entry "Git and metadata lifecycle" | 1, 4, 14 |
| R6 | Sandbox strategy (creation, refresh, data masking) | entry "Sandbox strategy" | 3, 14 |
| R7 | Deployment conflicts: profiles/permission sets, record types/layouts, Flows/Apex/dependencies | entries "Permission sets vs profiles", "Record types", "Page layouts", "Flows", "Apex and triggers" | 7, 14 |
| R8 | Best practices to reduce deployment failures and rework | `01-salesforce-key-principles/principles.md`, entry "DevOps-friendly design patterns" | 12, 14 |
| R9 | Partner with Developers, Admins, QA, Platform teams | `01-salesforce-key-principles/principles.md` | What this role owns |
| R10 | DevOps-friendly design patterns | entry "DevOps-friendly design patterns" | 12, 14 |
| R11 | Release processes, runbooks, rollback | entries "Runbook and rollback", "Three release speeds" | 10, 14 |
| R12 | Audit and change management | entry "Audit, security, compliance" | 11, 14 |

## Requirements

| # | Term / posting line | Research unit | Page section |
|---|---|---|---|
| Q1 | Salesforce metadata deployments | entry "Metadata deployments" | 1, 2, 13, 14 |
| Q2 | Git-based source control | entry "Git and metadata lifecycle" | 1, 4, 14 |
| Q3 | Salesforce limits, metadata dependencies, deployment constraints | `02-limits-constraints/` (all files) | 13, 14 |
| Q4 | CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab) | `04-cicd/` (all files) | 5, 5.1, 14 |
| Q5 | Branching strategies (feature, release, hotfix) | `01-salesforce-key-principles/release-model.md`, entry "Branching" | 4, 14 |
| Q6 | Automated testing and validation | entry "Automated testing and validation" | 9, 14 |
| Q7 | Gearset, Copado, AutoRABIT, or equivalent | `03-devops-tools/` (all files) | 6, 6.1, 14 |
| Q8a | Apex and Triggers | entry "Apex and triggers" | 7, 14 |
| Q8b | Flows (before/after save) | entry "Flows" | 7, 14 |
| Q8c | Permission sets vs profiles | entry "Permission sets vs profiles" | 7, 14 |
| Q8d | Record types | entry "Record types" | 7, 14 |
| Q8e | Page layouts | entry "Page layouts" | 7, 14 |
| Q8f | Security model | entry "Security model" | 7, 14 |
| Q9 | Troubleshooting deployment failures and dependency issues | entry "Troubleshooting", `02-limits-constraints/dependencies-and-constraints.md` | 2, 13, 14 |
| Q10 | Salesforce Platform Developer experience | entry "Platform Developer experience" | 14 |
| Q11 | Unlocked packages / managed packages | entries "Unlocked packages" and "Managed packages" | 8, 14 |
| Q12 | Salesforce DX | entry "Salesforce DX" | 1, 14 |
| Q13 | Regulated / enterprise environments | entry "Regulated environments" | 11, 14 |
| Q14 | Certifications (PD1, Advanced Admin, DevOps related) | `05-certifications/` (all files) | Certifications, 14 |

## Cross-cutting terms

| Term | Where |
|---|---|
| Sandbox creation, refresh, masking | entry "Sandbox strategy"; `01-salesforce-key-principles/release-model.md` |
| Data masking | entry "Sandbox strategy"; `02-limits-constraints/other-limits-and-system-settings.md` |
| Change management / CAB | entry "Audit, security, compliance" |
| Rollback / tag | entry "Runbook and rollback" |
| Audit evidence | entry "Audit, security, compliance" |
| System settings / org properties | `02-limits-constraints/other-limits-and-system-settings.md` |
| Governor limits | `02-limits-constraints/governor-limits.md` |
| Metadata dependencies | `02-limits-constraints/dependencies-and-constraints.md` |
| Deployment constraints | `02-limits-constraints/dependencies-and-constraints.md` |

<!-- ===== end: 06-term-deep-dives/term-index.md ===== -->

---

<!-- ===== begin: 06-term-deep-dives/term-entries.md ===== -->

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

<!-- ===== end: 06-term-deep-dives/term-entries.md ===== -->

---

<!-- ===== begin: 07-merge/merge-map.md ===== -->

# Merge map — research file → downstream page

**For the round-2 merge agent.** This file is instructions, not page content.

## 1. Target structure

The current page is `docs/salesforce/devops-engineer.md` in `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`. It has sections 1–12, Labs, Interview drills, Certifications, Quiz, and Related pages.

Recommended target structure:

```text
Header
Contents
What this role actually owns
Training items
JD coverage matrix                  ← new
1. Source of truth
2. Metadata that breaks releases
3. Environments and sandboxes
4. Branching
5. CI/CD
5.1 GitHub Actions pipeline         ← new
6. DevOps tools
6.1 Tool click-paths                ← new
7. Conflict clinic
8. Packages
9. Tests and validation
10. Releases, hotfixes, rollback
11. Banking change control
12. Design patterns
13. Limits, system settings, dependencies, constraints   ← new
14. JD term-by-term deep dive       ← new
Labs
Interview drills
Certifications
Quiz
Related pages
```

## 2. File-to-section map

| Research file | Page section | Action | Notes |
|---|---|---|---|
| `00-source-log/job-description.md` | Header + new JD coverage matrix | Insert matrix; update header | Keep the posting URL and requisition id. Do not paste the full JD. |
| `01-salesforce-key-principles/principles.md` | Intro, 11, 12, 14 | Weave in | Use the one-line interview answers, not the whole file |
| `01-salesforce-key-principles/release-model.md` | 3, 4, 10 | Expand | The page already has the shape; add the runbook/rollback detail and the environment gates |
| `02-limits-constraints/governor-limits.md` | New 13.1 | Insert | Keep the table and the bad/good Apex example; compress cursor rows |
| `02-limits-constraints/other-limits-and-system-settings.md` | New 13.2, 13.3 | Insert | Keep the system-settings table and the pre-flight checklist |
| `02-limits-constraints/dependencies-and-constraints.md` | New 13.4, 13.5; expand 2 and 7 | Insert | Keep the dependency graph, the record-type manifest, and the constraints table |
| `02-limits-constraints/inspection-and-drills.md` | New 13.6, 13.7 | Insert | Keep the inspection map, the command set with the `--help` note, and the drills |
| `03-devops-tools/tool-landscape.md` | 6 | Expand | Keep the layer cake and the selection matrix |
| `03-devops-tools/gearset-click-paths.md` | New 6.1 | Insert | Keep the task tables and the "verify in your tenant" caveat |
| `03-devops-tools/copado-autorabit-devopscenter.md` | New 6.1 | Insert/compress | Keep the Copado and DevOps Center tables; compress AutoRABIT |
| `04-cicd/github-actions-salesforce.md` | New 5.1 | Insert | Put the YAML in a collapsible block; keep the five-job table and the why table |
| `04-cicd/auth-secrets-environments.md` | 5.1, 11 | Insert | Keep the JWT flow, secrets table, environment approvals, and segregation-of-duties table |
| `04-cicd/other-ci-platforms.md` | 5 | Insert a short subsection | Keep the concept mapping and the invariants; no need for all three full pipelines |
| `05-certifications/certification-landscape.md` | Certifications, 14 | Replace/expand | Correct "Advanced Admin" to Platform Administrator II; state that no official DevOps cert exists |
| `05-certifications/salesforce-credentials.md` | Certifications | Expand | Keep the domain tables and study emphasis; do not publish unverified weights |
| `05-certifications/vendor-and-study-plan.md` | Certifications | Expand | Keep the vendor table with the caveat and the 10-week plan |
| `06-term-deep-dives/term-index.md` | 14 | Use as a checklist | Do not paste the index; it is for coverage |
| `06-term-deep-dives/term-entries.md` | 14 | Convert to collapsibles | Keep the five-part shape; compress entries already covered by 13 |
| `08-cross-bundle-notes.md` | — | Read before editing | Reconciles this bundle with the sibling `2026-11-14T020300Z-kilo-salesforceagain` bundle; lists verified corrections |
| `07-merge/content-gaps.md` | — | Read before editing | Lists the specific changes and priorities |

## 3. Collapsible markup

The downstream page is Jekyll + kramdown. Raw HTML blocks do **not** parse markdown by default. Use:

```html
<details markdown="1">
<summary><strong>Term — one-line description</strong></summary>

Markdown here, including tables and code fences.

</details>
```

Do **not** copy the `<details>` style from some other pages in the repo that omit `markdown="1"`; their inner tables render as raw pipes. The devops page should render correctly.

Add a blank line after `<summary>` and before `</details>`.

## 4. Content changes by priority

### P0 — required for the user's request

1. Add **13. Limits, system settings, dependencies, and deployment constraints** with the governor-limit table, the system-settings table, the dependency graph, and the constraints table.
2. Add **14. JD term-by-term deep dive** with a collapsible entry for every posting term.
3. Add **6.1 Tool click-paths**, with Gearset compare/deploy, CI, pipelines, backup, monitoring, and audit paths.
4. Add **5.1 GitHub Actions pipeline** with the runnable YAML, the five-job table, and the "why" table.
5. Add the **JD coverage matrix** near the top.

### P1 — quality improvements

6. Update the header confidence line: button-paths are now included, with a verify caveat.
7. Update the Contents list for 5.1, 6.1, 13, 14.
8. Expand the Certifications section with the PD1/App Builder/Admin II curricula and the "no official DevOps cert" statement.
9. Add the pre-flight checklist for a target org.

### P2 — optional

10. Add the Azure DevOps / GitLab concept mapping.
11. Add the 10-week study plan.
12. Add the full error-to-fix table if section 2 becomes too long.

## 5. Facts that must keep a caveat

- Apex governor numbers: "verify current release".
- Metadata payload ceiling (~39 MB compressed / ~600 MB uncompressed; 10,000 files for unlocked/2GP, 35,000 for AppExchange-reviewed 1GP): "verify the current Metadata API `deploy()` reference".
- Gearset/Copado/AutoRABIT/DevOps Center UI labels: "verify in your tenant; labels drift".
- Certification exam weights: do not publish without the current official exam guide.
- Scotiabank process: describe a regulated-environment pattern, not an internal procedure.

## 6. What not to merge

- Secrets, org auth files, JWT keys, consumer secrets, customer data.
- Any claim that a vendor UI path is universal.
- Any claim that a Salesforce DevOps Engineer certification officially exists.
- Any invented bank policy, approver, environment name, or licence.
- The full job description verbatim; use the coverage matrix.

## 7. Acceptance check for the merge

- [ ] Every posting bullet appears in the coverage matrix.
- [ ] Section 13 covers governor limits, org/platform limits, system settings, dependencies, and constraints.
- [ ] Section 14 has an entry for every term in the index.
- [ ] Section 6.1 has Gearset compare/deploy, CI, pipelines, backup, monitoring, and audit.
- [ ] Section 5.1 has a runnable YAML and a why table.
- [ ] All `<details>` blocks use `markdown="1"`.
- [ ] All changeable facts carry a caveat.
- [ ] No secrets or customer data.

## 8. Sibling-page opportunities

The research also feeds the other Salesforce guides in the same repo, not just the DevOps page.

| Research file | Sibling page | Suggested addition |
|---|---|---|
| `02-limits-constraints/governor-limits.md` | Salesforce Crash Course (`docs/salesforce/crash-course.md`) | A compact governor-limits table and the 200/10,000-record review questions; link to the DevOps page for the full deep dive |
| `02-limits-constraints/dependencies-and-constraints.md` | Crash Course; Labs & Design (`docs/salesforce/labs-design.md`) | A "missing dependency" lab and an error-to-fix table |
| `03-devops-tools/gearset-click-paths.md` | Navigation & Breadcrumbs (`docs/salesforce/navigation-breadcrumbs.md`) | A "Deployment & DevOps" row set: Setup → Deploy → Deployment Status, Setup → Sandboxes, Setup → DevOps Center, plus vendor-tool paths |
| `04-cicd/auth-secrets-environments.md` | Labs & Design | A lab: create a JWT auth flow, store a key in a CI secret, validate a deploy, never commit the key |
| `05-certifications/salesforce-credentials.md` | Learning Paths page (general docs) | A study order and the current credential names (Platform Administrator II, not "Advanced Admin") |
| `06-term-deep-dives/term-entries.md` | Crash Course; Interview Prep | Short definitions and the "interview line" for Apex, Flow, permission sets, record types, layouts, security |
| `02-limits-constraints/other-limits-and-system-settings.md` | User Management & Data (`docs/salesforce/user-management-data.md`) | A pre-flight checklist for permissions, SSO, named credentials, and email deliverability in a sandbox |
| `01-salesforce-key-principles/principles.md` | DevOps page; Crash Course | The principles spine as a shared intro; reuse the one-line answers |

**Rule for sibling pages:** add a short section and link to the DevOps page for the full treatment. Do not duplicate the full limits/dependency tables across four pages; the repo will drift.

<!-- ===== end: 07-merge/merge-map.md ===== -->

---

<!-- ===== begin: 07-merge/content-gaps.md ===== -->

# Content gaps and recommendations

**For the merge agent.** This is the audit of the current downstream page against the research. It explains what to change, not just what to add.

## 1. What the current page does well

- The role ownership table is clear and senior.
- Sections 1–12 cover the mechanics: source of truth, metadata failures, environments, branching, CI stages, tools, conflicts, packages, tests, releases, banking control, design patterns.
- The conflict clinic is strong on profiles, permission sets, record types, layouts, Flows, and Apex.
- The runbook template, rollback table, and audit-pack list are directly useful.
- The quiz and interview drills are good.

## 2. Gaps against the user's request

| Gap | Current state | What to add | Priority |
|---|---|---|---|
| Governor limits | The page only points to the crash course | A full per-transaction table, the org-wide limits, bulkification examples, `Limits` snippet, drills | P0 |
| Other limits | Not covered | API usage, metadata payload, storage, concurrency, email, Flow, custom-object caps | P0 |
| System settings / "system properties" | Not covered | Feature enablement, settings metadata, SSO, named credentials, certificates, email deliverability, sharing | P0 |
| Metadata dependencies | A failure table, no graph | Parent/child graph, deploy-order rules, record-type manifest, error-to-fix table | P0 |
| Deployment constraints | Scattered | A single constraints table with workarounds | P0 |
| Gearset UI | Category-level only | Compare/deploy, CI, pipelines, backup, data, monitoring, audit click-paths | P0 |
| Copado/AutoRABIT/DevOps Center | Category-level only | Task tables with caveats | P1 |
| GitHub Actions pipeline | Stage table only | Runnable YAML, five-job model, JWT auth, environment approvals, "why" table | P0 |
| Certifications | A short mapping table | Current names, curricula, vendor certs, study plan, "no official DevOps cert" | P1 |
| Term-by-term depth | Not present | A collapsible entry for every posting term | P0 |
| JD cross-reference | Training table, not a full matrix | A line-by-line matrix for responsibilities and requirements | P1 |

## 3. Specific edits

### 3.1 Header

- Update "Confidence" because the page now includes vendor click-paths. Suggested: "high on platform mechanics; vendor UI labels drift, so click-paths carry a verify-in-your-tenant caveat."
- Add a "Last expanded" date and a one-line summary of the new sections.

### 3.2 Contents

Add:

- JD coverage matrix
- 5.1 GitHub Actions pipeline, end to end
- 6.1 Tool click-paths
- 13. Limits, system settings, dependencies, and deployment constraints
- 14. JD term-by-term deep dive

### 3.3 Training items

Add rows 13 and 14:

| # | Item | JD line | Done when |
|---|---|---|---|
| 13 | Limits and constraints | Limits, dependencies, constraints | You can name the limit family, the setting, and the missing dependency for a failed deploy |
| 14 | Term deep dive | Every posting line | You can answer any term in 60 seconds |

### 3.4 Section 2

- Keep the failure table.
- Add the dependency graph and the error-to-fix table from `02-limits-constraints/dependencies-and-constraints.md`.
- Add a "deployment failure decision tree" or the troubleshooting method.

### 3.5 Section 3

- Keep the sandbox table.
- Add the refresh-completion checklist: masking, integration cut-over, SSO, access.
- Add the system-settings pre-flight checklist from `02-limits-constraints/other-limits-and-system-settings.md`.

### 3.6 Section 5

- Keep the stage table.
- Add 5.1 with the five-job model, the YAML, the JWT auth, the environment approvals, and the "what not to do" list.
- Add the Azure/GitLab concept mapping as a short subsection.

### 3.7 Section 6

- Keep the tool table.
- Add 6.1 with the Gearset task table, the Copado/DevOps Center tables, the Change Sets "why fail" list, and the CLI set.
- Add the selection matrix.

### 3.8 Section 7

- Keep the conflict clinic.
- Add the "why profiles conflict" permission-diff review step and the record-type four-part rule if not already clear.

### 3.9 Section 8

- Keep the package table.
- Add the package version/`04t` example and the "do not package the whole org" warning.

### 3.10 Section 9

- Keep the validate/quick deploy/real deploy table.
- Add the test levels and the `RunLocalTests` trade-off.
- Add the "tests create their own data" example.

### 3.11 Section 10

- Keep the three speeds and the runbook.
- Add the rollback table's "Git revert does not restore data" warning.
- Add the release tag as the rollback target.

### 3.12 Section 11

- Keep the audit-pack list.
- Add the segregation-of-duties table and the environment-approval mechanics.
- Add the "author is not the approver" rule.

### 3.13 Section 12

- Keep the design-pattern table.
- Add the "no environment branches" and "custom metadata toggles" examples.
- Add the "design so the deploy is boring" line.

### 3.14 New Section 13

Use `02-limits-constraints/` as the source. Keep the collapsible subsections:

1. Apex governor limits
2. Org-wide platform limits
3. System settings and org properties
4. Metadata dependencies
5. Deployment constraints
6. How to inspect limits
7. Limit-aware design and drills

### 3.15 New Section 14

Use `06-term-deep-dives/term-entries.md`. Convert each term to a `<details markdown="1">` block. Keep the five-part shape but compress entries already covered by section 13.

### 3.16 Certifications

- Correct the names: Platform Administrator and Platform Administrator II.
- State that there is no official Salesforce DevOps Engineer certification.
- Add the domain tables and study emphasis.
- Add the vendor certificate table with the caveat.
- Add the 10-week plan or a 6-step study order.

## 4. Technical rendering note

The repo uses Jekyll + kramdown. Raw HTML blocks do not parse markdown by default. Use:

```html
<details markdown="1">
<summary><strong>Title</strong></summary>

Markdown content.

</details>
```

Some existing pages in the repo use `<details>` without `markdown="1"`, and their inner tables render as raw pipes on the live site. Do not copy that pattern for the new devops sections.

## 5. What not to change

- Do not remove the existing labs, interview drills, quiz, or runbook template; they are good.
- Do not replace the banking change-control section with a generic DevOps essay.
- Do not add a vendor-specific procedure as if it were the bank's official process.
- Do not publish exact certification weights without the current official exam guide.
- Do not publish a real org id, consumer key, certificate, secret, or customer data.

## 6. Suggested merge order

1. Header + Contents.
2. JD coverage matrix.
3. Section 13 (limits/dependencies/constraints).
4. Section 14 (term deep dives).
5. Section 6.1 (tools) and Section 5.1 (pipeline).
6. Certifications.
7. Verify all `<details>` blocks and links.
8. Re-read the page as an interviewer: can every posting bullet be answered in one sentence?

<!-- ===== end: 07-merge/content-gaps.md ===== -->

---

<!-- ===== begin: 08-cross-bundle-notes.md ===== -->

# Cross-bundle notes — sibling research and reconciliation

**For the merge agent.** This bundle is one of at least two research drops for the same Scotiabank requisition. This file records the overlap, the corrections, and which bundle to prefer where.

## 1. Sibling bundle

| Field | Value |
|---|---|
| Sibling folder | `research/2026-11-14T020300Z-kilo-salesforceagain/` |
| Worktree | `salesforceagain` |
| Started | 2026-11-14T02:03:00Z |
| Status at write time | README and `00-plan.md` present; detailed artifacts in flight |
| Relationship | Independent research; same job, same downstream page |

The sibling README's headline findings triggered a verification pass in this bundle. The items below were checked against primary sources on 2026-11-14.

## 2. Verified corrections applied to this bundle

| # | Claim in the sibling README | Verification | Action in this bundle |
|---|---|---|---|
| 1 | Metadata API deploy ceiling is ~39 MB compressed / ~600 MB uncompressed, 10,000 files for unlocked/2GP, 35,000 for AppExchange-reviewed 1GP | Confirmed on the [Metadata API `deploy()` reference](https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html) | Replaced the earlier "10,000 components / 400 MB" figure in `02-limits-constraints/other-limits-and-system-settings.md` |
| 2 | Only one deployment runs at a time per org; queued deployments are not necessarily executed in submission order | Confirmed on the same `deploy()` reference | Added to `02-limits-constraints/other-limits-and-system-settings.md`, `dependencies-and-constraints.md`, `inspection-and-drills.md`, and `04-cicd/github-actions-salesforce.md` |
| 3 | There are five test levels, including `RunRelevantTests` (Beta), not four | Confirmed in the [Salesforce CLI deploy messages](https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md) and the `source-deploy-retrieve` types; requires API 66.0+ | Added the five-level table to `02-limits-constraints/dependencies-and-constraints.md`; updated the term entry, drills, and CI trade-offs |
| 4 | Gearset's current UI is grouped into My connections, Metadata deployments, Continuous delivery, Backup & archiving, Sandbox seeding & compliance, Problem analyzers, Observability, Settings | Confirmed by the [Gearset docs collections](https://docs.gearset.com/en/) and the article lists in those collections | Rewrote `03-devops-tools/gearset-click-paths.md` around the current categories; kept older labels in parentheses |
| 5 | Gearset backup is a separately licensed data + metadata backup product; Gearset does not perform or schedule the Salesforce sandbox refresh | Confirmed by the Backup & archiving collection (data backup/restore, restoring metadata) and the Sandbox seeding collection (seeding/masking around a refresh) | Added the correction to `gearset-click-paths.md`; removed any implication that Gearset refreshes the sandbox |
| 6 | Copado's current branding includes Copado CI/CD, Copado Essentials, Agentia, Robotic Testing, AI Platform; "Copado Fundamentals" and a Copado "DevOps Center" tier are not current names | Confirmed by the [Copado platform page](https://www.copado.com/platform-overview) | Updated `03-devops-tools/copado-autorabit-devopscenter.md` and `tool-landscape.md` |
| 7 | AutoRABIT's current products are ARM (CI/CD), Vault (backup/restore), CodeScan (static analysis), Guard (security posture); "Test Repository" and standalone "Data Masking" are not current product names | Confirmed by the [AutoRABIT products page](https://www.autorabit.com/products/) | Updated `03-devops-tools/copado-autorabit-devopscenter.md` and `tool-landscape.md` |
| 8 | Advanced Admin is now Platform Administrator II, with Platform Administrator as a prerequisite | Confirmed on the [Platform Administrator II credential page](https://trailhead.salesforce.com/credentials/platformadministrator-ii) | Already in this bundle; the prerequisite is now explicit in `05-certifications/` |

## 3. Where this bundle is the better source

| Area | Why |
|---|---|
| Apex governor limits | Full per-transaction table plus org-wide/24-hour limits, with the official source and bulkification examples |
| System settings / org properties | A dedicated table of feature enablement, SSO, named credentials, certificates, email deliverability, sharing, and what deploys vs what does not |
| Metadata dependencies | A parent/child graph, deploy-order rules, a record-type manifest, and an error-to-fix table |
| GitHub Actions pipeline | A runnable five-job YAML, JWT auth, environment-scoped secrets, required reviewers, and a "why" table |
| Certifications | PD1, Platform App Builder, Platform Administrator, Platform Administrator II domain tables; vendor certificates; a 10-week study plan |
| Term-by-term entries | Every posting term with definition, why, example, failure mode, interview line |
| Sibling-page mapping | `07-merge/merge-map.md` maps the bundle to the crash course, breadcrumbs, labs, and user/data pages |

## 4. Where the sibling bundle may be the better source

| Area | Why |
|---|---|
| Vendor UI click-paths and plan gates | The sibling README says it ran dedicated vendor-documentation agents and cross-read the Salesforce CLI plugin source. If its `03-devops-tools-ui.md` is primary-source verified, prefer it over this bundle's category-level tables. |
| Exact Gearset/Copado/AutoRABIT feature packaging | The sibling explicitly tracks plan gates and corrections (for example, which Gearset features are separately licensed). Prefer its detail where it cites current vendor docs. |
| Metadata API deploy limits | We now agree on the numbers; prefer whichever file has the most direct citation. Both point to the `deploy()` reference. |
| "Fifth test level" and deployment queue order | We now agree; use the table in this bundle or the sibling's equivalent. |

## 5. Merge recommendation

1. **Use the sibling bundle for vendor UI detail** if its artifacts are complete and primary-source cited. Use this bundle for the limits/constraints spine, the CI/CD YAML, the certification curricula, and the term-by-term structure.
2. **Reconcile disagreements with a primary source, not with a vote.** Record the resolution in the merge notes.
3. **Do not merge both vendor-UI sections verbatim.** The page will contradict itself on menu labels. Pick one current label set and keep the "verify in your tenant" caveat.
4. **Keep the corrections.** The five test levels, the 39/600 MB deploy ceiling, the one-deployment-at-a-time queue, and "Gearset does not refresh the sandbox" are all worth publishing because they correct common interview answers.
5. **Do not publish a certification percentage** unless the current official exam guide has been fetched and cited. Domain names and study-guide links are enough.

## 6. Open items

- The sibling bundle's detailed files were not present when this note was written. Re-read them before merge; update this file if a new disagreement appears.
- The exact Gearset enterprise plan gates and Copado/AutoRABIT edition packaging should be confirmed against the bank's contract, not a public pricing page.
- Salesforce release notes can change the deploy limits and test levels. Re-check the `deploy()` reference on the merge date.

<!-- ===== end: 08-cross-bundle-notes.md ===== -->

---

<!-- ===== begin: 00-source-log/SOURCES.md ===== -->

# Source log

Access date for all sources: **2026-11-14**.

## Primary sources

| # | Source | URL | Used for | Confidence | Notes |
|---|---|---|---|---|---|
| S1 | Scotiabank job posting, Requisition 276046 | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> | Scope contract: responsibilities and requirements | High | Public posting; captured in `job-description.md` |
| S2 | Salesforce DevOps Engineer training page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> | Current downstream content and section structure | High | Read-only reference; merge target |
| S3 | Apex execution governors and limits | <https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html> | Governor limit tables, async limits, cross-namespace limits | High | Developer docs blocked a direct browser fetch; content retrieved via a reader proxy on 2026-11-14. Verify numbers in the current release. |
| S4 | Metadata API guide | <https://developer.salesforce.com/docs/platform/api-metadata/guide/> | Deploy/retrieve model, metadata vs data | High | The old `meta_limits.htm` URL returned 404; the current deploy limits are on the `deploy()` reference (S23) |
| S5 | Salesforce Help — Sandboxes | <https://help.salesforce.com/s/articleView?id=sf.deploy_sandboxes_parent.htm&type=5> | Sandbox types and refresh | High | Help pages are JavaScript-heavy; use the in-product Help for exact steps |
| S6 | Salesforce Help — Quick Deploy | <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> | Validate vs quick deploy | High | Same access caveat |
| S7 | Salesforce Help — Data Mask | <https://help.salesforce.com/s/articleView?id=sf.data_mask.htm&type=5> | Masking | High | Product availability varies by licence |
| S8 | Salesforce Help — DevOps Center overview | <https://help.salesforce.com/s/articleView?id=sf.devops_center_overview.htm&type=5> | Native pipeline | High | Enablement required |
| S9 | Trailhead — Platform Developer I credential | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Credential description and study trail | High | Credential page is stable; exam weights are not on the page |
| S10 | Trailhead — Platform App Builder credential | <https://trailhead.salesforce.com/credentials/platformappbuilder> | Credential description and study trail | High | Same |
| S11 | Trailhead — Platform Administrator credential | <https://trailhead.salesforce.com/credentials/platformadministrator> | Administrator prerequisite | High | The old "Administrator" credential is now Platform Administrator |
| S12 | Trailhead — Platform Administrator II credential | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Current name for Advanced Administrator | High | Requires Platform Administrator as prerequisite |
| S13 | Trailhead — Platform Developer I study trail | <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> | Curriculum domains | Medium | Trail module list loads dynamically; domains taken from the official exam outline categories |
| S14 | Trailhead — Platform App Builder study trail | <https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-platform-app-builder-certification> | Curriculum domains | Medium | Same |
| S15 | Gearset documentation | <https://docs.gearset.com/en/> | Compare/deploy, CI, pipelines, backup, monitoring | Medium–High | Public docs; UI labels vary by edition |
| S16 | DevOps Launchpad (Gearset) | <https://devopslaunchpad.com/> | Free Salesforce DevOps certificate tracks | High | Lists Fundamentals, CI/CD, Leadership, Backup, Gearset Academy |
| S17 | Copado | <https://www.copado.com/> | Pipeline, user story, promotion, compliance | Medium | Product pages; certification URL returned 404 on 2026-11-14 |
| S18 | AutoRABIT | <https://www.autorabit.com/> | CI, deployment, data, backup, monitoring | Medium | Product pages are JavaScript-heavy; module names vary by edition |
| S19 | Salesforce CLI command reference | <https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/> | `sf` commands and flags | High | Flags move; always confirm with `--help` |
| S20 | GitHub Actions documentation | <https://docs.github.com/en/actions> | Workflows, environments, secrets, approvals | High | Feature availability depends on plan |
| S21 | `sfdx-git-delta` | <https://github.com/scolladon/sfdx-git-delta> | Delta manifest generation | Medium–High | Community plugin; verify command flags |
| S22 | Salesforce Help — API usage / limits | In-product: Setup → Company Information → API Usage | Org API allocation | High | Exact allocation is edition/licence-specific; inspect your org |
| S23 | Metadata API `deploy()` reference | <https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html> | Deploy limits (≈39 MB compressed / ≈600 MB uncompressed; 10,000 / 35,000 files), one deployment at a time, queue order, five test levels | High | Limits can change without notice; re-check on merge |
| S24 | Salesforce CLI deploy messages | <https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md> | `RunRelevantTests` (Beta, API 66.0+) description and the five test levels | High | CLI messages track the current implementation |
| S25 | Gearset docs collections | <https://docs.gearset.com/en/> | Current UI groupings: My connections, Metadata deployments, Continuous delivery, Backup & archiving, Sandbox seeding & compliance, Problem analyzers, Observability, Settings | Medium–High | Labels vary by edition; article lists checked on 2026-11-14 |
| S26 | Copado platform overview | <https://www.copado.com/platform-overview> | Current branding: Copado CI/CD, Copado Essentials, Agentia, Robotic Testing, AI Platform | Medium–High | Product packaging changes; verify the bank's licence |
| S27 | AutoRABIT products | <https://www.autorabit.com/products/> | ARM (CI/CD), Vault (backup/restore), CodeScan (static analysis), Guard (security posture) | Medium–High | Product packaging changes; verify the bank's licence |

## Source-quality notes

- **Official Salesforce docs are the authority for limits and platform behaviour.** Exact numbers change; the research keeps a verify note on every table.
- **Vendor UI paths are the least stable part of this research.** Gearset, Copado, AutoRABIT, and DevOps Center rename menus between editions. The bundle gives the task, the likely navigation, what to click, and what to verify. The merge agent must keep the caveat.
- **Certification exam weights were not copied from memory.** The bundle lists domains and official study-guide links. Add percentages only from the current official exam guide PDF.
- **No internal Scotiabank process is asserted.** The bundle describes a defensible regulated-environment pattern, not the bank's actual runbook.
- **No secrets or customer data.** None is included.

<!-- ===== end: 00-source-log/SOURCES.md ===== -->

---

<!-- ===== begin: 00-source-log/job-description.md ===== -->

# Job description — Scotiabank Requisition 276046

**Merge target:** page header + JD coverage matrix. Do not paste the whole posting into the page; use it as the scope contract.

**Source:** <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/>
**Captured:** 2026-11-14.

## Header facts

| Field | Value |
|---|---|
| Title | DevOps Engineer (Salesforce) |
| Requisition ID | 276046 |
| Team | Commercial Banking Engineering |
| Location | Canada: Ontario: Toronto (M5H 1A1) |
| Focus | Salesforce release, deployment, and environment management; CI/CD; automation; platform reliability |

## Role summary (verbatim)

> The Commercial Banking Engineering team is seeking a Salesforce DevOps Engineer who will be responsible for ideation support, design, development, and implementation of software to ensure continuous improvement and evolution in the CB Salesforce ecosystem.
>
> We are looking for a Salesforce DevOps Engineer to own and evolve our Salesforce release, deployment, and environment management processes. This role sits at the intersection of Salesforce development, CI/CD, automation, and platform reliability, and plays a critical role in enabling fast, safe, and scalable Salesforce releases in an enterprise environment.
>
> The ideal candidate has hands on experience with Salesforce metadata deployments, DevOps tooling, and environment strategy, and can collaborate effectively with developers, admins, QA, and security teams.

## Responsibilities (verbatim bullets, numbered for mapping)

| ID | Bullet |
|---|---|
| R1 | Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows |
| R2 | Manage multi environment release strategies (Dev, QA, UAT, Pre Prod, Prod) |
| R3 | Coordinate scheduled releases, hotfixes, and emergency deployments |
| R4 | Ensure deployment activities follow audit, security, and compliance standards |
| R5 | Manage Salesforce metadata lifecycle using source control (Git) |
| R6 | Handle sandbox strategy (creation, refresh, data masking) |
| R7 | Resolve deployment conflicts related to: Profiles and Permission Sets; Record Types & Page Layouts; Flows, Apex, and dependencies |
| R8 | Recommend best practices to reduce deployment failures and rework |
| R9 | Partner with Salesforce Developers, Admins, QA, and Platform teams |
| R10 | Provide guidance on DevOps friendly Salesforce design patterns |
| R11 | Document release processes, runbooks, and rollback procedures |
| R12 | Support audit and change management requirements |

## Requirements (verbatim bullets, numbered for mapping)

| ID | Bullet |
|---|---|
| Q1 | Strong experience with Salesforce metadata deployments |
| Q2 | Experience with Git based source control |
| Q3 | Understanding of Salesforce limits, metadata dependencies, and deployment constraints |
| Q4 | Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab, etc.) |
| Q5 | Understanding of branching strategies (feature, release, hotfix) |
| Q6 | Familiar with automated testing and validation concepts |
| Q7 | Hands on experience with Salesforce DevOps tools such as: Gearset, Copado, AutoRabit, or equivalent |
| Q8 | Good understanding of: Apex & Triggers; Flows (Before/After Save); Permission Sets vs Profiles; Record Types, Page Layouts, and Security model |
| Q9 | Ability to troubleshoot deployment failures and dependency issues |
| Q10 | Salesforce Platform Developer experience |
| Q11 | Experience with Unlocked Packages / Managed Packages |
| Q12 | Exposure to Salesforce DX |
| Q13 | Experience in regulated or enterprise environments (banking, insurance, healthcare) |
| Q14 | Salesforce certifications (PD1, Advanced Admin, DevOps related certs) |

## Mapping table

| Requirement | Research file | Downstream page section |
|---|---|---|
| R1, Q4 | `04-cicd/github-actions-salesforce.md`, `04-cicd/auth-secrets-environments.md`, `04-cicd/other-ci-platforms.md` | 5, 5.1 |
| R2, R3 | `01-salesforce-key-principles/release-model.md`, `06-term-deep-dives/term-entries.md` | 3, 4, 10 |
| R4, R12 | `06-term-deep-dives/term-entries.md`, `04-cicd/auth-secrets-environments.md` | 11 |
| R5, Q2 | `01-salesforce-key-principles/principles.md`, `06-term-deep-dives/term-entries.md` | 1, 4 |
| R6 | `02-limits-constraints/other-limits-and-system-settings.md`, `06-term-deep-dives/term-entries.md` | 3 |
| R7, Q8 | `03-devops-tools/`, `06-term-deep-dives/term-entries.md` | 7 |
| R8, R10 | `01-salesforce-key-principles/principles.md`, `06-term-deep-dives/term-entries.md` | 12 |
| R9 | `01-salesforce-key-principles/principles.md` | What this role owns |
| R11 | `06-term-deep-dives/term-entries.md` | 10 |
| Q1 | `02-limits-constraints/dependencies-and-constraints.md` | 1, 2, 13 |
| Q3 | `02-limits-constraints/` (all files) | 13 |
| Q5 | `01-salesforce-key-principles/release-model.md` | 4 |
| Q6 | `04-cicd/github-actions-salesforce.md` | 9 |
| Q7 | `03-devops-tools/` (all files) | 6, 6.1 |
| Q8 | `06-term-deep-dives/term-entries.md` | 7, 14 |
| Q9 | `02-limits-constraints/dependencies-and-constraints.md`, `02-limits-constraints/inspection-and-drills.md` | 2, 13 |
| Q10 | `06-term-deep-dives/term-entries.md` | 14 |
| Q11 | `06-term-deep-dives/term-entries.md` | 8, 14 |
| Q12 | `06-term-deep-dives/term-entries.md` | 1, 14 |
| Q13 | `06-term-deep-dives/term-entries.md` | 11, 14 |
| Q14 | `05-certifications/` | Certifications, 14 |

## What the posting does not say

The posting does not name a specific CI vendor, source-control host, sandbox licence tier, or internal change-management tool. Do not invent them. The page should present a defensible pattern and say that the team's written procedure wins where it differs.

<!-- ===== end: 00-source-log/job-description.md ===== -->

---

