# Inspecting limits and drilling the limits story

**Merge target:** section 13.6 and 13.7 of the downstream page. This file is the practical "where do I look?" companion to the limits tables.

## 1. UI and CLI inspection map

| What you need | UI path | CLI / code |
|---|---|---|
| API usage and allocation | Setup → Company Information → API Usage | `sf org list limits`; `sf limits api display` |
| Storage | Setup → Company Information → Storage | `sf org list limits` |
| Apex jobs / batch queue | Setup → Apex Jobs; Setup → Background Jobs | Job listing varies by CLI version |
| Test results and coverage | Setup → Apex Test Execution | `sf apex run test --code-coverage --result-format human --wait 30` |
| Deploy status and id | Setup → Deploy → Deployment Status | `sf project deploy report --job-id <id>` |
| Debug logs | Setup → Debug Logs | `sf apex tail log`; `sf apex get log` |
| Org identity and instance | Setup → Company Information | `sf org display --target-org <alias>` |
| Runtime counters | Debug log / `Limits` class | `Limits.getQueries()`, `getDmlStatements()`, `getHeapSize()`, `getCpuTime()` |

## 2. Useful command set

```bash
# Who am I connected to?
sf org display --target-org uat

# What does the org say about its limits?
sf org list limits --target-org uat
sf limits api display --target-org uat

# Run the honest test gate and capture coverage
sf apex run test --test-level RunLocalTests --code-coverage \
  --result-format human --wait 60 --target-org uat

# What happened to that validation/deploy?
sf project deploy report --job-id <job-id> --target-org uat

# Preview what a deploy would do
sf project deploy preview --manifest manifest/package.xml --target-org uat
```

CLI flags move. Confirm with `sf <command> --help` before you put a command in a runbook.

## 3. Limit-aware design checklist

- [ ] One SOQL for a collection, one DML for a list.
- [ ] No SOQL, DML, or HTTP callout in a loop.
- [ ] Before-save Flow for same-record field updates; after-save for side effects.
- [ ] Queueable for chaining/callouts; Batch for volume; Platform Events for decoupling.
- [ ] No Queueable chaining past the async `enqueueJob` limit.
- [ ] `HttpCalloutMock` in tests; no live endpoint.
- [ ] Test at 200 and 10,000 records.
- [ ] `Test.startTest()` around the code under test.
- [ ] `Limits` checks in long-running code to fail early.
- [ ] API usage checked before a release.
- [ ] Deploys serialized per org.
- [ ] Delta payload, not full-org.

## 4. Interview drills (limits and constraints)

1. **"What happens on 200 records?"** One trigger invocation, collections, one SOQL, one DML, no callouts in the loop.
2. **"A batch fails at 5,000 records but the unit tests pass."** Check CPU, heap, SOQL/DML inside `execute`, callout limits, and the daily async allocation.
3. **"The pipeline user gets `REQUEST_LIMIT_EXCEEDED` during a release."** Check API Usage, identify the consumer, stop retrying, move to a delta/off-peak window, use a dedicated CI user.
4. **"The deploy fails at the component limit."** Split the payload or use delta/package deployments; do not open a support ticket first.
5. **"The deploy is green but the feature is broken."** Check feature enablement, named credential secret, certificate, remote site, record type assignment, Lightning page activation, and Flow version.
6. **"A record type deploys and users cannot create it."** Missing business process/picklist values, missing layout assignment, or missing profile/permission-set visibility.
7. **"A Flow deploys and users see the old screen."** The new version is not active.
8. **"A callout works in Dev and fails in UAT."** Named credential secret, external credential, certificate, remote site setting, or endpoint.
9. **"Why is a 75% coverage result in Dev not enough?"** Coverage is per org; the target's tests and the target's package context decide whether production accepts the deploy.
10. **"What does a Git revert not undo?"** Data changes, destructive deletes, activated Flow versions, and any post-deploy script that already ran.

## 5. What to merge

**Merge:** the inspection map, the useful command set (with the `--help` caveat), the checklist, and drills 1–8.

**Compress:** drills 9–10 if the page already covers them in the tests and rollback sections.

**Do not merge:** command flags without a "confirm with `--help`" note. CLI syntax changes more often than the concepts.
