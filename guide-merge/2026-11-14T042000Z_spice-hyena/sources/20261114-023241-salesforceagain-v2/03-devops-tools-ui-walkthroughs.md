# 03 — DevOps Tools: Practical UI Walkthroughs

> **Scope:** the JD's "Hands on experience with Salesforce DevOps tools such as Gearset, Copado, AutoRABIT, or equivalent."
> **What this file is:** a *where-do-I-click* map for the actions a release engineer performs weekly — compare, deploy, validate, back up, roll back, promote.
> **Honesty note:** vendor UIs change by release and edition. Labels below are the **typical** navigation, not a guarantee for your tenant. Where a feature is edition-gated it is flagged. Always confirm in a free trial or your org before training others.

---

## 0. The architecture that makes all four tools comparable

Every one of these tools is a **UI and governance layer over Salesforce's Metadata API, Tooling API, and/or the `sf` CLI**. They differ in:

- **Dependency resolution** (how well they find the component you forgot).
- **Diff quality** (line-level vs rendered, e.g., Flow Navigator).
- **Governance** (work items, approvals, audit packs).
- **Git model** (tool-managed vs bring-your-own).
- **Backup/rollback depth** (metadata vs data vs both).
- **Regulated-industry features** (compliance evidence, SoD).

**Interview framing:** *"I don't care which UI we use; I care that it produces a reviewable diff, resolves dependencies, gates on tests, and leaves an audit trail. Under the hood it is the Metadata API."*

---

## 1. Quick action map (bookmark this)

| Action | Gearset | Copado | AutoRABIT ARM | DevOps Center |
|---|---|---|---|---|
| Compare two orgs | **Compare and deploy** | **Deployments** → compare / user story diff | **Create Deployment** → compare | Work item diff / **Pipeline** |
| Commit to Git | **Version control** / commit from compare | **User Story** → Commit | **CI Job** / commit | **Commit Changes** |
| Validate (dry run) | **Validate deployment** before Deploy | **Validate** on deployment record | Validate option in deployment wizard | Validate-only in promotion |
| Deploy | **Deploy now** | **Deploy** / **Promote** | **Deploy** | **Promote Selected** |
| Promote through stages | **Pipelines** stages | **Promotion** / pipeline | **CI/CD** pipeline | **Pipeline** stages |
| Roll back | **Deployment rollback** (Teams+) / redeploy a previous tag | Revert / back-promote | **Deployment History → Rollback** | Redeploy previous commit/bundle |
| Metadata backup | **Backup & restore** | Copado backup / Git history | **Vault → Backup** | Git history (no native backup) |
| Data backup | **Backup & restore** (data) | Limited / partner | **Vault** (data + metadata) | No |
| Sandbox seeding | **Sandbox seeding** | Limited | **Vault / Seed** | No |
| Static code analysis | Built-in checks | CodeScan/partner | **CodeScan** | Code Analyzer |
| Drift detection | **Org intelligence / change monitoring** | Pipeline monitoring | Compare / Guard | Pipeline view |

---

## 2. Gearset — where to click

<details>
<summary><strong>2.1 First-time setup: connect your orgs and Git</strong></summary>

1. Log in to Gearset.
2. **Org connections / Manage orgs** — add each Salesforce org (production, sandboxes). Authenticate via OAuth as an admin/integration user.
3. **Version control** — connect GitHub/Bitbucket/Azure DevOps/GitLab, authorize, and select the repo + branch.
4. Set a **default comparison filter** so you don't compare every metadata type on every run.

**Tip:** connect a dedicated **CI integration user** per org, not a human admin. Gearset's connection is the identity that deploys; treat it as a service account.
</details>

<details>
<summary><strong>2.2 Compare and deploy — the core workflow</strong></summary>

**Where:** top navigation → **Compare and deploy**.

1. **Source** — choose a Salesforce org **or** a Git branch/commit.
2. **Target** — choose the destination org (or Git, for a commit).
3. Choose a **comparison filter** (e.g., "Default" or a custom filter limited to the metadata types you care about).
4. Click **Compare now**.
5. Review the diff:
   - Left panel = metadata types (ApexClass, CustomObject, Flow, PermissionSet, Profile, Layout, etc.).
   - Items are marked **new / changed / deleted**.
   - Click an item to see the **line-level diff** (and, for Flows, the rendered **Flow Navigator**).
6. **Select** the components to deploy.
7. Click **Next** → **Deployment package**:
   - Gearset flags **missing dependencies** and offers suggestions.
   - Accept dependencies it suggests (especially objects/fields/record types).
8. **Pre-deployment summary** — review what will happen.
9. **Validate deployment** (dry run; no changes) if you want a rehearsal.
10. **Deploy now**. Optionally run **Apex tests** and add **post-deployment steps**.
11. Read the **deployment report**; download it for the audit pack.

**Where the failures show:** the deployment result page lists per-component errors and the test failures; the report is your evidence.
</details>

<details>
<summary><strong>2.3 Profiles and permission sets in Gearset</strong></summary>

- Gearset can **decompose profiles** so you deploy only the changed permissions rather than the whole profile.
- Use the **profile/permission diff view** to see exactly which object/field/system permissions change.
- Best practice in the tool: deploy **permission sets** per feature; use profile deploys only for profile-only settings, with a second reviewer reading the diff.
</details>

<details>
<summary><strong>2.4 Flow deployments (Flow Navigator)</strong></summary>

1. Compare source/target with a filter that includes **Flow** and **FlowDefinition** (and **CustomObject** for dependencies).
2. Open the Flow item → **Flow Navigator** renders the flow as in Flow Builder and highlights what changed.
3. Confirm the **version** and whether it will be **Active** in the target.
4. Deploy; then **verify activation** in the target org (Setup > Flows).

**Known gotcha:** a flow can deploy as a new **Draft** version. Gearset shows version/active state; still verify after deploy.
</details>

<details>
<summary><strong>2.5 Pipelines / CI jobs (Gearset's CI/CD)</strong></summary>

**Where:** **Pipelines** (automation area).

1. **Create pipeline** → name it and choose the source/target orgs and Git provider.
2. Add **stages** (e.g., Dev → QA → UAT → Prod) and map each to an org + branch.
3. Add a **CI job** to a stage:
   - **Trigger**: on commit / on PR / scheduled / manual.
   - **Source**: Git branch or org.
   - **Target**: the stage org.
   - **Validation**: validate-only or deploy.
   - **Tests**: specify Apex tests / run local tests.
   - **Approvals**: require a reviewer before promotion (Teams+).
   - **Post-deploy**: steps or notifications.
4. Run the job; read the run log; download the report.

**What to say in an interview:** *"Gearset Pipelines give me the same four stages as a GitHub Actions pipeline, with the dependency resolution and diff UI on top. The CLI is still underneath."*
</details>

<details>
<summary><strong>2.6 Backup and restore</strong></summary>

**Where:** **Manage data → Backup & restore** (edition-gated; typically Teams/Enterprise).

1. Connect the org (already done in org connections).
2. **Configure backup**: choose metadata and/or data, objects, and **schedule** (daily/weekly).
3. Run a **backup now** for an ad-hoc snapshot before a risky release.
4. **Restore**: pick a snapshot → choose components/records → restore to the org (or compare first).
5. For **metadata**, you can compare a backup snapshot to the live org to see drift.

**Release-engineering use:** take a metadata backup **before** a destructive change, and attach the snapshot ID/time to the change ticket.
</details>

<details>
<summary><strong>2.7 Deployment rollback</strong></summary>

**Where:** **Deployment history** → open a deployment → **Roll back** (edition-gated; often Teams+).

- Gearset can roll back a deployment by comparing the pre-deploy state to the current org and deploying the difference.
- It is a **forward deploy of the previous state**, not a time machine. Data changes are not undone.
- If your edition lacks rollback, the fallback is: redeploy the **previous release tag** from Git and restore data separately.

**Audit note:** record the rollback deployment ID and the reason in the ticket.
</details>

<details>
<summary><strong>2.8 Other Gearset features worth naming</strong></summary>

- **Change monitoring / Org intelligence** — detect drift and risky changes in an org.
- **Sandbox seeding** — populate a sandbox with a curated data subset.
- **Data deployment** — move records between orgs with external-ID matching (useful for custom metadata/settings and config data).
- **Code reviews** — PR-style review inside the tool.
- **Automated testing** — run test suites as part of a pipeline.
</details>

---

## 3. Copado — where to click

<details>
<summary><strong>3.1 Setup and environments</strong></summary>

1. Install Copado in your org (managed package) and assign the Copado permission sets.
2. **App Launcher → Copado**.
3. **Copado Setup / Environments** — register each org (Dev, QA, UAT, Pre-Prod, Prod) with credentials.
4. Connect your **Git repository** (Copado manages branches per environment/story).
5. Configure **Deployment Steps** and **Quality Gates** (what runs before a promotion is allowed).

**Mental model:** Copado is **work-item-centric**. You do not deploy a loose set of components; you commit components to a **User Story**, then promote the story through a pipeline.
</details>

<details>
<summary><strong>3.2 User Stories — the unit of change</strong></summary>

1. **Copado → User Stories → New**.
2. Fill title, project, sprint, assignee, and the source/target environments.
3. Work in your sandbox; **commit** the changed metadata to the story's branch:
   - **Commit** button on the user story → select components → commit.
4. The story now has a diff you can review and promote.
5. Move status: In Progress → Ready for Review → Ready to Promote.

**Why it matters for the JD:** the user story is the **audit trail** — ticket ↔ commit ↔ deployment ↔ approval.
</details>

<details>
<summary><strong>3.3 Deployments and validation</strong></summary>

1. Open the user story → **Deploy** (or create a **Deployment** record).
2. Choose the **destination environment**.
3. Select **Validate** (dry run) or **Deploy**.
4. Add **Apex tests** (specified tests / local tests).
5. Read the deployment log; per-component errors are listed.
6. After a successful validation, **Quick Deploy** can promote the validated deployment without re-running tests.

**Copado-specific:** deployments are records with status, logs, and links — good for audit packs.
</details>

<details>
<summary><strong>3.4 Pipelines / promotion path</strong></summary>

**Where:** **Copado → Pipelines** (or the Pipeline tab).

1. **Create pipeline** → define stages (Dev → QA → UAT → Pre-Prod → Prod).
2. Map each stage to an **environment** and a **Git branch**.
3. Add **Quality Gates** to a stage (e.g., required tests, code scan, approvals, coverage threshold).
4. Add **promotion** rules: who can promote, whether a validation is required, whether a bundle is required.
5. **Promote** a user story/bundle from one stage to the next.

**Bundling:** at the bundling stage, multiple stories are combined into a versioned bundle promoted as one unit — the equivalent of a release candidate.
</details>

<details>
<summary><strong>3.5 Back-promotion (the hotfix discipline)</strong></summary>

- A hotfix goes to production, then must be **back-promoted** to lower environments so the next release doesn't resurrect the bug.
- Copado models this as a pipeline running **from production back to downstream environments** (or a dedicated back-promote pipeline).
- **Do the back-promotion immediately after the hotfix deploys**; do not leave it as a manual TODO.

**Interview sentence:** *"A hotfix isn't done when prod is patched; it's done when it's back-promoted and the release branch is reconciled."*
</details>

<details>
<summary><strong>3.6 Rollback and revert</strong></summary>

Copado's rollback is typically:

- **Revert** the commit / redeploy the previous good state via a deployment.
- **Back-promote** a known-good version.
- Restore data separately (Copado is not primarily a data-backup tool; pair with a backup product).

Record the revert deployment ID and the ticket reference.
</details>

<details>
<summary><strong>3.7 Compliance / testing features</strong></summary>

- **Quality Gates** — mandatory checks before promotion.
- **Copado Robotic Testing** — functional/regression automation.
- **Compliance Hub / evidence** — audit-oriented records of who promoted what.
- **CodeScan integration** — static analysis (also sold standalone by AutoRABIT).
- **CI/CD YAML** — Copado supports pipeline-as-code style steps for advanced teams.
</details>

---

## 4. AutoRABIT (ARM) — where to click

<details>
<summary><strong>4.1 The deployment wizard (compare → validate → deploy)</strong></summary>

1. **ARM → Create Deployment**.
2. **Source** and **Destination** orgs.
3. **Deployment Settings** — this is the important screen:
   - **Take Backup** (enables rollback later — see 4.3).
   - **Pre-destructive changes** (delete before deploy).
   - **Post-destructive changes** (delete after deploy).
   - **Deploy purge on delete** (permanently delete rather than recycle bin — dangerous).
   - **Rollback on error** (abort the whole deploy on a component failure).
   - **Apex test level**.
4. **Select metadata** — choose components; ARM resolves and warns about dependencies.
5. **Validate** (dry run) or **Deploy**.
6. Read the deployment log and summary.

**Critical:** if **Take Backup** is unchecked, **Rollback will not be available** for that deployment. Make it a standard setting for production deploys.
</details>

<details>
<summary><strong>4.2 Compare</strong></summary>

- **Compare** screen: pick two orgs (or org vs snapshot) and see new/changed/deleted metadata.
- Use it for drift detection and for building a deployment package.
- ARM's compare can also compare **data** in Vault (snapshot vs org).
</details>

<details>
<summary><strong>4.3 Rollback</strong></summary>

**Where:** **Deployment History** → select the deployment → **Rollback**.

1. Confirm the deployment had **Take Backup** enabled.
2. Choose **Rollback**.
3. Select **which components** to revert (you can revert a subset, not always the whole deployment).
4. Run the rollback; read the log.

**Limits:** metadata rollback only; data changes need Vault restore or a reverse script. Purging (permanent delete) is not reversible.
</details>

<details>
<summary><strong>4.4 CI/CD jobs</strong></summary>

- **CI/CD / CI Jobs** — configure jobs that run on a schedule or trigger, with steps: fetch, validate, deploy, test, notify.
- Jobs can be tied to a **pipeline** across environments.
- Integrate with Jira/Azure DevOps/Slack for ticket + notification.

**Interview framing:** ARM is the most "compliance/regulated-industry" leaning of the three; it bundles **CodeScan** (static analysis) and **Vault** (backup) and **Guard** (security posture).
</details>

<details>
<summary><strong>4.5 Vault — backup, restore, seed</strong></summary>

**Where:** **AutoRABIT Vault**.

1. **Register the org** (Setup > Register New Org).
2. **Backup → configure**:
   - Select org, environment (Salesforce/nCino), and **backup configuration**.
   - Choose **Full** or **Incremental** backup.
   - **Incremental** can run as often as every ~5 minutes and backs up only changes since the last run.
   - Optionally **exclude deleted records**.
3. **Run backup** and view the **Backup Summary**.
4. **Restore**: pick a snapshot → choose records/metadata → restore; verify automation is re-enabled after the job.
5. **Compare** snapshots to the live org to find drift.
6. **Sandbox seeding** — populate a sandbox with a masked/curated subset.

**Regulated-industry note:** Vault's selling point is off-platform, scheduled, verifiable backup with restore — the evidence an auditor asks for after a data incident.
</details>

<details>
<summary><strong>4.6 CodeScan and Guard</strong></summary>

- **CodeScan** — static code analysis for Apex/LWC (security, quality, policy). Runs in CI or on demand; produces a report you can attach to a release.
- **Guard** — continuous security/compliance posture: permission risk, misconfigurations, exposure across orgs.
</details>

---

## 5. Salesforce DevOps Center — where to click

<details>
<summary><strong>5.1 Enable and configure</strong></summary>

1. **Setup → DevOps Center** → enable the slider → **Install Package** (Admins only).
2. Assign the DevOps Center **permission sets** and **permission set licence** to developers and release managers.
3. Create a **Connected App** if prompted.
4. **Connect GitHub** as the source control (DevOps Center is GitHub-first; Bitbucket support has been added over time — verify your org).
5. **Create a Project** and a **Pipeline**:
   - Add environments (Dev, QA, UAT, Prod).
   - Map each stage to an environment + branch.
   - Choose a **bundling stage** if you want versioned promotion.
6. **Activate** the pipeline.
</details>

<details>
<summary><strong>5.2 Work items and commits</strong></summary>

1. **App Launcher → DevOps Center → your project**.
2. **New Work Item** — title, description, assignee, source environment.
3. Work in the connected sandbox.
4. **Pull Changes** (source tracking shows what changed).
5. Select components → **Commit Changes** (creates/updates the feature branch).
6. **Create Review** (opens a PR in GitHub).
7. Reviewer approves → **Ready to Promote**.
</details>

<details>
<summary><strong>5.3 Promotion</strong></summary>

1. **Pipeline** tab → select approved work items → **Promote Selected**.
2. Choose **promotion options**:
   - **Changes not in stage** (promote only what the target lacks).
   - **Test level** (default/specified/local).
3. For production/bundling stages, **Promote as Work Item Bundle** and give it a **version**.
4. Monitor the promotion; resolve conflicts if surfaced.
5. Verify in the target org.

**Conflict handling:** DevOps Center surfaces merge conflicts; you resolve them **in Git**, then refresh the pipeline. It also lets you **combine work items** that share components to avoid downstream conflicts.
</details>

<details>
<summary><strong>5.4 What DevOps Center does not do</strong></summary>

- No native **data backup/restore** (use a backup product).
- Not a full replacement for a governed pipeline (approvals/quality gates are lighter than Copado/Gearset).
- GitHub-first; other VCS support varies.
- Unsupported metadata types exist (some Industries/managed-package metadata).

Use it when the bank wants a native, no-extra-vendor option and the team is willing to keep Git discipline.
</details>

---

## 6. Change Sets — the thing you explain and retire

<details>
<summary><strong>6.1 Where they live and why they fail at this scale</strong></summary>

**Where:** source org **Setup → Outbound Change Sets** → New → add components → Upload. Target org **Setup → Inbound Change Sets** → Validate → Deploy.

**Why they fail the JD:**

- No **reviewable diff** (you see a component list, not changes).
- No **branch**, no **tag**, no **rollback**.
- Manual dependency selection; easy to miss parents.
- Profile XML you cannot merge.
- Only between **related** orgs.
- No CI integration; no audit pack beyond the change set record.

**Interview answer:** *"Change sets are fine for a two-org admin shop. For a five-stage bank pipeline with hotfixes and audit, they cannot provide the diff, branch, tag, or rollback evidence. We use CLI/tooling with Git in front."*
</details>

---

## 7. Choosing a tool (for a bank interview)

<details>
<summary><strong>7.1 Decision factors</strong></summary>

| Factor | Why it matters |
|---|---|
| **Git model** | Bring-your-own (Gearset/Copado/AutoRABIT) vs tool-managed (DevOps Center) |
| **Governance depth** | Work items, approvals, quality gates, SoD, evidence (Copado strongest) |
| **Diff quality** | Rendered Flow diff, profile decomposition (Gearset strong) |
| **Backup/restore** | Metadata + data (AutoRABIT Vault / Gearset backup) |
| **Static analysis** | CodeScan (AutoRABIT) vs partner integrations |
| **Regulated features** | Compliance evidence, security posture, audit exports |
| **Cost/edition** | Per-user pricing; enterprise tiers gate rollback/approvals |
| **Team skills** | Admins need UI; developers may prefer CLI-first |

**Neutral answer that scores well:** *"The tool is a wrapper over the Metadata API. I'd pick based on governance depth, diff quality, and backup needs — and keep the pipeline portable by ensuring every deploy is also reproducible from Git + `sf` CLI. That way the tool is replaceable and the audit trail survives a vendor change."*
</details>

---

## 8. Interview drills

1. **Walk me through a Gearset deploy.** Compare and deploy → source/target → filter → compare → select → package → dependency warnings → validate → deploy → report.
2. **Where do you roll back in Gearset?** Deployment history → rollback (edition-gated); otherwise redeploy the previous tag.
3. **Where is backup in AutoRABIT?** Vault → Backup module; rollback needs "Take Backup" enabled on the deployment.
4. **What is a Copado user story?** The unit of change linking ticket → commit → deployment → approval.
5. **What does DevOps Center require?** GitHub, a project, a pipeline, work items; it surfaces but does not auto-resolve conflicts.
6. **What do all four tools sit on?** Metadata API / Tooling API / CLI — they differ in UX and governance, not in the fundamental deploy mechanism.
7. **What do none of them fix?** Assignments/activation (layout, record type visibility, FlexiPage activation, permission set assignment) and data rollback.
8. **How do you keep the pipeline portable?** Ensure every tool action is reproducible from Git + `sf` CLI; the vendor is a layer, not the source of truth.

---

**Next:** `04-cicd-github-salesforce.md` — the full GitHub Actions pipeline these tools are competing with (or wrapping).
