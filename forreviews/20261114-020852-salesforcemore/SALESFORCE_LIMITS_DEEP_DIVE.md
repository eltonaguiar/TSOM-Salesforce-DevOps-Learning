# Salesforce Limits, Metadata Dependencies & Deployment Constraints — Deep Dive

Maps to Scotiabank Req 276046 line: **"Understanding of Salesforce limits, metadata dependencies, and deployment constraints"** and the Release Engineering Training section **2 — Metadata that breaks releases**.

This is the section release engineers are grilled on: a deploy can succeed and the feature can still fall over in production because the code isn't bulkified or because a missing dependency only surfaces in the target org.

---

<details>
<summary>1. Governor limits — what they are and why release engineering owns them</summary>

Governor limits are Salesforce's per-transaction runtime caps. They exist because Salesforce is multi-tenant: one org's runaway loop cannot starve another org on the same instance. They reset per transaction (per Apex invocation, per asynchronous job, per Flow interview, per trigger batch).

### The limits a release engineer must be able to name

| Category | Limit (typical, Enterprise/Unlimited) | DevOps implication |
|----------|--------------------------------------|--------------------|
| SOQL queries (sync) | 100 per transaction | A loop querying inside a `for` hits this at ~100 records. Bulkify or fail. |
| SOQL queries (async / @future, Queueable, Batch) | 200 per transaction | Still finite. Bulk queries outside loops. |
| DML rows | 10,000 per transaction | A bulk upload or data load that updates 10,001 rows in one transaction fails mid-way — partial success leaves org inconsistent. |
| DML statements | 150 per transaction | 150 insert/update/delete calls max. Batch them. |
| Heap size (sync) | 6 MB (Apex), 12 MB (async) | Large collections or big string serialization blow heap. Stream, don't hoard. |
| CPU time (sync) | 10,000 ms | Complex logic in triggers/Flows eats CPU. Offload to async where safe. |
| CPU time (async) | 60,000 ms | Batch/Queueable get more time but still bounded. |
| Callouts | 100 per transaction, 120 seconds cumulative timeout | External callouts inside a loop = guaranteed failure at scale. Use platform events / Outbound Message / named credentials with timeout handling. |
| Batch Apex | 5 queued/active, 5 queued (flex queue), 250,000 records per execute | Don't chain 50 batches in one deployment. |
| Queueable jobs | 50 chained per transaction (from one starting job) | Deep chains break. |
| Future calls | 50 per transaction (shared with @future) | Don't fire future methods in loops. |
| Scheduled Apex | 250,000 records processed per 24 hours per org (some editions) | Monitor scheduled job volume. |
| Flow interviews | Limits per interview and per bulkified batch (200 records) | Before-save Flows run synchronously with trigger limits; after-save can be async but still bounded. |

> **Release engineer rule:** You don't write the Apex, but you reject a story you cannot describe, and you ask the 200-record question: "What happens when this trigger/Flow runs on 200 records at once?"

### System properties for inspecting limits at runtime

Use these in anonymous Apex or test setup to measure, not guess:

```apex
// Remaining limits in the current transaction
Integer queries = Limits.getQueries();
Integer limitQueries = Limits.getLimitQueries();
Integer dmlRows = Limits.getDmlRows();
Integer limitDmlRows = Limits.getLimitDmlRows();
Integer cpuTime = Limits.getCpuTime();
Integer limitCpuTime = Limits.getLimitCpuTime();
Integer heapSize = Limits.getHeapSize();
Integer limitHeapSize = Limits.getLimitHeapSize();

// Org-wide info (system properties)
Id userId = UserInfo.getUserId();
String userName = UserInfo.getUserName();
Id orgId = UserInfo.getOrganizationId();
Boolean isSandbox = Organization.isSandbox(); // via [SELECT IsSandbox FROM Organization]
String instanceName = [SELECT InstanceName FROM Organization LIMIT 1].InstanceName;

// Is the current user a system admin (relevant for deploy permissions)?
Boolean isAdmin = UserInfo.isCurrentUserLicensed('Salesforce') &&
                  [SELECT Id FROM PermissionSet WHERE Name = 'System Administrator' LIMIT 1] != null;
```

Key system-property facts for release engineering:
- `UserInfo.getOrganizationId()` — never hardcode org IDs in Apex or Flows. Use custom metadata or queries.
- `Organization.IsSandbox` — distinguishes sandbox from production. Do **not** branch business logic on this as a rule; config belongs in the target, not in a `uat`-only branch that can never merge cleanly.
- `Limits` class methods (`getQueries`, `getLimitQueries`, etc.) — use in test setup to assert your code stays under 50% of limits in CI so prod doesn't surprise you.

</details>

<details>
<summary>2. Other platform limits (non-governor) that block deployments</summary>

Governor limits are per-transaction. These are org-wide or metadata-level limits that block *deployments themselves*.

| Limit area | Typical boundary | What breaks |
|------------|------------------|-------------|
| Apex code size | 3 MB per class/trigger (6 MB total in some contexts) | Large generated classes fail compile. |
| Apex characters | 1 million per org (some editions) | Massive legacy orgs can't add more Apex without cleanup. |
| Custom fields per object | 800 (varies by edition) | Adding field #801 fails deploy. |
| Custom objects | Varies by edition (e.g., 2,000 Enterprise) | Deploying new custom objects can exceed org limit. |
| Flows per org | Edition-dependent (thousands) | Flow sprawl from ungoverned admin clicks. |
| Permission sets | Limits by edition; permission set groups bundle them | One giant `CB_Admin` permission set is brittle; split by feature. |
| Package.xml components | Metadata API has component-type limits per deploy call | Split very large deploys into multiple packages or use the CLI's directory deploy. |
| Quick deploy window | 10 days after a successful validation | If you validate Monday and try quick-deploy next Friday, the validation expired — re-validate. |
| Concurrent deployments | One Metadata API deploy per org at a time | Two pipelines deploying to the same sandbox simultaneously: one queues/fails. Serialize in CI. |
| Test execution | 75% org-wide coverage required for prod Apex deploys; 1% per class minimum | Deploying one Apex class with 0% test coverage blocks the whole payload. |
| Async Apex limits | 250,000 executions per 24 hours (some editions) | A misbehaving scheduled job or future call can burn the daily quota. |

### Deployment constraint: Metadata API atomicity
A Metadata API deploy is *mostly* atomic: if any component in the payload fails, the whole deploy rolls back. But some components (e.g., certain custom settings, reports, dashboards) deploy partially. Know which components are atomic vs. partial before you promise a clean rollback.

### Deployment constraint: component dependencies
Salesforce compiles the payload against the target org. If your payload references something missing, the deploy fails:

- Flow → custom field it references → deploy the field first (or same payload).
- Apex class → custom object/field → deploy the schema first.
- Record type → business process + picklist values + layout assignment + visibility (profile or permission set) → deploy all together in one payload.
- Layout → FlexiPage (Lightning) is separate from classic layout; activate the correct one for the app.
- Permission set → references object/field permissions; if the field isn't in the org, the permission set deploy can fail or create dangling access.

</details>

<details>
<summary>3. Metadata dependency graph — what must deploy together</summary>

This is the "missing dependency" failure mode from Training Section 2. The pipeline should catch it in dry-run; you must recognize it from the error text.

```
Apex Class A calls Class B
   └─ deploy B before A, or same payload

Flow F references Custom Field c__MyField__c
   └─ deploy the field before/in-same-payload as the flow

Record Type RT on Object O uses Business Process BP
   └─ deploy O, BP, picklist values, layout assignment, RT visibility together

Permission Set PS grants FLS on Field f
   └─ deploy f (and its object) before/in-same-payload as PS

Custom Metadata Type CMDT record references Custom Setting CS
   └─ deploy both; CMDT is deployable, CS may need data deploy

Page Layout references Field-Level Security settings
   └─ FLS lives on profiles/permission sets; layout assignment lives on profile + record type
```

### Practical dependency check before deploy
```bash
# 1. Retrieve from the trusted source org
sf project retrieve start --metadata ApexClass:CB_CreditClass --target-org dev

# 2. Inspect the class for references (grep for other classes, objects, fields)
grep -R "CB_OtherClass\|CustomObject__c\|CustomField__c" force-app/main/default/classes/

# 3. Build package.xml including every referenced component manually,
#    or use a tool (Gearset/Copado) that auto-suggests dependencies.
# 4. Dry-run deploy to a clean sandbox matching the target.
sf project deploy start --dry-run --manifest manifest/package.xml --target-org qa
```

### Error string → root cause mapping
| Error text | Likely cause | Fix |
|------------|--------------|-----|
| `entity of type CustomField ... not found` | Missing field in payload/target | Add field to package.xml |
| `invalid cross reference id` | Record type/layout points at missing business process or layout | Deploy parent components together |
| `Apex class ... does not exist` | Class B missing | Deploy dependency class first |
| `No such column 'X' on entity ...` | SOQL references field not in org | Add field or fix query |
| `Test method ... failed` | Test assumes org data exists | Test inserts its own data |
| `code coverage ... below 75%` | Apex deployed without enough tested lines | Add/fix test class |
| `CANNOT_MODIFY_MANAGED_OBJECT` | Editing managed-package component | Configure around it or upgrade package; don't fork in Git |

</details>

<details>
<summary>4. Practical per-limit examples — technical walkthrough</summary>

### Example 1: SOQL inside a loop (the classic governor-limit failure)
```apex
// BAD: 1 query per Account in the trigger batch. At 101 Accounts -> 101 queries -> LIMIT exceeded.
for (Account a : Trigger.new) {
    Contact c = [SELECT Id FROM Contact WHERE AccountId = :a.Id LIMIT 1];
    // ...
}

// GOOD: one query outside the loop, map by AccountId
Map<Id, Contact> contactsByAccount = new Map<Id, Contact>();
for (Contact c : [SELECT Id, AccountId FROM Contact WHERE AccountId IN :Trigger.new]) {
    contactsByAccount.put(c.AccountId, c);
}
for (Account a : Trigger.new) {
    Contact c = contactsByAccount.get(a.Id);
    // ...
}
```

### Example 2: DML rows limit with data loader
A data loader upserts 10,001 rows in one transaction:
- Rows 1–10,000 succeed; row 10,001 throws `Too many DML rows: 10001`.
- The transaction rolls back partially depending on `allOrNone`. With `allOrNone=false`, you get partial success and an inconsistent org.
- **Release engineering fix:** chunk data loads at ≤9,000 rows per batch; use `Database.insert(list, false)` and inspect `SaveResult` errors; never assume one big upsert is safe.

### Example 3: Heap size with large collections
```apex
// BAD: serializing 50,000 accounts into one string
String json = JSON.serialize([SELECT Id, Name FROM Account LIMIT 50000]); // heap > 6 MB

// GOOD: stream or process in batches
Database.QueryLocator q = Database.getQueryLocator([SELECT Id FROM Account LIMIT 50000]);
// use Batch Apex with scope 200
```

### Example 4: Test data in empty orgs
```apex
// BAD: assumes an Account exists
@IsTest static void myTest() {
    Account a = [SELECT Id FROM Account LIMIT 1];
    System.assertNotEquals(null, a); // passes in Dev (has data), fails in empty QA
}

// GOOD: test creates its own data
@IsTest static void myTest() {
    insert new Account(Name = 'Test');
    Test.startTest();
    // run code under test
    Test.stopTest();
    // assertions
}
```

### Example 5: Before-save vs After-save Flow timeout
- Before-save Flow runs synchronously in the trigger context. Complex logic → CPU limit → the whole save fails.
- After-save Flow can run asynchronously but still bounded per interview.
- **Release engineering check:** before promoting a Flow, ask whether it should be before-save or after-save; run it in a sandbox with 200 records and watch CPU time in debug logs.

</details>

<details>
<summary>5. System properties relevant to deployments</summary>

| Property | How to access | Release-engineering use |
|----------|---------------|-------------------------|
| `UserInfo.getOrganizationId()` | Apex | Never hardcode org IDs; query dynamically |
| `UserInfo.getUserId()` / `getUserName()` | Apex | Audit who triggered a deploy/run |
| `UserInfo.isCurrentUserLicensed('Salesforce')` | Apex | Gate features by license type |
| `Organization.IsSandbox` | SOQL on `Organization` | Distinguish sandbox vs prod (but don't branch business logic on it) |
| `Organization.InstanceName` | SOQL | Identify which instance for incident correlation |
| `Limits.getQueries()` / `getLimitQueries()` | Apex | Assert code stays under 50% of limits in CI |
| `Limits.getDmlRows()` / `getLimitDmlRows()` | Apex | Guard bulk operations |
| `Limits.getCpuTime()` / `getLimitCpuTime()` | Apex | Flag slow triggers/Flows |
| `Limits.getHeapSize()` / `getLimitHeapSize()` | Apex | Flag large collections |
| `Limits.getCallouts()` / `getLimitCallouts()` | Apex | Flag callout-heavy code |

</details>

<details>
<summary>6. Deployment constraints — how limits shape pipeline design</summary>

### Constraint: one deploy per org at a time
Salesforce allows only one Metadata API deployment per org at a time. If your GitHub Actions pipeline deploys to QA on every merge and a developer triggers a manual deploy to the same QA org, one will queue or fail.
- **Pipeline fix:** serialize deploys to a shared sandbox using a GitHub concurrency group or a deployment lock.

### Constraint: validation expires for quick deploy
- Validation (dry-run) result is valid for quick deploy for **10 days**.
- If prod receives a hotfix between your validation and the change window, the target org changed — quick deploy is no longer an honest rehearsal. Re-validate.
- **Pipeline fix:** validate immediately before the change window, then quick deploy; or skip quick deploy and do a fresh deploy inside the window.

### Constraint: destructive changes are explicit
- Deletes are not inferred from "missing from Git." You must supply `destructiveChanges.xml` (pre or post).
- A delete in production is not reversible by Git revert — records on a deleted custom object are gone.
- **Pipeline fix:** require a separate destructive-changes file and a second-person review before any deploy containing deletions.

### Constraint: managed packages cannot be edited
- You cannot deploy changes to managed-package Apex or components. `CANNOT_MODIFY_MANAGED_OBJECT`.
- **Pipeline fix:** configure around managed components via declarative settings, or upgrade the package via `sf package install`, never fork managed code in Git.

### Constraint: package.xml size / component count
- Very large `package.xml` files or thousands of components in one deploy call increase failure surface and debug time.
- **Pipeline fix:** split by release train or by metadata domain (e.g., credit-application package separate from core-security package). Use unlocked packages for real boundaries.

</details>

<details>
<summary>7. CLI commands to probe limits and dependencies</summary>

```bash
# Org info (sandbox flag, instance)
sf data query --query "SELECT Id, Name, IsSandbox, InstanceName FROM Organization LIMIT 1" --target-org qa

# Apex test run with coverage (the production gate)
sf apex run test --test-level RunLocalTests --code-coverage --result-format human --wait 30 --target-org qa

# Dry-run deploy (no changes)
sf project deploy start --dry-run --manifest manifest/package.xml --target-org qa

# Deploy with destructive changes
sf project deploy start --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChanges.xml --target-org qa

# Check deployment status by ID
sf project deploy start --target-org qa --json | jq '.result.id'
sf project deploy report --deploy-id <id> --target-org qa   # confirm exact flag with --help

# Anonymous Apex to print limits
sf apex run --apex-code "System.debug(Limits.getQueries() + '/' + Limits.getLimitQueries());" --target-org qa
```

> Always confirm exact flags with `sf <command> --help`; CLI flags move between versions.

</details>

<details>
<summary>8. Pre-deploy checklist (limits + dependencies + constraints)</summary>

Run this before every production promotion:

- [ ] All Apex has tests; org-wide coverage ≥ 75%; each class ≥ 1%.
- [ ] Tests insert their own data — no `SELECT ... LIMIT 1` assumptions.
- [ ] No SOQL/DML inside loops; bulkified for 200 records.
- [ ] No hardcoded IDs, org IDs, or environment-specific branches (`if (IsSandbox)`).
- [ ] Secrets in Named Credentials, never in Git or Apex strings.
- [ ] Every referenced dependency (field, object, class, flow, business process, record type, layout, permission set) is in the payload.
- [ ] Dry-run passed against an org matching the target (QA/UAT-like), not just Dev.
- [ ] Destructive changes (if any) in a separate, reviewed `destructiveChanges.xml`.
- [ ] No managed-package components being edited.
- [ ] No concurrent deploy targeting the same org.
- [ ] Validation is fresh (within quick-deploy window if using quick deploy).
- [ ] Non-author approver signed off; change ticket ID in commit/PR.
- [ ] Rollback tag identified (`release-<last-good>`).

</details>

---

*Cross-reference: this deep dive expands Training Section 2 ("Metadata that breaks releases") and Section 9 ("Tests and validation") of the Release Engineering Training page built from Scotiabank Requisition 276046. Verify current governor-limit numbers against the latest Salesforce release notes, as limits can change by edition and release.*
