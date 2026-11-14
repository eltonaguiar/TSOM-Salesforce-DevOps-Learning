# 02 — Salesforce limits, metadata dependencies, and deployment constraints

> JD line covered: **"Understanding of Salesforce limits, metadata dependencies, and deployment
> constraints"** (Q3) and **"Strong experience with Salesforce metadata deployments"** (Q1).
>
> Every number below is taken from the official Salesforce Apex Developer Guide or Metadata API
> Developer Guide unless explicitly tagged otherwise. See `sources.md`.

---

## 1. Why a release engineer must know the limits

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

## 2. Governor limits (per Apex transaction)

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

### 2.1 The rules that are easy to get wrong

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

### 2.2 Certified managed package namespace limits

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

### 2.3 Org-level limits (not per transaction)

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

### 2.4 Callout, query and code limits

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

## 3. Metadata API deploy and retrieve limits

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

### 3.1 Deployment queueing — the constraint nobody writes down

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

### 3.2 Deployment Status page

`Setup > Deploy > Deployment Status` (Quick Find: `Deployment Status`):

- Shows **real-time progress** of the current deployment.
- **Chart 1 — components:** how many components deployed out of total, and how many have errors.
- **Chart 2 — Apex tests:** how many tests have run out of total, how many errors, and the name of
  the currently running test.
- Deployments in progress or completed in the **last 30 days** are visible.
- `Cancel` is available while in progress or queued. The status becomes `Cancel Requested` until
  cancellation completes; a cancelled deployment is listed under **Failed**.

---

## 4. Metadata dependencies — what depends on what

A deploy is a **compile against the target org**, not a file copy. The payload must be internally
consistent and consistent with what already exists in the target.

### 4.1 Error → root cause → fix

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

### 4.2 The dependency rules that matter for package design

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

### 4.3 Destructive changes

| Rule | Detail |
|---|---|
| Deletions are a separate manifest | `destructiveChanges.xml`; the CLI exposes `--pre-destructive-changes` and `--post-destructive-changes` |
| Pre vs post | Pre-deletes run before additions (needed for renames that would collide); post-deletes run after. From API version **33.0**, both orders are supported. Earlier versions always deleted first. |
| Recycle Bin | By default deleted components go to the Recycle Bin. `--purge-on-delete` makes them immediately eligible for deletion instead (API 22.0+). |
| Git revert does not undo it | Rolling back a delete means **recreating** the metadata. Records on a deleted custom object are gone. A data restore is a separate, ticketed path (backup tool), not a Git operation. |
| Master-Detail caveat | See 4.2.6 — detail records are permanently deleted, not recycled. |

---

## 5. Test levels — the policy surface

**Source: Salesforce CLI plugin `deploy-retrieve` message definitions + Metadata API guide.** `verified`

There are **five**, not four. The existing page says four.

| Test level | Behaviour |
|---|---|
| `NoTestRun` | No tests run. Applies only to dev environments (sandbox, Developer Edition, trial). **This is the default for development environments.** |
| `RunSpecifiedTests` | Only the tests named with `--tests`. Coverage is computed **per class and trigger individually**, each needing **≥75%**. This differs from the overall coverage percentage. |
| `RunLocalTests` | All tests in the org **except** those from installed managed and unlocked packages. **This is the default for production deployments that contain Apex.** |
| `RunAllTestsInOrg` | All tests including managed packages. |
| `RunRelevantTests` *(Beta)* | Salesforce analyses the deployment payload and its dependencies and runs only the relevant tests. Each class/trigger in the payload still needs **≥75%** individually. Can be augmented with `@IsTest(critical=true)` (always runs) and `@IsTest(testFor='...')` (runs when the named class/trigger is new or changed). Requires explicit customer opt-in under Beta Services Terms. |

### 5.1 Which metadata types force a test run

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

### 5.2 Validation (`checkOnly`) vs quick deploy

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

## 6. Platform and org allocations (not per transaction)

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

## 7. Permissions the deploy identity needs

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

## 8. Debugging a failed deployment — the order to work in

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

## 9. Unverified / open items

| Item | Status | What would confirm it |
|---|---|---|
| Exact per-org storage, file-size and Big Object ceilings | Not retrieved here (the Salesforce Help storage page is client-rendered) | The org's `Setup > System Overview` storage panel, or the current Salesforce App Limits Cheatsheet storage page |
| Whether the 39 MB / 600 MB / 10,000-file figures changed since retrieval (2026-11-14) | `verified` as of 2026-11-14, but the guide itself says "limits can change without notice" | Re-read the Metadata API Developer Guide before quoting in a customer document |
| Per-org custom limits (e.g. raised Apex code size, raised API allocation) | Org-specific, not published | `Setup > Company Information` and the Salesforce support case history |
