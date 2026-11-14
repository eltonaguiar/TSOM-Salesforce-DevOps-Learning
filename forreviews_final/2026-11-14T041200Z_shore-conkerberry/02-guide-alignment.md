# 02 — Guide alignment: the five live Salesforce pages vs the review corpus

**Source of truth:** the live published pages under
<https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/#available-guides-1>
All five were read directly for this review (2026-11-14).

| # | Page | Path | Audience |
|---|---|---|---|
| 1 | Salesforce Crash Course | `docs/salesforce/crash-course/` | Complete beginners |
| 2 | Navigation & Breadcrumbs | `docs/salesforce/navigation-breadcrumbs/` | Admins/devs doing a task |
| 3 | Labs & Design | `docs/salesforce/labs-design/` | Learners doing 4 labs |
| 4 | User Management & Data | `docs/salesforce/user-management-data/` | Admins managing users/data |
| 5 | DevOps & Release Engineering | `docs/salesforce/devops-engineer/` | Release engineers (the target) |

---

## 1. Already absorbed — do not re-merge

The DevOps page (#5) is already comprehensive. It covers, on the live page:

- Source of truth / Salesforce DX / `sf` retrieve+deploy
- Metadata that breaks releases (failure string → cause → check)
- Five environments + sandbox types + masking discipline
- Branching (`main` / `hotfix` / `release` / `feature`)
- CI/CD four-stage model + JWT auth + `--test-level` values
- DevOps tools (CLI, DevOps Center, Gearset, Copado, AutoRABIT, Change Sets)
- Conflict clinic (profiles, permission sets, record types, layouts, Flows, Apex)
- Packages (unlocked / org-dependent / managed)
- Tests & validation (dry-run vs quick deploy vs real deploy)
- Releases, hotfixes, emergency, runbook template, rollback
- Banking change control / audit pack
- Design patterns to coach
- Labs A–E, interview drills, certifications, quiz

Everything in `forreviews/` that restates these is **already absorbed**. The review corpus is
research *for* this page; it is not new page content.

---

## 2. Real corrections still worth making

These are factual issues on the live pages. After the
`2026-11-14T030820Z_salesforceagain/03-defect-register.md` work, the residual set is small.
Confidence noted per item; verify against the Apex Developer Guide before publishing a number.

### 2.1 Crash Course — heap size row is internally inconsistent *(high confidence)*

The governor-limits table lists:

- `Heap size | 6 MB (sync) / 12 MB (async)`
- `CPU time | 10,000 ms (sync) / 60,000 ms (async)`

The async CPU figure (60,000 ms) matches current platform limits, but the heap figure is widely
cited today as **10 MB sync / 25 MB async**. A page that quotes the current CPU limit next to an
older heap limit is inconsistent. **Action:** verify against
<https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html>
and if 10/25 is confirmed, update the table, the "Heap Size" heading, and the
"where the heap limit doubles to 12 MB" sentence (10 → 25 is 2.5×, not 2×).

### 2.2 Crash Course — the debug-log path contradicts the row above it *(high confidence)*

The navigation table contains two adjacent rows:

- `Debug Logs | Setup > Debug Logs`
- `System Log / Apex Logs | Setup > Monitor > Logs > Debug Logs`

`Monitor` was retired; `System Log` is not a current destination. The breadcrumbs page (#2) already
uses `Setup > Debug Logs` in both places. **Action:** change the second row to `Setup > Debug Logs`
(one-line fix; removes a self-contradiction a beginner hits on their first log task).

### 2.3 Crash Course — Batch Apex "2,000" conflates two different limits *(medium confidence)*

`Batch Apex batch size | 200 default | Max 2,000 records per batch` — the 2,000 figure belongs to
platform-event / Change Data Capture trigger batches, not Batch Apex `Database.QueryLocator` scope.
**Action:** split the row; a trigger author and a batch author need different numbers.

### 2.4 Labs & Design — "Important System Properties" mixes real settings with internal flags *(medium confidence)*

Rows such as `apex.pageLimit` are internal/undocumented flags, not admin-configurable settings.
Presenting them next to `session.timeout` and `login.lockout` implies parity that is not real.
**Action:** drop the internal flags or move them to a clearly-labelled "internal/likely-unstable" note.

### 2.5 Labs & Design — Deployment Options table predates the merge tools *(low severity)*

It lists Change Sets, CLI, Metadata API, Ant, DevOps Center. Ant is legacy and the vendor tools are
covered on page #5. **Action:** add a one-line pointer to the DevOps track so readers do not stop at Ant.

### 2.6 DevOps page — small omissions worth adding *(medium confidence)*

Not defects, but gaps a commercial-banking release engineer will be asked about:

| Gap | Why it matters |
|---|---|
| **One deploy at a time per org** | Metadata API serialises deployments; a second concurrent deploy fails. Banks with several streams hit this. |
| **Deploy ceiling / component count** | Large payloads time out or exceed metadata caps; explains why releases are split. |
| **Gearset does not refresh sandboxes** | Sandbox refresh is a Salesforce operation, not a compare tool. Prevents a wrong interview answer. |
| **Debug-log data-leak surface** | The page mentions turning logs off in change control; elevate it to a checklist item under troubleshooting. |

### 2.7 User Management & Data — one framing gap *(high value, low effort)*

The page is technically correct but never states the single most important fact for a release
engineer: **profiles do not merge**. **Action:** add one sentence in the Profiles section pointing
to the DevOps conflict clinic.

---

## 3. Reject / do not merge

| Claim in corpus | Verdict | Reason |
|---|---|---|
| "1% per class minimum coverage" (`salesforcemore`, `salesforcemore-v3`) | **Reject** | No such rule. Production gate is 75% and is computed per class/trigger. |
| Vendor click-path dumps as new pages | **Reject as new pages** | Button labels drift by edition/release; page #5 already keeps them at category level. Keep only as `[Verify]`-tagged notes. |
| Merging PR #1 / #2 as new trees | **Reject** | Content already on `main`; a second copy recreates the duplication. |
| Publishing the private key as a CI artifact (`04-cicd-github-salesforce.md`) | **Reject outright** | Credential exposure; must never appear in a published workflow. |
| Caching `~/.sfdx` / `~/.sf` in CI | **Reject** | CLI auth state; stale/poisoned cache is a credential-injection path. |

---

## 4. Alignment summary

| Page | Needs correction | Needs addition | Status |
|---|---|---|---|
| Crash Course | 2.1, 2.2, 2.3 | deploy-identity user class; `Setup > Deploy > Deployment Settings` | **Patch** |
| Navigation & Breadcrumbs | — | Deployment Settings detail | **Minor add** |
| Labs & Design | 2.4, 2.5 | — | **Patch** |
| User Management & Data | — | "profiles do not merge" sentence | **One sentence** |
| DevOps & Release Engineering | — | 2.6 four platform facts | **Minor add** |

The pages are in good shape. This is a redline pass, not a rewrite.
