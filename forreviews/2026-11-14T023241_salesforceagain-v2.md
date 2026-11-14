# Salesforce DevOps Research — Consolidated Review Copy

| Field | Value |
|---|---|
| **Worktree / agent** | `salesforceagain-v2` |
| **Consolidated (UTC)** | 2026-11-14T02:32:41Z |
| **Source run folder** | `research/20261114T021017Z-salesforceagain-v2/` (PR #1) |
| **Target role** | DevOps Engineer (Salesforce), Scotiabank requisition 276046 |
| **Merge target** | `docs/salesforce/devops-engineer/` on the published training site |
| **Status** | Round 1 research — ready for review/merge |

This is a single-file review copy of the round-1 research run. The canonical, split version with per-file provenance lives in the source run folder and its PR. Sections below are the original files, concatenated in reading order.

## Contents

1. Run manifest (`README.md`)
2. Plan & Salesforce key principles (`PLAN.md`)
3. Limits, governor limits & system properties (`01`)
4. Metadata dependencies & deployment constraints (`02`)
5. DevOps tools UI walkthroughs — Gearset/Copado/AutoRABIT/DevOps Center (`03`)
6. GitHub Actions + Salesforce CI/CD (`04`)
7. JD term-by-term decoder (`05`)
8. Certifications & curriculum (`06`)
9. Sources & verification status (`sources.md`)

## Review notes

- Numbers and limits marked `[Verify]` are edition/version-dependent; confirm against current official Salesforce docs before publishing.
- Certification domain weights are intentionally omitted pending the current official exam guide.
- No secrets, customer data, org IDs, or tokens.


---

<!-- ===== begin: README.md ===== -->

# Salesforce DevOps Research — Run Manifest

| Field | Value |
|---|---|
| **Agent / worktree** | `salesforceagain-v2` (Kilo) |
| **Created (UTC)** | 2026-11-14T02:10:17Z |
| **Folder** | `research/20261114T021017Z-salesforceagain-v2/` |
| **Target role** | DevOps Engineer (Salesforce), Scotiabank, Requisition 276046, Commercial Banking Engineering, Toronto |
| **Primary source JD** | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| **Merge target** | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> and sibling Salesforce guides (crash course, breadcrumbs, labs, user & data) |
| **Status** | Round 1 — research complete, ready for merge round |
| **Confidence** | High on platform mechanics and limits; medium on vendor UI button paths (they change by edition/release — verify in-tenant) |

## What this folder is

This is a **self-contained round-1 research drop**. It is written so a later agent can merge it into the published training site without re-doing discovery. Every file states what it covers, what it assumes, and where it should land.

It deliberately **does not duplicate** the existing crash course. The published crash course already covers objects/fields, security basics, Flow vs Apex, and a first pass at governor limits. This drop goes **deeper**: exact limit values, per-transaction vs per-org vs per-24h, system properties, metadata dependency graphs, deployment constraints, tool UI walkthroughs, and a production-grade GitHub Actions pipeline.

## Files and merge destinations

| File | What it is | Merge destination on the docs site |
|---|---|---|
| `PLAN.md` | Structured approach, Salesforce key principles, research method, quality bar | New "Editorial standard / how this track is built" note, or `docs/salesforce/devops-engineer/#appendix-plan` |
| `01-limits-governors-and-system-properties.md` | Deep dive: governor limits, platform/org limits, API limits, system properties, how to measure | Extend `#2-metadata-that-breaks-releases` and crash-course governor-limit section; add a new "Limits & system properties" child page |
| `02-metadata-dependencies-and-deployment-constraints.md` | Dependency graphs, ordering, destructive changes, Metadata API constraints, failure catalogue | Extend `#2-metadata-that-breaks-releases` + `#7-conflict-clinic` |
| `03-devops-tools-ui-walkthroughs.md` | Gearset, Copado, AutoRABIT, DevOps Center: where to click for compare/deploy/backup/rollback | Expand `#6-devops-tools` into per-tool subsections |
| `04-cicd-github-salesforce.md` | End-to-end GitHub Actions pipeline, auth, delta deploys, gates, promotion, rollback | Expand `#5-cicd` with a full worked pipeline |
| `05-jd-term-by-term.md` | Every JD line and skill parsed into term → definition → config/settings/variations → what you do in the role | New "JD decoder" page linked from the track index |
| `06-certifications-and-curriculum.md` | PD1, Platform Administrator II (ex-Advanced Admin), Development Lifecycle & Deployment Architect, vendor certs; curricula + study order | Expand `#certifications` |
| `sources.md` | Every URL used, with what it was used for and access caveats | Provenance appendix |

## Reading order for the merge agent

1. `PLAN.md` — understand the principles and the intended structure.
2. `05-jd-term-by-term.md` — the spine; it maps 1:1 to the requisition.
3. `01`, `02`, `04` — the technical core (limits, dependencies, pipeline).
4. `03` — tool-specific UI evidence.
5. `06` — credential mapping.
6. `sources.md` — verify any claim that looks time-sensitive.

## Hard constraints respected

- **No invented numbers.** Limits are the canonical Salesforce values; anything edition-dependent or release-dependent is flagged.
- **No fabricated UI screenshots.** UI paths are described as "typical layout; verify in your tenant."
- **No secrets.** No org IDs, tokens, customer data, or real endpoints.
- **Regulated-environment lens.** Every recommendation is framed for a bank: audit trail, segregation of duties, change ticket, rollback evidence.

## Known gaps for round 2

- Vendor pricing and exact edition feature-gating (Gearset/Copado/AutoRABIT) — commercial, changes often.
- Exact certification domain weights — must be confirmed from the current official exam guide PDF (Salesforce gates its docs behind auth/bot checks; see `sources.md`).
- Screenshots/diagrams — text-only in this round; a diagram pass would help `02` and `04`.
- Real org-verified `sf` CLI flags — flags move between CLI majors; run `--help` before publishing command blocks.

<!-- ===== end: README.md ===== -->


---

<!-- ===== begin: PLAN.md ===== -->

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

<!-- ===== end: PLAN.md ===== -->


---

<!-- ===== begin: 01-limits-governors-and-system-properties.md ===== -->

# 01 — Salesforce Limits, Governor Limits, and System Properties

> **Scope:** the "Understanding of Salesforce limits, metadata dependencies, and deployment constraints" line in requisition 276046, plus the "System properties" ask.
> **Audience:** a DevOps/release engineer who will not write most of the Apex but must predict when a deploy or a release will fall over.
> **Rule of thumb used throughout:** a limit is either **per transaction**, **per execution context**, **per org per 24 h**, **per org total**, or **per edition/licence**. Confusing these is the most common interview mistake.

<details>
<summary><strong>How to read the confidence labels</strong></summary>

- **[Canonical]** — stable, widely documented Salesforce value. Safe to quote.
- **[Verify]** — edition-, version-, or licence-dependent. Confirm in the target org and the current official docs before publishing a hard number.
- **[Behaviour]** — not a number, but a platform rule that causes most deploy failures.

This file deliberately avoids inventing numbers. Where a value is edition-dependent it is labelled, not guessed.
</details>

---

## 1. Why governor limits exist (and why they are a DevOps problem)

Salesforce is **multi-tenant**. Your Apex runs on shared application servers against a shared database cluster. Governor limits are the fairness mechanism: they cap what a single transaction can consume so one tenant cannot starve the others. When you exceed one, the runtime throws `System.LimitException` and the transaction rolls back.

For a release engineer this matters because:

1. **A deploy can be green and the feature can still fail in production.** Deployment validates compilation + tests; it does not simulate your production data volume.
2. **The same code path can pass in Dev and hit a limit in Prod** because Prod has data skew, more records, or more automation firing.
3. **Your CI pipeline itself consumes limits** (API calls, test executions, metadata retrievals). A busy release week can exhaust the org's 24-hour API budget.

> The interview sentence: *"Governor limits are per-transaction fairness caps on a multi-tenant platform, so a successful deploy is necessary but not sufficient — I validate against prod-like volume and review for bulkification."*

---

## 2. The five clocks — classify every limit before you quote it

<details>
<summary><strong>Per transaction (governor limits)</strong></summary>

Reset at the start of each Apex transaction. A trigger + its handler + all cascaded DML share **one** budget. This is the budget most people mean by "governor limits."

Typical: SOQL queries, DML statements/rows, heap, CPU, callouts, email invocations.
</details>

<details>
<summary><strong>Per execution context (async)</strong></summary>

Batch chunks, Queueable jobs, `@future` methods, and scheduled jobs each get their **own** governor budget. Async contexts usually get **more** room (e.g., CPU and heap double), and Batch Apex gets **200 SOQL queries per batch** rather than 100.
</details>

<details>
<summary><strong>Per org per rolling 24 hours</strong></summary>

API requests, async Apex executions, and some email caps are org-wide and **rolling** (not midnight-to-midnight). A pipeline that retrieves and validates hundreds of times a day spends this budget.
</details>

<details>
<summary><strong>Per org total (capacity)</strong></summary>

Custom objects, fields, record types, validation rules, permission sets, storage. These do not reset; they are your schema ceiling. They are the limits a release engineer hits when a "small" change needs "just one more field."
</details>

<details>
<summary><strong>Per edition / licence (entitlements)</strong></summary>

Developer vs Professional vs Enterprise vs Unlimited vs Performance, and sandbox type, change what you are allowed. Always state the edition when you quote a capacity number.
</details>

---

## 3. Apex governor limits — the table you must know

### 3.1 Synchronous vs asynchronous (per transaction)

| Resource | Synchronous | Asynchronous | Notes |
|---|---:|---:|---|
| Total SOQL queries | **100** | **200** | Batch Apex: 200 per batch |
| Total SOQL rows retrieved | **50,000** | **50,000** | Rows, not queries |
| Total SOSL queries | **20** | **20** | |
| Total SOSL rows | **2,000** | **2,000** | |
| DML statements | **150** | **150** | Statement count ≠ row count |
| DML rows | **10,000** | **10,000** | |
| Records via `Database.getQueryLocator` | **10,000** | **10,000** | |
| Heap size | **6 MB** | **12 MB** | |
| CPU time | **10,000 ms** | **60,000 ms** | 10 s / 60 s |
| HTTP callouts per transaction | **100** | **100** | |
| Timeout per callout | **120 s** | **120 s** | |
| Cumulative callout time | **120 s** | **120 s** | |
| Email invocations | **10** | **10** | |
| Push notifications | **10** | **10** | |
| `@future` calls enqueued | **50** | **50** | |
| Queueable jobs enqueued | **50** | **50** | |
| Batch jobs queued/active concurrently | **5** | **5** | Org-wide |
| Concurrent scheduled Apex jobs | **100** | — | Org-wide |
| Max size of one Apex class/trigger | **1,000,000 characters** | — | Per class/trigger |

> **[Verify]** Some rows have edition nuances and Salesforce adjusts async caps over time. The 100/200, 50,000, 150, 10,000, 6/12 MB, 10 s/60 s, 100 callouts, 10 email rows are the canonical values used in interviews.

### 3.2 The distinction that trips people up

- **SOQL queries vs SOQL rows.** 100 queries is generous; 50,000 rows is not. `SELECT Id FROM Account` on a million-row object can blow the row limit in one query.
- **DML statements vs DML rows.** 150 statements but only 10,000 rows. One `insert` of 20,000 records fails on rows; 200 single-row inserts fail on statements.
- **Heap vs CPU.** Heap is memory (row width × count), CPU is processing. Both can fail independently.

---

## 4. The limit families in detail

<details>
<summary><strong>4.1 SOQL and SOSL</strong></summary>

**Hard limits**

- 100 SOQL queries per sync transaction / 200 async.
- 50,000 rows retrieved per transaction.
- 20 SOSL queries; 2,000 SOSL rows.
- Query timeout: a single SOQL query is bounded (commonly **120 s**); long-running queries are cancelled. **[Verify]**

**Why releases fail**

- Query inside a `for` loop over `Trigger.new` → 1 query per record × 200 records = instant `Too many SOQL queries: 101`.
- Non-selective query on a large object → timeout or full-table scan warnings in the query plan.
- `SELECT` of unnecessary fields → heap pressure.

**What the reviewer asks**

> "What happens when `Trigger.new` has 200 records and the Account table has 5 million rows?"

**Bulkification pattern**

```apex
// Collect keys first, query once, map, then iterate in memory.
Set<Id> accountIds = new Set<Id>();
for (Case c : Trigger.new) {
    if (c.AccountId != null) accountIds.add(c.AccountId);
}
Map<Id, Account> accounts = new Map<Id, Account>(
    [SELECT Id, Name, OwnerId FROM Account WHERE Id IN :accountIds]
);
```

**Selectivity / indexes (why Prod differs from Dev)**

- `Id`, `Name`, `OwnerId`, `CreatedDate`, `SystemModstamp`, external-ID/unique fields, and custom indexed fields are selective.
- Leading wildcards (`LIKE '%foo'`), `!=`, `NOT IN`, and null checks on unindexed fields are not.
- **Data skew** (e.g., one Owner owns 90% of records) defeats selectivity even on an indexed field.
- Sandboxes with tiny data hide these problems. This is why UAT/Pre-Prod should be Pre-Prod-like or data-masked Full.
</details>

<details>
<summary><strong>4.2 DML</strong></summary>

**Hard limits:** 150 DML statements and 10,000 DML rows per transaction.

**Platform behaviours that cause incidents**

- **Partial success:** `Database.insert(records, false)` returns per-record errors instead of throwing. If you use `false`, you must inspect `SaveResult`.
- **Savepoints:** `Database.setSavepoint()` / `rollback()` let you undo within a transaction, but they consume resources and do not cross async boundaries.
- **Row locks:** `UNABLE_TO_LOCK_ROW` happens when two transactions touch overlapping parent/child rows. Common with roll-up summaries, master-detail, and batch jobs running during business hours.
- **Recursion:** triggers that update the same object can re-fire. Use a static guard and one trigger per object.
- **Order of execution:** validation rules → before triggers → duplicate rules → after triggers → assignment/auto-response/workflow → roll-ups → sharing → commit. A before-trigger cannot see a roll-up that recalculates later.

**Bulk pattern:** build a `List`, mutate in memory, one `update`.
</details>

<details>
<summary><strong>4.3 Heap and CPU</strong></summary>

- **Heap:** 6 MB sync / 12 MB async. Query width matters: 50,000 rows × many fields can exceed heap even if rows are under the limit.
- **CPU:** 10,000 ms sync / 60,000 ms async. Nested loops, string concatenation in loops, and repeated regex are typical causes.
- **Mitigations:** query fewer fields, `LIMIT`, stream via Batch Apex, use `Map` lookups instead of nested loops, move heavy work async.

**Smell test:** three nested `for` loops over collections in a trigger handler = a CPU incident waiting for volume.
</details>

<details>
<summary><strong>4.4 Callouts</strong></summary>

- **100 callouts per transaction**, **120 s per callout**, **120 s cumulative**.
- **6 MB** request and response size for an Apex HTTP callout. **[Verify]** Larger payloads need Bulk API or an external store.
- **"You have uncommitted work pending"**: you cannot make a callout after DML in the same transaction. Move the callout to `@future(callout=true)`, Queueable, or Batch.
- **Named Credentials / External Credentials** hold endpoint + auth; never hardcode secrets.
- **Remote Site Settings** are still required for callouts **not** using Named Credentials; prefer Named Credentials.

**Release-engineering angle:** a callout limit failure is usually a design failure (callout in a loop), not a data-volume failure.
</details>

<details>
<summary><strong>4.5 Asynchronous Apex — future, Queueable, Batch, Scheduled</strong></summary>

| Mechanism | Governor budget | Best for | Key limits |
|---|---|---|---|
| `@future` | Async (200 SOQL, 12 MB, 60 s CPU) | One-off fire-and-forget; callouts | 50 per transaction; no chaining; primitive params only |
| Queueable | Async, own budget | Chaining, complex objects, callouts | 50 enqueued per transaction; one job can enqueue one more |
| Batch Apex | Per batch (200 records default, max 2,000) | Millions of records | 5 concurrent batch jobs org-wide; `Database.Stateful` for counters |
| Scheduled Apex | Async | Cron-like work | 100 concurrent scheduled jobs org-wide |

**Release-engineering angle:** async work survives the transaction but **not** a failed deploy. If a batch is mid-run during a deploy that changes its class, you can get version-skew errors. Freeze long-running batches around release windows, or drain them before deploying.
</details>

<details>
<summary><strong>4.6 Email and notifications</strong></summary>

- 10 email invocations per transaction; 10 push notifications.
- Org-wide daily email caps are **edition/licence dependent** and are separate from Apex invocation limits. **[Verify]**
- `Messaging.SingleEmailMessage` is the transactional path; mass email is a different product with its own caps.
- In sandboxes, **Email Deliverability** defaults to "System email only" — a common cause of "the Flow didn't send the email" in UAT. See §9.
</details>

---

## 5. API limits (the ones your pipeline spends)

<details>
<summary><strong>5.1 The 24-hour API request allocation</strong></summary>

Salesforce allocates API requests per org per rolling 24 hours. The widely cited formula for Enterprise/Unlimited/Performance is:

```
15,000 base + (number of user licences × 1,000) per 24 hours
```

Developer Edition and some lower editions have a flat allocation. **[Verify]** the exact entitlement for the target edition in Setup > Company Information / System Overview.

**Why DevOps cares:** every `sf project retrieve`, `sf project deploy`, `sf apex run test`, and metadata poll is API traffic. A pipeline that validates on every commit across many PRs, plus sandbox refreshes, plus integrations, can exhaust the org budget and block *integrations*, not just your pipeline.

**Mitigations**

- Use **delta** deploys (only changed files) rather than full retrieves/deploys.
- Cache or gate: validate on PR, deploy on merge.
- Prefer a dedicated **CI integration user** so you can attribute consumption.
- Monitor Setup > System Overview and Event Monitoring (API events).
</details>

<details>
<summary><strong>5.2 Request size and concurrency</strong></summary>

- Synchronous REST/SOAP request and response payloads are bounded (**commonly 6 MB**). **[Verify]**
- Concurrent long-running requests (≥ 20 s) are capped (commonly **25**). **[Verify]**
- Bulk API 2.0 exists for large data volumes and has its own job/batch limits; it still consumes API entitlement.
- Streaming API / Pub-Sub has subscriber and event limits.

**Interview answer:** "For large data I use Bulk API, not synchronous REST; for large metadata I split the payload or package it."
</details>

<details>
<summary><strong>5.3 API version drift</strong></summary>

Every org has an API version. Metadata retrieved at one version can fail to deploy to an org on an older version. A bank with staggered sandbox refreshes can have mixed versions.

**Check:** Setup > Company Information (instance), or `sf org display`. Pin the `sourceApiVersion` in `sfdx-project.json` and in the CI workflow.
</details>

---

## 6. Metadata API and deployment constraints (the release engineer's real limits)

<details>
<summary><strong>6.1 The hard deployment gates</strong></summary>

| Constraint | Value / rule | Confidence |
|---|---|---|
| Production Apex code coverage | **≥ 75% org-wide**, zero test failures | Canonical |
| `NoTestRun` in production with Apex | **Not allowed** | Canonical |
| Test levels | `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg` | Canonical |
| Quick Deploy window after validation | **10 days** (validation must still match the payload) | Canonical |
| Rollback on error | Deploy option; when on, a component failure rolls back the whole deploy | Canonical |
| Destructive changes | Separate pre/post `destructiveChanges.xml`; **not** implied by absence from the payload | Canonical |
| Component count per deploy | Bounded (commonly cited ceiling **10,000** components) — split large payloads | Verify |
| Package/ZIP size | Bounded; very large payloads should be split or packaged | Verify |
| Deploy concurrency | Deployments queue; a long deploy blocks the next one | Behaviour |
| API version of payload vs target | Must be compatible; older target rejects newer metadata | Behaviour |

> The two that cause the most outages: (a) assuming a component's absence deletes it, and (b) forgetting that **Quick Deploy is only valid for 10 days and only if nothing relevant changed**.
</details>

<details>
<summary><strong>6.2 Why "it deployed" does not mean "it works"</strong></summary>

These are deployment **constraints** in the practical sense — the deploy succeeds but the feature is dead:

- **Record type deployed, but not assigned** to the profile/permission set → users cannot create records of that type.
- **Page layout deployed, but assignment not deployed** → users still see the old layout.
- **Lightning record page (FlexiPage) deployed, but not activated** for the app/record type → Lightning users see the classic layout.
- **Flow new version deployed as Draft** → users keep running the old active version.
- **Permission set deployed, but not assigned** → access not granted.
- **Custom metadata record not deployed** → code falls back to a default or null.
- **Named Credential / External Credential principal not configured in target** → callouts fail at runtime.

Every one of these is a "deploy green, feature broken" case. Your validation checklist must include **post-deploy verification**, not just a green deployment.
</details>

<details>
<summary><strong>6.3 Metadata types that behave badly in deployments</strong></summary>

| Type | Why it breaks | Mitigation |
|---|---|---|
| **Profiles** | Huge, contain user/org-specific values, merge poorly, can time out | Deploy thin deltas; prefer permission sets; review permission diff with a second person |
| **Permission sets** | Conflict if everyone edits one monolith | One per feature/persona; permission set groups to bundle |
| **Flows** | XML does not merge; active-version semantics | One owner per flow; deploy as active; verify version |
| **Layouts** | Assignment lives elsewhere | Deploy layout + assignment + record type + permission together |
| **Record types** | Depend on business process + picklist values | Deploy the full dependency set in one payload |
| **Reports/dashboards** | Folder dependency; API quirks | Deploy folders first; use a tool that resolves Public Reports |
| **Managed package metadata** | `CANNOT_MODIFY_MANAGED_OBJECT` | Configure around it or upgrade the package |
| **Sharing rules / OWD** | Ordering and recalculation | Deploy after objects/fields; expect recalculation time |
| **Apex** | Compile-time dependency on other classes | Deploy class + dependencies + tests together |
</details>

---

## 7. Org capacity limits ("system limits" that block releases)

These are per-org totals, not per-transaction. They are edition-dependent, so treat the numbers as **order-of-magnitude** until verified in the org.

<details>
<summary><strong>7.1 Schema and configuration ceilings to check before promising a design</strong></summary>

| Area | Typical ceiling | Notes |
|---|---|---|
| Custom objects | Hundreds (edition-dependent) | Unlimited/Performance higher |
| Custom fields per object | High hundreds | Relationship fields are capped separately |
| Master-detail relationships per object | **2** | Canonical |
| Lookup relationships per object | **~40** | Verify |
| Validation rules per object | **100** | Canonical |
| Record types per object | Bounded | Check before a "record type per region" design |
| Page layouts per object | Bounded | |
| Active Flows | Thousands org-wide | Check before a "flow per record type" design |
| Permission sets | Bounded | A monolith-per-feature strategy will exhaust it |
| Roles | Bounded | Deep hierarchies cost performance |
| Sharing rules | Bounded per object | |
| Custom settings / custom metadata types | Bounded | |
| Named credentials / remote site settings | Bounded | |
| Tabs / apps | Bounded | |
| Reports / dashboards | Bounded | |

**How to check the real numbers for *this* org:** Setup > Company Information, the Salesforce "Features and Edition Allocations" reference, and the relevant object's limit messages. Do not quote a blog number as if it were universal.
</details>

<details>
<summary><strong>7.2 Storage and data limits</strong></summary>

- **Data storage** and **file storage** are separate allocations, edition- and licence-based.
- Sandbox storage is a fraction of production; a Full sandbox copy can fail or be partial if production storage is near the cap.
- Big objects and archive strategies exist for very large volumes; they are a design decision, not a deploy-time fix.

**Release-engineering angle:** a Full sandbox refresh is not instant. It depends on production size, Salesforce's refresh queue, and your edition's refresh interval. Never promise a same-day Full refresh.
</details>

---

## 8. "System properties" — the phrase, decoded

"System properties" is not one Salesforce object. In this role it means **the org-level settings and runtime properties that are not obviously "metadata in Git" but that change behaviour and must be recorded per environment.** There are three useful meanings; cover all three.

<details>
<summary><strong>8.1 Org identity and capacity properties (record these per environment)</strong></summary>

| Property | Where | Why it matters |
|---|---|---|
| Org ID (15/18 char) | Setup > Company Information | Identifies the target; never hardcode |
| Edition | Company Information | Determines limits and features |
| Instance | Company Information / `sf org display` | Affects IP allowlists and endpoints |
| Namespace prefix | Company Information | Changes metadata names; package behaviour |
| Default locale / timezone / currency | Company Information | Can break date/currency tests |
| Licences (user types) | Company Information | Drives API allocation and test users |
| Storage used / limit | Company Information | Blocks sandbox copies and data loads |
| API version | Company Information / `sfdx-project.json` | Deploy compatibility |
| My Domain | Setup > My Domain | SSO, redirects, callout URLs |
| Sandbox name / type / refresh eligibility | Setup > Sandboxes | Release calendar |

**Practice:** keep a per-environment "org fact sheet" in the release repo (no secrets): org ID, edition, instance, API version, My Domain, refresh cadence, integration endpoints.
</details>

<details>
<summary><strong>8.2 Settings that are configuration, not metadata-in-Git (drift sources)</strong></summary>

These often do **not** travel with a metadata deploy, or travel differently, so a refreshed sandbox may silently differ:

| Setting | Where | Failure if wrong |
|---|---|---|
| **Email Deliverability** | Setup > Email Administration > Deliverability | Sandbox defaults to "System email only" → no emails from Flow/Apex |
| **Apex Settings** (enable/disable, API version) | Setup > Apex Settings | Apex disabled or wrong version |
| **Process Automation Settings** (default workflow user) | Setup > Process Automation Settings | Flows/approvals fail with no default user |
| **Deployment Settings** (rollback on error, etc.) | Setup > Deploy > Deployment Settings | Unexpected partial deploys |
| **Session Settings** (timeout, IP locking, caching) | Setup > Security > Session Settings | Test logins time out or fail |
| **Password / Login policies** | Setup > Security | CI integration user locked out |
| **Login IP Ranges / Trusted IP Ranges** | Profile / Network Access | CI runner blocked |
| **CORS / CSP Trusted Sites** | Setup > CORS / CSP Trusted Sites | Browser callouts blocked |
| **Remote Site Settings** | Setup > Remote Site Settings | Callouts blocked |
| **Named/External Credentials** (principals) | Setup > Named Credentials | Callouts 401 |
| **Certificates & Keys** | Setup > Certificate and Key Management | JWT auth fails |
| **Connected Apps / OAuth policies** | Setup > App Manager | CI auth fails, tokens expire |
| **SSO / Identity Provider** | Setup > Identity | Sandbox login broken after refresh |
| **Feature flags** (Person Accounts, Multi-currency, Territory Management, Field History, Duplicate Rules, Lightning) | Setup > Feature Settings | Tests/data model differ |
| **Org-Wide Defaults** | Setup > Sharing Settings | Security model drift |
| **Audit Trail** | Setup > Security > View Setup Audit Trail | Evidence for change control |

**DevOps implication:** after a sandbox refresh, run a **post-refresh checklist** that re-verifies the rows above before anyone logs in broadly.
</details>

<details>
<summary><strong>8.3 Apex runtime "system" properties: the <code>System</code> and <code>Limits</code> classes</strong></summary>

**`System` — runtime context and utilities**

| Member | Use |
|---|---|
| `System.now()` / `today()` / `currentTimeMillis()` | Deterministic-ish time; tests should not depend on wall clock |
| `System.isBatch()` / `isFuture()` / `isQueueable()` / `isScheduled()` | Branch behaviour by context; common in shared handlers |
| `System.getApplicationReadWriteMode()` | Detect read-only mode (e.g., during maintenance) |
| `System.requestVersion()` | API version of the current request |
| `System.debug()` | Logging (respects log levels) |
| `System.assert()` / `assertEquals()` | Test assertions |
| `System.Type` / `System.JSON` | Reflection and serialization |
| `System.LimitException` | The exception thrown when a governor limit is exceeded |

**`Limits` — read the budget at runtime**

```apex
System.debug('SOQL ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug('DML rows ' + Limits.getDmlRows() + '/' + Limits.getLimitDmlRows());
System.debug('Heap ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
System.debug('CPU ' + Limits.getCpuTime() + '/' + Limits.getLimitCpuTime());
System.debug('Callouts ' + Limits.getCallouts() + '/' + Limits.getLimitCallouts());
System.debug('Email ' + Limits.getEmailInvocations() + '/' + Limits.getLimitEmailInvocations());
System.debug('Future ' + Limits.getFutureCalls() + '/' + Limits.getLimitFutureCalls());
System.debug('Queueable ' + Limits.getQueueableJobs() + '/' + Limits.getLimitQueueableJobs());
```

**Use it for:** early warning in complex orchestrations, adaptive batching, and tests that assert a handler stays under a threshold.

**Do not use it for:** hiding a bad design. If you are at 90 queries in a simple trigger, fix the query pattern, not the log line.
</details>

<details>
<summary><strong>8.4 "System properties" as SAP-style system settings? (clarifying the ambiguity)</strong></summary>

Some interviews use "system properties" loosely to mean **environment-level configuration** (like SAP system properties or JVM system properties). In Salesforce the closest equivalents are:

- **Custom Settings / Custom Metadata Types** for application configuration and feature flags.
- **Named Credentials / External Credentials** for endpoint + auth configuration.
- **Org settings** in §8.2.
- **`System` class** in §8.3.

Say this explicitly in an interview: *"Salesforce doesn't have a single 'system properties' file; the equivalents are org settings, custom metadata/settings for app config, named credentials for endpoints, and the System/Limits classes at runtime."* That answer signals real platform knowledge.
</details>

---

## 9. Measuring and monitoring limits

<details>
<summary><strong>9.1 In-org tools</strong></summary>

| Tool | Where | What it shows |
|---|---|---|
| **System Overview** | Setup > System Overview | API usage, storage, user counts |
| **Company Information** | Setup > Company Information | Org identity, edition, storage, licences |
| **Apex Jobs / Background Jobs** | Setup > Apex Jobs / Background Jobs | Batch/Queueable/Future status, failures |
| **Scheduled Jobs** | Setup > Scheduled Jobs | Scheduled Apex and scheduled flows |
| **Debug Logs** | Setup > Debug Logs | Per-transaction LIMIT_USAGE lines, `FATAL_ERROR`, `LimitException` |
| **Apex Exception Email** | Setup > Apex Exception Email | Runtime errors in prod |
| **Setup Audit Trail** | Setup > View Setup Audit Trail | Who changed what (audit evidence) |
| **Deployment Status** | Setup > Deploy > Deployment Status | Deploy history, component failures |
| **Event Monitoring** (Shield/ add-on) | Setup > Event Monitoring | API, login, report, Apex execution events |
| **Optimizer** | Setup > Optimizer | Page performance and some advisory checks |
</details>

<details>
<summary><strong>9.2 Reading a debug log for limits</strong></summary>

A debug log contains `LIMIT_USAGE_FOR_NS` lines, e.g.:

```
LIMIT_USAGE_FOR_NS|default|Number of SOQL queries: 12 out of 100
LIMIT_USAGE_FOR_NS|default|Number of DML statements: 3 out of 150
LIMIT_USAGE_FOR_NS|default|Maximum CPU time: 1450 out of 10000
```

- Set a **Trace Flag** on the user (Setup > Debug Logs), log level **Finest** for limits detail.
- Search for `FATAL_ERROR` and `System.LimitException`.
- Correlate with the request ID from the user's error.

**CI tip:** on a failed validation, download the deploy result and the test failures; do not ask the developer to "try again in the UI."
</details>

<details>
<summary><strong>9.3 Pipeline-level monitoring</strong></summary>

- Track **API consumption** per CI run (System Overview before/after, or Event Monitoring).
- Track **validation duration** and **test duration**; a creeping test suite is a release-window risk.
- Track **coverage trend**; a slow decline toward 75% is a future blocked release.
- Alert on **failed deploys**, **quick-deploy expiry**, and **approaching 24 h API caps**.
</details>

---

## 10. How limits shape release engineering (the part the JD actually tests)

<details>
<summary><strong>10.1 Why validation must be against a prod-like org</strong></summary>

A Developer sandbox has ~200 records and no data skew. A validation there proves compilation, not runtime safety. The honest gate is a **Pre-Prod/Full or masked Partial** with production-like volume and configuration. That is why the environment ladder in the published track puts UAT on Partial/Full and Pre-Prod on Full.

**Interview answer:** *"I validate where the data shape is real, not where the deploy is convenient."*
</details>

<details>
<summary><strong>10.2 Bulkification review checklist (for any Apex in the release)</strong></summary>

- [ ] No SOQL or DML inside a loop.
- [ ] Handler accepts collections, not single records.
- [ ] One trigger per object, logic in a handler class.
- [ ] Recursion guard (static boolean/Set).
- [ ] Queries are selective on indexed fields; `LIMIT` where appropriate.
- [ ] Callouts are async and not after DML.
- [ ] Tests create their own data (no `LIMIT 1` assumptions).
- [ ] Test asserts behaviour under 200-record bulk where relevant.
- [ ] No hardcoded IDs (use custom metadata/query).
- [ ] Async work drains before the release window.

</details>

<details>
<summary><strong>10.3 Release-window capacity planning</strong></summary>

- **Drain async jobs** before deploying (Batch, Queueable, Scheduled).
- **Freeze** long-running integrations during the window if the deploy changes their contracts.
- **Budget API calls**: validation + quick deploy + smoke tests + rollback rehearsal all consume the 24 h allowance.
- **Stagger sandbox refreshes**: they consume API and storage and can collide with release validation.
- **Pin API versions** across orgs to avoid mixed-version deploy failures.
- **Plan for deploy queueing**: two teams deploying at once serialize; one slow profile deploy blocks the window.

</details>

---

## 11. Interview drills (say these out loud)

1. **What are governor limits and why do they exist?** Per-transaction fairness caps on a multi-tenant platform; exceeding one throws `LimitException` and rolls back.
2. **SOQL queries vs rows?** 100 queries / 50,000 rows per sync transaction; async gets 200 queries. Rows are usually the binding constraint on large objects.
3. **Why can a green deploy still fail in prod?** Deployment validates compile + tests, not production data volume, data skew, or runtime limits.
4. **What is the production coverage gate?** 75% org-wide with zero test failures; `NoTestRun` is rejected when Apex is in the payload.
5. **How long is a validation good for?** Quick Deploy within 10 days, and only if nothing relevant changed since validation.
6. **How do you find which limit a transaction hit?** Debug log `LIMIT_USAGE_FOR_NS` + `FATAL_ERROR`/`LimitException`; correlate request ID.
7. **How do callouts interact with DML?** You cannot call out after uncommitted DML in the same transaction; move to async.
8. **What org settings most often break a refreshed sandbox?** Email deliverability, SSO/My Domain, connected apps/certs, named credentials, remote sites, default workflow user.
9. **How does your pipeline consume limits?** Every retrieve/deploy/test is API traffic against the 24 h allocation; use delta deploys and gate on PR.
10. **What do you hand an auditor when a deploy hits a limit?** Deploy ID, test run ID, debug log/request ID, the fix commit, and the re-validation ID.

---

## 12. Quick self-quiz

<details>
<summary>Answers</summary>

1. Sync SOQL query limit? **100** (async 200).
2. Sync heap? **6 MB** (async 12 MB).
3. Sync CPU? **10,000 ms** (async 60,000 ms).
4. DML rows per transaction? **10,000**.
5. Callouts per transaction? **100**, 120 s each and 120 s cumulative.
6. Production coverage gate? **75%**, zero failures.
7. Quick Deploy validity? **10 days**, payload must be unchanged.
8. Concurrent batch jobs? **5**.
9. Scheduled Apex concurrent? **100**.
10. The three "system properties" meanings in Salesforce? Org settings, app config (custom metadata/settings + named credentials), and the `System`/`Limits` runtime classes.
</details>

---

**Next:** `02-metadata-dependencies-and-deployment-constraints.md` turns these limits into a dependency-driven deploy order and a failure catalogue.

<!-- ===== end: 01-limits-governors-and-system-properties.md ===== -->


---

<!-- ===== begin: 02-metadata-dependencies-and-deployment-constraints.md ===== -->

# 02 — Metadata Dependencies & Deployment Constraints

> **Scope:** "Understanding of Salesforce limits, metadata dependencies, and deployment constraints" + "Resolve deployment conflicts" + "Troubleshoot deployment failures and dependency issues."
> **Companion:** `01-limits-governors-and-system-properties.md` covers numeric limits. This file covers **ordering, reference graphs, and the failure catalogue**.

---

## 1. The one-sentence model

A Salesforce deploy is a **set of instructions applied to an existing schema**. The Metadata API checks every reference in your payload against (a) the payload and (b) what already exists in the target. A missing reference fails the deploy; a present reference with missing *assignment* succeeds but leaves the feature broken. Release engineering is therefore **dependency management plus post-deploy verification**.

---

## 2. The dependency graph you must be able to draw

<details>
<summary><strong>2.1 Object-level dependency chain (left must exist before right)</strong></summary>

```text
Custom Object
  └─ Fields (including formula/logic that reference other fields)
       ├─ Validation Rules (reference fields)
       ├─ Record Types (select picklist values / business processes)
       │    └─ Business Processes (Sales/Support/Lead/...)
       ├─ Page Layouts (reference fields + record types)
       │    └─ Layout Assignments (per profile / record type)
       ├─ Compact Layouts
       ├─ Field-Level Security (profile / permission set)
       ├─ List Views (reference fields + filters)
       └─ Search Layouts

Lightning Record Page (FlexiPage)
  └─ Activation / assignment (app + record type + profile)
       └─ depends on fields, components, Apex/LWC bundles

Custom Tab
  └─ Custom App (tab membership)
       └─ Profile / Permission Set (app + tab visibility)

Apex Class
  ├─ referenced Apex Classes / interfaces
  ├─ referenced custom objects/fields/SObjectType
  ├─ Custom Metadata Types / Custom Settings
  └─ Test Class (must be in payload or already present)

Flow
  ├─ referenced objects/fields
  ├─ referenced Apex (invocable)
  ├─ subflows
  ├─ custom metadata/settings
  └─ Flow Definition (active version pointer)

Permission Set
  ├─ objects/fields (must exist)
  ├─ Apex classes (must exist)
  ├─ Flows (must exist)
  └─ Custom permissions / tabs / apps

Profile
  └─ everything a permission set does, plus layout assignments + login IP ranges
```

**Interview move:** draw this on a whiteboard. It immediately explains most "invalid cross reference id" errors.
</details>

<details>
<summary><strong>2.2 The deploy order that avoids most failures</strong></summary>

A safe default order for a mixed payload:

1. **Objects** (custom objects, custom metadata types, custom settings)
2. **Fields** (including formula/roll-up, but watch references)
3. **Picklist values / global value sets / business processes**
4. **Record types**
5. **Validation rules**
6. **Layouts** (page, compact, search) and **Lightning pages (FlexiPages)**
7. **Apex classes** (dependency order), **LWC bundles**, **Aura bundles**
8. **Flows** (and subflows)
9. **Custom tabs, apps**
10. **Permission sets / permission set groups**
11. **Profiles** (thin deltas only)
12. **Layout assignments / FlexiPage activation / app assignments**
13. **Sharing rules / OWD** (after objects/fields; expect recalculation)
14. **Custom metadata records / custom settings data**
15. **Named credentials / external credentials / remote sites** (or verify they exist)
16. **Reports / dashboards / folders**

> The Metadata API does not guarantee your order within a single deploy, but it does resolve many intra-payload dependencies. When it can't, split into **phased deploys** in this order. Tools (Gearset/Copado/AutoRABIT) implement a version of this ordering for you — know what they do so you can debug when they get it wrong.

</details>

<details>
<summary><strong>2.3 Renames are not renames</strong></summary>

Salesforce metadata generally does **not** support an in-place rename in a deploy. A "rename" is:

1. Create the new component (new API name).
2. Migrate references (formulas, layouts, Apex, Flows, reports).
3. Deploy the new component + references.
4. Deploy a **destructive change** to remove the old component (pre- or post-destructive).
5. Migrate data if it was a field (data migration is **not** metadata).

**Consequence:** a rename is a multi-step, multi-deploy change with a data component. Never let a developer "just rename it in the sandbox and deploy."

</details>

---

## 3. The failure catalogue (error string → cause → first check)

<details>
<summary><strong>3.1 Compile / reference errors</strong></summary>

| Error you see | Usual cause | First check |
|---|---|---|
| `Invalid cross reference id` | Record type / layout / business process assignment points at something missing | Deploy the parent (object, record type, layout) in the same payload |
| `no such column` / `field does not exist` | Flow/layout/formula/Apex references a field not in payload and not in target | Add the field to the payload |
| `entity not found` | Apex references an sObject not deployed | Add the object |
| `Variable does not exist` / `Method does not exist` | Apex dependency class/method missing | Deploy the dependency or remove the reference |
| `Duplicate value found` | Unique field / duplicate rule conflict on deploy of data | Deploy metadata without data; handle data separately |
| `Cannot modify managed object` | You edited a managed-package component | Configure around it or upgrade the package |
| `Insufficient access rights on cross-reference id` | Deploying user lacks access to a referenced record (e.g., record type) | Use an integration user with Modify All Data / appropriate perms |
| `The package is not valid` / `Unknown user permission` | Profile/permset contains a permission not available in target (edition/feature) | Remove or feature-gate the permission |
| `Apex compile failure` | Missing dependency or API version mismatch | Add dependency; check `sourceApiVersion` |
</details>

<details>
<summary><strong>3.2 Test failures that look like deploy failures</strong></summary>

| Symptom | Cause | Fix |
|---|---|---|
| Passes in Dev, fails in QA/UAT | Test reads existing org data (`LIMIT 1`) or relies on a record type/profile present only in Dev | Tests create their own data; no org-data assumptions |
| `Too many SOQL queries: 101` inside a test | Handler not bulkified; test inserts 200 records | Bulkify; query once |
| `UNABLE_TO_LOCK_ROW` in tests | Parallel DML on same rows; or `SeeAllData` | Avoid `SeeAllData`; isolate data |
| Coverage below 75% | New Apex not covered | Add tests; coverage is org-wide but new code must be covered by the tests you run |
| `Test execution time exceeded` | Slow tests, callouts in tests | Mock callouts (`HttpCalloutMock`), reduce data |
| Managed package test failures | `RunAllTestsInOrg` runs package tests | Use `RunLocalTests` for release validation |

> **Rule:** production rejects the deploy if tests fail, even if the metadata is valid. Test design is part of release engineering.
</details>

<details>
<summary><strong>3.3 "Green deploy, broken feature" (not an error — a constraint)</strong></summary>

| Symptom after a green deploy | Missing piece | Where to fix |
|---|---|---|
| Users can't create a new record type | Record type not assigned to profile/permission set; or no page layout assignment | Setup > Object > Record Types / Page Layouts; Permission Sets |
| Users see an old layout | Layout assignment not deployed; or Lightning page not activated | Setup > Object > Page Layouts; Lightning App Builder activation |
| Flow change has no effect | New Flow version deployed as **Draft**, not Active | Setup > Flows > version → Activate |
| Permission set has no effect | Not assigned to users | Setup > Permission Sets > Manage Assignments |
| Custom metadata record missing | Data not deployed (metadata type ≠ records) | Deploy custom metadata records; or data tool |
| Callout 401 | Named/External Credential principal not configured in target | Setup > Named Credentials / External Credentials |
| Validation rule not firing | Rule inactive, or field-level security hides the field | Setup > Object > Validation Rules; FLS |
| Record page shows old components | FlexiPage not activated for app/record type | Lightning App Builder > Activation |

**Release checklist:** for every deployed component, name the **assignment/activation** step. If you cannot, you have not finished the change.
</details>

---

## 4. Profiles and permission sets (the #1 conflict source)

<details>
<summary><strong>4.1 Why profiles conflict</strong></summary>

A profile XML is a grab-bag: user permissions, object permissions, field permissions, layout assignments, record-type visibility, tab visibility, app visibility, login hours, login IP ranges, and more. Two branches editing the same profile produce a conflict in a file that is thousands of lines long and not human-reviewable at a glance. A bad merge can **grant or revoke access nobody reviewed**.

**What the role expects you to say:** *"We stop putting story access in profiles. We ship a permission set per feature/persona and deploy that. Profiles are only touched for profile-only settings, with a second reviewer reading the permission diff."*
</details>

<details>
<summary><strong>4.2 The permission-set strategy</strong></summary>

| Pattern | Use |
|---|---|
| One permission set per **feature** | Small, reviewable, deployable with the story |
| One permission set per **persona/job function** | Bundled into a **permission set group** |
| Permission set **group** | Assigns a job function's set of sets; avoids a new monolith |
| Muting permission set | Temporarily revoke within a group |
| Profile | Only for profile-only settings (layout assignment historically, login hours/IP, default app) |

**Anti-pattern:** one giant `CB_Admin` permission set that every story edits → you recreated the profile merge problem.
</details>

<details>
<summary><strong>4.3 Deploying profiles safely when you must</strong></summary>

- Deploy a **thin delta**, not the whole profile, where the tool supports profile decomposition (Gearset does; Copado/AutoRABIT have equivalents).
- **Diff the permission changes** and have a second person read them.
- Never hand-merge a 10,000-line profile XML.
- Watch for **org-specific values** in profiles (user licence–specific permissions) that should not travel.
- Deploy profiles **after** objects/fields/classes/flows they reference.
- Expect **timeouts** on large profiles; split or use a tool with profile-aware deploys.
</details>

<details>
<summary><strong>4.4 Permission set vs profile — the comparison table</strong></summary>

| Aspect | Profile | Permission Set |
|---|---|---|
| Required per user | Exactly one | Zero or more |
| Can grant access | Yes | Yes (additive only) |
| Can deny/remove access | Yes (relative to baseline) | No (use muting sets in a group) |
| Merge-friendliness | Poor (huge, noisy) | Better if small |
| Deploy size/time | Large | Smaller |
| Typical role in a modern org | Baseline only | Feature/persona access |
| Record-level sharing | No (roles/OWD/rules do that) | No |
| Layout/app/tab assignment | Yes (historically) | Yes for many settings |

**Security model reminder:** record access = OWD + role hierarchy + sharing rules + manual sharing + teams + territory (if enabled) + Apex sharing. Profiles/permsets control **object and field** access, not row access.
</details>

---

## 5. Record types, page layouts, and Lightning pages

<details>
<summary><strong>5.1 The minimum viable record-type payload</strong></summary>

Deploy in one payload (or in this order):

1. Object + fields used by the record type's picklists/business process.
2. Business process (e.g., Support Process, Sales Process) and picklist values.
3. **Record Type** itself.
4. **Page Layout** for that record type.
5. **Page Layout Assignment** (profile + record type).
6. **Permission Set / Profile** granting record-type visibility.
7. **Lightning Record Page** (if used) + **activation** for app/record type.
8. **Compact Layout** assignment (if used).

Miss 5 or 6 → "deploy succeeded, users can't use it."
Miss 7 → "Lightning users see the classic layout."
</details>

<details>
<summary><strong>5.2 Classic layout vs Lightning record page (FlexiPage)</strong></summary>

- **Page Layout** = classic layout; still used for some components and for Classic, and for layout assignment.
- **FlexiPage / Lightning Record Page** = the Lightning Experience page built in Lightning App Builder. It must be **activated** for specific apps/record types/profiles.
- Testers say "the page is wrong" when the **FlexiPage was never activated**, not when the layout failed.

**Check:** Setup > Lightning App Builder > open page > Activation, or Object Manager > [Object] > Lightning Record Pages.
</details>

<details>
<summary><strong>5.3 Record type visibility vs layout assignment (two different things)</strong></summary>

- **Record type visibility** (profile/permset): can the user *see/select* this record type?
- **Page layout assignment** (profile + record type): which layout renders for that user/record type?

Both are needed. A user can see the type but get the wrong layout, or get the right layout but not see the type.
</details>

---

## 6. Flows and Apex dependencies

<details>
<summary><strong>6.1 Flow-specific constraints</strong></summary>

- **XML does not merge.** Two developers editing the same flow lose one side.
- **Version semantics:** a flow has versions; only one is **Active**. A deploy can create a new version that is Draft. Verify activation.
- **Flow Definition** points to the active version; deploying the flow and the definition matters.
- **Subflows** must be deployed with (or before) the parent.
- **Invocable Apex** referenced by a flow must exist.
- **Custom metadata/settings** referenced must exist or the flow faults at runtime.
- **Before-save vs after-save:** before-save flows are faster and avoid extra DML; after-save flows can update other records. A flow built as after-save that should be before-save will time out under volume.

**Mitigation:** one owner per flow per release, or split into subflows.
</details>

<details>
<summary><strong>6.2 Apex dependency ordering</strong></summary>

- Deploy a class with every class/interface it references (or ensure they exist in target).
- Deploy the **test class** in the same payload (or it must already exist and be valid).
- Inner classes, enums, and `SObjectType` references are dependencies too.
- Trigger + handler + service + selector + test is the usual bundle.
- API version must be compatible with the target.

**Failure signature:** `Method does not exist` or `Variable does not exist` at compile time in the target → missing member, not a syntax error in your file.
</details>

<details>
<summary><strong>6.3 Order of execution (why before/after matters to the release)</strong></summary>

A simplified order:

1. Loads the original record.
2. System validation (required fields, field format).
3. **Before-save Flows / before triggers** (can modify the same record without a second DML).
4. Custom validation rules.
5. Duplicate rules.
6. **After-save Flows / after triggers** (can modify other records; changes cause another save cycle).
7. Assignment rules, auto-response, workflow rules.
8. Escalation rules.
9. Roll-up summaries recalculate.
10. Sharing recalculation.
11. Commit.

**Release-engineering angle:** a before-trigger cannot see a roll-up that recalculates later. A change that "worked in Dev" can fail under volume if it creates recursive save cycles.
</details>

---

## 7. Destructive changes (deletes)

<details>
<summary><strong>7.1 How deletes actually work</strong></summary>

- A component **not present** in your payload is **not** deleted. Deletion requires explicit **destructive changes** metadata (`destructiveChanges.xml` / `destructiveChangesPre.xml` + `package.xml`).
- **Pre-destructive** deletes before the deploy (use when a rename would collide).
- **Post-destructive** deletes after the deploy (the common case).
- Deletes are **not** undone by a Git revert. Rollback means recreating metadata; **records on a deleted custom object are gone**.
- Deleting a field deletes its data (after the recycle bin / if not restored).
- Deleting a custom object can cascade to children (master-detail).

**Rule:** a destructive change is a separate, reviewed, ticketed deploy with a data backup plan. Never bundle a delete into a "normal" release without calling it out.
</details>

<details>
<summary><strong>7.2 Delete checklist</strong></summary>

- [ ] Confirm nothing references the component (Apex, Flow, layout, report, integration, validation rule).
- [ ] Confirm data can be lost (or is backed up).
- [ ] Confirm the delete is post- or pre-destructive, and why.
- [ ] Confirm the change ticket names the data impact.
- [ ] Confirm rollback plan is "recreate metadata + restore data," not "git revert."
- [ ] Deploy and verify the component is actually gone.
- [ ] Remove references from Git so the next full retrieve does not resurrect it.
</details>

---

## 8. Dependency analysis tooling

<details>
<summary><strong>8.1 What tools do for you (and what they miss)</strong></summary>

| Tool | Dependency help | Limitation |
|---|---|---|
| **Salesforce CLI** | `sf project deploy start` resolves many intra-payload deps; error messages name the missing component | No visual graph; you must read errors |
| **Gearset** | Dependency analysis, "missing dependency" suggestions, Flow Navigator, profile decomposition | Can still miss runtime/assignment deps |
| **Copado** | Deployment dependency tracking, commit/back-promotion | Depends on metadata being committed correctly |
| **AutoRABIT ARM** | Compare + dependency resolution, pre/post destructive | Same class of tool |
| **DevOps Center** | Git + work items + promotion; surfaces conflicts | GitHub-first; unsupported metadata types |
| **SFDX plugins** (e.g., dependency/community plugins) | Generate a dependency tree | Plugin quality varies; verify output |

**What none of them fix:** assignment/activation (layout assignment, record type visibility, FlexiPage activation, permission set assignment). That is your post-deploy checklist.
</details>

<details>
<summary><strong>8.2 A practical pre-deploy dependency audit</strong></summary>

1. List every component in the payload (`sf project deploy preview` / tool diff).
2. For each, list its references (object, fields, classes, flows, metadata types, credentials).
3. Confirm each reference is **in the payload or already in the target**.
4. Confirm each component's **assignment/activation** step is in the runbook.
5. Confirm **destructive changes** are explicit and reviewed.
6. Confirm **test class coverage** for any Apex.
7. Confirm **API version** compatibility.
8. Confirm **permission diff** reviewed by a second person.
</details>

---

## 9. Deployment constraints by strategy

<details>
<summary><strong>9.1 Change sets</strong></summary>

**Constraints**

- Only between related orgs (sandbox ↔ production, or same-hub sandboxes).
- Component selection is manual; easy to miss dependencies.
- No reviewable diff; no branch; no tag; no rollback.
- Profile XML you cannot merge.
- Inbound change set must be validated and deployed; size limits apply.

**Verdict for this role:** explain it, then retire it. Use CLI or a Metadata-API tool with Git in front.
</details>

<details>
<summary><strong>9.2 Unpackaged metadata from Git (the default for a large bank org)</strong></summary>

**Constraints**

- The whole repo can become one unreviewable tree.
- Deploy order is on you (or your tool).
- Delete tracking needs destructive manifests.
- No versioning/upgrade semantics.

**Verdict:** still the right default for a large existing org; add packages at real boundaries later.
</details>

<details>
<summary><strong>9.3 Unlocked packages</strong></summary>

**Constraints**

- Requires a Dev Hub.
- Versioned; upgradeable; dependency list.
- Org-dependent unlocked packages are easier to adopt but cannot install elsewhere without the same unpackaged deps.
- Not a silver bullet for "package the entire org."

**Verdict:** use at **real module boundaries** (a credit-application module, not "all of Sales Cloud").
</details>

<details>
<summary><strong>9.4 Managed packages</strong></summary>

**Constraints**

- You upgrade them; you do not edit their metadata.
- `CANNOT_MODIFY_MANAGED_OBJECT` if you try.
- Package upgrades can change behaviour; test before production.
- Namespace prefix changes names.

**Verdict:** treat upgrades as releases with their own validation and rollback (previous version install, if supported).
</details>

---

## 10. Interview drills

1. **Draw the dependency chain for a new record type.** Object → fields → business process/picklists → record type → layout → layout assignment → record type visibility → (FlexiPage + activation) → permission set.
2. **Why did the record type deploy "succeed" but users can't use it?** Missing record type visibility on profile/permset and/or layout assignment.
3. **Why do profiles conflict?** They are huge, noisy, and contain access; two edits collide and a bad merge changes permissions.
4. **How do you delete a field safely?** Explicit destructive change, second review, data backup, verify references gone, ticket, recreate-to-rollback plan.
5. **How do you deploy Apex with dependencies?** Class + dependencies + test in one payload; read compile errors as missing-member, not syntax.
6. **What do tools not fix?** Assignments/activation and post-deploy verification.
7. **What is the order of execution and why does it matter?** Before-save vs after-save; roll-ups recalc later; recursion risk under volume.
8. **How do you handle a rename?** New component + migrate references + destructive delete + data migration; it is multi-deploy.
9. **How do you prove a deploy is safe?** Validation against prod-like org, named tests, dependency audit, permission diff review, assignment checklist, rollback tag.
10. **What breaks first at scale?** Missing dependencies and unassigned metadata, then runtime limits (see `01`).

---

**Next:** `03-devops-tools-ui-walkthroughs.md` — where these actions live in Gearset, Copado, AutoRABIT, and DevOps Center.

<!-- ===== end: 02-metadata-dependencies-and-deployment-constraints.md ===== -->


---

<!-- ===== begin: 03-devops-tools-ui-walkthroughs.md ===== -->

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

<!-- ===== end: 03-devops-tools-ui-walkthroughs.md ===== -->


---

<!-- ===== begin: 04-cicd-github-salesforce.md ===== -->

# 04 — CI/CD on GitHub + Salesforce (Best-Practice Pipeline)

> **Scope:** "Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows" + "Experience building or managing CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab)" + "branching strategies" + "automated testing and validation" + "runbooks, rollback procedures."
> **Assumption:** GitHub Actions as the reference implementation. §10 maps the same stages to Azure DevOps and GitLab.

---

## 1. The pipeline in one picture

```text
feature/<ticket> ──PR──▶ release/<date> ──▶ main (prod)
      │                     │                  │
   validate.yml         deploy-uat.yml     release-prod.yml
   (dry-run + tests)    (real deploy)      (validate → approval → quick deploy)
      │                     │                  │
   CI sandbox            QA / UAT           Pre-Prod → Prod
```

**Two rules that do most of the work:**

1. **Nothing reaches a protected branch without a green validation.**
2. **Production is deployed from `main` only, inside a change window, by a pipeline with an approval gate — never by a human clicking in Setup.**

---

## 2. Branch → environment mapping

| Branch | Purpose | Deploys to | Trigger |
|---|---|---|---|
| `feature/<ticket>-slug` | Short-lived work | CI sandbox (validate only) | PR open/sync |
| `release/<YYYY-MM-DD>` | Release candidate | QA → UAT | Merge / manual |
| `main` | Mirror of production | Pre-Prod validate → Prod | Merge / manual with approval |
| `hotfix/<ticket>` | Prod defect | Prod (same gates, smaller payload) | Cut from `main`, manual with approval |

**Rules**

- Feature branches live **days**, not weeks — Salesforce XML does not merge well.
- A hotfix is cut from **`main`** (what production runs), then merged back to `main` and any open release branch.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the **change ticket ID**. That is the audit trail.

---

## 3. Authentication: the part that gets audited

<details>
<summary><strong>3.1 JWT bearer flow (recommended)</strong></summary>

A **Connected App** with a digital certificate, plus a dedicated **integration user**, plus JWT. The private key lives in GitHub Secrets; the pipeline authenticates without a password and without a browser.

**Setup once**

1. Create a **Connected App** (Setup > App Manager > New Connected App).
2. Enable OAuth; select **Use digital signatures**; upload the certificate.
3. Scopes: at minimum `api`, `refresh_token` (and `web` if needed).
4. Create/assign a dedicated **integration user** with a permission set that allows metadata deploy + Apex test. Not a human admin.
5. Pre-authorize the connected app for the integration user (or use the JWT `sub`).
6. Store the **consumer key**, **username**, **instance URL**, and **private key** as GitHub secrets/environment secrets.

**Login**

```bash
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file server.key \
  --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" \
  --alias ci
```

**Why JWT over username/password:** no stored password, no MFA bypass, revocable certificate, attributable to one integration identity.
</details>

<details>
<summary><strong>3.2 SFDX auth URL (simpler, still acceptable)</strong></summary>

```bash
echo "$SFDX_AUTH_URL" | sf org login sfdx-url --sfdx-url-stdin --alias ci
```

- Generated from an already-authenticated CLI session: `sf org display --verbose --json` → `sfdxAuthUrl`.
- Treat the auth URL as a **secret** (it contains a refresh token).
- Rotate it; scope it to a dedicated integration user.
- Prefer JWT for long-lived CI; auth URLs are convenient for short-lived or dev-only pipelines.
</details>

<details>
<summary><strong>3.3 Never do these</strong></summary>

- `sf org login web` on a runner (interactive, non-deterministic).
- Store a password, security token, or private key in the repo.
- Use a human admin's credentials.
- Give the integration user **System Administrator** when a scoped permission set suffices.
- Log the auth URL or token (`set -x` with secrets).
</details>

<details>
<summary><strong>3.4 Secrets layout</strong></summary>

Use **GitHub Environments** so production secrets are only available to jobs that target the production environment (and can require reviewers).

| Secret | Scope | Contents |
|---|---|---|
| `SF_CONSUMER_KEY` | repo/env | Connected App consumer key |
| `SF_USERNAME` | repo/env | Integration user username |
| `SF_INSTANCE_URL` | repo/env | `https://login.salesforce.com` or test.salesforce.com |
| `SF_JWT_KEY` | repo/env | Private key PEM |
| `SF_CI_ORG_ALIAS` | repo | Alias/username for the CI sandbox |
| `SF_UAT_ORG_ALIAS` | uat env | UAT alias |
| `SF_PROD_ORG_ALIAS` | production env | Prod alias |

> For sandboxes, the instance URL is typically `https://test.salesforce.com` for login, and the org-specific My Domain URL after auth.
</details>

---

## 4. Delta deploys (why and how)

<details>
<summary><strong>4.1 Why delta</strong></summary>

Full-repo deploys are slow, consume API limits, and can accidentally deploy unrelated in-flight work. A **delta** deploy sends only the components changed between two Git refs.

- Faster validations → more PRs validated per day.
- Fewer API calls → protects the 24 h allocation.
- Smaller blast radius → easier rollback reasoning.
- Better for monorepos and long histories.

Trade-off: delta tools can miss dependencies. Always deploy the generated `package.xml` **and** let the platform/tool resolve dependencies, then read failures.
</details>

<details>
<summary><strong>4.2 `sfdx-git-delta` (the common plugin)</strong></summary>

```bash
sf plugins install sfdx-git-delta

mkdir -p delta
sf sgd source delta \
  --from "origin/${{ github.base_ref }}" \
  --to "HEAD" \
  --output-dir delta \
  --generate-delta
```

Produces:

- `delta/package/package.xml`
- `delta/` source tree
- `delta/destructiveChanges/destructiveChanges.xml` (post-destructive)

Deploy the delta:

```bash
sf project deploy validate \
  --source-dir delta \
  --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
  --target-org ci \
  --test-level RunLocalTests \
  --wait 60
```

> `--post-destructive-changes` should be used only when the file exists. In CI, guard it.

**Flag drift warning:** plugin and CLI flags change between majors. Run `sf sgd source delta --help` and `sf project deploy validate --help` in the pipeline image before publishing a command.
</details>

---

## 5. Workflow: validate on every PR

`.github/workflows/validate.yml`

```yaml
name: Salesforce Validate

on:
  pull_request:
    branches: [main, 'release/**']
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: validate-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - name: Checkout (full history for delta)
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Salesforce CLI
        run: |
          npm install --global @salesforce/cli
          sf --version

      - name: Install delta plugin
        run: |
          echo y | sf plugins install sfdx-git-delta

      - name: Write JWT key
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key

      - name: Authenticate to CI org (JWT)
        run: |
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias ci
          sf org display --target-org ci

      - name: Build delta package
        run: |
          mkdir -p delta
          sf sgd source delta \
            --from "origin/${{ github.base_ref }}" \
            --to "HEAD" \
            --output-dir delta \
            --generate-delta

      - name: Validate delta (dry run, run local tests)
        run: |
          if [ ! -f delta/package/package.xml ]; then
            echo "No metadata changes; skipping validation."
            exit 0
          fi
          DESTRUCTIVE=""
          if [ -f delta/destructiveChanges/destructiveChanges.xml ]; then
            DESTRUCTIVE="--post-destructive-changes delta/destructiveChanges/destructiveChanges.xml"
          fi
          sf project deploy validate \
            --source-dir delta \
            $DESTRUCTIVE \
            --target-org ci \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Publish summary
        if: always()
        run: |
          echo "## Salesforce validation" >> "$GITHUB_STEP_SUMMARY"
          echo "Ref: \`${{ github.head_ref }}\` → \`${{ github.base_ref }}\`" >> "$GITHUB_STEP_SUMMARY"
          echo "Result: see the *Validate delta* step log." >> "$GITHUB_STEP_SUMMARY"

      - name: Cleanup key
        if: always()
        run: rm -f server.key
```

**Design notes**

- `fetch-depth: 0` is required for a correct merge-base delta.
- `cancel-in-progress: true` saves API budget on rapid pushes.
- `RunLocalTests` (not `RunAllTestsInOrg`) avoids running managed-package tests.
- The key is deleted even on failure.
- The PR comment/summary is the human-readable evidence link.

---

## 6. Workflow: deploy to UAT on merge to the release branch

`.github/workflows/deploy-uat.yml`

```yaml
name: Deploy to UAT

on:
  push:
    branches: ['release/**']

permissions:
  contents: read

concurrency:
  group: deploy-uat-${{ github.ref }}
  cancel-in-progress: false   # never cancel a deploy mid-flight

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    environment:
      name: uat
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI + delta
        run: |
          npm install --global @salesforce/cli
          echo y | sf plugins install sfdx-git-delta

      - name: Auth to UAT
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias uat

      - name: Build delta from previous commit
        run: |
          mkdir -p delta
          sf sgd source delta \
            --from "HEAD^" \
            --to "HEAD" \
            --output-dir delta \
            --generate-delta

      - name: Deploy to UAT
        run: |
          DESTRUCTIVE=""
          if [ -f delta/destructiveChanges/destructiveChanges.xml ]; then
            DESTRUCTIVE="--post-destructive-changes delta/destructiveChanges/destructiveChanges.xml"
          fi
          sf project deploy start \
            --source-dir delta \
            $DESTRUCTIVE \
            --target-org uat \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Cleanup
        if: always()
        run: rm -f server.key
```

> For UAT you often want a **full release-branch payload**, not a single-commit delta, because UAT must match the release candidate. Use `--source-dir force-app` or the release manifest in that case. Delta is right for feature/PR validation; the release candidate should be deployed as a coherent unit.

---

## 7. Workflow: production release with approval + quick deploy

`.github/workflows/release-prod.yml`

```yaml
name: Release to Production

on:
  workflow_dispatch:
    inputs:
      release_tag:
        description: 'Tag to deploy (e.g. release-2026-11-27)'
        required: true
      change_ticket:
        description: 'Change ticket ID'
        required: true

permissions:
  contents: read

concurrency:
  group: deploy-prod
  cancel-in-progress: false

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    environment:
      name: preprod
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.release_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Pre-Prod
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias preprod

      - name: Validate release against Pre-Prod
        id: validate
        run: |
          sf project deploy validate \
            --source-dir force-app \
            --target-org preprod \
            --test-level RunLocalTests \
            --wait 120 \
            --json > validate.json
          JOB_ID=$(jq -r '.result.id' validate.json)
          echo "job_id=$JOB_ID" >> "$GITHUB_OUTPUT"
          echo "Validated. Job: $JOB_ID"

      - name: Upload validation evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-${{ inputs.change_ticket }}
          path: |
            validate.json
            server.key
          retention-days: 30

      - name: Cleanup key
        if: always()
        run: rm -f server.key

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 60
    environment:
      name: production        # configure required reviewers in repo settings
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.release_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Production
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod

      - name: Quick deploy the validated job
        run: |
          sf project deploy quick \
            --job-id "${{ needs.validate.outputs.job_id }}" \
            --target-org prod \
            --wait 60 \
            --verbose

      - name: Create release tag
        run: |
          git tag -a "deployed-$(date -u +%Y%m%dT%H%M%SZ)" -m "Prod deploy ${{ inputs.change_ticket }}"
          git push origin --tags

      - name: Cleanup key
        if: always()
        run: rm -f server.key
```

**Critical details**

- The **quick deploy is only honest if nothing relevant changed** in Pre-Prod/Prod since validation. If a hotfix landed, re-validate.
- Quick Deploy is valid for **10 days**; the release calendar must fit inside that.
- The `production` GitHub Environment must have **required reviewers** configured in Settings → Environments. That is the segregation-of-duties control.
- `needs.validate.outputs.job_id` requires `id: validate` and the `job_id` output — shown above.
- Tag **after** a successful deploy; the tag is the rollback target.
- If `sf project deploy quick` is unavailable in your CLI major, use `sf project deploy resume --job-id` or re-validate + deploy; run `--help`.

---

## 8. Gates and quality checks

<details>
<summary><strong>8.1 The gate table</strong></summary>

| Gate | Where | Blocks |
|---|---|---|
| Compile/validate | PR workflow | Merge |
| Apex tests (`RunLocalTests`) | PR + release validation | Merge / deploy |
| 75% coverage | Platform-enforced in prod | Prod deploy |
| Static analysis (PMD/CodeScan) | PR workflow (optional) | Merge (if configured) |
| Permission diff review | PR review + tool diff | Merge |
| Required reviewers | GitHub Environment `production` | Prod deploy |
| Change ticket present | Workflow input validation | Prod deploy |
| Rollback tag exists | Pre-release check | Prod deploy |
| Concurrency lock | `concurrency` group | Parallel prod deploys |
</details>

<details>
<summary><strong>8.2 Optional static analysis (PMD)</strong></summary>

```yaml
- name: Install PMD
  run: |
    curl -sSLo pmd.zip https://github.com/pmd/pmd/releases/latest/download/pmd-dist.zip
    unzip -q pmd.zip
- name: Run PMD on Apex
  run: |
    ./pmd-bin-*/bin/run.sh pmd \
      -d force-app \
      -R rulesets/apex/quickstart.xml \
      -f text
```

Use it to catch SOQL/DML-in-loop and sharing violations **before** review. Do not make it the only gate; it is not a substitute for tests.
</details>

<details>
<summary><strong>8.3 Coverage parsing</strong></summary>

```bash
sf apex run test --target-org ci --test-level RunLocalTests \
  --code-coverage --result-format json --wait 60 > test.json

jq '[.result.coverage.coverage[] | {name: .name, pct: .coveredPercent}] | sort_by(.pct) | .[0:10]' test.json
```

Fail the job if org-wide coverage drops below a threshold (e.g., 80% internal bar, above the 75% platform gate).
</details>

---

## 9. Rollback runbook

<details>
<summary><strong>9.1 Rollback workflow</strong></summary>

`.github/workflows/rollback.yml`

```yaml
name: Rollback Production

on:
  workflow_dispatch:
    inputs:
      target_tag:
        description: 'Last known-good tag (e.g. release-2026-11-20)'
        required: true
      incident_ticket:
        description: 'Incident/change ticket'
        required: true

permissions:
  contents: read

concurrency:
  group: deploy-prod
  cancel-in-progress: false

jobs:
  rollback:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: ${{ inputs.target_tag }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install CLI
        run: npm install --global @salesforce/cli

      - name: Auth to Production
        run: |
          printf '%s' "${{ secrets.SF_JWT_KEY }}" > server.key
          sf org login jwt \
            --client-id "${{ secrets.SF_CONSUMER_KEY }}" \
            --jwt-key-file server.key \
            --username "${{ secrets.SF_USERNAME }}" \
            --instance-url "${{ secrets.SF_INSTANCE_URL }}" \
            --alias prod

      - name: Validate the rollback payload first
        run: |
          sf project deploy validate \
            --source-dir force-app \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 60

      - name: Deploy the last known-good tag
        run: |
          sf project deploy start \
            --source-dir force-app \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 60 \
            --verbose

      - name: Cleanup
        if: always()
        run: rm -f server.key
```

</details>

<details>
<summary><strong>9.2 What rollback cannot do</strong></summary>

- **Undo data changes.** Metadata rollback ≠ data rollback. Restore data from a backup (Vault/Gearset/own tooling) or run a reviewed reverse script.
- **Undelete records** on a destructively deleted object.
- **Rescue a deleted field's data** after the recycle bin window.
- **Fix a managed-package upgrade** unless the vendor supports version rollback.

**The rule:** if you do not have a tag from the last good production deploy, you do not have a rollback. Fix that before the next release.
</details>

---

## 10. Same pipeline, other tools

<details>
<summary><strong>10.1 Azure DevOps</strong></summary>

- **Repos** for Git; **Pipelines** (YAML) for CI/CD.
- **Environments** + **Approvals and checks** replace GitHub Environments for SoD.
- **Variable groups** + Azure Key Vault replace GitHub Secrets.
- Stages: `Validate`, `DeployQA`, `DeployUAT`, `DeployProd` with `dependsOn`.
- Same `sf` CLI commands; same delta plugin.
</details>

<details>
<summary><strong>10.2 GitLab CI</strong></summary>

- `.gitlab-ci.yml` with `stages: [validate, deploy-qa, deploy-uat, deploy-prod]`.
- **Protected environments** + **Deploy approvals** for SoD.
- **CI/CD variables** (masked/protected) for secrets; or external secret manager.
- Same `sf` CLI commands; cache the CLI and plugins.
</details>

<details>
<summary><strong>10.3 Jenkins (legacy but common in banks)</strong></summary>

- Pipeline as code (`Jenkinsfile`), credentials binding, agents.
- Same `sf` CLI + delta; the hard part is secrets and agent hygiene.
- Common in regulated enterprises; document it even if you prefer GitHub Actions.
</details>

---

## 11. Anti-patterns (each one is an interview red flag)

| Anti-pattern | Why it fails |
|---|---|
| `sf org login web` in CI | Interactive, brittle, no audit identity |
| Password/security token in repo | Secret leak; MFA incompatibility |
| Deploying from a feature branch to prod | Bypasses release branch + review |
| `NoTestRun` in prod with Apex | Platform rejects; or ships untested |
| Full-repo deploy on every PR | API exhaustion; slow; deploys unrelated work |
| No `fetch-depth: 0` | Delta is wrong or empty |
| Cancel a deploy mid-flight | Partial state; inconsistent org |
| No concurrency lock | Two prod deploys race |
| No rollback tag | No rollback |
| Human clicks Setup in prod | Drift; no audit trail |
| Pipeline uses a human admin identity | No SoD; credential risk |
| Green deploy treated as "done" | Assignments/activation missed |

---

## 12. Runbook template (fill for every prod promotion)

```text
Change ticket:
Release tag:
Payload (source dir or manifest):
Source branch / commit:
Validation org / deploy id / time:
Tests run and coverage:
Prod deploy id / time:
Approver (not the author):
Post-deploy steps (assignments/activation/flags):
Rollback tag:
Rollback owner:
How we will know it worked (one query, one screen, one test):
Data changes (if any) and reverse plan:
```

---

## 13. Interview drills

1. **Walk a change to prod.** Feature branch → PR → validate (delta + tests) → merge to release → UAT deploy → Pre-Prod validate → approval → quick deploy → tag → ticket updated with both deploy IDs.
2. **Why delta deploys?** Speed, API budget, smaller blast radius; trade-off is dependency resolution.
3. **How does CI authenticate?** JWT via connected app + certificate + dedicated integration user; secrets in GitHub Environments.
4. **How do you enforce segregation of duties?** Required reviewers on the `production` environment; integration user deploys, a human approves; different identities.
5. **What is quick deploy and when is it invalid?** Applies a prior successful validation within 10 days; invalid if the payload or target changed.
6. **How do you roll back?** Redeploy the last known-good tag after validating; data restore is separate.
7. **What stops a bad profile merge?** Permission sets per feature, thin profile deltas, second reviewer reading the permission diff.
8. **How do you keep it portable across CI vendors?** The pipeline is just `sf` CLI + Git; the CI tool is a runner and an approval mechanism.
9. **What is your evidence pack?** Ticket, PR, reviewer, validation ID, test/coverage, prod deploy ID, approver, tag, post-deploy verification, rollback tag.

---

**Next:** `05-jd-term-by-term.md` — every requisition line decoded, with the configuration/setting variations behind each term.

<!-- ===== end: 04-cicd-github-salesforce.md ===== -->


---

<!-- ===== begin: 05-jd-term-by-term.md ===== -->

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

<!-- ===== end: 05-jd-term-by-term.md ===== -->


---

<!-- ===== begin: 06-certifications-and-curriculum.md ===== -->

# 06 — Salesforce Certifications & Curriculum Research

> **Scope:** the JD line "Salesforce certifications (PD1, Advanced Admin, DevOps related certs)" plus the round-2 requirement to research the **curriculum** behind each.
> **Important:** exact exam domain weights change with each release. This file describes the **domains and study path**, and tells you where to confirm the current weightings. Do not memorise percentages from a blog.

---

## 1. What the JD actually names

| JD phrase | Current Salesforce credential | Notes |
|---|---|---|
| **PD1** | **Salesforce Certified Platform Developer I** | Exam code `Plat-Dev-201` |
| **Advanced Admin** | **Salesforce Certified Platform Administrator II** | Formerly "Advanced Administrator"; exam code `Plat-Admn-301`. Prerequisite: Platform Administrator |
| **DevOps related certs** | **Salesforce Certified Platform Development Lifecycle and Deployment Architect** | Exam code `Plat-Arch-202`; this is the closest official "DevOps" credential |

There is **no** official certification literally called "Salesforce DevOps Engineer." When an interviewer says "DevOps cert," they usually mean the **Development Lifecycle and Deployment Architect**, or a **vendor** certification (Copado/Gearset/AutoRABIT). Say this precisely — it signals you know the credential landscape.

> Credential names were modernised: "Salesforce Certified Administrator" → **Salesforce Certified Platform Administrator**; "Advanced Administrator" → **Platform Administrator II**; "Development Lifecycle and Deployment Architect" → **Platform Development Lifecycle and Deployment Architect**. Use both names in conversation.

---

## 2. Credential map

<details>
<summary><strong>2.1 At a glance</strong></summary>

| Credential | Level | Prerequisite | Best for | Maps to JD |
|---|---|---|---|---|
| Platform Administrator | Foundational admin | None | Admin baseline | Indirect |
| Platform Administrator II | Advanced admin | Platform Administrator | Senior admin / release admin | "Advanced Admin" |
| Platform App Builder | Declarative builder | None (Admin recommended) | Designing objects, Flow, security | Strong adjacent |
| Platform Developer I (PD1) | Developer | None | Apex, tests, deploy | "PD1" |
| Platform Developer II (PDII) | Advanced developer | PD1 | Complex Apex, integrations, advanced | Optional depth |
| Platform Development Lifecycle & Deployment Architect | Architect | Recommended: PD1/Admin + experience | Release architecture, environments, governance | "DevOps related" |
| Application Architect / System Architect | Architect track | Multiple prerequisites | Broader architecture | Career ceiling |

</details>

---

## 3. Platform Developer I (PD1)

<details>
<summary><strong>3.1 What it proves</strong></summary>

You can build and deploy custom business logic and interfaces on the Lightning Platform: Apex, SOQL/SOSL, DML, triggers, testing, and the deployment model. It is the **developer baseline** the JD asks for under "Salesforce Platform Developer experience."

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperi>
**New experience / exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201>
**Study trail:** "Study for the Salesforce Platform Developer Certification"
**Prep trailmix:** "Prepare for Your Salesforce Platform Developer Certification"
</details>

<details>
<summary><strong>3.2 Domain areas (study these; verify current weights in the exam guide)</strong></summary>

- **Salesforce fundamentals** — platform architecture, MVC, multi-tenancy, metadata.
- **Data modeling and management** — objects, relationships, schema builder, SOQL/SOSL, DML.
- **Process automation and logic** — Flow, Apex, triggers, order of execution.
- **User interface** — Lightning components (LWC/Aura basics), Visualforce (legacy), Lightning pages.
- **Testing, debugging, and deployment** — test classes, coverage, debug logs, Metadata API, change sets, CLI, packages.
- **Performance** — governor limits, bulkification, async Apex, query selectivity.
- **Integration** — REST/SOAP callouts, Named Credentials, remote sites, Platform Events.

**How it maps to this role:** the "Testing, debugging, and deployment" and "Performance" domains are exactly the release-engineering skills in `01` and `02`. The role does not require you to be the best Apex author, but PD1 fluency lets you **review** Apex for bulkification and dependency risks.
</details>

<details>
<summary><strong>3.3 PD1 study sequence (practical)</strong></summary>

1. **Developer Beginner** trail (objects, Apex basics, SOQL, DML).
2. **Apex Basics & Database** module + **Apex Triggers** module.
3. **Apex Testing** module — write a test class, assert bulk behaviour.
4. **Asynchronous Apex** module — future, Queueable, Batch, Scheduled.
5. **Search Solution Basics** (SOSL) and **SOQL** deep dive.
6. **Lightning Web Components Basics** trail.
7. **Metadata API / deployment** modules + `sf` CLI hands-on.
8. Build the four labs in the published **Labs & Design** page.
9. Take practice exams; review every wrong answer against the official guide.

**Evidence you can show an interviewer:** a repo with an Apex trigger + handler + test class, a delta deploy workflow, and a debug log showing you diagnosed a limit.
</details>

---

## 4. Platform Administrator II (the JD's "Advanced Admin")

<details>
<summary><strong>4.1 What it proves</strong></summary>

Advanced declarative administration: complex security, data management, automation at scale, and environment/change management. It is the **admin-side counterpart** to PD1.

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
**Exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301>
**Prerequisite:** <https://trailhead.salesforce.com/credentials/platformadministrator>
**Prep trailmix:** "Prepare for Your Salesforce Platform Administrator II Certification"
</details>

<details>
<summary><strong>4.2 Domain areas</strong></summary>

- **Security and access** — profiles, permission sets, permission set groups, OWD, role hierarchy, sharing rules, territory, login policies.
- **Object and data model** — objects, fields, relationships, record types, schema design.
- **Process automation** — Flow, approvals, order of execution, fault handling.
- **Data management** — import/export, duplicate management, data quality, validation rules.
- **Analytics / reporting** — reports, dashboards, report types (lighter weight).
- **Environment and change management** — sandboxes, change sets, deployment, DevOps Center.
- **Audit and compliance** — field history, setup audit trail, access reviews.

**How it maps to this role:** the security model and environment-management domains are directly relevant to `02` (profiles/permsets, record types/layouts, security model) and `05` B10/B11.
</details>

<details>
<summary><strong>4.3 Why "Advanced Admin" matters for a DevOps engineer</strong></summary>

Most release conflicts in a bank are **admin metadata**: profiles, permission sets, record types, layouts, sharing. An engineer who only knows Apex will misdiagnose them. Admin II gives you the vocabulary to resolve conflicts and to coach admins toward deployable patterns.
</details>

---

## 5. Platform Development Lifecycle and Deployment Architect (the "DevOps cert")

<details>
<summary><strong>5.1 What it proves</strong></summary>

You can assess environments and requirements and design a **development lifecycle, release, and deployment architecture**: environment strategy, source control, CI/CD, testing, governance, and change management.

**Official page:** <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect>
**Exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-dev-lifecycle---Plat-Arch-202>
**Study trailmix:** "Architect Journey: Development Lifecycle and Deployment"
</details>

<details>
<summary><strong>5.2 Domain areas</strong></summary>

- **Development lifecycle** — org development vs package development vs hybrid; environment strategy; sandbox types.
- **Source control and branching** — Git models, branching strategy, release branching, hotfix.
- **Deployment** — Metadata API, change sets, CLI, packages, tools (Gearset/Copado/AutoRABIT/DevOps Center), destructive changes.
- **Testing** — unit/integration/UAT, test levels, coverage, test data, automation.
- **Environment management** — refresh, seeding, masking, parity, scratch orgs, Dev Hub.
- **Governance** — approvals, segregation of duties, audit, compliance, change management.
- **Architecture and metrics** — release architecture, DORA-style metrics, scaling teams.

**How it maps to this role:** this is essentially the JD. If you can only pursue one "DevOps" credential, pursue this one after PD1/Admin foundations.
</details>

<details>
<summary><strong>5.3 Study path</strong></summary>

1. Complete the **Architect Journey: Development Lifecycle and Deployment** trailmix.
2. Study the three lifecycle models (org-dependent, package-based, hybrid) and when each fits.
3. Build a small end-to-end pipeline (this repo's `04` is a starter).
4. Practise designing an environment ladder for a regulated org (five stages, mask, SoD).
5. Read the **Architect** credential overview: <https://trailhead.salesforce.com/credentials/architectoverview>
6. Review governance/audit case studies (banking analogies are fine).
</details>

---

## 6. Adjacent credentials worth knowing

<details>
<summary><strong>6.1 Platform App Builder</strong></summary>

Declarative app design: objects, relationships, Flow, security, UI. It fills gaps between Admin and Developer and is often the easiest "next" credential for an admin-heavy team.

<https://trailhead.salesforce.com/credentials/platformappbuilder>
</details>

<details>
<summary><strong>6.2 Platform Developer II (PDII)</strong></summary>

Advanced Apex, integration, performance, and lifecycle. Useful if you want to be the person who can fix the Apex, not just deploy it. Requires PD1.

<https://trailhead.salesforce.com/credentials/platformdeveloperii>
</details>

<details>
<summary><strong>6.3 Salesforce Certified Platform Administrator (foundation)</strong></summary>

The prerequisite for Admin II and the vocabulary baseline for everything else.

<https://trailhead.salesforce.com/credentials/platformadministrator>
</details>

---

## 7. Vendor certifications (Copado, Gearset, AutoRABIT)

<details>
<summary><strong>7.1 What they are worth</strong></summary>

Vendor credentials show **tool time**, not platform fundamentals. In an interview they are a plus when the bank already owns the tool; they do not replace PD1 or the Deployment Architect credential.

| Vendor | Credential area | What it signals |
|---|---|---|
| **Copado** | Copado certifications / Copado Fundamentals | Work items, pipelines, promotion, compliance |
| **Gearset** | Gearset DevOps certifications / training | Compare/deploy, pipelines, backup |
| **AutoRABIT** | AutoRABIT certifications | ARM deployments, CodeScan, Vault |

**Advice:** if the job posting names a tool the bank uses, a vendor badge is a cheap differentiator — but only after you can explain the Metadata API underneath it (see `03` §0).
</details>

<details>
<summary><strong>7.2 How to talk about vendor certs without over-claiming</strong></summary>

*"I've used Gearset/Copado/AutoRABIT at the UI level for compare, deploy, and promotion, and I understand they sit on the Metadata API. My platform fundamentals are PD1/Admin-level, so I can debug when the tool's dependency resolution misses something."*
</details>

---

## 8. Curriculum: 8-week plan for this role

<details>
<summary><strong>8.1 Week-by-week</strong></summary>

| Week | Focus | Modules / trails | Repo file |
|---|---|---|---|
| 1 | Platform fundamentals | Admin Beginner; Developer Beginner | crash course |
| 2 | Data model + security | Data Security; Profiles & Permission Sets; Sharing | `05` B10/B11 |
| 3 | Apex + triggers + tests | Apex Basics, Triggers, Apex Testing | `05` B8 |
| 4 | Limits + performance | Asynchronous Apex; governor limits; query selectivity | `01` |
| 5 | Metadata + deployment | Metadata API; `sf` CLI; package.xml; destructive changes | `02` |
| 6 | Git + CI/CD | Git basics; build the `04` pipeline in a dev org | `04` |
| 7 | Environments + governance | Sandboxes; Data Mask; release architecture; SoD | `05` A2/A4/A6 |
| 8 | Cert + mock interview | PD1 or Admin II practice exams; mock drills | `05` §Interview |

</details>

<details>
<summary><strong>8.2 Hands-on evidence to build (better than badges)</strong></summary>

- Two Developer Edition orgs, aliased `dev` and `qa`.
- A Git repo with `force-app`, `sfdx-project.json`, `.forceignore`.
- A permission set deployed via PR validation.
- An Apex trigger + handler + bulk test.
- A delta-deploy GitHub Actions workflow.
- A runbook filled for a fake production release.
- A one-page environment ladder diagram.

</details>

---

## 9. Exam logistics and maintenance (verify current terms)

<details>
<summary><strong>9.1 What to confirm before booking</strong></summary>

- **Exam guide PDF** for the current release — read the domain weights and objectives. Salesforce gates some docs behind login/bot checks; if a URL 403s, use the Trailhead Academy "See New Experience" link or the official exam guide linked from the credential page.
- **Prerequisites** (Admin II requires Platform Administrator).
- **Format** — proctored, multiple-choice/multi-select; some exams include scenario questions.
- **Maintenance** — Salesforce requires completing maintenance modules each release cycle to keep a credential active; check <https://trailhead.salesforce.com/credentials/verification>.
- **Cost and scheduling** — via Trailhead Academy; prices and delivery options vary by region.

**Do not** publish a hard domain-weight table from memory. Link the official guide and describe the domains.
</details>

---

## 10. Recommended study order for requisition 276046

```text
Platform Administrator (foundation)
   → Platform Developer I (PD1)        ← JD explicitly names
   → Platform Administrator II         ← JD's "Advanced Admin"
   → Platform Development Lifecycle
     and Deployment Architect          ← JD's "DevOps related cert"
   → (optional) Platform App Builder / PDII
   → (optional) vendor cert for the bank's tool
```

**Why this order:** the role is release engineering, so you need both sides — developer (deploy/compile/test) and admin (security/config conflicts). The Deployment Architect credential is the synthesis, and it is much easier once PD1 and Admin II vocabulary is in place.

---

## 11. How to present certifications in an interview

<details>
<summary><strong>11.1 The framing</strong></summary>

- Lead with the **credential that matches the JD** (PD1, Admin II, Deployment Architect).
- Say what each one **lets you do**, not just that you passed it.
- Be honest about vendor tools: "UI-level experience, understands the Metadata API underneath."
- Connect each credential to a **release outcome**: fewer failed deploys, safer permission changes, auditable promotions.

**Example:** *"PD1 gives me the Apex/testing/deployment vocabulary to review a change before it ships. Admin II gives me the security-model vocabulary to resolve profile and record-type conflicts. The Deployment Architect track is the one that maps directly to this role — environment strategy, CI/CD, governance."*
</details>

---

## 12. Sources for this file

- Platform Developer I: <https://trailhead.salesforce.com/credentials/platformdeveloperi>
- Platform Administrator II: <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
- Platform Administrator: <https://trailhead.salesforce.com/credentials/platformadministrator>
- Platform App Builder: <https://trailhead.salesforce.com/credentials/platformappbuilder>
- Platform Developer II: <https://trailhead.salesforce.com/credentials/platformdeveloperii>
- Platform Development Lifecycle and Deployment Architect: <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect>
- Architect overview: <https://trailhead.salesforce.com/credentials/architectoverview>
- Certification verification/maintenance: <https://trailhead.salesforce.com/credentials/verification>

> Verified 2026-11-14: credential names and exam codes above. Domain weights intentionally not stated — confirm from the current official exam guide before publishing a table.

<!-- ===== end: 06-certifications-and-curriculum.md ===== -->


---

<!-- ===== begin: sources.md ===== -->

# Sources, Access Notes, and Verification Status

**Compiled:** 2026-11-14
**Rule:** every claim that is time-sensitive or edition-dependent is either linked here or explicitly flagged in the file. If a source was blocked, that is recorded rather than hidden.

---

## 1. Primary sources

| # | Source | Used for | Access |
|---|---|---|---|
| 1 | Scotiabank requisition 276046 — <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> | The job description verbatim; all JD decoding in `05` | OK |
| 2 | Published DevOps track — <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> | Cross-reference, anchors, existing structure to extend | OK |
| 3 | Published crash course — <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/> | Understanding what already exists (so this drop adds depth, not duplication) | OK |

---

## 2. Salesforce platform documentation

| Source | Used for | Access / caveat |
|---|---|---|
| Apex Developer Guide — Execution Governors and Limits | Canonical governor limits in `01` | **403 to automated fetch.** Values written from platform knowledge; verify at <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm> |
| Salesforce App Limits Cheat Sheet | Limit taxonomy in `01` | **403 to automated fetch.** Verify at <https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/> |
| Metadata API Developer Guide | Deploy constraints, destructive changes | **403 to automated fetch.** Verify limits and component ceilings before publishing hard numbers |
| Salesforce Help — Limits Quick Reference | Org capacity limits | **JS-only / returned loading shell.** Verify in-org via Setup > Company Information |
| Salesforce Help — Sandboxes / Sandbox Templates / Data Mask | Environment strategy in `05` A6 | Linked in published track; verify edition gating in your org |
| Salesforce Help — Quick Deploy | 10-day quick-deploy window in `01`/`04` | Verify at <https://help.salesforce.com/s/articleView?id=sf.deploy_quick_deploy.htm&type=5> |
| Salesforce Help — Promote Work Items Through Your Pipeline | DevOps Center promotion in `03` | OK via help article mirror/search |
| DevOps Center Developer Guide | Promotion model, bundles, data model | <https://developer.salesforce.com/docs/platform/devops-center-dev/guide/devops-center-dev-promotions.html> |
| Salesforce Developers Blog — Get Started with DevOps Center | Enabling, hybrid teams, combining work items | <https://developer.salesforce.com/blogs/2022/06/get-up-and-running-with-devops-center-today> |

> **Why the 403s matter:** Salesforce's developer docs and Help site actively block automated fetches. The numbers in `01` are the widely documented canonical values, but a merge agent MUST spot-check the current official pages before publishing exact ceilings (especially component counts, package sizes, and per-24h async caps).

---

## 3. DevOps tool sources

### Gearset

| Source | Used for |
|---|---|
| <https://docs.gearset.com/en/articles/2934192-a-sample-source-driven-development-workflow-for-salesforce> | 7-step workflow (branch → refresh → compare → PR → CI → validation → monitoring) in `03` §2 |
| <https://gearset.com/blog/how-to-deploy-flows-in-salesforce/> | Flow Navigator, comparison filters in `03` §2.4 |
| <https://gearset.com/blog/deploy-lightning-page-in-salesforce/> | Lightning page deploy steps in `03` |
| <https://gearset.com/blog/how-to-deploy-salesforce-reports-and-dashboards/> | Compare/deploy report flow |
| <https://gearset.com/video/scaling-salesforce-development-with-ci-cd> | Manual compare → pipeline maturity |
| <https://gearset.com/salesforce-administrator/> | Capability map (compare/deploy, data, source control, backup) |

**Caveat:** Gearset's Help Center article URLs changed during research (some 404). The paths above resolved via search results; treat UI labels as typical, not guaranteed.

### Copado

| Source | Used for |
|---|---|
| <https://trailhead.salesforce.com/content/learn/modules/salesforce-devops-with-copado/let-innovation-flow-with-continuous-delivery> | Pipeline/promotion concepts |
| <https://www.copado.com/resources/blog/salesforce-ci-cd-best-practices-build-run-test-cddd> | CI/CD best practices |
| <https://docs.essentials.copado.com/en/articles/6935764-best-practices-with-copado-essentials-plus> | Git + CI jobs, back-promotion |
| <https://helpmetest.com/blog/copado-cicd-pipeline-salesforce> | Pipeline connections, branch strategy, quality gates |
| <https://www.copado.com/resources/blog/successful-salesforce-deployment-best-practices-checklist-cddd> | Deploy ordering (objects → Apex → profiles → sharing) |

### AutoRABIT

| Source | Used for |
|---|---|
| <https://knowledgebase.autorabit.com/product-guides/arm/arm-features/deployment/deployment-rollback> | Rollback requires "Take Backup"; deployment history |
| <https://knowledgebase.autorabit.com/product-guides/vault-1/vault-features/backup> | Vault backup capabilities |
| <https://knowledgebase.autorabit.com/product-guides/vault/vault-features/backup/start-the-backup> | Full vs incremental backup steps |
| <https://knowledgebase.autorabit.com/fundamentals/what-we-do> | ARM / CodeScan / Vault / Guard product map |
| <https://www.autorabit.com/> | DevSecOps positioning |

### DevOps Center

| Source | Used for |
|---|---|
| <https://hicglobalsolutions.com/blog/devops-center-setup-and-deployment> | Setup → project → pipeline → work item → promote walkthrough |
| <https://www.salesforceben.com/complete-guide-to-salesforce-devops-center-how-to-get-started/> | Enable, permission sets, bundling stage, promotion |
| <https://salesforcedictionary.com/how-to/devops-center> | Gotchas (GitHub-first, unsupported metadata, conflicts resolved in Git) |
| <https://www.dreaminforce.com/salesforce-devops-center-quick-setup-example> | Promotion flow |
| <https://help.salesforce.com/s/articleView?id=platform.devops_center_work_items_promote.htm&type=5> | Promotion limits/guidance |

---

## 4. CI/CD references

| Source | Used for |
|---|---|
| <https://tech.robotpayment.co.jp/entry/2025/08/28/070000> | PR-triggered `sf project deploy validate`, JWT auth pattern |
| <https://medium.com/@AmritWritesHere/step-by-step-how-to-set-up-ci-cd-for-salesforce-using-git-and-github-actions-60e1851b0e2e> | JWT + changed-file deploy |
| <https://soomjeetsahoo.medium.com/implementing-salesforce-ci-cd-with-github-actions-to-validate-deploy-checks-with-pmd-e7a280e46c71> | `sfdx-git-delta`, PMD, `.gitignore` |
| <https://blog.beyondthecloud.dev/blog/simple-salesforce-cicd> | Scratch org CI, auth URL |
| <https://www.kylecapehart.com/posts/github-actions> | `sf org login sfdx-url`, branch protection |
| <https://1sync.co/blog/build-salesforce-deployment-pipeline-with-github-actions> | Branch→environment pipeline |
| <https://qiita.com/krile136/items/01b891fa6cff69bf55ee> | Full vs delta deploy patterns, revert-on-failure |

**Caveat:** all pipeline YAML in `04` is a **reference implementation**, not a copy of any single article. CLI flags must be verified with `sf <cmd> --help` in the target CLI major before publishing.

---

## 5. Certification sources (verified 2026-11-14)

| Credential | URL | Verified |
|---|---|---|
| Platform Developer I | <https://trailhead.salesforce.com/credentials/platformdeveloperi> | Page loaded; exam code `Plat-Dev-201` |
| Platform Administrator II | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> | Page loaded; prerequisite + exam code `Plat-Admn-301` |
| Platform Administrator | <https://trailhead.salesforce.com/credentials/platformadministrator> | Linked from Admin overview |
| Platform App Builder | <https://trailhead.salesforce.com/credentials/platformappbuilder> | Linked from credential pages |
| Platform Developer II | <https://trailhead.salesforce.com/credentials/platformdeveloperii> | Linked from PD1 page |
| Platform Development Lifecycle and Deployment Architect | <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect> | Page loaded; exam code `Plat-Arch-202` |
| Architect overview | <https://trailhead.salesforce.com/credentials/architectoverview> | Linked from credential pages |
| Verification/maintenance | <https://trailhead.salesforce.com/credentials/verification> | Linked from all pages |

**Not stated:** domain weights. Trailhead credential pages are JS-rendered and do not expose the exam guide outline to fetches; the official exam guide PDF is the authority.

---

## 6. Claims that require a re-check before publishing

| Claim | File | Why |
|---|---|---|
| Exact component-count / package-size deployment ceilings | `01` §6.1 | Salesforce docs blocked; edition-dependent |
| Per-24h async execution caps | `01` §4.5 | Changes by release |
| API request formula and payload sizes | `01` §5 | Edition-dependent; confirm entitlement |
| Sandbox refresh intervals | `05` A2 | Licence-dependent |
| Vendor UI labels and edition gating | `03` | Changes by release |
| `sf`/`sgd` CLI flags | `04` | Drift between CLI majors |
| Certification domain weights | `06` | Must come from current official exam guide |

---

## 7. Deliberate omissions

- **No customer data, org IDs, tokens, or endpoints.**
- **No vendor pricing** — commercial and volatile.
- **No screenshots** — text-only round; a diagram pass is a round-2 task.
- **No invented exam percentages.**

<!-- ===== end: sources.md ===== -->
