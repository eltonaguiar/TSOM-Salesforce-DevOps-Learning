# 01 — Cross-reference: the review surface

Everything below is evidence-backed from `gh`, `git`, and the worktree at `1d9354ab9e2`.
Counts taken 2026-11-14 03:10 UTC.

## 1. Where `jet-slime` sits relative to `main`

`origin/main` tip at review time: `7fe5a8ce94e` ("Scanner data update [2026-11-14 03:08 UTC] [skip ci]").
`main` is a **high-churn automated branch** — the last 15 commits are all bot/scanner commits
(`[skip ci]`), firing every few minutes (Signal Engine, Meme scanner, Conviction scan, Prediction
market, Rapid Fire, etc.). That matters for review: a branch cut from `main` is stale within an hour.

`jet-slime` is **5 commits ahead of `origin/main`**, and those 5 are the entire review payload:

| # | sha | Title | Nature |
|---|---|---|---|
| 1 | `df2eadf054c` | Retire the Inception (Mercury) API from every provider registry | code (36 files) |
| 2 | `83787bd97b` | docs: add the dated FREEBUFF chatlog | doc |
| 3 | `2c08a4bb14` | docs: extend the dated chatlog with the review inventory | doc |
| 4 | `4294fd835f` | test: deploy broken mermaid diagram to GH pages | test/CI scaffolding |
| 5 | `1d9354ab9e` | simulation: deploy broken mermaid diagram for swarm audit | test/simulation |

`git diff --stat origin/main...jet-slime` = **41 files, +4254 / −348**. The bulk is
`litellm_config.yaml` (+816/−…), the four new `tools/*.py` discovery/audit tools, and the
`start_litellm_proxy.sh` hardening.

**Cross-reference:** `df2eadf054c` is the same commit the FREEBUFF chatlog
(`updates/2026-11-12-FREEBUFF-chatlog-1959UTC.md`) documents as the Mercury retirement on branch
`scrub/inception-mercury-2026-11-12`. The chatlog says "37 files changed vs main, two commits"; on
`jet-slime` it is 41 files / 5 commits because the two mermaid-test commits and the two chatlog
commits sit on top. **A reviewer must review the code commit, not the chatlog's file count.**

## 2. Open pull requests — 33 open, all `reviewDecision: ""` (none has a review)

All 33 are authored by `eltonaguiar`, and **not one has a recorded review decision** — every PR is
un-reviewed. They cluster into three groups:

**A. Recent, plausibly mergeable (Oct–Nov 2026):**
- #766 ServiceNow/Salesforce jobs scan (Nov 2) · #765 kilo skills (Nov 2) · #763 sci-fi TV watchlist
  (Nov 1) · #762 ServiceNow/Salesforce job scan (Oct 30) · #761 FTP credential rotation (Oct 23)
- #760 fund walk-forward review fixes · #759 95-fund durability audit · #758 BTC MTM guard
  · #757 audit evidence cards · #756 DSR>1 + resolver batch-close · #751 Actions health monitor
- #750/#749/#747/#746/#745/#744/#736/#735 — Oct 18–20 resolver / audit / KPI cluster

**B. Stale since June–July 2026 (no activity ~4 months):**
- #667, #666, #665, #657, #600, #595, #581, #564, #562 — all `updatedAt` 2026-06/07-13. These are
  the "edge hunt / money-ready / forward-track" generation. They are almost certainly **behind
  `main` by thousands of commits** and will conflict.

**C. Security / CI hygiene (Oct 2026):**
- #713 backup-verify false failures + issue spam · #711 stale-tag defects · #701 pick rationale
  through audit_push · #700 LLM free-first + Discord loud-failure · #696 Discord webhook rotation

**Cross-reference risk:** PR #761 ("rotated FTP credentials, no embedded password defaults") and the
`jet-slime` branch both touch deploy/credential plumbing. If both land, review them together — the
Salesforce lens (secrets never in the repo) applies to both.

## 3. Open issues — 44 open, dominated by bot noise

The 44 break down as:
- **~30 `[backup-verify] Restore check FAILED`** bot issues, one every ~30 min, dating back to
  2026-06-15. This is the **issue-spam** that PR #713 claims to fix. It is real, ongoing, and the
  single loudest signal in the issue list.
- **Monthly `[Security] Monthly Secret Rotation Reminder`** — Jul/Aug/Sep/Oct/Nov 2026 (#668, #675,
  #685, #695, #764). These are the repo's own reminder that secrets need rotation; relevant to the
  `jet-slime` credential changes (OpenRouter key surfaced in terminal output per the FREEBUFF chatlog
  §7 — **rotation still owner-actionable**).
- **#748 "Production resolver predates _priceless_close -> exit_price=0.0 flat closes"** — a real
  human-filed data-correctness bug, open since Oct 20. This is the highest-value non-bot issue and it
  is still open.
- **#654 weekly event gap scan — DEGRADED** (scrapers blocked). Data-quality issue.

## 4. Branches — 242 local / 220 remote

The branch list is large and mostly per-agent/per-feature (`buffy/*`, `copilot/*`, `docs/*`,
`fix/*`, `feat/*`, `chore/*`, `audit-*`, `archive/*`). For review purposes the relevant ones are:
- `scrub/inception-mercury-2026-11-12` — the original Mercury scrub branch (source of `df2eadf054c`).
- `wiring` — **the branch the mermaid-test workflow triggers on** (see finding F-04 in `02`).
- `main` — production; the promotion target for anything here.

## 5. Recent review-style artifacts already in the repo (context, not my output)

The repo already carries many review docs (`REVIEWFORBUFF.MD`, `REVIEWFORBUFF_V2.MD`,
`COMPREHENSIVE_CODE_REVIEW_REPORT.md`, `June42026_claude_opus_4_7_peer_reviews.MD`,
`review_picks_audit/`, `review_signal_analysis*/`). These are **prior** reviews. My set does not
duplicate them; it reviews the *current* branch state and cross-references them only where they
overlap (e.g. the Mercury retirement is also documented in `updates/2026-11-12-inception-mercury-api-sunset-migration.md`).

## 6. Cross-reference summary (the one-screen version)

- **`main`** = bot-driven, moving every few minutes; any review branch is stale on arrival.
- **`jet-slime`** = 5 commits: 1 real code change (Mercury retirement + litellm hardening + 4 new
  tools), 2 chatlog docs, 2 mermaid-test scaffolding commits that should not ship.
- **33 open PRs** = none reviewed; ~9 stale since June/July; 2 security/CI hygiene PRs overlap this
  branch's credential work.
- **44 open issues** = mostly `backup-verify` spam (PR #713 target) + 5 monthly secret-rotation
  reminders + 1 real data bug (#748).