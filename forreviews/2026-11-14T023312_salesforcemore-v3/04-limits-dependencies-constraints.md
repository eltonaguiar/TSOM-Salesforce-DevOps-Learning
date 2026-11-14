# Limits, metadata dependencies & deployment constraints (deep dive)

> This is the section the JD calls out explicitly: *"Understanding of Salesforce limits, metadata
> dependencies, and deployment constraints."* Values marked `[Verify]` are edition/release-dependent —
> confirm against the current Apex Developer Guide and Metadata API Developer Guide before publishing.

## 1. Apex governor limits — per transaction

These are enforced **during unit tests**, so a deployment that runs tests can fail purely on limits.

| Limit | Synchronous | Asynchronous (Batch/Queueable/Future) |
|---|---|---|
| SOQL queries | 100 | 200 |
| SOQL rows retrieved | 50,000 | 50,000 |
| SOSL queries | 20 | 20 |
| DML statements | 150 | 150 |
| DML rows | 10,000 | 10,000 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |
| Callouts per transaction | 100 | 100 |
| Max callout timeout | 120 s | 120 s |
| Email invocations | 10 | 10 |
| Future method calls | 50 | 50 |
| Queueable jobs chained | — | 50 |
| `getQueryLocator` rows | 10,000 | 10,000 |
| Max trigger recursion depth | 16 `[Verify]` | — |

### What each limit does to a deployment

- **SOQL/DML in loops** → `Too many SOQL queries: 101` during tests → red validation.
- **Tests that query without `LIMIT`** against prod-like volumes → `Too many query rows: 50001`.
- **CPU time** from nested loops / regex / large Flow interleaving → `Apex CPU time limit exceeded`.
- **Heap** from deserializing large JSON → `Apex heap size too large`.
- **Un-mocked callouts** in tests → `Methods defined as TestMethod do not support Web service callouts`
  → fix with `HttpCalloutMock`.

### Cumulative limits

A chain of transactions in one execution context also has a cumulative CPU/heap budget; long Queueable
chains can hit the cumulative cap even when each link is under the per-transaction limit. `[Verify]`
current cumulative values in the Apex Developer Guide.

### The design question you ask in review

> "What happens when this runs on 200 records?"

A deploy can be green and the feature can still fall over at volume. Governor limits still matter to a
release engineer even when they did not write the trigger.

## 2. Per-org / per-24h limits that affect release engineering

| Limit | Typical value | Why a DevOps engineer cares |
|---|---|---|
| API requests / 24h | Enterprise/Unlimited ~15,000 + per-user; Professional ~5,000 `[Verify tier]` | CI runs, backups, and integrations compete for the same budget. A chatty pipeline can starve production integrations. |
| Metadata API calls / 24h | ~5,000 `[Verify]` | Every compare/validate/deploy consumes calls. Gearset/CI fan-out multiplies this. |
| Bulk API batches / 24h | ~15,000; 10,000 records/batch `[Verify]` | Data seeding and post-refresh loads count here. |
| Concurrent long-running requests | ~10 `[Verify]` | Parallel deploys to the same org can queue or fail. |
| Simultaneous schema-changing deploys to one org | Effectively one at a time | Two pipelines deploying schema to the same org → `UNABLE_TO_LOCK_ROW` / deploy queue. |
| Sandbox refreshes | Developer/Dev Pro: daily; Partial Copy: every 5 days; Full: every 29 days | Never promise a same-day Full refresh; check the next eligible date in Setup first. |

## 3. Metadata API deployment limits

| Constraint | Value | Notes |
|---|---|---|
| Max files per deployment | 10,000 files `[Verify]` | Exceeding it fails the payload; use delta or split packages. |
| Max compressed payload | ~400 MB `[Verify current byte cap]` | Applies to deploy/retrieve; large static resources dominate. |
| Single deploy batch timeout | ~10 minutes per batch `[Verify]` | Long test runs are chunked; a hung test can time out the request. |
| Quick Deploy window | 240 hours (10 days) | Invalidated by **any** later deployment to the target org, a package install, or direct Setup edits to deployed metadata. |
| Production code coverage | 75% org-wide | A payload containing Apex will not deploy to production with `NoTestRun`. Every trigger needs some coverage `[Verify the 1% trigger rule]`. |
| `--test-level` values | `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg` | `RunLocalTests` excludes managed-package tests — the honest pre-release gate. |
| Destructive changes | Separate `destructiveChanges.xml` | Deletes are not implied by absence; a Git revert does **not** undelete. |

## 4. Metadata dependency graph — failure string → cause → fix order

| Failure you see | Root cause | Correct fix order |
|---|---|---|
| `no such column` / field does not exist | Flow/formula/Apex/layout references a field not in the payload and not already in the target | Add the field to the same payload (or deploy to an org that has it) |
| `invalid cross reference id` | Record type / layout / business-process assignment points at something missing | Deploy parent object → record type → layout → permission grant together |
| `entity not found` / dependent class invalid | Apex class A uses class B; B not in payload | Add B, or remove the reference |
| `Cannot create a Master-Detail relationship … existing records` | Adding M-D to an object that already has rows in the target | 1) deploy as **Lookup** → 2) backfill every row via data load/batch → 3) redeploy as **Master-Detail** |
| `UNABLE_TO_LOCK_ROW` | Schema deploy racing live DML on the same object | Schedule schema changes off-peak; pause integrations; retry in the window |
| Record type deploys but users cannot use it | Missing page-layout assignment, business process/picklist values, or permission-set/profile visibility | Deploy record type + layout + permission set in one payload |
| Flow deploys but users see old behavior | New version not **Active** | Activate the version (or ensure the tool deploys as Active); confirm in a sandbox first |
| `CANNOT_MODIFY_MANAGED_OBJECT` | Editing a managed-package component | Configure around it or upgrade the package — never fork it |
| Coverage below 75% | Insufficient/irrelevant tests in the target | Add tests that create their own data; re-validate against the real target |
| Deploy succeeds, feature fails at volume | Not bulkified (SOQL/DML in loops, before/after-save misuse) | Refactor; ask the 200-record question before sign-off |

### The two-step Master-Detail rule (worked example)

A custom object that already has records in the target org cannot receive a **new** Master-Detail field in
one deploy, because existing rows would have a null required parent. The safe sequence:

1. Deploy the field as a **Lookup**.
2. Run a data step (data load / batch Apex) to populate the lookup on every existing row.
3. Deploy the metadata change switching the field from **Lookup → Master-Detail**.

This is the classic example of "deployment constraint that is really a data-ordering constraint."

### Destructive-change ordering

You cannot delete a field referenced by an active Flow, Apex, formula, or workflow. Sequence:

1. Deploy an update removing all code/formula/Flow references.
2. Deactivate old Flow versions in the target.
3. Deploy the `post-destructive-changes` payload removing the field.

## 5. System settings / "system properties" a release engineer must control

| Setting | Where (Setup path) | Release impact |
|---|---|---|
| Deployment Settings (allow inbound/outbound changes, require tests) | Setup → Deploy → Deployment Settings | Blocks or permits change-set/metadata deploys entirely |
| Deployment Status (in-flight/validated jobs) | Setup → Deploy → Deployment Status | Shows validated job ids and their expiry |
| Apex Settings (e.g. parallel testing toggles) | Setup → Apex Settings | Changes test runtime and flakiness |
| Process Automation Settings (deploy flows/processes as active) | Setup → Process Automation Settings | Determines whether a deployed Flow version is Active |
| Named Credentials / External Credentials | Setup → Named Credentials | Endpoints/secrets are org-specific; never commit secrets; set non-prod endpoints |
| Remote Site Settings (legacy) | Setup → Remote Site Settings | Missing entry → callout blocked after deploy |
| CORS / CSP Trusted Sites | Setup → CORS / CSP Trusted Sites | Front-end integrations break silently |
| Email Deliverability | Setup → Deliverability | Sandbox refresh sets it to system-only/no access — reset if testing email |
| Session Settings / Login IP Ranges / Password Policies | Setup → Session Settings / Profiles | Security posture; profile-deployed settings conflict easily |
| Custom Metadata Types (CMDT) | Setup → Custom Metadata Types | Deployable config/feature flags — preferred over custom settings data |
| Custom Permissions | Setup → Custom Permissions | Feature-flag gate checked in Apex/Flow/formula |
| Sandboxes / Sandbox Templates | Setup → Sandboxes | Refresh eligibility and data shape |
| Data Mask | App Launcher → Data Mask (if installed) | PII masking before broad login to a Full copy |
| DevOps Center | Setup search "DevOps Center" (must be enabled) | Native work-item/pipeline option |

### Config that must NOT live in Git

- Secrets inside Named/External Credentials (commit the metadata, not the secret).
- `.sfdx/`, org auth files, consumer secrets, JWT private keys.
- Retrieved junk you did not mean to ship (profile user lists, certificate bodies, sandbox-only endpoints).

## 6. Validation vs quick deploy vs real deploy

| Action | Changes the org? | Why you run it |
|---|---|---|
| Validate / dry-run (`--dry-run`, validate-only job) | No | Prove the payload compiles and tests pass against that org |
| Quick deploy | Yes | Apply a validation that already passed, inside the 10-day window, without paying test runtime again |
| Real deploy | Yes | First deploy, expired validation, or payload changed |

Quick deploy only works if nothing relevant changed since validation. If someone hotfixed prod after your
validation, the quick deploy is no longer an honest rehearsal — **re-validate**.

## 7. Rollback reality (metadata ≠ data)

| Situation | First move | Then |
|---|---|---|
| Bad Flow, previous version still in the org | Activate the previous Flow version | Redeploy the last good tag so Git matches the org |
| Bad Apex or config | Stop the bleeding (deactivate automation if safe) | Validate the previous tag, deploy it |
| Destructive delete already ran | You cannot undelete records | Restore metadata from Git; data restore is a separate ticketed path (backup tool), not a Git revert |
| Post-deploy data script already ran | Git revert will not undo the rows | The script needs its own reverse script, reviewed before the window |

If you do not have a tag from the last good prod deploy, you do not have a rollback. Fix that before the
next release.
