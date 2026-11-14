# PLAN — How This Research Is Structured

**Round:** 1 (research)
**Author:** `salesforceagain-v2`
**Date:** 2026-11-14
**Purpose:** Give the merge round a principled skeleton, not just a pile of notes.

---

## 1. Objective

Produce training material that makes a competent Salesforce practitioner able to **own release engineering** for a Commercial Banking Salesforce estate: Git as source of truth, multi-stage environment promotion, conflict resolution, auditable deploys, and rollback. The material is anchored to Scotiabank requisition 276046 and cross-referenced to the published `devops-engineer` track.

## 2. Framing: what kind of system Salesforce actually is

Every recommendation below follows from seven properties. If you remember nothing else, remember these — they explain *why* Salesforce release engineering looks different from normal software delivery.

<details>
<summary><strong>Principle 1 — Multi-tenant, shared-resource platform</strong></summary>

Thousands of orgs share application servers and database clusters. Salesforce enforces **governor limits** per transaction so one tenant's code cannot starve another. This is why "it worked in Dev" is not evidence: a different data volume or a different test level can push you over a limit that the platform enforces at runtime, not at deploy time.

**Release-engineering consequence:** A green deploy is necessary but not sufficient. You must also reason about runtime limits (SOQL, DML, CPU, heap, callouts) for the *production* data shape.
</details>

<details>
<summary><strong>Principle 2 — Metadata-driven, not file-deployed</strong></summary>

A Salesforce deploy is not "copy files onto a server." You send a **metadata payload** to the Metadata API, which **compiles and reconciles** it against the target org's existing schema. The target org already has state; the deploy is a set of instructions against that state.

**Consequence:** Dependencies matter. If a payload references a field, record type, layout, Apex class, or permission that is neither in the payload nor already present in the target, the deploy fails — or worse, succeeds while the feature is unusable.
</details>

<details>
<summary><strong>Principle 3 — Declarative and programmatic changes share one metadata surface</strong></summary>

Admins (Flow, layouts, permission sets) and developers (Apex, LWC) both produce metadata in the same repo and the same deploy. There is no separate "config pipeline" and "code pipeline."

**Consequence:** Your branching, review, and conflict strategy must work for **XML that does not merge well** (Flows, profiles, layouts) as well as for Apex that merges reasonably.
</details>

<details>
<summary><strong>Principle 4 — The org is mutable and tempting</strong></summary>

Anyone with Setup access can change production directly. That is the central governance risk of the platform.

**Consequence:** Git must be the source of truth; the org is a target. Drift between Git and the org is an **incident**, not a workflow. Your pipeline should make the correct path the easy path.
</details>

<details>
<summary><strong>Principle 5 — Security is a graph, not a checkbox</strong></summary>

Access is the intersection of profile, permission set, permission set group, role hierarchy, org-wide defaults, sharing rules, and record ownership. A deploy can grant or revoke access nobody reviewed.

**Consequence:** Treat permission changes as high-risk changes with a second reviewer. Prefer small permission sets over profile edits.
</details>

<details>
<summary><strong>Principle 6 — Tests are a production gate</strong></summary>

Production deploys containing Apex must run tests and meet **75% org-wide code coverage** (with no test failures). Tests must not depend on org data that exists only in Dev.

**Consequence:** Validation is not a formality; it is the gate. Design tests that create their own data.
</details>

<details>
<summary><strong>Principle 7 — Releases are governed events in a regulated environment</strong></summary>

In banking, the deploy is the easy part. The **evidence** is the deliverable: ticket, reviewer, validation ID, test evidence, deploy ID, approver, rollback tag, sandbox-mask confirmation.

**Consequence:** Build the audit pack into the pipeline, not into a spreadsheet someone fills in afterwards.
</details>

---

## 3. Research method

1. **Primary source first.** Read the requisition literally, line by line, and turn each line into a requirement.
2. **Platform truth over vendor marketing.** Where a vendor claims a capability, ask "which API does it call?" Every DevOps tool is a UI over the Metadata API / Tooling API / CLI.
3. **Failure-first.** For each concept, ask: *what does the failure look like, and what is the first thing I check?* That is what interviews and incidents test.
4. **Regulated lens.** Every pattern must survive an auditor's question: "show me who approved this and how you would undo it."
5. **Explicit provenance.** `sources.md` records every URL, what it supported, and whether it was blocked (some Salesforce docs return 403 to automated fetches).

## 4. Deliverable map (requisition line → file)

| Requisition line / skill | Covered in |
|---|---|
| Design/implement/maintain CI/CD pipelines, Git workflows | `04`, `05` |
| Multi-environment release strategies (Dev→QA→UAT→PreProd→Prod) | `05`, `03` |
| Scheduled releases, hotfixes, emergency deployments | `05`, `04` |
| Audit, security, compliance standards | `05`, `PLAN` §2 P7 |
| Metadata lifecycle via Git | `02`, `04` |
| Sandbox strategy (create/refresh/mask) | `05` |
| Conflicts: profiles/permission sets, record types/layouts, Flows/Apex/deps | `02`, `03` |
| Best practices to reduce failed deploys | `02`, `04`, `05` |
| Partner with devs/admins/QA/platform | `PLAN`, `05` |
| DevOps-friendly design patterns | `05` |
| Runbooks, rollback procedures | `04`, `05` |
| Source control experience | `04`, `05` |
| Salesforce limits, metadata dependencies, deployment constraints | `01`, `02` |
| CI/CD tools (GitHub Actions/Azure DevOps/GitLab) | `04` |
| Branching strategies (feature/release/hotfix) | `04`, `05` |
| Automated testing & validation | `01`, `04` |
| Gearset/Copado/AutoRABIT | `03` |
| Apex & Triggers | `05`, `02` |
| Flows (before/after save) | `05`, `02` |
| Permission sets vs profiles | `05`, `02` |
| Record types, page layouts, security model | `05`, `02` |
| Troubleshoot deployment failures/dependencies | `02` |
| Platform Developer experience | `06` |
| Unlocked/Managed packages | `05` |
| Salesforce DX | `04`, `05` |
| Regulated/enterprise environments | `PLAN`, `05` |
| Certifications (PD1, Advanced Admin, DevOps) | `06` |

## 5. Quality bar for the merge round

A section is publishable only if it satisfies all of:

- **Accurate:** numbers and limits match current Salesforce documentation; edition-dependent values are labelled.
- **Actionable:** every concept has a "where / what / why" — ideally a path (Setup > …), a command, or a tool location.
- **Failure-aware:** the common failure and the first diagnostic step are stated.
- **Audit-ready:** the control or evidence produced is named.
- **Non-duplicative:** links to the crash course/breadcrumbs instead of repeating them.

## 6. Merge plan (round 2)

1. **Preserve anchors.** The published page uses anchors like `#6-devops-tools`, `#2-metadata-that-breaks-releases`. Extend under those anchors; do not renumber existing ones.
2. **Split long sections into child pages** if the main page exceeds a reasonable scroll: propose `limits-and-system-properties.md`, `deployment-constraints.md`, `tools-ui.md`.
3. **Reconcile terminology.** The published track says "Pre-Prod"; the JD says "Pre Prod." Pick one and be consistent.
4. **Add diagrams** for the dependency graph (`02`) and the pipeline (`04`).
5. **Verify commands** against the installed CLI (`sf <cmd> --help`) before publishing; flags drift.
6. **Keep the banking lens.** Do not let the merged page drift into generic DevOps advice.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Limits change by release/edition | Cite canonical numbers, label edition variance, link to official docs; re-verify each Salesforce release |
| Vendor UI paths change | Describe intent + typical label; tell readers to verify; never claim a screenshot |
| CLI flags drift (`sfdx` → `sf`) | Prefer `sf`; run `--help`; show intent over exact flags |
| Over-generalising "banking" | Use concrete controls: SoD, change ticket, mask evidence, rollback tag |
| Duplicating the crash course | Cross-link; put only *new* depth here |
