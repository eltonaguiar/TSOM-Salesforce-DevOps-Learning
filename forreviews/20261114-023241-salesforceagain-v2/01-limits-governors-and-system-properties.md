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
