# 03 — DevOps tools in practice: Gearset, Copado, AutoRABIT

> JD line covered: **"Hands on experience with Salesforce DevOps tools such as: Gearset, Copado,
> AutoRABIT, or equivalent"** (Q7).
>
> All navigation paths below were read from each vendor's current official documentation on
> **2026-11-14**. Where a label people commonly quote could **not** be found in current
> documentation, that is stated explicitly. Vendor UIs change; every path here is written so it can
> be re-verified from the linked article.

---

## 0. Premise corrections (read before quoting any of this)

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

## 1. Gearset

### 1.1 Navigation map (left sidebar)

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

### 1.2 Connecting an org

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

### 1.3 Compare — the screen that replaces "diff two orgs by hand"

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

### 1.4 Deploy — the exact flow

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

### 1.5 Deployment history, reports, rollback

`Metadata deployments` → `Deployment history`:

- filter by date / source / target; search
- `View details`, `View errors`, PDF report, package download, CSV deployment details
- **`Roll back`** — choose metadata to reverse. Gearset creates a **new rollback deployment**; it
  does not erase history. Metadata rollback needs Teams or Enterprise.
- `Clone package` — re-deploy the same package to another target.
- `Deploy to target` — promote a validated/successful package onward.

### 1.6 CI jobs

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

### 1.7 Pipelines

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

### 1.8 Backups and restore (the "where do I click for backup" answer)

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

### 1.9 Data masking and sandbox seeding

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

### 1.10 GitHub integration

- GitHub / GitHub Enterprise: OAuth connection; repository integration via a **GitHub App**.
- GitHub App repository permissions: `Administration` (read), `Commit statuses` (read/write),
  `Contents` (read/write), `Deployments` (read/write), `Metadata` (read), `Pull requests`
  (read/write), plus Webhooks/Workflows access.
- **Required status check:** repository `Settings` → `Branches` → `Branch protection rules` →
  enable `Require status checks to pass before merging` → select the Gearset validation check.
- **Webhooks:** CI-job webhook (pooled URL, can trigger multiple CI jobs) and Pipeline webhook
  (pull-request events and propagation). Manual setup: CI-job page → job menu → `Webhook setup`.

### 1.11 Other Gearset features worth naming

| Feature | Where | Note |
|---|---|---|
| `Change monitoring` | `Continuous delivery` → `Change monitoring` | Scheduled org scans detect metadata changes; can trigger alerts/webhooks |
| `Express Deploy` | Deployment mode | Open pilot — deploy without a separate pre-validation. Availability varies |
| Code-review enforcement | Pipeline settings | Require reviews, approvals and validation before promotion |
| Problem Analyzer | Deployment flow + CI job | Runs before deployment; may correct the package |

---

## 2. Copado

### 2.1 Product lines and licences

| Product | Contents |
|---|---|
| **Copado Essentials** — Free | Up to 15 deployments/month, Knowledgebase support |
| **Copado Essentials** — Basic | Unlimited deployments; org comparison and change detection; fast deployments; full metadata support; team roles and collaboration |
| **Copado Essentials** — Essentials Plus | Adds **Release Pipelines & Work Items**, **Version Control & Backup**, **Automation & Continuous Integration** (custom CI jobs to back up, schedule, automate and validate deployments) |
| Enterprise | **Agentia Pipeline Pro** (SFDX CI/CD), **Agentia Pipeline** / Agentia Testing / Agentia AI Context Hub. Legacy docs: *Copado Deployer*, *Salesforce Metadata Pipelines (MFP)*, *Salesforce Source Format Pipelines (SFP)* |

**Licence types (Glossary of Terms):** *Copado User*, *Copado Plan* (planning records — user
stories, sprints, epics; Kanban, Sprint Wall, Work Manager), *Copado Branch Management*,
*Copado Compliance Hub*, *Copado Data Deploy*.

### 2.2 Pipeline Manager

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

### 2.3 Core objects (Glossary, verbatim in intent)

`Pipeline` (unidirectional flow of environments) · `User Story` (container for develop, commit,
promote, deploy) · `Environment` (an org or another cloud instance) · `Promotion` (container that
deploys one or more user stories between environments) · `Release` (groups user stories and tracks
the version after each deployment) · `Feature Branch` (created on user-story commit) ·
`Promotion Branch` (destination + promoted content) · `Credential` (connection between user and
environment) · `Git Snapshot` (org ↔ Git branch) · `Deployment Step` · `Job Template` / `Job Step` /
`Job Execution` · `Connection Behavior` (promotion/back-promotion behaviour, automation and quality
gates).

### 2.4 Promotion flow

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

### 2.5 Deployment steps and quality gates

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

### 2.6 Essentials Plus: Work Items and CI Jobs

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

### 2.7 Compliance Hub

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

### 2.8 Credentials and security

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

### 2.9 Validation and test levels

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

## 3. AutoRABIT

### 3.1 Product suite

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

### 3.2 CI Job (classic ARM)

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

### 3.3 Deployment

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

### 3.4 Release labels, scheduled deployments, approvals

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

### 3.5 Data masking (AutoRABIT Vault)

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

### 3.6 Credentials and audit

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

## 4. The comparison that matters in an interview

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

## 5. Unverified / uncertain

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
