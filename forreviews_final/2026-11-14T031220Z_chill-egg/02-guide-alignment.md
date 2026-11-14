# Live guides vs review claims

Compared on 2026-11-14 against the five published pages, not against the gap lists. A claim marked **already published** must not be merged again.

## DevOps Engineer page

URL: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/

The page already has the spine the research bundles were written to supply:

- Role ownership table, training items 1–12, source-of-truth CLI retrieve/dry-run
- Metadata failure table, sandbox map, feature/release/hotfix, four-stage CI
- Tool table (CLI, DevOps Center, Gearset, Copado, AutoRABIT, Change Sets)
- Conflict clinic for profiles, permission sets, record types, layouts, Flows, Apex
- Unlocked vs managed vs unpackaged, `04t` install example, “do not package the whole org”
- Validate vs quick deploy vs real deploy, `NoTestRun` / `RunSpecifiedTests` / `RunLocalTests` / `RunAllTestsInOrg`
- Three release speeds, runbook template, rollback table including “Git revert does not undo rows”
- Banking audit pack and segregation of duties
- Design patterns: permission sets, one flow owner, tests create data, no hardcoded ids, Named Credentials, custom metadata toggles, bulkify, no environment branches
- Labs A–E, eight interview drills, quiz
- Credential rename: Advanced Admin is Platform Administrator II, and there is no official Salesforce DevOps Engineer cert

`forreviews/2026-11-14T023507_salesforcemore-v2/07-merge/content-gaps.md` sections 3.8–3.13 are stale. Those adds are on the page. Do not append them again.

### Still open on this page

| Item | Status | Source to prefer |
|---|---|---|
| Fifth test level `RunRelevantTests` (research says Beta, API 66.0+) | Page lists four levels only | `023507` bundle `02-limits-constraints/dependencies-and-constraints.md`. Re-check `sf project deploy start --help` before publishing the Beta label. |
| Metadata API deploy ceiling (~39 MB zip / ~600 MB uncompressed; 10,000 files unlocked/2GP; 35,000 for reviewed 1GP) | Not on the page | Same bundle, citing the Metadata API `deploy()` reference. Not re-fetched in this pass. Cite, do not memorize a round number from a sibling README. |
| One deployment at a time per org; queue order is not submission order | Not on the page | Same `deploy()` reference, via the `023507` bundle |
| Gearset does not refresh sandboxes; backup is a separate license | Page stays category-level and does not make the wrong claim, but also does not warn | Add two sentences in section 6. Do not paste the Gearset click-path file. |
| Copado / AutoRABIT current product names | Page uses the posting’s names, which is fine, and does not teach retired product names | One caveat sentence. Not a menu tour. |
| Quick-deploy window length | Page says “inside the window” and does not give a duration | Salesforce Help is the source. Commonly cited as 10 days. Confirm the Help article on the edit date before writing the number. |
| Full per-transaction governor table | Intentionally delegated to the crash course | Fix the crash course. Do not duplicate a second limits chapter here. |

### Reject

- Vendor click-path dumps on the published page. The page’s own confidence line says button labels drift. The `023507` cross-bundle note agrees: pick one label set or stay category-level. Stay category-level.
- A second JD term encyclopedia on the page. Training items 1–12 already map the posting. A collapsible term dump will rot.
- Certification percentage weights. Neither the page nor this pass fetched the current exam guide PDF.
- Any claim that Gearset, Copado, or AutoRABIT is the bank’s tool. The posting lists them as examples.

## Crash course

URL: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/

Useful and mostly right: objects/records/fields, profile vs permission set vs role vs OWD, lookup vs master-detail, bulkified SOQL and DML examples, Named Credential `callout:` pattern, Trailhead pointers, link onward to the DevOps track.

Errors and stale lines, observed on the live page this pass:

| Location | Problem | Correction |
|---|---|---|
| Automation, “When to Code vs When to Flow” | “Callouts to external APIs (not supported in Flow easily)” is under Use Apex. Flow HTTP Callout has been generally available since 2023. | Flow HTTP Callout for a simple Named-Credential GET/POST. Apex when the callout is from a trigger, needs bulk/retry, or the payload is not a simple wizard. |
| Same table | “Approval processes” sits in the Flow column. Classic Approval Processes are their own Setup feature. Flow can also run approvals. The row teaches the wrong split. | Delete the row or split it: classic Approval Process vs Flow approval, and say which one the org already uses. |
| Automation intro | Workflow Rules and Process Builder are described as current tools “being retired.” End of support was 31 Dec 2025. Today is 14 Nov 2026. | Say retired. Do not create new ones. Migration target is Flow. |
| Governor summary table | “Scheduled jobs 100 concurrent” is annotated `@future`, Queueable, Batch Apex. Those are different limits. 100 is scheduled Apex (cron). `@future` is 50 per transaction. Queueable enqueue limit is not the cron cap. | Split the row. |
| Same table | “Email (mass) 10 per day” is not a number this pass verified. | Remove it or replace it only after citing the current Apex governor-limit page. Do not teach 10. |
| Same table | “Apex classes/triggers 1 million characters” is the per-class cap, labeled as if it were the org cap. Org-wide Apex code size is 6 MB. | Say both. |
| DML deep dive | Section is titled DML rows (10,000) but the bad example (`update` inside a loop) hits the 150 DML *statements* limit first. | Name the limit the example actually breaks. |
| Navigation table | “Lightning Components (LWC) → Setup > Lightning Components” is the list of components already in the org, not where you author LWC. | Author in the project. Deploy with `sf project deploy start`. Setup only shows the result. |
| Navigation table | “Setup > Monitor > Logs > Debug Logs” is the Classic path. | Lightning path is Setup > Debug Logs, which the breadcrumbs page already uses. |

SOQL 100 sync, heap 6 MB / 12 MB, callouts 100, CPU 10s / 60s, and the bulkified examples are fine. Async SOQL is 200; the deep dive is labeled sync, so leave it if the label stays.

## Navigation breadcrumbs

URL: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/

Deployment section matches the DevOps page: Sandboxes, Change Sets, Deployment Settings, Deployment Status, Sandbox Templates, DevOps Center, and a link to the DevOps track. Debug Logs path is the Lightning one. This page is the path reference. Do not invent ServiceNow-style property keys here.

Still missing, low priority: Data Mask (App Launcher > Data Mask, after the package is installed) and a one-line note that External Client Apps are the newer Connected App model. Neither blocks the DevOps track.

## Labs and design

URL: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/

Labs 1–4 (custom object + Flow, trigger + test, LWC, REST callout) are the right first week. The deployment-options table correctly points at the DevOps track and lists CLI, Metadata API, DevOps Center, and the three vendors.

Two teaching errors, read from `origin/main:docs/salesforce/labs-design.md` this pass:

1. **Fake system properties.** The “Important System Properties” table lists `org.wideSharing.default`, `setup.locked`, and `apex.pageLimit`. Salesforce has no ServiceNow System Properties table. Those keys will not be found in Setup. The “Where” column happens to name real pages (Sharing Settings, Deployment Status, Session Settings). Delete the property-name column. Keep the Setup paths.
2. **Sharing default is backwards.** The security table says “Apex respects sharing rules by default; use `without sharing` only when necessary.” A class with no keyword does not enforce sharing. It inherits the caller. Triggers run in system context. Declare `with sharing` or `inherited sharing` on purpose.

“≥75% coverage” in the maintenance table is the production deploy gate, not a design target to stop at. The DevOps page already says a green sandbox coverage number is not evidence. One cross-link is enough.

## Users and data

URL: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/

Profiles, permission sets, permission set groups, OWD, and role hierarchy match the crash course and the DevOps conflict clinic. No contradiction that needs a rewrite.

Caveat, not a patch: the Private OWD row says “owner and above in the role hierarchy.” Role hierarchy grant can be turned off per object. Add that only if this page is edited for another reason.

## What the guides already agree on

These do not need another review file:

- Git is the source of truth. Production is a deploy target.
- Permission sets over profile edits for story access.
- Flow XML does not merge. One owner per flow in a release.
- Tests insert their own rows.
- Named Credentials, not hardcoded tokens.
- Full sandbox refresh is not done until masking is confirmed.
- Change Sets do not scale to this role.
- There is no official Salesforce DevOps Engineer certification. Platform Administrator II is the current name of Advanced Admin.
