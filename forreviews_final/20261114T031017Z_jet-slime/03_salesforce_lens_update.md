# 03 — Update: the review re-read through the Salesforce training guides

Source: `eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` — the five
Salesforce guides (Crash Course, Navigation & Breadcrumbs, Labs & Design, User Management & Data,
DevOps & Release Engineering). Used as a **rubric**, not as product docs. Each section names the
guide, the principle, and what it changes about the `jet-slime` review.

The repo is a Python trading/event platform, not a Salesforce org, so each principle is applied by
**analogy** — the control is the same, the artifact differs. The mapping is stated every time so a
reviewer can reject an analogy they disagree with.

---

## 1. Crash Course → least privilege, Named Credentials, governor limits, bulkify

| Salesforce principle (Crash Course) | `jet-slime` analog | Verdict |
|---|---|---|
| **Named Credentials — never hardcode URL/password** | `dbpasses.txt` keys are read at runtime, never committed; endpoints live in the script | ✅ already correct — the new tools read `$HOME/dbpasses.txt`, not the repo. Keep it. |
| **Least privilege** (don't give everyone System Administrator) | The proxy exports ~40 provider keys into one process env | ⚠️ broad by design, but see L-02 (file perms / rotation). |
| **Governor limits are per-transaction resource caps** | Probe tools make one network callout per model × per provider | L-07: treat free-tier daily caps (OpenRouter 50/day) as the governor limit. Batch / `--no-probe`. |
| **Bulkify — don't query/DML/callout in a loop** | `free_model_discovery.py` / `free_provider_audit.py` loop callouts | same as L-07; use a thread pool with a cap (the audit tool already uses `ThreadPoolExecutor` — good — but discovery should too). |
| **Debug logs / "why did it fail"** | The `[REDACTED]`/zero-match `parse_key` class fails **silently** | L-03: the Crash Course's "Debug Logs" section is exactly the missing control — add a startup assertion. |

**Net change to the review:** confirms F-03 (parse_key zero-match) is the highest-value fix, and
reframes it as "the deploy that succeeds but the feature falls over" — the Crash Course's governor-limit
warning applied to config loading.

---

## 2. User Management & Data → secrets at rest, masking, data integrity

| Principle (User & Data guide) | `jet-slime` analog | Verdict |
|---|---|---|
| **Shield Platform Encryption / FLS — protect sensitive fields** | `dbpasses.txt` holds ~40 plaintext provider keys in `$HOME` | **L-02 (new):** this is the "unmasked Full sandbox" of the repo. Enforce `chmod 600`, and rotate (ties to the 5 monthly `[Security] Secret Rotation` issues + the OpenRouter key that surfaced in terminal output per FREEBUFF chatlog §7). |
| **Duplicate Management — block dupes at save** | Two `parse_key` labels → one env var (F-02) | The guide's "Duplicate Rules" analog: detect two labels mapping to one credential and **block/warn**, don't silently last-win. |
| **Data Integrity — required fields, validation rules** | `parse_key` should require exactly one match per label | same as L-03. |
| **Import/Export — know your source of record** | `dbpasses.txt` is the source of record for credentials | ✅ correct that it lives outside Git; the review should state that explicitly so nobody "helpfully" commits it. |

**Net change:** adds **L-02** (credential file hygiene + rotation) and reinforces **F-02** as a
duplicate-management problem, not just a logging nit.

---

## 3. Navigation & Breadcrumbs → deployment paths exist, use them

The guide's **Deployment & DevOps** breadcrumb table (Sandboxes, Deploy > Deployment Status, Deploy >
Change Sets, Apex Test Execution) is a checklist of *stages that must exist*. The repo's analog:

| Salesforce breadcrumb | Repo analog | Gap |
|---|---|---|
| Setup > Sandboxes (Dev/QA/UAT/Pre-Prod) | local dev → FTP prod, no staging | **L-01: no staging/validation tier.** |
| Setup > Deploy > Deployment Status | GitHub Actions run history | present (Actions), but no per-deploy record tied to a tag. |
| Setup > Deploy > Quick Deploy (promote a validation) | — | missing: no "validate then promote" path; the mermaid workflow (F-08) deploys directly. |
| Setup > Apex Test Execution (run tests before deploy) | `pytest`, `assert_no_conflict_markers.sh` | present but not wired as a gate in front of the Pages/FTP deploy. |

**Net change:** the breadcrumb table becomes the argument for **L-01** (add a dry-run/validate stage)
and **F-08** (the Pages deploy skips the validate stage).

---

## 4. Labs & Design → design patterns, buy-vs-build, "who maintains this"

| Principle (Labs & Design) | `jet-slime` analog | Verdict |
|---|---|---|
| **"Can Flow do this instead of code?"** (declarative before code) | shell wrapper does config merge via an inline Python heredoc + 4 new Python tools | L-04: prefer one documented generator over four overlapping tools (F-10). |
| **"Will this scale?" / bulkify | selector/domain/service layers** | The four tools have no shared core — F-10. Extract a `discovery core` + thin CLIs. |
| **"Is it documented? Who maintains it?"** | Docstrings are good; but four tools with no README | F-10 fix: a README stating which tool is canonical. |
| **Buy vs build** | `litellm` (buy) + custom discovery (build) is the right split | ✅ keep. |
| **Deployment options table** (Change Sets / CLI / Metadata API / DevOps Center) | `git push` (hangs per FREEBUFF §4) + Git Data API + FTP | L-01: pick one documented deploy path. |

**Net change:** promotes **F-10** (four overlapping tools) to a design-pattern finding and adds the
"who maintains it" question (a README).

---

## 5. DevOps & Release Engineering → the biggest update

This is the guide that changes the review most. Its 12 training items map almost one-to-one onto the
repo's release process, and the repo is missing most of them.

| # | DevOps item (guide) | Repo today | Finding |
|---|---|---|---|
| 1 | **Source of truth = Git, not prod** | FTP prod + bot commits to `main`; branches stale in an hour | **L-01** |
| 2 | **Metadata that breaks releases** (deploy fails on missing dependency) | `parse_key` order / generated config merge | F-02, F-03, L-03 |
| 3 | **Environments: Dev/QA/UAT/Pre-Prod/Prod; sandbox + mask** | local → FTP, no staging, `dbpasses.txt` unmasked | L-01, L-02 |
| 4 | **Branching: feature / release / hotfix; hotfix cut from `main`** | 242 branches, no release/hotfix model, no tags | **L-05** |
| 5 | **CI/CD: validate (dry-run) → integrate → stage → release** | Actions exist; no validate stage before deploy | L-01, F-08 |
| 6 | **DevOps tools (Gearset/Copado/AutoRABIT) sit on the Metadata API; CLI underneath** | shell + Python + Git Data API + FTP | fine, but document the one path (L-01) |
| 7 | **Conflict clinic: profiles don't merge; Flows don't merge** | 816-line generated `litellm_config.yaml` committed; long-lived branches | **L-04** |
| 8 | **Packages: unlocked/managed vs unpackaged** | monorepo, no package boundary | note only |
| 9 | **Tests: dry-run vs quick deploy vs real deploy** | tests exist, not a deploy gate | L-01 |
| 10 | **Releases/hotfix/rollback: tag prod; rollback = forward-deploy last good tag** | no tags → no rollback target | **L-01 / L-05** |
| 11 | **Banking change control: audit pack, segregation of duties** | bot commits, single author, no second-person gate | **L-06** |
| 12 | **Design patterns to coach: permission sets over profiles, tests create own data, no hardcoded ids, Named Credentials** | F-02/F-03, F-10, L-02, L-07 | cross-cut |

### New findings from the DevOps lens

**L-01 · S1 (release-engineering) · No promotion path: no staging tier, no validate stage, no tag/rollback.**
The repo deploys to production (FTP / Pages) continuously with `[skip ci]`, from a `main` that moves
every few minutes, with no Dev→QA→UAT→Prod path and **no annotated tag on the last good prod deploy**.
The guide (§10) is blunt: "If you do not have a tag from the last good prod deploy, you do not have a
rollback." This is the single biggest gap the Salesforce lens exposes, and it is *process*, not code.
Fix: (a) tag every prod deploy (`release-YYYY-MM-DD`); (b) add a `validate` job (dry-run) that must be
green before the FTP/Pages deploy; (c) document the one deploy path.

**L-04 · S2 · Generated config committed to Git = the "profiles don't merge" conflict.**
`litellm_config.yaml` grew +816 lines and is machine-merged at boot into
`litellm_config.runtime.yaml`. Committing a generated artifact is the exact anti-pattern the conflict
clinic warns about (two stories editing one giant file → bad merge → access you didn't review). Here
the "access" is routing: a bad merge silently drops a provider group.
Fix: commit the **base config + the generator**, not the generated output; or if the generated file
must be committed, mark it generated and never hand-edit it.

**L-05 · S2 · No release/hotfix branch model; 242 branches; hotfix would be cut from a moving `main`.**
The guide's branching shape (`main` = prod; `hotfix/*` from `main`; `release/<date>`; `feature/*` into
the release) does not exist here. With bot commits landing every few minutes, a hotfix cut from `main`
is cut from a moving target.
Fix: adopt `release/<date>` cut points + tag; hotfix from the tag, merge back to `main`.

**L-06 · S2 · Segregation of duties: every commit is bot-or-single-author; the review is the only second pair of eyes.**
Banking change control (§11) requires "the developer who wrote it does not approve their own prod
deploy." The repo has no structural separation — the same automation that writes the change also ships
it. This review is, in effect, the second-person read; the repo should make that structural (a required
review on deploy PRs, an approver ≠ author).
Fix: require a review on any PR that touches deploy workflows / credential plumbing (PR #761, #700,
#696, and this branch).

**L-07 · S3 · Probe/audit tools burn free-tier daily caps (the "callouts are slow/costly, batch them" rule).**
Crash Course §Governor Limits "Callouts" + DevOps §2 "governor limits still matter." The auditors make
one live completion per model per provider; on OpenRouter's 50 req/day that is a real budget.
Fix: `--no-probe` default in CI/cron; cap concurrency; never overlap the auditor with the proxy's own
fallback chain (they compete for the same free quota).

**L-08 · S3 · Tests can't reproduce because tools depend on `~/dbpasses.txt` (the "tests create their own data" rule).**
DevOps §7 "Apex and dependencies": tests that rely on org data pass in Dev and fail in an empty org.
The new tools read an external mutable file, so CI cannot run them deterministically.
Fix: fixture `dbpasses.txt` in tests; `--keys-file` already exists on the audit tool — use it.

---

## 6. What the lens changed, in one list

- **Confirmed** F-03 (parse_key silent zero-match) as the top code fix → reframed as L-03.
- **Corrected a first-pass error:** F-06 started as "conditional / couldn't verify." Byte-level
  checking proved it is real — six source files literally contain `[REDACTED]`, introduced by this
  branch (main = 0). It is now **S1 / P0-1**, and it is the clearest example of the lens's own theme:
  the change *parses and imports*, so nothing fails loudly, but the tools silently stop finding their
  credentials. That is the Crash-Course governor-limit / DevOps "green deploy, dead feature" pattern.
- **Elevated** F-08 (Pages deploy) → part of L-01 (no validate stage).
- **Added** L-01 (promotion path + tags), L-02 (credential file hygiene/rotation), L-04 (don't commit
  generated config), L-05 (branching/hotfix model), L-06 (segregation of duties), L-07 (free-tier
  callout budget), L-08 (fixtures for tests).
- **No downgrades:** nothing in the first pass was wrong; the lens added process findings the code
  review could not see, and one verification pass (F-06) turned a "maybe" into a confirmed S1.