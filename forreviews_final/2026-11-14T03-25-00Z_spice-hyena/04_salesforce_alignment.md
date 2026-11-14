# 04 — Salesforce-guide alignment

What the guides actually require, and where this repo's engineering practice measures against it.

The five guides are:
1. **Salesforce Crash Course** — objects, records, fields, navigation, security, automation, Apex/VF/LWC, integration, troubleshooting, governor limits.
2. **Navigation & Breadcrumbs** — Setup paths for every admin/dev task.
3. **Labs & Design** — 4 labs, design patterns, system properties, OOB features.
4. **User Management & Data** — users, profiles, permission sets, roles, licenses, import/export, validation, FLS, duplicate management.
5. **DevOps & Release Engineering** — the training track mapped to requisition 276046.

The DevOps guide is the one that matters for this exercise. It states the job plainly:

> "The posting is not 'write features.' It is 'make Salesforce releases fast, safe, and auditable.'"

and

> "Production is not the source of truth. Git is. The org is a target you deploy to."

That is a **release-engineering** discipline, and it applies to this repo exactly as it applies to a Salesforce org. The medium differs; the control does not.

## 1. The guide's 12 training items, applied to this repo

The guide's table maps each item to a "done when" test. Here it is, with this repo's state and evidence.

| # | Training item | Guide's "done when" | This repo today | Gap |
|---|---|---|---|---|
| 1 | Source of truth | "You can retrieve one metadata type, commit it, and dry-run deploy it to a second org" | Git is the source for code; **but the deployed site is not in Git** — `TORONTOEVENTS_ANTIGRAVITY/index.html` is, while `_next/static/chunks/*` are only on the FTP server | **Partial.** The built artifact is outside version control |
| 2 | Metadata that breaks releases | "Name the dependency a failed deploy is missing without opening the org" | N/A — no Salesforce. Analogue: Python/JS import graph and CI `paths:` filter | **Weak.** The `paths:` filter is the dependency graph, and it is hand-maintained |
| 3 | Environments & sandboxes | "Draw the path, say which sandbox type each stage uses" | No Dev/QA/UAT/Pre-Prod/Prod path. Worktrees stand in for dev; `main` is both integration and production | **Missing entirely** |
| 4 | Branching | "Say where a hotfix is cut from, and which branches it merges back into" | 462 branches, no written model, no hotfix topology | **Missing.** See §3 |
| 5 | CI/CD | "Describe the same four stages in any of those tools" | GitHub Actions only. Validate stage does not exist — CI tests, it does not validate a deploy | **Partial** |
| 6 | DevOps tools | "Say what the CLI does that the vendor UI does not replace" | N/A — no vendor tool. Analogue: the `safe_patch.py` / `ast_reviewer_codemod.py` tooling on unmerged branches | **Present but unmerged** |
| 7 | Conflict clinic | "You have a fix for each, not just the symptom" | Merge conflicts are real: #758 is `CONFLICTING`, and 462 branches guarantee more | **Reactive, not designed** |
| 8 | Packages | "Say when unpackaged source is still the right deploy" | N/A. Analogue: the 4,254-line `wiring` retirement is one unreviewable blob | **Weak** — no modular release unit |
| 9 | Tests & validation | "Explain dry-run vs quick deploy vs a real prod deploy" | CI runs tests; there is no validate-only deploy stage and no separate prod gate | **Missing** |
| 10 | Releases, hotfixes, rollback | "Fill the runbook template from memory" | No runbook. Deploy is `deploy_*.py` scripts run by hand; `deploy_updates_v05.py` is explicitly excluded from review | **Missing.** See `06_salesforce_runbook_template.md` |
| 11 | Banking change control | "List the artifacts an auditor asks for after a prod deploy" | `updates/*.md` records exist per fix (good), but no deploy id, no approver, no tag, no test run id | **Partial** — records exist, audit pack does not |
| 12 | Design patterns you coach | "Reject a story that edits `Admin.profile` for one field" | N/A directly. Analogue: reject a change that bypasses `safe_patch.py` anchors | **Present as tooling, absent as policy** |

**Score: 0 complete, 4 partial, 7 missing, 1 N/A-equivalent.**

## 2. The one idea worth importing wholesale

The guide's §1:

> "Destructive deletes are a separate file, not a side effect of 'it was not in the folder.'"
>
> "A delete in production is not undone by Git. Rollback of a delete means recreating the metadata, and any records that lived on a deleted custom object are gone."

This repo has the identical hazard with **database migrations**. `schema-baseline.sql` is 256 KB and
`purge_fantasy_data.py` exists. There is no `destructiveChanges` equivalent — a `DROP COLUMN` in a
migration is not undone by `git revert`, and the guide's rule is exactly right here: destructive changes
belong in a separate, explicitly reviewed file, never as a side effect of a schema diff.

## 3. Branching: the gap with the clearest evidence

The guide prescribes:

```
main                         ← matches production
  hotfix/<ticket>            ← cut from main only
  release/2026-11-27         ← cut from main when the release freezes
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

and four rules, of which two are directly violated here:

- *"A feature branch lives days, not weeks."* — **Violated at scale.** 21 branches are unmerged; the
  oldest (`buffy/batch-close-rootcause`) is from 2026-10-20, and the 5 `job-search-*` branches date from
  2026-11-03 with 42–45 commits each. The guide's warning is precise: *"Salesforce XML (Flows, profiles)
  does not merge. Long branches become 'delete one side of the conflict and hope.'"* The analogue here is
  `litellm_config.yaml` — PR #700 conflicts because it is a 346-line snapshot against a 790-line file,
  which is exactly "delete one side of the conflict".
- *"Tag production after a successful deploy: `release-<date>`. That tag is the rollback target."* —
  **Absent.** There are no release tags; `main` HEAD *is* production. So there is no rollback target,
  which the guide calls out as the precondition for taking a release at all: *"If you do not have a tag
  from the last good prod deploy, you do not have a rollback."*

**Recommendation:** adopt the model verbatim, including the hotfix-from-`main` rule, and tag each production
deploy. This is the single highest-leverage change in this section, because it converts "main is
production and it is red" from an emergency into a normal release-engineering state.

## 4. The `paths:` filter is an undeclared dependency graph

The guide's §2 is about metadata dependencies, and its key sentence is:

> "If the payload references something the target does not have, and you did not include it, the deploy fails."

`ci-tests.yml` encodes the repo's dependency graph by hand:

```yaml
paths:
  - 'paper_trading/**'
  - 'alpha_engine/**'
  - 'audit_trail/**'
  - 'audit_dashboard/template.html'
  - 'audit_dashboard/dashboard_enhancements.js'
  - 'tests/**'
  - 'requirements.txt'
  - 'alpha_engine/requirements.txt'
  - '.github/workflows/ci-tests.yml'
```

Every entry is a hand-maintained claim of the form "a change here can break a test". The guide's discipline
— *deploy the parent and the child in one payload* — is the missing rule. Concretely, verified by matching
each path against the filter:

| Changed file | CI runs? |
|---|---|
| `audit_trail/universal_pick_resolver.py` | yes |
| `tools/safe_patch.py` | **no** |
| `tools/check_retired_providers.py` | **no** |
| `config/api_model_roster.json` | **no** |
| `litellm_config.yaml` | **no** |

A change to `tools/` or `config/` that breaks a test will **not** run CI at all. That is a silent dependency
the filter does not declare — and it is not hypothetical: `tools/safe_patch.py`,
`tools/check_retired_providers.py`, and `config/api_model_roster.json` are all in the current review set
(the four small tool branches, and the `wiring` retirement), so **every one of them merges with zero test
evidence.**

**The asymmetry that makes this worse.** The workflow *executes* `tools/tests/` in its run step
(`ci-tests.yml:203`):

```
python -m pytest tests/ paper_trading/tests/ alpha_engine/tests/ tools/tests/ ...
```

but `tools/tests/**` is **not** in the `paths:` filter, and `tools/**` is not either. So there are two test
files that exist and would run — `tools/tests/test_edge_filter_engine.py` and
`tools/tests/test_forex_unblock_tracker.py` — and neither can ever be triggered by a change to the code they
test. The test directory is reachable only when something *else* changes.

That is the exact shape of the guide's warning: a payload whose child is not in it. The child exists; the
trigger does not include it.

**Recommendation:** either widen the filter to the whole repo, or add a guard that fails when a changed
file is imported by a file inside the filter. The latter is the `sf project deploy start --dry-run`
equivalent — validate the real dependency graph rather than a declared one.

## 5. Validate vs quick deploy vs real deploy

The guide's three-way distinction (`devops-engineer.md` §9) maps onto this repo like this:

| Guide | This repo's equivalent | Present? |
|---|---|---|
| **Validation / dry-run** — "Changes the org? No. Prove the payload compiles and tests pass" | `pytest` on PR | Yes — this is what `ci-tests.yml` is |
| **Quick deploy** — "Promote a validation that already succeeded, inside the window" | Nothing. There is no promoted-artifact path; deploy scripts rebuild from source | **No** |
| **Real deploy** — "First deploy, or the validation expired" | `deploy_*.py` run by hand | Yes, but ungated |

The guide's warning about quick deploy is the one this repo would trip over first:

> "Quick deploy only works if nothing relevant changed since the validation. If someone hotfixed prod after your validation, the quick deploy is no longer an honest rehearsal. Re-validate."

Because `deploy_*.py` scripts rebuild from current source, a deploy after a green PR is **not** the thing
that was validated. That is the honest-rehearsal problem, and it is why the `updates/*.md` record-per-fix
rule exists — it is a manual substitute for a validated-artifact pipeline.

## 6. Change control: what the repo already does right

The guide's §11 audit pack:

| Artifact the guide requires | This repo has it? |
|---|---|
| Change ticket id in the commit and PR | **Yes** — `[SAM-IMPLEMENTATION-GAP-ANALYSIS-2026-11-13]` style tags in commit subjects |
| Diff a second person read | **Partially** — PR review is requested but no review is recorded (`reviewDecision` is empty on all 20 PRs) |
| Validation deploy id and prod deploy id | **No** |
| Test run id and coverage number | **Partial** — `ci-tests.yml:246` publishes a coverage summary and `:238` uploads `coverage.xml`, but `--cov-fail-under=10` is the only gate, and nothing writes the coverage number into the fix record |
| Named approver, different from the author | **No** — `eltonaguiar` authors and merges |
| Release tag | **No** |
| Mask-complete evidence for a Full sandbox | N/A (no Salesforce), but the analogue — evidence that a production data change was reviewed — is also absent |

The `updates/*.md` convention is the repo's real strength here. It is the guide's "runbook" in spirit, and
the Freebuff chatlog's §9 is a genuinely good example of the audit pack done by hand. The gap is that it is
**per-fix, not per-deploy** — there is no document that says "this is what went to production, when, from
which commit, with which deploy id".

## 7. Certifications: the corrected list

From the guide's own Certifications section (`docs/salesforce/devops-engineer.md`), which is the authoritative
source for this track:

| Credential | Maps to |
|---|---|
| Platform Developer I | The PD1 the posting names — Apex, tests, platform model |
| Platform App Builder | The metadata you move weekly — objects, Flow, security |
| Platform Administrator II | What the posting calls "Advanced Admin" (Salesforce renamed it; use both names) |

And the guide's explicit statement, which is the correction for B4:

> "A Salesforce 'DevOps Engineer' cert — There is not an official one to list as if it existed. Copado,
> Gearset, and AutoRABIT offer their own certificates. Those show tool time. They do not replace PD1."

So `forreviews/salesforceyetagain-v4/certifications.md` does two things wrong: it invents a "ServiceNow
Certified Salesforce Admin", and it presents vendor tooling as a certification track without the guide's
caveat that vendor certs do not substitute for PD1.

**One claim I am deliberately not repeating.** Two peer bundles in the learning repo assert that a
"Development Lifecycle and Deployment Architect" credential is the DevOps credential. That credential exists,
but the DevOps guide does not name it, and I did not verify it against the official credential page in this
session. It is recorded as a follow-up for the merge round, not as a finding here.