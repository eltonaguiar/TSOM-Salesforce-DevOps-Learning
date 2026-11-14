# Corrections still worth making

Updated against the live guides on 2026-11-14. This replaces the stale “add sections 13 and 14” merge plan in `forreviews/2026-11-14T023507_salesforcemore-v2/07-merge/content-gaps.md`.

Do not apply these in this folder. They are the edit list for the ServiceNow learning repo, `docs/salesforce/`.

## P0 — labs page, delete invented keys

In `docs/salesforce/labs-design.md`, section “Important System Properties”:

Remove `org.wideSharing.default`, `setup.locked`, and `apex.pageLimit`. Replace the table with the Setup paths only:

| Task | Path |
|---|---|
| Org-wide defaults | Setup > Sharing Settings |
| Whether a deploy is running | Setup > Deploy > Deployment Status |
| Session timeout and lockout | Setup > Session Settings |

Salesforce is not ServiceNow. There is no System Property key for those.

## P0 — labs page, sharing default

Replace “Apex respects sharing rules by default” with:

Apex does not enforce sharing unless the class says so. No keyword means the class inherits the caller. A trigger runs in system context. Use `with sharing` or `inherited sharing` unless the class must bypass sharing, and then say why.

## P0 — crash course, retired automation and the Flow/Apex table

In `docs/salesforce/crash-course.md`:

- State that Workflow Rules and Process Builder are past end of support (31 Dec 2025). Do not teach them as tools to build.
- Move simple HTTP callouts out of the “use Apex” column. Flow HTTP Callout plus a Named Credential is the declarative path. Apex remains the path from a trigger, and for bulk, retry, and non-trivial payloads.
- Remove “Approval processes” from the Flow-vs-Apex table. Point at Setup > Approval Processes, and note that Flow approvals exist as a separate choice.

## P0 — crash course, governor table

Split or delete the conflated rows:

- Scheduled Apex: 100 concurrent scheduled jobs. Not the `@future` or Queueable limit.
- `@future`: 50 calls per transaction. Do not file it under the cron cap.
- DML: 150 statements and 10,000 rows are different. The loop example breaks the statement limit.
- Per-class size: 1,000,000 characters. Org Apex code size: 6 MB. Say which one.
- Delete “mass email 10 per day” until the current governor-limit page is cited.

Leave the bulkified SOQL and DML samples. They are the right teaching.

## P1 — crash course navigation

- LWC is authored in the project and deployed with the CLI. Setup > Lightning Components is a list, not an editor.
- Drop “Setup > Monitor > Logs > Debug Logs”. Use Setup > Debug Logs, matching the breadcrumbs page.

## P1 — DevOps page, four facts, not four new chapters

Add to the existing sections. Do not add sections 13 and 14.

1. Section 5 or 9: fifth `--test-level` value `RunRelevantTests`, only after `sf project deploy start --help` confirms it on the edit date. Keep the four production-relevant levels as the ones to say out loud. Production still will not accept `NoTestRun` when the payload contains Apex.
2. Section 2: one deployment runs at a time per org, and the queue is not “first submitted, first run.” Cite https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html
3. Same section: zip and file ceilings from that same page. Do not copy a round number from a sibling README without opening the reference on the edit date.
4. Section 6: Gearset does not refresh the sandbox and does not replace Data Mask. Backup is a separate license. Copado and AutoRABIT product names move; interview the promotion path, not the menu.

Optional, same edit: state the quick-deploy eligibility window only if the current Help article is open. Do not guess 10 days into the page if the article has moved.

## P2 — breadcrumbs

Add Data Mask: App Launcher > Data Mask, after the managed package is installed. One line under Deployment & DevOps. The DevOps page already names the product.

## Do not do

- Do not paste Gearset, Copado, or AutoRABIT click-paths onto the published page.
- Do not add a second governor-limits chapter to the DevOps page. Fix the crash course and keep the cross-link.
- Do not re-add the `04t` example, the runbook, the rollback table, the Platform Administrator II rename, or the “author is not the approver” rule. They are already on the DevOps page.
- Do not publish exam-domain percentages.
- Do not deploy GitHub Pages from `direction-a-gaps-sam-guide-2026-11-13` or `docs/sam-guide-gaps-2026-11-13`. Those branches do not contain `devops-engineer.md`.

## Rendering

If a later edit adds `<details>`, kramdown will not parse markdown inside raw HTML unless the tag is `<details markdown="1">`. Existing pages that omit `markdown="1"` show raw pipe tables on the live site. This correction list does not need new `<details>` blocks.
