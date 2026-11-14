# 04 — Prioritized actions v2 (the work, updated)

Consolidated after both passes (code review `02` + Salesforce lens `03`). Deduplicated and ordered by
what blocks the `jet-slime` merge first, then what improves the repo's release posture. Effort is a
rough S/M/L. "Evidence" points at the finding id in `02`/`03`.

## P0 — fix before `jet-slime` merges (branch-local)

| # | Action | Evidence | Effort |
|---|---|---|---|
| **P0-1** | **Revert the literal `[REDACTED]` regression in 6 source files** (`verify_all_keys.py`, `api_model_roster.py`, `local_swarm_review.py`, `model_picks_research.py`, `_graphify_docs_multibackend.py`, `config/api_model_roster.json`). They parse but are silently broken at runtime. Restore the real names from `origin/main` and re-apply only the Mercury removals; add a CI guard `git grep -n '\[REDACTED\]' -- '*.py' '*.json'` == empty for code. | **F-06 (S1)** | M |
| P0-2 | Restore the executable bit: `git update-index --chmod=+x tools/start_litellm_proxy.sh` | F-01 | S |
| P0-3 | Remove the mermaid Pages-deploy scaffolding from this branch (or gate it off `push`): drop `.github/workflows/mermaid-test-deploy.yml` + `docs/mermaid_tests/`; keep the fixture under `tests/` only | F-08, F-09 | S |
| P0-4 | Prove the committed `litellm_config.yaml` has **no secret literals** (`grep -iE 'sk-|token|password|key' → only ${ENV}`); and decide whether a generated runtime config belongs in Git at all | F-13, L-04 | S |

## P1 — should-fix on this branch (code quality)

| # | Action | Evidence | Effort |
|---|---|---|---|
| P1-1 | Add a `parse_key` **exactly-once assertion**: warn/fail at boot when a label matches zero lines, and when two labels map to one env var (`OPENCODE_API_KEY_ALT`). This kills the whole silent-degradation class. | F-02, F-03, L-03 | M |
| P1-2 | Consolidate the four discovery/audit tools around one core; document which is canonical (`discovery` = offline report, `dynamic` = boot-time merge) in a README. | F-10 | M |
| P1-3 | Credential-file hygiene: `chmod 600 ~/dbpasses.txt`; rotate the OpenRouter key that surfaced in terminal output (FREEBUFF §7); confirm the monthly `[Security] Secret Rotation` reminders are actioned. | L-02 | S |
| P1-4 | Align the "fail-open" docstring with the fail-closed `requests` import, or wrap the import to degrade gracefully. | F-11 | S |

## P2 — release-engineering (repo process, the biggest gap)

| # | Action | Evidence | Effort |
|---|---|---|---|
| P2-1 | **Tag every prod deploy** (`release-YYYY-MM-DD`) so a rollback target exists; "no tag = no rollback." | L-01 | M |
| P2-2 | Add a **validate/dry-run stage** that must be green before the FTP/Pages deploy (extend the existing `assert_no_conflict_markers.sh` / `safe_push.sh` / `db-freshness-guardian.yml` pattern). | L-01, F-08 | L |
| P2-3 | Adopt a **release/hotfix branch model**: cut `release/<date>` from `main`, `hotfix/*` from the tag, merge back; stop cutting hotfixes from a `main` that moves every few minutes. | L-05 | M |
| P2-4 | **Segregation of duties**: require a review (approver ≠ author) on any PR touching deploy workflows or credential plumbing — this branch, #761, #700, #696. | L-06 | S |

## P3 — nice-to-have / notes

| # | Action | Evidence | Effort |
|---|---|---|---|
| P3-1 | Document the bash floor for `[[ -v ]]` (≥4.2) or use a portable check. | F-04 | S |
| P3-2 | Fix the FREEBUFF chatlog's reproduction grep so it excludes `mercury2` and `inception_paper_trading`. | F-07 | S |
| P3-3 | Default the audit/discovery tools to `--no-probe` in CI/cron; cap concurrency; don't overlap them with the proxy's fallback chain (they share the free-tier budget). | F-12, L-07 | S |
| P3-4 | Add `dbpasses.txt` fixtures so the tools are testable in CI without live credentials (`--keys-file` already exists). | L-08 | M |

---

## Definition of done for `jet-slime`

The branch is mergeable when **all P0** are done and **P1-1** (parse_key assertion) is in. **P0-1
(the `[REDACTED]` regression) is the true blocker**: the six files parse and import, so nothing fails
loudly — the tools just silently stop finding their credentials. P1-1 is the change that would
otherwise let a future credential re-order silently break a provider group in production. P2 items are
the repo's release debt and do not block this merge, but P2-1 (tags) should be scheduled next — it is
cheap and it is the precondition for every other rollback story.

## What I did *not* do (so a reviewer can trust the boundary)

- I did not modify any code — this is a review deliverable only.
- I did not line-review `litellm_config.yaml` (816 lines) or the full bodies of the four new tools;
  those are design-level + entry-point reviews (F-10..F-13).
- I did not read all 40k files or all 33 PRs line-by-line; PR review is metadata/diff level (`01`).
- I did not print any secret; `[REDACTED]` in the raw diff is tooling redaction, not file content.