# 05 — Term-by-term deep dive

> Every JD phrase, with the **settings**, **variations**, **failure modes** and a one-line
> "say it like this" answer behind it. Numbers and platform behaviour come from `02`; vendor UI
> paths from `03`; pipeline mechanics from `04`.

---

## 1. "Design, implement, and maintain CI/CD pipelines for Salesforce using Git based workflows"

**What it actually means:** a pipeline that moves *metadata*, not code, from a branch to an org,
and stops when the metadata is wrong. The pipeline is the enforcement point for every other
control in this job.

### 1.1 The four knobs every Salesforce pipeline has

| Knob | Options | Where it lives |
|---|---|---|
| **Trigger** | PR open/update, push to branch, schedule, manual, pipeline event | GitHub Actions `on:` / Gearset CI-job trigger / Copado CI Job schedule / AutoRABIT Schedule section |
| **Payload** | source dir, manifest, metadata types, package directory | `--source-dir`, `--manifest`, `--metadata`, package.xml |
| **Test level** | `NoTestRun` / `RunSpecifiedTests` / `RunLocalTests` / `RunAllTestsInOrg` / `RunRelevantTests` | `--test-level` (+ `--tests`) |
| **Target** | org alias, target URL, environment | `--target-org`, GitHub `environment:` |

### 1.2 What "maintain" means (the part people forget)

A pipeline is a **product with a support burden**:

- **Version pinning.** Pin the Salesforce CLI version (`npm i -g @salesforce/cli@2.x.x`) so a CLI
  release does not change your deploy behaviour overnight. Record the pin in the repo, not in a
  wiki.
- **API version pinning.** The `sfdx-project.json` `sourceApiVersion` and `package.xml` `version`
  control which API semantics apply. Behaviour changed at API 33.0/34.0 (destructive change
  ordering, test-triggering metadata types) and at 65.0 (deploy cancellation in `Finalizing
  Deploy`).
- **Secret rotation.** Connected-app certificates and client secrets expire. Salesforce refresh
  tokens expire after 30 days of inactivity — Copado documents this as a credential that
  "expires with no proactive warning".
- **Runner hygiene.** Cache `~/.npm` only. **Never cache `~/.sfdx` or `~/.sf`** — they hold the
  CLI's auth state (org aliases, refresh tokens), so a restored runner can present a stale
  credential and a poisoned cache becomes a credential-injection path. A poisoned npm cache is a
  supply-chain problem; a poisoned auth cache is an authentication problem, which is worse.
- **Failure triage.** The pipeline must publish the **deployment id** as an artifact. Without it,
  the audit trail starts at "the pipeline went green".

### 1.3 The pipeline that will actually pass a bank's architecture review

| Control | Implementation |
|---|---|
| No direct push to `main` | Branch protection, required PR, required status checks |
| Segregation of duties | The pipeline identity deploys; a **named human in a different identity** approves the `prod` environment |
| No credentials in the repo | JWT cert + secrets in the CI secret store; secrets scoped per environment |
| Immutable evidence | Deployment id, test run id, coverage %, commit SHA and tag written to the change ticket |
| Reversibility | Annotated tag on every prod deploy; rollback = forward deploy of the previous tag |
| Restricted network | Org-side deployment IP allowlist for prod |

### 1.4 Say it like this

> "The pipeline is the only path into a non-dev org. Git is the source of truth, the org is a
> target, and the pipeline — not a person with Setup access — is what promotes. Every prod
> deployment carries a ticket, a validation id, a prod id, a test run, a coverage number, an
> approver who is not the author, and a tag."

---

## 2. "Manage multi environment release strategies (Dev, QA, UAT, Pre Prod, Prod)"

### 2.1 The stage table with the one fact that matters per stage

| Stage | Purpose | Org type | The fact that matters |
|---|---|---|---|
| Dev | Build + unit test | Developer / Developer Pro / scratch | Scratch orgs are **not** sandboxes: no managed packages, SSO, named credentials or production licences unless recreated |
| QA | Automated validation, integration | Developer Pro / Partial Copy | CI burns **API allocation** here — schedule it, don't run it on every PR |
| UAT | Business testers | Partial Copy or masked Full | Testers need *some* rows; a Partial Copy from a template is cheaper and safer than a Full |
| Pre-Prod | Dress rehearsal | Full or recent Partial | The only stage where **volume and performance** are meaningful |
| Prod | Customers | Production | Only one deploy runs at a time; queue order is **not** submission order |

### 2.2 Promotion strategies (the "variations")

| Strategy | How promotion works | Best when | Cost |
|---|---|---|---|
| **Forward-only (waterfall)** | Git is the only promotion path: deploy the same commit to each stage | Small team, strict audit | Slow; hotfixes need a separate path |
| **Forward + back-propagation** | After a prod change, the change is pushed back to earlier stages | Salesforce metadata genuinely diverges between stages | Two-way merge risk; needs a conflict policy |
| **Environment branching (release branches)** | Each stage has a branch; promotion = merge | Complex config, many parallel stories | Merge conflicts are constant |
| **Package promotion** | The same 2GP/unlocked package version is installed at each stage | You have already adopted packaging | Requires a package boundary and version discipline |
| **Delta / change detection** | Deploy only what differs from the target (Gearset Delta CI, CLI source tracking) | Large orgs, frequent deploys | Requires a trustworthy baseline |
| **Rebuild-from-source** | Each stage is rebuilt from `main` + release notes | Cleanest audit story | Slowest; loses stage-specific customisations |

> **The honest answer for a bank:** they will run **forward-only with a release branch**, plus
> **back-propagation only for genuine emergencies**, because bidirectional promotion in a regulated
> org creates an audit question ("which change is in prod now?") that is expensive to answer.

### 2.3 Gate design per stage

| Gate | Implementation | Evidence produced |
|---|---|---|
| PR → Dev | Required status check: validation deploy + tests | CI run id, test result |
| Dev → QA | Merge to the release branch triggers a real deploy | Deployment id |
| QA → UAT | QA sign-off recorded against the release branch commit | Sign-off + deployment id |
| UAT → Pre-Prod | Full validation in Pre-Prod; performance/smoke | Validation id |
| Pre-Prod → Prod | `checkOnly` validation, then quick deploy or full deploy in the window | Validation id + prod id |

### 2.4 Say it like this

> "Five stages, one promotion path, one direction of truth. The release branch is what QA and UAT
> deploy; developers never deploy their feature branch into UAT. Promotion is a deploy of the same
> commit, never a rebuild from someone's laptop."

---

## 3. "Coordinate scheduled releases, hotfixes, and emergency deployments"

### 3.1 Three speeds, three branch topologies

| Speed | Trigger | Cut from | Merge back to | Approval |
|---|---|---|---|---|
| **Scheduled release** | Release calendar | `main` → `release/<date>` | `main` on close | Full: ticket + window + named approver |
| **Hotfix** | Production defect, next release too late | `main` → `hotfix/<ticket>` | `main` **and** every open release branch | Full, but smaller payload and shorter window |
| **Emergency** | Active customer or regulatory harm | `main` → `hotfix/<ticket>` | `main` + open release branches | **Shortened chain, same pipeline.** Emergency is a shorter approval path, not a skipped one. |

> **The rule that prevents the classic incident:** a hotfix cut from `main` and merged only back to
> `main` will be **resurrected** by the next release branch, which was cut before the fix. Merge
> the hotfix into every open release branch, or the bug comes back.

### 3.2 Scheduled releases: the mechanics

- **Frequency.** Common bank pattern: one release train every 2–4 weeks, plus a weekly low-risk
  train for configuration-only changes.
- **Freeze.** A code/config freeze before the release branch is cut. Freeze mechanics belong in
  the branch-protection rules (no merges to `main` after freeze) and in the calendar, not in
  discipline.
- **Change ticket completeness.** The ticket must be in the release **before** the branch is cut.
  A ticket added after the cut either rides the train late (breaking the test matrix) or waits for
  the next one.
- **Payload assembly.** The release payload is the **diff between the last prod tag and the release
  branch tip**, not "whatever each developer merged". A diff-based payload makes the release
  auditable and makes the rollback payload computable.

### 3.3 Hotfix: the runbook, in order

1. Announce in the change channel with the ticket id.
2. `git switch -c hotfix/<ticket> main`
3. Reproduce, fix, **test in a sandbox** (not in prod).
4. Open a PR into `main` with the ticket id in the commit message.
5. CI validates (dry-run + tests) against a CI sandbox.
6. Validate against prod (`checkOnly`) — the prod validation, not the sandbox one.
7. Obtain approval from the named approver (not the author).
8. Deploy in the window; capture the prod deployment id.
9. **Tag** `release-<date>-<ticket>`.
10. Merge the hotfix branch into `main` and every open release branch. **Do not skip this.**
11. Update the ticket with both deployment ids, the tag, the test run and the approver.
12. Verify with one query and one screen (define both in the ticket before you deploy).

### 3.4 Emergency: what makes it different

| Dimension | Normal | Emergency |
|---|---|---|
| Branch | `hotfix/<ticket>` | Same |
| Pipeline | Full | Same |
| Approval | Named approver + window | **Pre-named on-call approver**, shorter SLA |
| Validation | `checkOnly` then deploy | `checkOnly` then deploy — **never skip validation** |
| Rollback | Tag + forward redeploy | Same, rehearsed |
| Documentation | Full evidence pack | Same — an emergency is audited **harder**, not less |

**The mistake:** treating "emergency" as licence to deploy from a laptop with a personal token.
Every emergency deploy that bypasses the pipeline creates the next emergency.

### 3.5 Say it like this

> "Three speeds, one pipeline. Emergency changes to who approves and how fast — not to what gets
> validated. A hotfix is cut from main and merged back into main **and every open release branch**,
> because otherwise the next release resurrects the bug."

---

## 4. "Ensure deployment activities follow audit, security, and compliance standards"

### 4.1 The evidence pack (what an auditor asks for)

| Item | Produced by | Where it lives |
|---|---|---|
| Change ticket id | Human | Commit message, PR title, branch name, tag annotation |
| Diff reviewed by a second person | PR review | PR record |
| Validation deployment id | `checkOnly` deploy | CI artifact + ticket |
| Production deployment id | Real deploy | CI artifact + ticket |
| Test run id + coverage % | `sf apex run test` / deploy | CI artifact |
| Named approver ≠ author | Environment protection rule | GitHub deployment record |
| Release tag | `git tag -a` annotated | Git |
| Approver identity | Human, different identity | Change record |
| Mask-complete confirmation (Full sandbox refresh) | Masking run | Refresh ticket |
| Logged-in-user list for a refreshed sandbox | Access list | Refresh ticket |

### 4.2 Segregation of duties — make it structural

| Role | Identity | Can do | Cannot do |
|---|---|---|---|
| Author | Developer | Commit, open PR | Approve own change; deploy to prod |
| Reviewer | Second developer/admin | Approve PR | — |
| Release engineer | Pipeline service account | Deploy on approval | Approve own deployment |
| Approver | Named human, GitHub environment reviewer | Approve prod environment | Write the code |
| Platform owner | Salesforce admin | Manage org config | Approve changes they authored |

**Technical enforcement:**
- The GitHub **Environment** for `prod` has required reviewers → the approving identity is
  recorded by the platform, not claimed in a ticket.
- The Salesforce integration user **cannot** be a human's personal credential. It is a named
  integration user with a dedicated permission set.
- Branch protection requires the PR review and the CI check.

### 4.3 Compliance controls that are org settings, not good intentions

See `07-system-properties-setup-paths.md` for the Setup paths. The ones that matter most:

| Setting | Why it matters for compliance |
|---|---|
| Deployment IP allowlist (prod) | Only the CI runner can deploy |
| API Usage Notifications | Early warning of runaway automation |
| Session timeout / IP relax | Limits for a stolen session |
| Password policies, lockout policy | Credential brute-force control |
| Audit trail retention | Determines how far back you can prove something |
| Debug log retention | Debug logs contain field values — a data-leak surface, not just a troubleshooting tool |
| Org-wide "Allow Users to View All Data" | Test and integration users should not see all data |
| API Enabled per profile | Least privilege for the integration user |

### 4.4 Say it like this

> "I make segregation of duties structural rather than cultural: the pipeline identity deploys, a
> named human in a different identity approves, and the platform records both. Every prod deploy
> leaves a ticket, two deployment ids, a test run, a coverage number and a tag — and that pack is
> what I hand the auditor."

---

## 5. "Manage Salesforce metadata lifecycle using source control (Git)"

### 5.1 The lifecycle, step by step

| Step | Command / action | Artefact |
|---|---|---|
| 1. Retrieve | `sf project retrieve start --metadata <Type:Name> --target-org <org> --output-dir <dir>` | XML in the working tree |
| 2. Review | `git diff` | Reviewable diff — **the whole point** |
| 3. Commit | `git commit -m "<TICKET> <description>"` | Traceable commit |
| 4. Validate | `sf project deploy start --dry-run --target-org <ci>` or `sf project deploy validate` | Validation deployment id |
| 5. Deploy | `sf project deploy start --target-org <target>` | Deployment id |
| 6. Tag | `git tag -a release-<date> -m "<ticket>"` | Rollback target |
| 7. Roll back | `git checkout <previous-tag>` then forward-deploy | New deployment id |

### 5.2 What to commit and what never to commit

| Commit | Never commit |
|---|---|
| Custom objects, fields, validation rules | `.sfdx/`, `.sf/`, auth files |
| Flows, Apex, LWC, Aura, Visualforce | OAuth refresh tokens, JWT private keys, client secrets |
| Permission sets, permission set groups | Certificates, keystores |
| Custom metadata **definitions** (not secret **values**) | Sandbox-only endpoints hardcoded in code |
| Named credential **metadata** (not the secret) | Retrieved junk: profile user lists, full `*.profile` dumps |
| `package.xml` / `sfdx-project.json` | Production data, CSV exports, debug logs |

**Named Credentials are the pattern:** the *metadata* (endpoint, auth scheme) lives in Git; the
*secret* lives in the org's External Credentials / Secret Store. That is what makes the same
package deployable to five environments.

### 5.3 Source tracking — what it does and when it helps

| Concept | Behaviour |
|---|---|
| Source tracking | Salesforce records which components came from which local files, so `sf project deploy start` can deploy **only what changed** |
| Where it is enabled by default | Scratch orgs and sandboxes. **Production orgs never allow source tracking.** |
| How to disable it | `sf org create scratch --no-track-source` / `sf org create sandbox --no-track-source` |
| What it buys you | Fast incremental deploys in dev; a "who edited this in the org" signal |
| What it costs you | In dev, a change made **in the org UI** silently exists only in the org until someone retrieves it. That is how "works in sandbox, vanishes in Git" happens. |

**Policy:** in dev and QA, either disable source tracking or run a scheduled "retrieve and diff"
job that reports org-side drift. In prod, source tracking is off, so **the only** way a prod
config change happens is a deploy — enforce that with a permission set, not a policy document.

### 5.4 Branching topology (detailed)

```
main                    ← tag: matches production
├─ hotfix/<ticket>      ← cut from main; merges to main + every open release branch
└─ release/<date>       ← cut from main at freeze
   └─ feature/<ticket>  ← cut from release/<date>; short-lived
```

Rules:
- Feature branches live **days**, not weeks. Salesforce XML (Flows, profiles, layouts) does not
  merge; a long-lived branch becomes "keep one side and hope".
- The **release branch** is what QA and UAT deploy.
- Tag production after a successful deploy.
- Commit messages carry the change-ticket id. That is the audit trail.

**GitHub branch protection that makes this real:**

| Setting | Value |
|---|---|
| `Require a pull request before merging` | On; require review; dismiss stale reviews |
| `Require status checks to pass` | The validation check; require branches up to date |
| `Require conversation resolution` | On |
| `Require signed commits` | If the bank's policy demands it |
| `Do not allow bypassing the above settings` | On — this is the one that stops the "admin pushes straight to main" pattern |
| `Restrict who can push` | Release engineers only |

### 5.5 Say it like this

> "Git is the source of truth; the org is a deploy target. If Setup and Git disagree, that is an
> incident, not a workflow. I retrieve, review the diff, commit with the ticket id, validate, deploy,
> tag. Production never allows source tracking, so in prod the only path in is a deploy."

---

## 6. "Handle sandbox strategy (creation, refresh, data masking)"

### 6.1 Sandbox types (the table to memorise)

| Type | Metadata | Data | Use for | Licence constraint |
|---|---|---|---|---|
| **Developer** | Yes | No | Isolated build | Cheapest; smallest storage |
| **Developer Pro** | Yes | No | QA when you do not need rows | More file/storage room |
| **Partial Copy** | Yes | A template sample | UAT with some rows | Refreshes from a template you define |
| **Full** | Yes | **All of production** | Pre-prod, performance, volume | Slowest; **carries customer data** |
| **Scratch org** (not a sandbox) | From a definition file | No | Package builds, disposable CI | Needs a Dev Hub; no managed packages/SSO/licences unless recreated |

**The trap:** "UAT is a scratch org". In a commercial-banking org with managed packages, SSO, named
credentials and licences, a scratch org is not a substitute unless someone encoded all of it.

### 6.2 Refresh constraints

| Constraint | Detail |
|---|---|
| Cadence | Licence-limited; refresh eligibility is visible in `Setup > Sandboxes` |
| Full refresh | Slowest; **do not promise a same-day Full refresh** in an interview |
| Partial refresh | Refreshes from a template, not from prod |
| Refresh destroys customisations | Any direct change made in the sandbox since the last refresh is lost — hence the "Git is the truth, sandbox is disposable" rule |
| In-flight work | Re-sync the environment branch and redeploy after a refresh |

### 6.3 Data masking — the control, not the feature

| Step | Detail |
|---|---|
| 1 | Refresh the sandbox |
| 2 | **Restrict logins.** Until masking is confirmed, only the people named on the ticket may access it |
| 3 | Mask | Mask the fields that carry customer identity: name, email, phone, address, SSN/SIN, date of birth, account number, description/notes free text |
| 4 | Repoint integrations | Named credentials / endpoints must point at non-prod **before** anyone logs in |
| 5 | Confirm | Record mask-complete, time, who confirmed, and the access list in the refresh ticket |
| 6 | Audit | Treat the masked sandbox as containing production-shaped data — it still has real account structures, real values in unmasked fields, and real attachments |

**Which fields must be masked in a Canadian bank:** government identifiers (SIN), account and
card numbers, customer names, addresses, email, phone, date of birth, account balances,
transaction details, free-text notes and attachments. "Free text" is the one people forget —
`Description` and `Notes` fields are where PII hides.

### 6.4 Tool support (detail in `03`)

- **Gearset:** `Sandbox seeding` → `Configure and deploy` → `Configure in-place masking`; default
  sensitive-field classification; masking templates reusable across seeding/in-place/data deploy.
- **AutoRABIT:** Vault → `Masking Rules` (global) and `Live Data Masking` (JOB CONFIG → NEW CONFIG
  → Object Info → rules); `Config Details` can disable workflows, validation rules, triggers and
  flows during masking; rollback window 7 days.
- **Salesforce:** Data Mask (App Launcher → Data Mask, after the managed package is installed) — not
  assumed in every org.
- **Copado:** **no masking product** (see `03 §2`). Data Deploy is a different thing.

### 6.5 Say it like this

> "Sandboxes are disposable and Git is the truth, so a refresh destroys nothing important. A Full
> copy carries production data, so masking is a **gate**, not a chore: logins are restricted to the
> ticket's names until mask-complete is confirmed, endpoints are repointed before anyone connects,
> and the confirmation is in the refresh ticket."

---

## 7. "Resolve deployment conflicts"

### 7.1 Profiles and Permission Sets

**Why profiles conflict:** `Admin.profile` is a single XML file containing object permissions,
field permissions, layout assignments, record-type visibility, user licence and **the user
assignment list**. Two stories touching it produce a textual conflict, and a bad manual merge can
silently grant or revoke access that nobody reviewed.

**The resolution pattern:**

1. Classify the change: *business access* (→ permission set) vs *profile-only setting* (layout
   assignment, login hours, user assignment) vs *licence*.
2. Business access becomes a **permission set per persona or per feature**, not a profile edit.
3. Where the bank still deploys profiles, deploy a **thin delta** with a tool that supports profile
   decomposition, and require a second reader on the permission diff. Never hand-merge a
   10,000-line profile.
4. Bundle for a job function with a **permission set group**.

**Permission set groups** are the modern answer: one group contains multiple permission sets,
assigned to users like a single object. The release-engineering benefit is that a feature's access
lands as one deployable unit.

**The deploy identity's permissions (also a conflict source):** a permission set granting
`Modify All Data` to the integration user is itself metadata. It must be deployed like everything
else, and reviewed like everything else.

**Failure mode to watch:** a profile deploy that strips a permission because the target's profile
had drifted (someone edited it in the UI). The diff that shows it is the artefact you need — that
is why profiles need a second reader.

### 7.2 Record Types and Page Layouts

**The assignment chain — all of it must be in one payload:**

```
Custom Object
 └─ Record Type
     ├─ Business Process (picklist values it depends on)
     ├─ Picklist values on the status/Type field
     ├─ Page Layout (classic Layout assignment)
     ├─ Lightning Record Page (FlexiPage) for the app
     └─ Visibility: Profile or Permission Set (record type + layout assignment)
```

**Symptoms and causes:**

| Symptom | Cause | Fix |
|---|---|---|
| `Invalid cross reference id` on deploy | Business process or picklist values missing | Deploy the dependencies in the same payload |
| Deploy succeeds, users cannot create the record type | No layout assignment, or no record-type visibility on their profile/permission set | Deploy record type + layout + permission set together |
| Classic layout is right, the screen is wrong | The **Lightning record page** (`FlexiPage`) was never activated for the app | Deploy/activate the `FlexiPage`, and check app assignment |
| Users see the field but cannot edit it | Field-level security is not in the permission set | Add the field permission to the same permission set |
| The layout reverts after the next release | A profile in another release overwrote the layout assignment | Move the assignment to a permission set |

**The rule:** the record type, the layout, the business process and the permission set are **one
deployable unit**. "We deployed the record type on Monday and the permission set later" is exactly
how a release leaves a broken feature in production.

### 7.3 Flows, Apex, and dependencies

**Flows:**

| Rule | Detail |
|---|---|
| Flow XML does not merge | Two developers editing the same flow will lose one side |
| One owner per flow per release | Or split into subflows and compose |
| Draft vs Active | A deploy can leave the new version **Draft** — users see the old behaviour and the deploy was "successful". Check what your tool does; verify in a sandbox |
| Fast mitigation | Activate the previous version in `Setup > Flows` — a **mitigation**, not a rollback |
| Before-save vs after-save | A before-save requirement built as after-save will time out under volume. A flow you cannot describe is a flow you should not deploy |
| Flow test coverage | The metadata type `Flow` is on the list that **forces all local tests to run** in a deployment |

**Apex:**

| Rule | Detail |
|---|---|
| Class + test + dependencies in one payload | A class calling a class you did not retrieve fails to compile in the target |
| Tests create their own data | `SELECT Id FROM Account LIMIT 1` and assume a row exists → passes in dev, fails in an empty QA sandbox |
| Coverage is per class/trigger | Each needs ≥75% under `RunSpecifiedTests` / `RunRelevantTests` |
| Bulkification is a release concern | A deploy can be green and the feature can still fall over on 200 records. The review question is "what happens when this runs on 200 records?" |
| Deployment ceiling | **7,500 class/trigger code units per deployment** |
| Trigger batch size | 200 (2,000 for platform events and CDC) |
| Recursion depth | 16 levels of trigger-firing recursion |
| 6 MB total Apex code in the org | 10 MB in scratch; raisable via support case |

**Dependency resolution order for a payload:** object → fields → record types → validation rules →
layouts → permission sets → Apex → Flows → approval processes → workflows.

### 7.4 Say it like this

> "Profiles do not merge and a bad profile merge changes access nobody reviewed, so business access
> ships as permission sets. A record type, its layout, its business process and the permission set
> that grants visibility are one payload. Flow XML does not merge, so one flow owner per release.
> And the two questions I ask in every code review are: does the test create its own data, and
> what happens when this runs on 200 records?"

---

## 8. "Recommend best practices to reduce deployment failures and rework"

| Practice | Failure it prevents | How to enforce |
|---|---|---|
| One payload per release unit | Partial deployments that "succeed" but leave an unusable feature | Manifest/package per unit; CI validates the same payload |
| Thin profiles | Merge conflicts and unreviewed access changes | Permission sets; profile decomposition tool |
| Small permission sets | The same conflict in a different file | One permission set per persona/feature, not one `CB_Admin` |
| One flow owner per release | Lost XML | Release branch has a flow ownership register |
| Tests create their own data | Green in dev, red in UAT | CI runs against an empty sandbox at least once |
| No hardcoded IDs | Environment-specific bugs | Custom Metadata / Custom Settings |
| Named Credentials for callouts | Wrong endpoint in prod | Secret Store + per-org credentials |
| Config toggles in Custom Metadata | Redeploy to turn a feature on | Ship dark, enable after deploy |
| Bulkified Apex | Runtime failure after a green deploy | Code review + static analysis |
| One deployment at a time | Queue-order surprises | Serialise prod promotions |
| Validate before the window | Window overruns | `checkOnly` earlier in the day/week |
| Tag every prod deploy | No rollback target | `git tag -a` in the release job |
| Minimal payload | Deploy time and blast radius | Diff-based payloads, `--metadata` filters |

**The meta-practice:** *reduce the number of files two stories touch.* Every conflict is a file two
people edited. A monorepo of Salesforce XML will always conflict; the fix is structure, not
discipline.

---

## 9. "Partner with Salesforce Developers, Admins, QA, and Platform teams"

| Partner | What they need from you | What you need from them |
|---|---|---|
| **Developers** | A pipeline that fails fast with a readable error; a stable branch model; permission sets instead of profile asks | Tests that create their own data; no admin config inside a story |
| **Admins** | Permission sets they can assign; config-as-metadata; a change calendar | Admin changes captured in Git, not made directly in prod |
| **QA** | A deployment to test that they can identify by commit SHA; a known-good baseline | A test plan tied to the release; defect triage that names the component |
| **Platform teams** | A pipeline that respects network restrictions and API budgets | IP allowlists, runner network access, secret rotation |
| **Security / compliance** | Evidence packs; least-privilege deploy identities; no prod data outside prod | A named approver who is available in the window |

**The handoff artefact that matters:** a **release note per deploy** that a QA lead can act on
without reading the diff — ticket id, component list, feature flags flipped, what to test, what
changed for users, what to revert if it breaks.

---

## 10. "Provide guidance on DevOps friendly Salesforce design patterns"

| Pattern | Deployability consequence | Review rule |
|---|---|---|
| Permission sets over profile edits | Profiles do not merge | Reject a story whose only change is an `Admin.profile` field permission |
| One flow owner per release; subflows for parallel work | Flow XML does not merge | No two stories in the same flow |
| Tests create their own data | Empty and prod-like sandboxes behave the same | No `SELECT ... LIMIT 1` + assume |
| No hardcoded IDs | IDs differ per org | Custom Metadata / Custom Settings |
| Named Credentials for callouts | Endpoints differ per sandbox | No endpoint literals in code |
| Custom Metadata / Custom Settings for toggles | Ship dark, enable after deploy | A feature is never enabled by a deploy alone |
| Bulkified Apex | A green deploy can still fall over in production | "What happens at 200 records?" |
| No environment-specific branches | `if (org.IsSandbox)` branches never merge | Config in the target, not in the branch |
| Feature flags as Custom Metadata + Apex service | Rollback without a redeploy | Flag defaults false in prod |
| Unlocked packages for real module boundaries | Makes a boundary reviewable and upgradeable | Do not "package the whole org" on day one |
| Protected Custom Metadata | Prevents accidental deletion of config in an org | Mark config types as protected |

---

## 11. "Document release processes, runbooks, and rollback procedures"

### 11.1 The runbook fields (expanded from the existing page's template)

| Field | Filled by | Notes |
|---|---|---|
| Change ticket | Requester | Must be in the release before the branch is cut |
| Release tag / source branch / commit SHA | Release engineer | The rollback anchor |
| Payload (package dir or manifest) | Release engineer | The exact artefact that was deployed |
| Validation org + validation deployment id + time | Pipeline | Evidence the payload compiles |
| Tests run and coverage % | Pipeline | Per class, not just overall |
| Prod deployment id + time | Pipeline | |
| Approver (not the author) | Named human | Enforced by the GitHub environment |
| Feature flags / config to flip after deploy | Developer | The post-deploy checklist |
| Sandbox or flags to restore | Release engineer | |
| Rollback tag | Release engineer | Must exist before the deploy starts |
| Rollback owner | Named human | Different from the deployer if possible |
| **Verification** (one query, one screen, one test) | QA | Written **before** the deploy |
| **Data scripts run and their reverse script** | Developer | A Git revert does not undo rows |

### 11.2 Rollback decision tree

```
Deploy produced a bad state
├── Is the metadata still recoverable from a tag?
│   ├── Yes → forward-deploy the last good tag (a NEW deploy, recorded)
│   └── No  → you have no rollback. This is why tagging is mandatory.
├── Is it a Flow version problem and is the previous version still in the org?
│   └── Activate the previous version (MITIGATION) → then still forward-deploy the tag
├── Is it Apex / config?
│   └── Stop the bleeding (deactivate the automation if safe) → validate → deploy the tag
├── Did a destructive delete already run?
│   └── Metadata can be recreated from Git. RECORDS ON A DELETED OBJECT ARE GONE.
│       Data restore is a separate ticketed path (backup tool), not a Git revert.
└── Did a post-deploy data script run?
    └── Git revert does not undo rows. The script needs its own reviewed reverse script.
```

### 11.3 Say it like this

> "Rollback is a forward deploy of the last known-good tag, not a magic button. So before a prod
> deploy I verify the tag exists, the payload is recorded, the reverse data script is reviewed, and
> the verification query and screen are written down — because during an incident nobody invents
> them."

---

## 12. "Support audit and change management requirements"

| Requirement | How release engineering satisfies it |
|---|---|
| Traceable change | Ticket id in commit, branch, PR, tag, deployment record |
| Separation of duties | Different identities for author, deployer, approver |
| Reproducibility | The exact payload artefact + commit SHA + API version stored |
| Evidence of validation | Validation deployment id, test run id, coverage |
| Change control | Named approver, window, calendar, freeze rules |
| Emergency procedure | A written, rehearsed path — not improvisation |
| Retention | Org audit trail retention; Git repository retention; backup retention (7 years for records in Gearset, indefinite for metadata snapshots) |
| No data leakage | No prod data in tickets, slides, debug logs, or unmasked sandboxes |
| Periodic access review | The deploy identity's permissions reviewed on a cadence |
| Evidence that the change was tested | Test results tied to the deployed commit |

**What the release engineer supplies to the change-management system:** the ticket, the plan, the
impact assessment (which orgs, which components, which users), the rollback plan, the test
evidence, and the post-implementation verification.

---

## 13. "Experience with Unlocked Packages / Managed Packages"

| Kind | Who owns it | Deploy mechanism | Release-engineering notes |
|---|---|---|---|
| **Unlocked package** | Your team | `sf package version create` → `sf package install` | Versioned, upgradeable, has a dependency list. Best when a boundary is real (a credit-application module), not "all of Sales Cloud". **10,000-file ceiling** |
| **Org-dependent unlocked package** | Your team, but coupled to unpackaged metadata in the org | Same | Faster to adopt, harder to install elsewhere. Say the limitation out loud |
| **2GP managed package** | ISV or a hard IP boundary | `sf package install` with a `04t` version id | You **upgrade** it; you do not edit its Apex in Git |
| **1GP managed package** | Legacy ISV | Same | 35,000-file ceiling, only if AppExchange Security Review passed |

**The commands:**

```
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```

The `04t` id is the package version. Promote that version before production. **Never install a beta
package version into prod.**

**Certified managed package namespaces get their own governor limits** (plus a cumulative
cross-namespace ceiling of 1,100 SOQL / 1,650 DML). An unlocked package does **not** — its usage
counts against the org's limits. That is a capacity-planning fact, not trivia.

**Practical position:** unpackaged metadata deployed from Git is still the right default for a large
existing commercial-banking org. Packaging is how you stop the folder becoming one unreviewable
tree. "Package the entire org on day one" is not a plan.

---

## 14. "Exposure to Salesforce DX"

| DX concept | What it gives you | Release-engineering use |
|---|---|---|
| `sfdx-project.json` | Package directories, source API version, namespace | The project's contract |
| `package.xml` (manifest) | Explicit component list | The deployable unit; makes the payload reviewable |
| `sfdx-project` / `force-app` layout | Metadata in source format | What every deploy tool expects |
| Source tracking | Org ↔ file provenance | Incremental deploys in dev; **off in prod** |
| Scratch orgs | Disposable org from a definition file | CI test target; package builds |
| `sf org login jwt` | Non-interactive auth with a certificate | The CI auth model |
| `sf project deploy preview` | Shows what *would* be deployed and deleted, plus conflicts | Pre-deploy diff without a deploy |
| `sf project deploy validate` | Validation-only deploy | The `checkOnly` equivalent as a first-class command |
| `sf project deploy quick` | Quick deploy from a validation | The fast path into the window. Uses `--job-id`, **not** `--deploy-id` |
| `sf project deploy report` | Re-reads the status of a running/finished deploy | Uses `--job-id`; add `--coverage-formatters`/`--junit`/`--results-dir` for test artefacts |

**CLI commands a release engineer should know cold:**

```
sf org login jwt --client-id <id> --username <u> --jwt-key-file <cert.pem> --instance-url <url> --alias <name>
sf project retrieve start --metadata <Type:Name> --target-org <org> --output-dir <dir>
sf project deploy preview --target-org <org>
sf project deploy validate --manifest package.xml --test-level RunLocalTests --target-org <org> --wait 30
sf project deploy start --manifest package.xml --target-org <org> --wait 30
sf project deploy quick --job-id <id> --target-org <org> --wait 30
sf apex run test --test-level RunLocalTests --code-coverage --result-format human --wait 30 --target-org <org>
sf data query --query "SELECT Id FROM Account LIMIT 1" --target-org <org>
```

---

## 15. "Experience in regulated or enterprise environments (banking, insurance, healthcare)"

| Regulatory pressure | Release-engineering consequence |
|---|---|
| Change control | Every deploy traces to an approved ticket; freeze windows; emergency procedure documented |
| Segregation of duties | Structural identities, not policy |
| Data protection | Masking as a gate; no prod data in lower environments; no debug logs in tickets |
| Evidence retention | Git, CI artifacts and org audit trail retained per policy; record backups 7 years where the vendor supports it |
| Least privilege | Deploy identity with a narrow permission set; quarterly review |
| Availability | Deploy off-peak; never deploy during a business-critical batch window |
| Vendor/third-party risk | Managed packages upgraded on a controlled cadence, not opportunistically |
| Reproducibility | Exact payload, API version and CLI version pinned |

**What is different in a bank from a commercial org:** the change window, the named approver, the
masking gate, the evidence pack, and the fact that an emergency still goes through the pipeline.

---

## 16. "Good understanding of Apex & Triggers" / "Salesforce Platform Developer experience"

What the release engineer needs from Apex, even if they do not write it:

| Concept | Release relevance |
|---|---|
| Triggers | Order of execution; before/after; recursion (16 levels); bulkification; trigger batch size 200 |
| Governor limits | The production capacity model — `02 §2` |
| Test coverage | Per class/trigger ≥75%; tests create their own data |
| Deployment | Class + test + dependencies in one payload; 7,500 code-unit ceiling |
| Async | 250,000 async executions/day floor; 5 concurrent batch jobs; 60,000 ms async CPU |
| Managed package Apex | You cannot edit it; you upgrade it |
| LWC / Aura | Bundle metadata; `Customize Application` permission needed to deploy |
| Integration | Named Credentials; callout timeout 10 s; 6 MB/12 MB payload ceiling; 100 callouts per transaction |

**The review questions a release engineer asks** (and should be able to ask out loud):

1. "What happens when this runs on 200 records?"
2. "Does this test create its own data?"
3. "What does this trigger do when it fires recursively?"
4. "Which metadata types does this deployment touch, and do any of them force a full local test run?"
5. "What is the rollback if this behaves differently in production?"

---

## 17. Quick reference — the "say it like this" answers, collected

1. **Where is the source of truth?** Git. Production is a deploy target. If Setup and Git disagree,
   that is an incident, not a workflow.
2. **Walk a change to prod.** Feature branch → PR with ticket id → CI validation → merge to the
   release branch → QA → UAT → `checkOnly` against prod → approval → quick deploy or full deploy →
   tag → ticket updated with both deployment ids.
3. **Hotfix during an open release?** Cut from `main`; merge back to `main` **and** the open
   release branch.
4. **Why did this profile deploy scare you?** Profiles are a grab bag of access; two stories
   conflict; a bad merge changes access nobody reviewed. Prefer permission sets.
5. **Flow deployed but users see the old screen.** The new version is probably not active. Check
   that before redeploying.
6. **Validate vs quick deploy?** Validate changes nothing. Quick deploy applies a validation that
   already passed, inside the window — and is only honest if nothing changed in the target since.
7. **Unlocked vs managed?** Unlocked is yours and versioned. Managed is something you upgrade.
8. **What do you hand an auditor?** Ticket, reviewed diff, approver who is not the author,
   validation id, prod id, test run, coverage, tag — and mask-complete evidence for any Full
   sandbox refresh.
9. **What is the deployment payload ceiling?** ≈39 MB compressed (base64 payload ≤50 MB),
   ≈600 MB uncompressed, 10,000 files for unlocked/2GP packages.
10. **Why does only one deploy run at a time?** Because queued deployments are not guaranteed to
    run in submission order. Serialise prod promotions.
11. **What are the test levels?** Five, not four: `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`,
    `RunAllTestsInOrg`, `RunRelevantTests` (Beta).
12. **Which packages force all local tests to run?** Anything containing Apex, Flow, PermissionSet,
    Profile, CustomField, CustomObject, RecordType, Validation Rule, Workflow, and 20 other types.
    A reports-only package runs zero tests.
13. **Which credential do I give the pipeline?** A named integration user with `API Enabled`,
    `Modify Metadata Through Metadata API Functions` (per-type) or `Modify All Data`, plus
    `Customize Application` for Flow/LWC/custom metadata. Never a human's password.
