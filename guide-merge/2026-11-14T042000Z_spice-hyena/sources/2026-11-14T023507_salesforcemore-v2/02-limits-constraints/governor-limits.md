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
