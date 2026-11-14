# 05 — JD Term-by-Term Decoder (Requisition 276046)

> **How to use this file:** each requisition line is decoded into four things — **what it means**, **the configuration/settings/variations behind it**, **what you actually do**, and **what a strong interview answer sounds like**. This is the merge agent's spine: everything else hangs off these terms.

---

# Part A — Responsibilities

## A1. "Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows"

<details>
<summary><strong>What it means</strong></summary>

You own the automation that takes a change from a developer's branch to production: validation, tests, deploy, approval, evidence. "Git based" means Git is the source of truth; the pipeline reads Git, not the org.

See `04-cicd-github-salesforce.md` for the full implementation.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Dimension | Variations |
|---|---|
| CI platform | GitHub Actions, Azure DevOps Pipelines, GitLab CI, Jenkins, Bitbucket Pipelines |
| Auth | JWT (connected app + certificate), SFDX auth URL, OAuth 2.0 (less common in CI) |
| Deploy unit | Full source, manifest (`package.xml`), delta (`sfdx-git-delta`), unlocked package version |
| Test level | `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg` |
| Trigger | PR open/sync, merge to branch, tag, schedule, manual dispatch |
| Approval | CI-native (GitHub Environments/Azure Environments/GitLab protected env), tool-native (Gearset/Copado), ITSM ticket |
| Environment promotion | Branch-to-env mapping, package promotion, tool pipeline stages |
| Secrets | CI secret store, environment-scoped secrets, external vault |
</details>

<details>
<summary><strong>What you do</strong></summary>

- Define stages: validate → integrate → release validate → prod deploy (+ rollback).
- Configure auth with a dedicated integration user and least-privilege permission set.
- Add delta logic, test gates, coverage gates, static analysis.
- Enforce approvals and concurrency locks.
- Keep the pipeline reproducible from Git + `sf` CLI so the vendor/tool is replaceable.
- Document the runbook and evidence pack.

</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"The pipeline is four gates: validate on PR, deploy on merge to the release branch, validate against Pre-Prod, then an approved quick deploy to Prod. The CI tool is a runner and an approval mechanism; the actual work is `sf` CLI against the Metadata API, and Git is the source of truth."*
</details>

---

## A2. "Manage multi-environment release strategies (Dev, QA, UAT, Pre Prod, Prod)"

<details>
<summary><strong>What it means</strong></summary>

You decide which environment type plays which role, how changes flow, and how parity is maintained. Five named stages, but the important part is **what each stage is allowed to prove**.

See `01` and `02` for the limits/dependency reasons behind the ladder.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Stage | Typical sandbox | Purpose | Promotion rule |
|---|---|---|---|
| Dev | Developer / Developer Pro (scratch org for packages) | Build + unit test | Commit to feature branch |
| QA | Developer Pro / Partial Copy | Automated validation + integration | Merge to release branch |
| UAT | Partial Copy (or masked Full) | Business acceptance | Release manager, from release branch |
| Pre-Prod | Full (or fresh Partial) | Dress rehearsal at prod-like volume | Release manager |
| Prod | Production | Customers | Approved deploy in change window |

**Sandbox type variations**

| Type | Metadata | Data | Refresh interval | Use |
|---|---|---|---|---|
| Developer | Yes | No | ~1 day | Isolated build |
| Developer Pro | Yes | No (more storage) | ~1 day | QA without data |
| Partial Copy | Yes | Template sample | ~5 days | UAT with sample data |
| Full | Yes | All production | ~29 days | Pre-Prod / performance |

**[Verify]** refresh intervals and storage are edition/licence dependent.

**Parity levers**

- Sandbox **templates** (which objects/records to copy for Partial).
- **Data masking** before broad access on Full.
- **Seeding** (Gearset/AutoRABIT) for deterministic test data.
- **Post-refresh checklist** (see `01` §8.2) because settings like email deliverability, SSO, named credentials, and connected apps drift after refresh.
- **API version pinning** across orgs.
</details>

<details>
<summary><strong>What you do</strong></summary>

- Draw the ladder and publish it.
- Define entry/exit criteria per stage ("UAT exit = business sign-off + no Sev-1/2").
- Schedule refreshes around the release calendar and API budgets.
- Never let a feature branch deploy to UAT; UAT gets the release branch.
- Re-verify org settings after every refresh.
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"Dev builds, QA proves automation, UAT proves the business, Pre-Prod proves production volume and configuration, Prod is customers. I match sandbox type to purpose, refresh and mask Full copies before broad access, and re-verify org settings because a refresh silently changes email deliverability, SSO, and credentials."*
</details>

---

## A3. "Coordinate scheduled releases, hotfixes, and emergency deployments"

<details>
<summary><strong>What it means</strong></summary>

Three speeds with different governance, not three names for the same deploy.

See `04` §2 and §9.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Speed | Branch | Approval | Test bar | Window |
|---|---|---|---|---|
| Scheduled | `release/<date>` | Standard CAB/change ticket | Full validation + UAT sign-off | Release calendar |
| Hotfix | `hotfix/<ticket>` from `main` | Same gates, smaller payload | Full validation | As soon as approved |
| Emergency | `hotfix/<ticket>` from `main` | Pre-written short chain (named approver) | Validation where possible; documented exception if not | Immediate, within an incident |

**Variations**

- **Release train** (fixed cadence) vs **continuous delivery** (on-demand).
- **Change freeze** periods (quarter-end, regulatory windows).
- **Feature flags** to ship dark and enable after deploy without a second deploy.
- **Emergency change** must still be **written down**; the short path is pre-approved, not improvised.
</details>

<details>
<summary><strong>What you do</strong></summary>

- Maintain the release calendar and freeze windows.
- Cut hotfixes from `main`; merge back to `main` and the open release branch.
- Keep a documented emergency path with named approvers.
- Tag every production deploy.
- Do the back-promotion immediately after a hotfix.
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"Scheduled releases use the release branch and a full validation. A hotfix is cut from main, goes through the same gates with a smaller payload, then merges back to main and any open release branch. Emergency is a shorter approval chain, not a skipped pipeline — the 2 a.m. path is already written."*
</details>

---

## A4. "Ensure deployment activities follow audit, security, and compliance standards"

<details>
<summary><strong>What it means</strong></summary>

In a bank, the deploy is the easy part; the **evidence** and **segregation of duties** are the deliverable.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Control | Salesforce / tool setting |
|---|---|
| Segregation of duties | CI environment reviewer + separate integration identity; Copado/Gearset approvals |
| Change traceability | Commit message ticket ID; user story/deployment record; PR link |
| Audit trail | Setup Audit Trail; Field Audit Trail (Shield/History); Event Monitoring |
| Access control | Least-privilege permission sets; login IP ranges; MFA; session settings |
| Data protection | Data Mask; Shield Platform Encryption; field audit; debug-log hygiene |
| Evidence retention | CI artifacts, deploy reports, validation/test IDs, tags |
| Destructive-change control | Explicit destructive manifests + second review + data backup |

**Variations**

- **SoD strictness** (author ≠ approver ≠ deployer, or author ≠ approver only).
- **Evidence system** (ServiceNow/Jira ticket vs tool record vs CI artifact).
- **Encryption** (Shield Platform Encryption / Cache-Only Key Service) — affects test data and search.
</details>

<details>
<summary><strong>What you do</strong></summary>

- Put the ticket ID in commits and PRs.
- Make the approval structural (environment protection), not cultural.
- Keep debug logs clean; do not paste customer data into tickets.
- Attach deploy/test/validation evidence to the ticket.
- Ensure a Full sandbox is masked and access-limited before broad login.
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"The developer who wrote the change does not approve their own production deploy. The integration user deploys, a human approves, and the pipeline stores the ticket, diff, validation ID, test evidence, deploy ID, and tag. For a Full sandbox I attach mask-complete evidence before anyone logs in broadly."*
</details>

---

## A5. "Manage Salesforce metadata lifecycle using source control (Git)"

<details>
<summary><strong>What it means</strong></summary>

Git is the source of truth; the org is a deploy target. You retrieve, review, commit, version, and deploy — and you treat drift as an incident.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Dimension | Variations |
|---|---|
| Project shape | `sfdx-project.json` + `force-app` (source format), or manifest-based (`package.xml`) |
| Repo layout | Single app repo, monorepo with package directories, one repo per package |
| Ignore rules | `.gitignore` (secrets, `.sfdx/`, `.sf/`); `.forceignore` (metadata excluded from retrieve/deploy) |
| Metadata format | Source format (DX) vs metadata format (MDAPI) |
| Commit scope | Component-level, feature-level, full retrieve |
| Branching | GitHub Flow, GitFlow, trunk-based, release train |
| Tags | Release tags, deploy tags, hotfix tags |
| Destructive deletes | Pre/post `destructiveChanges.xml` |
| API version | `sourceApiVersion` in `sfdx-project.json` |

**What to commit:** objects, fields, validation rules, flows, Apex, LWC, permission sets, custom metadata *definitions*, named credential *definitions* (not secrets), layouts, record types, apps/tabs.

**What not to commit:** `.sfdx/`, `.sf/`, auth files, private keys, consumer secrets, retrieved user lists, sandbox-only endpoints, certificate bodies.

**Variations in retrieve strategy**

- **Org → Git**: retrieve what changed and commit (source-driven with a review step).
- **Git → Org**: deploy from branch (source of truth).
- **Hybrid**: admins work in sandbox, retrieve, commit; developers work in VS Code, commit, deploy.
</details>

<details>
<summary><strong>What you do</strong></summary>

- Keep the repo clean and reviewable; no "retrieve everything" commits.
- Review diffs before commit; XML is code.
- Use `.forceignore` to exclude noise.
- Handle deletes explicitly.
- Tag releases; never rely on the org as history.
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"Production is not the source of truth. I retrieve, review the XML diff, commit with the ticket ID, and deploy from Git. If Setup and Git disagree, that's drift — an incident, not a workflow. Deletes are explicit destructive manifests, and secrets never enter the repo."*
</details>

---

## A6. "Handle sandbox strategy (creation, refresh, data masking)"

<details>
<summary><strong>What it means</strong></summary>

You own the non-production estate: which sandbox type, when it refreshes, what data it gets, and how sensitive data is masked before people log in.
</details>

<details>
<summary><strong>Configuration / settings / variations</strong></summary>

| Task | Where | Notes |
|---|---|---|
| List/create sandboxes | Setup > Sandboxes → New Sandbox | Type + template + name |
| Partial Copy template | Setup > Sandboxes > Sandbox Templates | Choose objects + record limits |
| Refresh | Setup > Sandboxes → Refresh | Check next eligible date first |
| Deployment settings | Setup > Deploy > Deployment Settings | Allow inbound/outbound |
| Data Mask | App Launcher > Data Mask (managed package) | Or vendor/scripted masking |
| Seeding | Gearset / AutoRABIT | Deterministic subset |
| Storage/licences | Company Information | Full copy needs capacity |

**Variations**

- **Full** for Pre-Prod/performance; **Partial** for UAT; **Developer/Pro** for build/QA; **scratch orgs** only for package work.
- **Masking approaches:** Salesforce Data Mask, vendor masking, reviewed scripts. Must cover email, phone, government IDs, account numbers, birth dates, addresses — per the bank's data classification.
- **Refresh cadence:** licence-limited; Full is slowest. Never promise same-day.
- **Post-refresh:** re-point integrations to non-prod; disable outbound email; verify SSO/connected apps/certs.
</details>

<details>
<summary><strong>What you do</strong></summary>

- Check the next eligible refresh before committing a date.
- Attach a mask-complete confirmation to the refresh ticket.
- Restrict logins until masking is confirmed.
- Re-point endpoints and email before users log in.
- Keep a post-refresh checklist (see `01` §8.2).
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"A refresh isn't done when the copy finishes; it's done when masking has run, integrations point at non-prod, and access is limited to the ticket. A Full copy contains customer data — in a bank that's SIN-adjacent identifiers and account numbers — so no broad logins before mask confirmation."*
</details>

---

## A7. "Resolve deployment conflicts related to Profiles/Permission Sets, Record Types & Page Layouts, Flows/Apex/dependencies"

<details>
<summary><strong>What it means</strong></summary>

You are the person who unblocks a failed or dangerous deploy. See `02` for the full catalogue.

**Conflict matrix**

| Area | Root cause | Resolution |
|---|---|---|
| Profiles | Huge, noisy, access-bearing | Permission sets per feature; thin profile delta; second reviewer |
| Permission sets | One monolith everyone edits | Split by feature/persona; permission set groups |
| Record types | Missing business process/picklist/layout/visibility | Deploy full dependency set together |
| Page layouts | Assignment lives elsewhere | Deploy layout + assignment + record type + perms |
| Lightning pages | Not activated | Activate for app/record type |
| Flows | XML doesn't merge; version/active | One owner; subflows; verify active version |
| Apex | Missing class/dependency/test | Deploy dependency + test together; read compile error |
</details>

<details>
<summary><strong>Strong answer</strong></summary>

*"I don't hand-merge a 10,000-line profile. I move the access into a permission set, deploy a thin profile delta only for profile-only settings, and have a second person read the permission diff. For record types I deploy the object, fields, business process, layout, assignment, and visibility together. For flows I keep one owner per release and verify the active version."*
</details>

---

## A8. "Recommend best practices to reduce deployment failures and rework"

<details>
<summary><strong>The checklist you actually give teams</strong></summary>

- Small, frequent commits with ticket IDs.
- One owner per Flow per release; subflows for parallel work.
- Permission sets over profile edits; one per feature.
- Tests create their own data; no `LIMIT 1` assumptions; mock callouts.
- No hardcoded IDs; use custom metadata/query.
- Named Credentials for callouts; no secrets in Git.
- Custom metadata/settings for toggles; ship dark, enable after deploy.
- Bulkify Apex; ask "what happens at 200 records?"
- Deploy assignments/activation with the component.
- Validate against a prod-like org.
- Explicit destructive changes with data backup.
- Tag every deploy; rehearse rollback.
- No environment-specific branches.
</details>

---

## A9. "Partner with Salesforce Developers, Admins, QA, and Platform teams"

<details>
<summary><strong>RACI you can describe</strong></summary>

| Activity | Dev | Admin | QA | Platform/DevOps | Release Eng |
|---|---|---|---|---|---|
| Feature code/Flow | R | R | C | I | I |
| Metadata commit | R | R | I | C | A |
| Pipeline changes | C | I | I | R | A |
| Sandbox refresh/mask | I | C | C | R | A |
| UAT sign-off | I | C | R | I | A |
| Prod deploy | I | I | C | C | R/A |
| Rollback decision | C | C | I | C | R/A |

**What good looks like:** a written definition of "ready for release," a review SLA, and a single place (ticket) where evidence lives.
</details>

---

## A10. "Provide guidance on DevOps friendly Salesforce design patterns"

<details>
<summary><strong>Patterns worth being stubborn about</strong></summary>

| Pattern | Why release engineering cares |
|---|---|
| Permission sets over profile edits | Profiles don't merge; small sets do |
| One flow owner per release; subflows | Flow XML doesn't merge |
| Tests create their own data | Empty sandboxes behave like prod-like ones |
| No hardcoded IDs | IDs differ per org |
| Named Credentials | Endpoints differ per sandbox; secrets stay out of Git |
| Custom metadata/settings for config | Ship dark, toggle after deploy |
| Bulkified Apex | Green deploy can still fail at first real batch |
| No environment-specific branches | `if (org.IsSandbox)` is a last resort; config belongs in the target |
| Unlocked packages at real boundaries | Stops the repo becoming one unreviewable tree |
| Destructive changes explicit | A Git revert doesn't undelete |
</details>

---

## A11. "Document release processes, runbooks, and rollback procedures"

<details>
<summary><strong>The three documents</strong></summary>

1. **Release process** — stages, gates, roles, calendar, entry/exit criteria.
2. **Runbook** — per-release checklist (ticket, tag, payload, validation ID, tests, deploy ID, approver, post-deploy steps, rollback tag, verification).
3. **Rollback procedure** — forward-deploy last good tag; data restore path; who decides; communication.

Use the runbook template in `04` §12.
</details>

---

## A12. "Support audit and change management requirements"

<details>
<summary><strong>The evidence pack</strong></summary>

- Change ticket ID in commit + PR.
- Diff read by a second person (not the author).
- Validation deploy ID + prod deploy ID.
- Test run ID + coverage.
- Named approver ≠ author.
- Release tag.
- Post-deploy verification result.
- For Full sandbox: refresh time, mask-complete confirmation, access list.
- For destructive changes: data impact + backup reference.

**Regulated-environment framing:** this is the same discipline as a ServiceNow change: ticket, window, backout, evidence. The metadata tool changes; the control does not.
</details>

---

# Part B — Skills

## B1. "Strong experience with Salesforce metadata deployments"

<details>
<summary><strong>Variations of the deployment mechanism</strong></summary>

| Mechanism | When | Trade-off |
|---|---|---|
| Change sets | Two related orgs, admin-only shop | No diff/branch/tag/rollback; manual deps |
| `sf` CLI (Metadata API) | Standard for source-driven | You own ordering/deps |
| Gearset/Copado/AutoRABIT | Teams wanting UI + governance | Cost; still Metadata API underneath |
| DevOps Center | Native, GitHub-first | Lighter governance; GitHub-centric |
| Unlocked packages | Module boundaries | Dev Hub required; versioning overhead |
| Managed packages | ISV/IP boundary | Upgrade-only; cannot edit |

**Deployment settings that matter:** rollback-on-error, test level, quick deploy, destructive pre/post, API version, ignore warnings, allow missing files.
</details>

---

## B2. "Experience with Git based source control"

<details>
<summary><strong>What "good" looks like</strong></summary>

- Protected `main`; PR required; review required.
- Short-lived feature branches.
- Tags for every production deploy.
- Commit messages with ticket IDs.
- `.gitignore` for `.sfdx/`, `.sf/`, keys; `.forceignore` for metadata noise.
- No secrets; no generated junk; no full-org dumps.
- Destructive changes explicit.
</details>

---

## B3. "Understanding of Salesforce limits, metadata dependencies, and deployment constraints"

→ See `01` (limits/system properties) and `02` (dependencies/constraints). This is the most technically testable line in the JD.

---

## B4. "Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab, etc.)"

→ See `04`. Be able to describe the same four stages in any of the three tools.

---

## B5. "Understanding of branching strategies (feature, release, hotfix)"

<details>
<summary><strong>Strategy variations</strong></summary>

| Strategy | Shape | Fit |
|---|---|---|
| GitHub Flow | `main` + short feature branches | Small teams, continuous delivery |
| GitFlow | `main`, `develop`, `release/*`, `hotfix/*`, `feature/*` | Scheduled releases, multiple versions |
| Trunk-based | Everyone commits to trunk; short-lived branches; feature flags | Mature CI/CD, high discipline |
| Release train | Fixed `release/<date>` branches | Banks with calendar releases |

**Salesforce-specific rule:** long-lived branches are dangerous because XML (Flows, profiles, layouts) does not merge well. Prefer short branches + small PRs + feature flags.
</details>

---

## B6. "Familiar with automated testing and validation concepts"

<details>
<summary><strong>The vocabulary</strong></summary>

| Concept | Meaning |
|---|---|
| Validation / dry run | Compile + tests against target without changing it |
| Quick deploy | Apply a prior successful validation (10-day window) |
| Test levels | NoTestRun / RunSpecifiedTests / RunLocalTests / RunAllTestsInOrg |
| Coverage | 75% org-wide gate for production Apex |
| Test data factory | Code that creates its own records |
| Mocking | `HttpCalloutMock`, `Test.setMock` for callouts |
| Static analysis | PMD/CodeScan for anti-patterns |
| Regression | Re-run critical tests after change |
| Smoke test | Post-deploy check that the feature works |
</details>

---

## B7. "Hands on experience with Gearset, Copado, AutoRABIT, or equivalent"

→ See `03` for UI walkthroughs and the action map.

---

## B8. "Good understanding of Apex & Triggers"

<details>
<summary><strong>What a DevOps engineer must know</strong></summary>

- One trigger per object; logic in a handler class.
- Bulkification (collections, no SOQL/DML in loops).
- Recursion guard.
- Order of execution.
- `with sharing` / `without sharing` / `inherited sharing`.
- Test class with `@isTest`, `Test.startTest/stopTest`, data factory.
- Async: future/queueable/batch/scheduled.
- Governor limits (see `01`).
- Compile-time dependencies for deploys.
</details>

---

## B9. "Flows (Before/After Save)"

<details>
<summary><strong>Definitions and when to use each</strong></summary>

| Aspect | Before-save | After-save |
|---|---|---|
| Runs | Before the record is committed | After the record is committed |
| Can update triggering record without extra DML | **Yes** (fast field updates) | No (causes another save) |
| Can create/update/delete other records | **No** | **Yes** |
| Can callout / submit approval / post | No | Yes |
| Performance | Faster | Slower, recursion risk |
| Use for | Field derivation, defaults, simple validation-ish updates | Related records, notifications, callouts, approvals |

**Configuration variations**

- Start element: object, trigger (create/update/delete), entry conditions, "Optimize for: Fast Field Updates" vs "Actions and Related Records."
- Run order relative to triggers; before-save flows run with before triggers.
- Fault paths and custom error elements.
- Versioning and activation.
- Limits: flow interviews, element counts, per-transaction limits.

**DevOps angle:** flow XML does not merge; deploy as active; verify the active version; one owner per release.
</details>

---

## B10. "Permission Sets vs Profiles"

<details>
<summary><strong>Full comparison</strong></summary>

| Capability | Profile | Permission Set |
|---|---|---|
| One per user | Yes | No (many) |
| Additive permissions | Yes | Yes |
| Remove permissions | Yes (sets baseline) | No (muting set in a group can) |
| Object/field permissions | Yes | Yes |
| System permissions | Yes | Yes |
| Apex class access | Yes | Yes |
| Flow access | Yes | Yes |
| Tab/app visibility | Yes | Yes |
| Layout assignment | Yes (classic) | Some settings |
| Login hours / IP ranges | Yes | No |
| Default app / locale | Yes | No |
| Merge-friendliness | Poor | Good if small |
| Deploy size | Large | Small |
| Recommended role | Baseline only | Feature/persona access |

**Permission set group:** bundles permission sets for a job function; supports **muting** sets.
</details>

---

## B11. "Record Types, Page Layouts, and Security Model"

<details>
<summary><strong>Record types — configuration</strong></summary>

- Name, developer name, active.
- **Business process** (Sales/Support/Lead/...).
- **Picklist values** available to the type.
- **Page layout assignment** per profile.
- **Visibility** per profile/permission set.
- **Compact layout** assignment.
- **Lightning record page** activation per app/type.

**Variation:** "record type per region/product" explodes the matrix; prefer a picklist + dynamic forms or a single type with conditional visibility where possible.
</details>

<details>
<summary><strong>Page layouts — configuration</strong></summary>

- Fields, related lists, buttons, actions.
- Required/read-only fields (at layout level).
- Compact layouts (for highlights/kanban).
- **Assignment** per profile + record type.
- **Dynamic Forms** (field sections on Lightning pages) reduce layout sprawl.

**Gotcha:** layout ≠ assignment; Lightning page ≠ layout.
</details>

<details>
<summary><strong>Security model — the layers</strong></summary>

| Layer | Controls |
|---|---|
| **Object permissions** (profile/permset) | CRUD |
| **Field-level security** (profile/permset) | Read/edit per field |
| **Org-wide defaults** | Baseline record access (Private / Public Read Only / Public Read/Write / Controlled by Parent) |
| **Role hierarchy** | Vertical record access |
| **Sharing rules** | Horizontal record access (owner-based / criteria-based) |
| **Manual sharing / teams** | Record-specific |
| **Territory management** | Territory-based (if enabled) |
| **Apex sharing** | Programmatic (`__Share` records) |
| **Guest/Experience Cloud** | External user access |
| **Session settings / login IP / MFA** | How users authenticate |

**Key sentence:** profiles and permission sets control **what you can do**; OWD, roles, and sharing control **which records you can see**. They are different graphs.
</details>

---

## B12. "Ability to troubleshoot deployment failures and dependency issues"

<details>
<summary><strong>The 60-second triage</strong></summary>

1. Read the **first** error, not the last. Deploys cascade.
2. Classify: compile/dependency, test failure, coverage, permission, managed package, destructive, timeout.
3. Check the missing component is **in the payload or in the target**.
4. Check the **API version**.
5. Check the **deploying user's permissions**.
6. Reproduce with a **validate** against a clean org.
7. Fix, re-validate, and add the case to the runbook.

See `02` §3 for the error → cause table.
</details>

---

## B13. "Salesforce Platform Developer experience"

<details>
<summary><strong>What the role expects</strong></summary>

You are not the primary Apex author, but you can read Apex, spot bulkification and dependency problems, write a test if needed, and deploy it safely. PD1-level fluency is the bar (see `06`).
</details>

---

## B14. "Experience with Unlocked Packages / Managed Packages"

<details>
<summary><strong>Comparison</strong></summary>

| Aspect | Unlocked package | Org-dependent unlocked | Managed package |
|---|---|---|---|
| Owner | Your team | Your team | ISV / vendor |
| Namespace | Optional | Optional | Required |
| Upgradeable | Yes (versioned) | Yes | Yes |
| Portable to other orgs | Yes | No (needs same unpackaged deps) | Yes |
| Editable metadata | Yes | Yes | No |
| Dev Hub required | Yes | Yes | No (to install) |
| Fit | Internal modules | Incremental adoption | AppExchange / IP boundary |

**Commands (verify flags):**

```bash
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

**Rule:** do not propose "package the entire existing bank org" as the first move. Package at real boundaries.
</details>

---

## B15. "Exposure to Salesforce DX"

<details>
<summary><strong>The DX toolkit</strong></summary>

- `sfdx-project.json` (package directories, `sourceApiVersion`).
- **Scratch orgs** + **Dev Hub** (for packages/scratch).
- **Source tracking** (source format, `sf project retrieve/deploy`).
- **Source format** (`force-app`) vs **metadata format** (`mdapi`).
- **Unlocked packages** (2GP).
- **CLI plugins** (`sfdx-git-delta`, scanners).
- **VS Code Salesforce Extensions**.
- **DevOps Center** as the native UI on top.

**Variation:** scratch orgs are not sandboxes — they lack managed packages, SSO, licenses, and data unless you script them. Use them for package builds, not UAT.
</details>

---

## B16. "Experience in regulated or enterprise environments (banking, insurance, healthcare)"

<details>
<summary><strong>What changes vs a startup</strong></summary>

- **Segregation of duties** is mandatory.
- **Change tickets** and CAB/approval records.
- **Evidence retention** (years, not days).
- **Data residency/classification**; masking; encryption.
- **Vendor risk** (tool security review, data processing agreements).
- **Audit** (internal/external) asks for deploy evidence months later.
- **Freeze windows** (quarter-end, regulatory).
- **Least privilege** and periodic access reviews.

**Interview sentence:** *"In a regulated environment the deploy is the easy part; the evidence and segregation of duties are the deliverable."*
</details>

---

## B17. "Salesforce certifications (PD1, Advanced Admin, DevOps related certs)"

→ See `06-certifications-and-curriculum.md`.

---

## Cross-reference: JD line → deep-dive file

| JD line | File |
|---|---|
| CI/CD pipelines, Git workflows | `04` |
| Multi-environment strategy | `05` A2, `01` |
| Releases/hotfixes/emergency | `04` §2/§9, `05` A3 |
| Audit/security/compliance | `05` A4/A12, `PLAN` |
| Metadata lifecycle/Git | `05` A5, `02` |
| Sandbox strategy | `05` A6, `01` §8 |
| Conflicts | `02`, `03` |
| Reduce failures | `02`, `04`, `05` A8 |
| Partnering | `05` A9 |
| Design patterns | `05` A10 |
| Runbooks/rollback | `04` §12/§9 |
| Limits/deps/constraints | `01`, `02` |
| Branching | `04` §2, `05` B5 |
| Testing/validation | `01` §6, `04` §8, `05` B6 |
| Gearset/Copado/AutoRABIT | `03` |
| Apex/Triggers | `05` B8 |
| Flows before/after | `05` B9 |
| Perm sets vs profiles | `05` B10 |
| Record types/layouts/security | `05` B11 |
| Troubleshooting | `02` §3, `05` B12 |
| Packages | `05` B14 |
| Salesforce DX | `05` B15 |
| Regulated | `05` B16 |
| Certifications | `06` |
