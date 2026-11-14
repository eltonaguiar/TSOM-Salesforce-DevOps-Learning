# 07 — Org settings and system properties that change release behaviour

> JD lines covered: R4 (audit/security/compliance), R6 (sandbox strategy), Q3 (limits and
> deployment constraints), and the "configuration/setting/variation" requirement behind every
> term in the posting.
>
> **Accuracy rule applied here.** Setup **paths** are stable and match the repository's existing
> `navigation-breadcrumbs.md`. Exact **field labels inside a settings page** vary by Salesforce
> release, edition and whether a feature (DevOps Center, Data Mask) is installed — where that is
> true, the row says so and tells you how to find the setting. Behaviour that is verified against
> the Metadata API Developer Guide or vendor documentation is marked `verified`.

---

## 1. The DevOps Setup surface — path reference

| Task | Path |
|---|---|
| Sandboxes | `Setup > Sandboxes` |
| Sandbox templates (Partial Copy source) | `Setup > Sandboxes > Sandbox Templates` |
| Deployment settings (inbound deploy gate) | `Setup > Deploy > Deployment Settings` |
| Deployment status / last 30 days of deploys | `Setup > Deploy > Deployment Status` |
| Deployed components | `Setup > Deploy > Deployed Components` |
| Change sets (legacy) | `Setup > Deploy > Change Sets` |
| Apex test execution | `Setup > Apex Test Execution` |
| Custom metadata types (incl. Protected flag) | `Setup > Custom Metadata Types` |
| Custom settings | `Setup > Custom Settings` |
| Named credentials | `Setup > Named Credentials` |
| External credentials / secret store | `Setup > External Credentials` |
| Connected apps / external client apps | `Setup > App Manager > Connected Apps` (or `External Client Apps`) |
| Debug logs | `Setup > Debug Logs` |
| Apex jobs | `Setup > Apex Jobs` |
| Scheduled jobs | `Setup > Scheduled Jobs` |
| Users, permissions, "view all data" | `Setup > Users > Users` |
| Permission sets / groups | `Setup > Permission Sets`, `Setup > Permission Set Groups` |
| Profiles | `Setup > Profiles` |
| Session settings | `Setup > Session Settings` |
| Password policies | `Setup > Password Policies` |
| Lockout policies | `Setup > Lockout Policies` |
| System properties | `Setup > System > System Properties` |
| Org system overview / API usage | `Setup > System Overview` |
| Data import / export | `Setup > Data > Data Import Wizard`, `Setup > Data > Export` |
| Salesforce backups (native) | `Setup > Data > Backups` |
| DevOps Center (if enabled) | `Setup`, Quick Find `DevOps Center` |
| Data Mask (if installed) | App Launcher → `Data Mask` |

> **Search, don't browse.** Salesforce Setup's Quick Find is the fastest route. Most of the rows
> above are one search away, and the search term is also what you should write in a runbook.

---

## 2. Deployment and CI settings — `Setup > Deploy > Deployment Settings`

This is the single page that decides **whether a pipeline can deploy into an org at all**.

| Setting | Effect | Release-engineering note |
|---|---|---|
| **Allow inbound deployments** | Master switch for Metadata API deployments into the org | If off, every pipeline fails with an auth/deploy error that does not name the cause. **Check this first when a pipeline that worked yesterday fails today on a new org.** |
| **Enable Salesforce CLI deploys** | Allows `sf project deploy start` (the CLI-specific deploy path) as opposed to raw Metadata API calls | Some orgs have the CLI path separately gated from the API path. `verified` that these are distinct controls; the exact field name varies by release |
| **Restrict deployments to specific IP ranges** | Only traffic from the listed CIDRs may deploy | This is how a bank enforces "only the CI runner deploys to prod". Combine with the runner's static egress IP. Verify the current field name in your org — the setting has been renamed across releases |
| **Deployment history retention** | Deployments in progress or completed in the **last 30 days** are visible in `Setup > Deploy > Deployment Status` | `verified` (Metadata API Developer Guide). If your audit needs 7 years of deployment evidence, Salesforce's 30-day view is **not** enough — you must export the CI artefacts yourself |

**Variations and traps**

| Variation | Trap |
|---|---|
| Inbound deployments disabled | "Invalid session id"/"deploy not permitted" style errors with no mention of the switch |
| CLI deploys disabled but API deploys enabled | `sf project deploy start` fails while the vendor tool's Metadata API path succeeds — and vice versa |
| IP allowlist set, but the runner uses a NAT or an egress proxy | Deploys intermittently fail from a different runner pool. The fix is the network config, not the retry |
| Allowlist set to a corporate CIDR rather than the CI runner's | A human on the corporate network can deploy. This quietly destroys segregation of duties |

**Audit implication:** record the Deployment Settings values in the org's configuration baseline and
review them on the same cadence as the deploy identity's permissions. A setting change here is a
control change and belongs in the change process.

---

## 3. Sandbox settings

| Setting / path | Effect | Note |
|---|---|---|
| `Setup > Sandboxes` | Lists every sandbox, its type, its refresh history and the **next eligible refresh** | The page is the source of truth for refresh cadence — do not quote a cadence from memory |
| `Setup > Sandboxes > Sandbox Templates` | Defines the data set copied into a **Partial Copy** | A template is the difference between a Partial Copy that is useful and one that leaks. Review the template the way you review a data masking rule |
| Sandbox refresh permissions | Who may request a refresh | For a bank, refresh should be a **ticketed, named-person** operation. Some orgs restrict refresh to admins so that a casual "refresh my sandbox" cannot create an unmasked production copy |
| Refresh notifications | Salesforce emails on refresh completion | Use it as the trigger for the masking step — do not rely on a human noticing the email |
| Sandbox naming convention | E.g. `CB-DEV-01`, `CB-UAT-02` | Naming is how the pipeline maps a target. If `target-org` aliases and Salesforce sandbox names drift, the pipeline deploys to the wrong org. Make the alias derivation mechanical |

**Refresh variations**

| Variation | Behaviour |
|---|---|
| Developer / Developer Pro | No data; fast; can be refreshed often (licence-limited) |
| Partial Copy | Data from the **template**, not from production; template is the privacy control |
| Full | **All production data and metadata**; slowest; carries the masking obligation |
| Scratch org | Created from a definition file on a Dev Hub; **not a sandbox**; disposable |

---

## 4. User, permission and identity settings that gate deployments

| Setting | Why a release engineer cares |
|---|---|
| `Modify All Data` on the integration user | The broad metadata + data deploy permission. Narrowest acceptable alternative is `Modify Metadata Through Metadata API Functions` **plus** per-type permissions for everything you deploy |
| `API Enabled` | Without it the identity cannot connect at all |
| `Customize Application` | Required to deploy some Flow, LWC, app, custom-metadata and custom-setting components |
| `Author Apex`, `Manage Flow`, `Manage Profiles and Permission Sets` | Recommended for the deploy identity so it can deploy the metadata types the bank actually uses |
| "Allow Users to View All Data" (org-wide) | A QA or integration user with this sees everything, including unmasked customer data. In a bank, this should be off and granted per-user through a permission set, if at all |
| `Setup > Users` → user lifecycle | Deactivate, never delete. A deleted user referenced by an approval process or an assignment breaks a deploy with `Invalid cross reference id` |
| Permission set groups | The bundling unit for a persona's access. Deploy them like any other component |
| Session settings (timeout, IP relax) | A CI token that is idle too long gets invalidated mid-release — keep the timeout compatible with your longest test run |
| Password policies / lockout policies | A shared human credential that trips the lockout policy fails a deploy. This is exactly why the pipeline uses a certificate, not a password |

---

## 5. Security and compliance settings

| Setting | Control it supports |
|---|---|
| `Setup > Session Settings` | Session timeout, IP relax, "Require secure URL" |
| `Setup > Password Policies` | Credential hygiene for human admins |
| `Setup > Lockout Policies` | Brute-force protection — and a deploy-failure cause if a shared account locks itself out |
| `Setup > IP Relax` (login IP ranges) | Where the bank restricts human logins by network |
| Connected App / External Client App policies | Token lifetime, scopes, IP relax for the deploy identity |
| `Setup > System > System Properties` | The org-wide switches; **the exact list varies by edition and release** — use Quick Find for the specific property rather than a remembered menu path |
| Audit trail / field history retention | Determines how far back "who changed this" can be answered. If your retention policy is 7 years, org field history will not cover it — externalise it |
| `Setup > System Overview` → API Usage | Monitoring; feeds the API budget decision in `02 §6` |

**The debug-log data leak.** Debug logs contain field values, query text and sometimes payload.
In a bank, a debug log pasted into a ticket is a **data incident** if it contains customer data.
Practices: capture logs only in a masked sandbox; set log retention short; scrub before attaching;
prefer the "trace flag + deployment id" pair over a full log.

---

## 6. Apex, limits and platform settings that change deploy behaviour

| Setting / limit | Where | Effect on a release |
|---|---|---|
| Concurrent Apex limit per org | `Setup > Apex Settings` (org-wide) | Caps parallel long-running transactions (10–50 depending on licences). A nightly batch + a release validation compete for the same pool |
| Concurrent Apex limit per user | `Setup > Apex Settings` | The integration user running tests counts against it |
| Apex CPU time limit | Apex settings / org limit | Determines whether a test run is killed mid-deploy |
| Total Apex code in the org (6 MB; 10 MB scratch) | Org limit; raisable via support case | The 6 MB ceiling is an **org-level** constraint on how much custom code a bank can accumulate — a release-engineering concern over years, not days |
| 7,500 class/trigger code units per deployment | Platform limit | The per-deploy ceiling that bites large orgs |
| Async executions per 24 h | Org limit (`DailyAsyncApexExecutions`) | A release that triggers a lot of async work can exhaust the day's budget |
| Batch Apex concurrent jobs (5) | Platform limit | A release that enqueues many batches will queue behind itself |
| API request allocation per 24 h | `Setup > System Overview`; `API Usage Notifications` | CI validation burns it. If the org is API-constrained, validate on a schedule, not per PR |
| `API Usage Notifications` | `Setup`, Quick Find `API Usage Notifications` | Alert a named owner before a release, not after |

---

## 7. Logging, tracing and observability settings

| Setting | Use |
|---|---|
| `Setup > Debug Logs` | Retrieve logs for a failed test/deploy. **Set a short retention; logs contain field values** |
| `Setup > Trace Flags` | Narrow diagnostic flags (e.g. Apex, workflow) to reproduce a production issue in a masked sandbox — **never** enable a trace flag at high verbosity in production during business hours |
| `Setup > Apex Test Execution` | The org-side record of a test run; the second source of test evidence alongside CI |
| `Setup > Apex Jobs` / `Setup > Scheduled Jobs` | Confirm an async job actually ran after a deploy — a common "deployed but nothing happened" cause |
| `Setup > Platform Events` / `Setup > Event Monitoring` | Verify event-driven integrations consumed the post-deploy events |
| Salesforce Setup → **API Usage** | Delivery of the post-deploy integration calls |

**The "deployed but nothing happened" checklist** — run this after every prod deploy that involves
automation:

1. Is the Flow version **Active**? (Draft is the default for some deploy tools.)
2. Did the permission set actually assign the user? (Deploy succeeded; assignment may be missing.)
3. Is the feature flag in Custom Metadata still off? (A deliberate dark launch — check it was turned on.)
4. Did the async job run? (`Setup > Apex Jobs` / `Scheduled Jobs`)
5. Did the integration endpoint point at prod? (Named Credential, not a literal URL.)
6. Is the record type visible on the user's profile/permission set?

---

## 8. Metadata and configuration settings that make releases portable

| Setting / pattern | Effect |
|---|---|
| **Custom Metadata types marked Protected** | Prevents accidental deletion of config in an org — and prevents a "delete everything I did not retrieve" deploy from removing your toggles |
| **Custom Settings (hierarchy or list)** | Org-level configuration that can differ per sandbox without a code branch |
| **Custom Metadata for feature flags** | Ship dark; flip after deploy; roll back without a redeploy |
| **Named Credential metadata** | Endpoint + auth scheme live in Git; the secret lives in the org's secret store. This is what makes one package deploy to five environments |
| **External Credentials / Secret Store** | Where the secret actually lives; not in Git |
| **Protected Custom Metadata and destructive changes** | If a type is protected, a destructive change that deletes it fails the deploy instead of silently removing config |

**The anti-pattern to name in an interview:** a hardcoded endpoint or an `if (org.IsSandbox)`
branch in Apex. It creates an environment-specific branch that can never merge, and it puts a
production URL in Git.

---

## 9. Feature gates that change the release model

| Feature | Where | Effect if enabled |
|---|---|---|
| **DevOps Center** (Salesforce-native) | `Setup`, Quick Find `DevOps Center` | Work items, Git integration and promotion inside Salesforce. Native alternative to a vendor tool; does not remove the need for Git discipline |
| **Data Mask** | App Launcher → `Data Mask` | Native sandbox masking. Not installed in every org |
| **Salesforce Native Backups** | `Setup > Data > Backups` | Native metadata backup; complement to a vendor backup product |
| **Approval Processes** | `Setup > Approval Processes` | A metadata type that **forces all local tests** in a production deployment |
| **Enhanced Field Security / Field History** | `Setup > Object Manager` | Affects what a retrieve returns, and therefore what a retrieve-all would overwrite |
| **Sandbox templates** | `Setup > Sandboxes > Sandbox Templates` | The data privacy control for Partial Copy sandboxes |
| **Flow / Process Builder retirement** | `Setup > Flows`, `Setup > Process Builder` | A legacy automation still in an org is metadata you must keep deploying. Migrate deliberately, not during a release |
| **Source tracking** | Cannot be turned on in production | This is why prod config changes must go through Git |

---

## 10. Settings matrix by JD term

| JD term | Settings that implement it | Who owns them |
|---|---|---|
| CI/CD pipelines using Git workflows | `Setup > Deploy > Deployment Settings` (inbound + CLI + IP allowlist); GitHub branch protection; GitHub Environment required reviewers | Release engineer + platform team |
| Multi-environment release strategies | `Setup > Sandboxes`; sandbox naming and aliases; per-environment GitHub Environments | Release engineer |
| Scheduled releases / hotfixes / emergency | GitHub `schedule` trigger; Environment deployment rules; freeze via branch protection; change calendar | Release manager |
| Audit / security / compliance | IP allowlist; deploy identity permissions; audit trail retention; debug log retention; API usage notifications; session/password/lockout policies | Platform + security |
| Metadata lifecycle in Git | `.gitignore` for auth files; `sfdx-project.json` source API version; `package.xml`; source-tracking policy | Developers + release engineer |
| Sandbox creation / refresh / masking | `Setup > Sandboxes`; Sandbox Templates; refresh permissions; Data Mask or a vendor masking product | Release engineer + data protection |
| Deployment conflicts (profiles / permission sets) | Permission set groups; profile decomposition tooling; `Manage Profiles and Permission Sets` on the deploy identity | Salesforce admin |
| Deployment conflicts (record types / layouts) | `Setup > Object Manager` assignment rules; app assignment for Lightning record pages | Salesforce admin |
| Flows / Apex / dependencies | Apex settings (CPU, concurrency); test level; `Setup > Apex Test Execution`; 7,500-unit deployment ceiling | Developers + release engineer |
| Reducing failures / rework | `Setup > Apex Test Execution`; `Setup > Debug Logs`; `Setup > Trace Flags`; CI gates | Release engineer |
| Unlocked / managed packages | Dev Hub (`Setup > Dev Hub`); package namespace; `sfdx-project.json` `packageDirectories` | Developers + architect |
| Regulated environment | Everything in §5, plus the evidence pack in `05 §4` | Compliance |
| DevOps-friendly design patterns | Protected Custom Metadata; Custom Metadata flags; Named Credentials; Custom Settings per sandbox | Developers + architect |
| Runbooks and rollback | Release tags; CI artefact retention; `Setup > Deploy > Deployment Status` (30-day view — export to CI for longer) | Release engineer |

---

## 11. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| Exact field label for the deployment IP allowlist in the current Salesforce release | Renamed across releases | `Setup > Deploy > Deployment Settings` in the target org |
| Exact contents of `Setup > System > System Properties` in each edition | Org-dependent | Quick Find the property name in the org |
| Whether `Allow inbound deployments` and `Enable Salesforce CLI deploys` are one setting or two in the current release | Behaviour differs by org vintage | Inspect the Deployment Settings page in a non-prod org |
| Exact refresh cadence limits by licence | Not retrieved; the Salesforce Help sandbox page is client-rendered | `Setup > Sandboxes` in the org — it shows the next eligible refresh |
| Native Salesforce backup retention and scope | Not retrieved | `Setup > Data > Backups` |
