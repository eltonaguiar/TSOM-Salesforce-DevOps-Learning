# Salesforce Key Principles Deep Dive

**Worktree/session:** salesforcemore  
**Date-time stamp:** 20261114-020852  
**Purpose:** Planning frame — the core Salesforce principles that govern all research, labs, and certification study for the DevOps Engineer role.  
**Sources:** crash-course.md, navigation-breadcrumbs.md, labs-design.md, user-management-data.md, SALESFORCE_LIMITS_DEEP_DIVE.md, SALESFORCE_DEVOPS_DEEP_DIVE.md

---

## Principle 1: Metadata-Driven Platform

**Core idea:** Everything configurable in Salesforce is metadata. Objects, fields, record types, page layouts, validation rules, Flows, profiles, permission sets, Apex classes, triggers, LWC components, Visualforce pages, Named Credentials, Connected Apps — all of it is metadata that can be extracted, versioned, and deployed between orgs.

**Implications for DevOps / release engineering:**
- Metadata is extracted from a source org (retrieve), reviewed in Git, then deployed to a target org.
- Deployments move metadata via the Metadata API / Salesforce CLI (`sf project deploy start` / `sf project retrieve start`) or vendor tools (Gearset, Copado, AutoRABIT) which sit on the same API.
- The org is a *target*, not the source of truth. Git is the source of truth. If Setup and Git disagree, that is an incident, not a workflow.

**Where documented:**
- crash-course.md — “The Big Picture: Objects, Records, Fields”; “Code: Apex, Visualforce, LWC”
- navigation-breadcrumbs.md — Object & Field Configuration, Development (Code), Deployment & DevOps paths
- labs-design.md — Lab 1 (custom object & Flow), Lab 2 (Apex trigger), Lab 3 (LWC), Lab 4 (REST callout)

---

## Principle 2: Org Is Not Source of Truth; Orgs Are Deploy Targets

**Core idea:** Production is a deploy target. Changes flow: Git → CI validate → QA → UAT → Pre-Prod → Prod. No one edits production in Setup and “remembers to copy it later.”

**Environment map (from DevOps training track):**

| Stage | Purpose | Typical sandbox | Promoted by |
|-------|---------|-----------------|-------------|
| Dev | Build & unit test | Developer / Developer Pro / scratch org | Developer via Git |
| QA | Automated validation, integration | Developer Pro or Partial Copy | Pipeline on merge |
| UAT | Business tester sign-off | Partial Copy or masked Full | Release engineer |
| Pre-Prod | Dress rehearsal, prod-like metadata/volume | Full or recent Partial | Release engineer |
| Prod | Customers | Production | Release engineer, approved, in window |

**Scratch orgs vs sandboxes:** Scratch orgs are empty orgs created from a Dev Hub + definition file; good for package builds, not for the bank’s Dev→Prod path (commercial-banking orgs carry managed packages, SSO, named credentials, licenses a scratch org won’t reproduce unless encoded).

**Where documented:**
- SALESFORCE_DEVOPS_DEEP_DIVE.md — Section 3 (Environments and sandboxes), Section 1 (Source of truth)
- navigation-breadcrumbs.md — Deployment & DevOps (Sandboxes, Change Sets, DevOps Center)

---

## Principle 3: Multi-Tenant Governor Limits

**Core idea:** Salesforce runs thousands of customers on shared servers. Governor limits are per-transaction runtime caps so one org’s inefficient code cannot starve another. Exceeding a limit throws `LimitException` and stops execution.

**Key limits a release engineer must name:**

| Category | Limit (typical) | DevOps implication |
|----------|-----------------|-------------------|
| SOQL queries (sync) | 100 per transaction | No queries inside loops; bulkify |
| SOQL queries (async) | 200 per transaction | Still finite; bulk queries outside loops |
| DML statements | 150 per transaction | Batch DML, not inside loops |
| DML rows | 10,000 per transaction | Chunk data loads ≤ ~9,000 rows/batch |
| Heap size | 6 MB sync / 12 MB async | Stream, don’t hoard large collections |
| CPU time | 10,000 ms sync / 60,000 ms async | Offload heavy processing to async |
| Callouts | 100 per transaction, 120s cumulative | Named Credentials, async callouts, batch external requests |
| Batch Apex | 5 queued/active; 200 default batch size | Don’t chain 50 batches in one deploy |
| Queueable | 50 chained per transaction | Avoid deep chains |
| Future calls | 50 per transaction | Don’t fire future methods in loops |

**The release-engineer question:** “What happens when this trigger/Flow runs on 200 records at once?” A deploy can be green and still fail in production under real volume.

**System properties for probing limits at runtime:** `Limits.getQueries()`/`getLimitQueries()`, `Limits.getDmlRows()`/`getLimitDmlRows()`, `Limits.getCpuTime()`/`getLimitCpuTime()`, `Limits.getHeapSize()`/`getLimitHeapSize()`, `Limits.getCallouts()`/`getLimitCallouts()`; `UserInfo.getOrganizationId()`, `Organization.IsSandbox`, `Organization.InstanceName`.

**Where documented:**
- SALESFORCE_LIMITS_DEEP_DIVE.md (full deep dive)
- crash-course.md — “Governor Limits Deep Dive”

---

## Principle 4: Security Model Layers

**Core idea:** Access is enforced at multiple layers, and each layer has a different merge/deploy behavior.

| Layer | Controls | Merge/deploy note |
|-------|----------|-------------------|
| Profile | Object permissions, FLS, page layouts, apps/tabs, login hours, IP ranges | Profile XML is a permission grab-bag; two stories editing it conflict; bad merge ships unreviewed access |
| Permission Set | Additional object/field access beyond profile | Smaller, merges better if kept small; split by feature/persona |
| Permission Set Group | Bundles permission sets for a job function | Avoids monolithic permission sets |
| Role | Record-level sharing position in hierarchy | Higher roles see records owned by lower roles |
| Org-Wide Defaults | Baseline record visibility (Private, Public Read Only, Public Read/Write) | Sharing only expands access, never restricts below OWD |
| Sharing Rules | Criteria-based / owner-based / territory-based | Extends access beyond OWD + hierarchy |
| Field-Level Security | Visible / Read Only / Hidden per field per profile | Set at Profile level, not page layout (layouts bypassable via API) |

**Release-engineer coaching:** Story access goes in permission sets, not `Admin.profile`. Profiles do not merge well; permission sets do (if kept small).

**Where documented:**
- crash-course.md — “Users, Profiles, Roles & Security”
- navigation-breadcrumbs.md — Security & Access
- user-management-data.md — Profiles & Permission Sets, Roles & Record Sharing, Field-Level Security & Encryption
- labs-design.md — Security Design patterns

---

## Principle 5: Testing as the Production Gate

**Core idea:** Apex deployment to production requires tests. Salesforce requires ≥75% org-wide code coverage, and each Apex class needs ≥1% coverage. Tests must create their own data (no reliance on org data).

**Three distinct validation actions:**

| Action | Changes org? | Purpose |
|--------|--------------|---------|
| Validation / dry-run (`--dry-run`) | No | Prove payload compiles + tests pass against target org |
| Quick deploy | Yes | Promote a validation that already passed, inside the 10-day platform window |
| Real deploy | Yes | First deploy, or validation expired, or payload changed |

**Test levels:** `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`. Production rejects `NoTestRun` when payload contains Apex.

**Test best practices:** Tests insert their own data; no `SELECT ... LIMIT 1` assumptions on org data; `@testSetup` for shared test data; assert behavior not just execution.

**Where documented:**
- SALESFORCE_DEVOPS_DEEP_DIVE.md — Section 13 (Automated testing and validation)
- labs-design.md — Lab 2 (trigger + test class, 100% coverage)

---

## Principle 6: Deployment Constraints

**Core idea:** Metadata API deploys are mostly atomic (one failure rolls back the whole payload), but with important constraints.

| Constraint | Detail |
|------------|--------|
| Atomicity | Mostly atomic; some components (custom settings, reports, dashboards) deploy partially |
| Dependency order | Deploy dependencies before dependents (field before flow; class B before class A calling it) |
| One deploy per org at a time | Concurrent deploys to same org queue/fail; serialize in CI |
| Quick-deploy window | 10 days after a successful validation; expired → re-validate |
| Destructive changes | Explicit `destructiveChanges.xml`; not inferred from “missing from Git”; deletes not reversible by Git revert |
| Managed packages | Immutable (`CANNOT_MODIFY_MANAGED_OBJECT`); configure around or upgrade via `sf package install`; never fork in Git |
| package.xml size | Very large component lists increase failure surface; split by release train or metadata domain |

**Where documented:**
- SALESFORCE_LIMITS_DEEP_DIVE.md — Sections 2, 4, 6
- SALESFORCE_DEVOPS_DEEP_DIVE.md — Section 6 (metadata lifecycle), Section 10 (rollback)

---

## Principle 7: Change Control in Regulated Environments

**Core idea:** Commercial banking (and insurance/healthcare) requires audit evidence for every production change.

**Audit pack to keep, every release:**
- Change-ticket ID in the commit message and pull request
- Non-author diff review (second pair of eyes)
- Validation deploy ID + prod deploy ID
- Test run ID + coverage number
- Named approver different from the author
- Release tag (e.g., `release-2026-11-27`)
- For Full sandboxes: refresh time, mask-complete confirmation, who may log in

**Segregation of duties:** Developer who wrote Apex does not approve their own prod deploy. Pipeline makes it structural: integration user deploys; human approves; different identities.

**Data hygiene:** No production customer data (PII/SIN-adjacent IDs, account numbers) in slides, debug logs pasted to tickets, or unmasked sandboxes. Data Mask (Salesforce product) or vendor script for Full sandbox masking.

**Where documented:**
- SALESFORCE_DEVOPS_DEEP_DIVE.md — Section 5 (audit/security/compliance), Section 11 (banking change control)
- navigation-breadcrumbs.md — Deployment & DevOps, Monitoring & Troubleshooting (Debug Logs)

---

## Principle 8: “Can Flow Do This Instead of Code?”

**Core idea:** Before building, evaluate the build-vs-buy-vs-declare choice.

| Option | Best for |
|--------|----------|
| AppExchange app | Save time, costs money |
| Flow | Fastest to build, easiest to maintain, no test classes |
| Apex | Complex logic, callouts, bulk operations, triggers |
| LWC | Custom UI beyond standard page layouts |

**Maintenance checklist:** Who maintains it after you leave? Can an admin modify it? Is it documented? Are there test classes (≥75% coverage)? Can it be deployed to production (tested in sandbox first)?

**Where documented:**
- crash-course.md — “When to Code vs. When to Flow”, “When to Use Each”
- labs-design.md — “The Buy vs Build Decision”, “The Maintenance Question”, Design Considerations checklist

---

## Mapping to Certification Study

| Principle | PD1 | Platform App Builder | Platform Administrator II |
|-----------|-----|---------------------|--------------------------|
| Metadata-driven platform | ✅ (Apex, Visualforce, deploy) | ✅ (declarative customization) | ✅ (org configuration) |
| Org not source of truth | ✅ (deploy model) | ✅ (change sets / deployment) | ✅ (sandboxes, deployment) |
| Governor limits | ✅ (core Apex topic) | ⚠️ (awareness) | ⚠️ (awareness) |
| Security model layers | ⚠️ (CRUD/FLS in Apex) | ✅ (profiles, permission sets, FLS, roles, OWD) | ✅ (security, sharing) |
| Testing as gate | ✅ (75% coverage, test classes) | ⚠️ (awareness) | ⚠️ (awareness) |
| Deployment constraints | ✅ (Metadata API, change sets) | ✅ (deployment basics) | ✅ (sandboxes, change sets) |
| Change control / audit | ⚠️ | ⚠️ | ✅ (advanced admin topics) |
