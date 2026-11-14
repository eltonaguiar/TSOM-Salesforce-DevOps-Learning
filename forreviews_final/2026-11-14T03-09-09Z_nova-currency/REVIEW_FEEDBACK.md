# Cross-Branch Review Feedback — Worktree `nova-currency`

**Generated:** 2026-11-14T03:09:09Z
**Worktree/branch:** `nova-currency`
**Remote:** `origin` = git@github.com:eltonaguiar/findtorontoevents_antigravity.ca.git
**Coordinator note:** Another agent is also working on this review. Do not duplicate effort; merge findings into this folder only.

---

## 1. Worktree / branch state vs `main`

| Metric | Value |
|--------|-------|
| Current branch | `nova-currency` (checked out, clean working tree) |
| Commits in `nova-currency` not in `main` | 5 |
| Commits in `main` not in `nova-currency` | 2632 |
| Status | `nova-currency` is **significantly behind** `main` (diverged). `main` fast-forwards 2632 commits ahead of this worktree. |

### 5 commits unique to `nova-currency` (not yet on `main`)
```
1d9354ab9e2 simulation: deploy broken mermaid diagram for swarm audit
4294fd835f1 test: deploy broken mermaid diagram to GH pages
2c08a4bb143 docs: extend the dated chatlog with the review inventory
83787bd97b0 docs: add the dated FREEBUFF chatlog
df2eadf054c Retire the Inception (Mercury) API from every provider registry
```

**Review feedback:** `nova-currency` should be rebased/merged onto current `main` before any review-based changes are landed, otherwise feedback will conflict with 2632 commits of upstream activity. These 5 unique commits are documentation/simulation-only and low-risk.

---

## 2. Open PRs awaiting review (base = `main` unless noted)

32 open PRs were returned (page limit 50). All authored by `eltonaguiar`.

| # | Title | Head branch | Base | Created | Review status |
|---|-------|-------------|------|---------|---------------|
| 766 | docs: add kilo today's ServiceNow/Salesforce Canada jobs scan (Nov 2 2026) | add-kilo-todays-servicenow-salesforce-jobs | main | 2026-11-02 | Unreviewed |
| 765 | docs: add kilo additional skills/certifications | add-kilo-additional-skills | main | 2026-11-02 | Unreviewed |
| 763 | Add verified sci-fi TV watchlist and upcoming releases to weather | copilot/weather-tv-2026-11-01 | main | 2026-11-01 | Unreviewed |
| 762 | Job Scan: ServiceNow & Salesforce - Huggle Agent 2026-10-30 | huggle-agent-2026-10-30 | main | 2026-10-30 | Unreviewed |
| 761 | fix: rotated FTP credentials, no embedded password defaults, verified FTPS | fix/ghcopilot-ftp-credential-loading | main | 2026-10-23 | Unreviewed |
| 760 | fix: fund walk-forward review fixes (FXAIX same-window CI + identical-pairs proof) | oc/fund-walkforward-review-fixes | oc-winning-candidate | 2026-10-23 | Unreviewed |
| 759 | research (opt-in): 95-fund durability audit and genuine zero-expense ETFs | research/ghcopilot-symbol-durability | main | 2026-10-23 | Unreviewed |
| 758 | Fix BTC evaluator daily drawdown and unsupported gate passes | fix/ghcopilot-btc-mtm-guard | oc-winning-candidate | 2026-10-22 | Unreviewed |
| 757 | Fix audit evidence cards and explain strategy readiness | feat/ghcopilot-grok-scorecard | main | 2026-10-22 | Unreviewed |
| 756 | Fix DSR>1 + resolver batch-close/flat-exit bugs (Grok quick-fixes 1-4) | fix/grok-quickfixes-dsr-resolver | main | 2026-10-22 | Unreviewed |
| 751 | ci: add GitHub Actions health monitor job | feat/gha-actions-health | main | 2026-10-22 | Unreviewed |
| 750 | Nemotron Money Ready: Bond Yield Curve Slope Strategy Test | nemotron/money-ready | main | 2026-10-20 | Unreviewed |
| 749 | fix(resolver): true TP/SL exit time + UNRESOLVED_NO_PRICE (batch-close root cause) | buffy/batch-close-rootcause | main | 2026-10-20 | Unreviewed |
| 747 | feat(opencode): crypto money-ready backtest + report (no passes) | opencode/money-ready | main | 2026-10-20 | Unreviewed |
| 746 | spec: KPI page (spec only, no code this week) | opencode/kpi-page-spec | main | 2026-10-20 | Unreviewed |
| 745 | fix(audit): smart_picks gate-validated only + curated_feed + empty-state reasons | opencode/audit-empty-state-v2 | main | 2026-10-20 | Unreviewed |
| 744 | fix(forward_validator): enforce BLACKLISTED_STRATEGIES in save_active_picks | fix/blacklist-save-active-picks | main | 2026-10-20 | Unreviewed |
| 736 | fix(fc+weather): persist category Apply/filter + weather reset-look recovery button | fix/fc-category-persist-weather-reset-look | main | 2026-10-18 | Unreviewed |
| 735 | fix(audit): symbol→asset-class cache fallback + dynamic /audit core stats | fix/assetclass-cache-live-core-stats | main | 2026-10-18 | Unreviewed |
| 713 | fix(ci): backup-verify false failures + issue spam; speed up dup-guard scan | fix/ci-backup-verify-and-dupguard | main | 2026-10-04 | Unreviewed |
| 711 | fix(audit): correct two defects in per-tab/per-class staleness code | fix/stale-tag-defects | main | 2026-10-04 | Unreviewed |
| 701 | Preserve pick rationale through *_audit_push normalizers | fix/pick-reason-audit-push | main | 2026-10-04 | Unreviewed |
| 700 | LLM free-first routing + message tracing; Discord loud-failure + secret scrub | fix/oct3-llm-discord-loud-failure | main | 2026-10-04 | Unreviewed |
| 696 | fix(discord): read webhooks from secrets only after exposed hook deletion | fix/discord-webhook-secret-rotation | main | 2026-10-03 | Unreviewed |
| 667 | feat(b5): forward-track cell selector | feat/b5-forward-track-tool-20260624-151517 | main | 2026-06-24 | Stale (unreviewed ~5mo) |
| 666 | fix(resolver): B1 backfill price guard at resolution-write | feat/b1-backfill-price-guard-20260624-150302 | main | 2026-06-24 | Stale |
| 665 | audit(stalled-producer-detector): v2.0+2 frame-correction + health-step cron | fix/ci-tests-drift-reconciliation | main | 2026-06-24 | Stale |
| 657 | feat(contract-test): cold-merge atomic contract-test gate (4 files) | feat/contract-test-cold-merge-2026-06-22 | main | 2026-06-22 | Stale |
| 600 | feat(edge): money-ready hunt — intrabar tools + 4-agent verdict | worktree-equity-reachability-tp-2026-06-13 | main | 2026-06-13 | Stale |
| 595 | feat(validate): non-crypto intrabar replay scaffold (Stage-4 gate) | feat/intrabar-replay-noncrypto-2026-06-13 | main | 2026-06-13 | Stale |
| 581 | feat(audit): P2-9 /audit/model_portfolios.html roster page + investigations | feat/minimax-next-steps-batch | main | 2026-06-12 | Stale |
| 564 | docs: Audit Edge Hunt Action Plan & Deep Dive (2026-06-12) | audit-dig-deeper-2026-06-12 | main | 2026-06-12 | Stale |
| 562 | feat(audit): edge hunt session docs, pass-hunter tools, P0/P1 plans | feat/audit-edge-hunt-session-docs | main | 2026-06-12 | Stale |

**Review feedback:** 25 of 32 open PRs are from June–October 2026 and show no review activity. Prioritize the 7 November PRs (750–766) first; triage or close the stale June PRs.

---

## 3. Salesforce training cross-reference (from `main`)

`main` contains the Salesforce DevOps research at:
`forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` (also on branches `salesforceyetagain` and `salesforceagain`, each 5 commits ahead of `main`).

Files present:
- `crash_course.md` — Salesforce ELI5 crash course (objects/records/fields, navigation, security, Flow vs Apex vs Visualforce vs LWC, REST/SOAP, governor limits, Trailhead resources)
- `key_principles.md` — 10 Salesforce DevOps engineering principles (bulkify, selective queries, least privilege, governor limits, master-detail vs lookup, Named Credentials, troubleshooting, sandboxes, CI/CD, documentation)
- `certifications.md` — Certification landscape (Admin → Platform Developer → Apex/LWC Developer), Trailhead courses, gap analysis
- `research_index.md` — Index + status tracker; pending deliverables: DevOps/release-engineering notes, navigation/breadcrumbs, labs/design, user-management/data notes
- `research_plan.md` — 4-phase research plan (Foundation → DevOps → Integration → Synthesis) mapped to Scotiabank requisition 276046

**Source page:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/#available-guides-1
(Salesforce Training track is separate from the ServiceNow guides.)

**Review feedback on Salesforce training content:**
- The crash course and key_principles.md are complete and consistent with the source page's Salesforce Crash Course track (objects, records, fields, navigation breadcrumbs, users/profiles/roles, data integrity, Flow vs Apex vs Visualforce vs LWC, REST/SOAP, troubleshooting, design considerations).
- The DevOps & Release Engineering track from the source page (Git metadata lifecycle, Dev/QA/UAT/Pre-Prod/Prod, sandbox refresh & masking, CI validation, Gearset/Copado/AutoRABIT vs CLI, deploy conflicts, unlocked packages, rollback, banking change control) is only partially captured — `key_principles.md` Principle 8/9 covers sandboxes/CI/CD, but there is **no dedicated `devops_release_engineering.md`** yet (marked ⏳ Pending in `research_index.md`).
- Navigation & Breadcrumbs, Labs & Design, and User Management & Data notes are also ⏳ Pending.

**Action:** If this worktree produces Salesforce-related review feedback, add it to this folder and cross-reference `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` on `main`. Do not edit files on `main` from this worktree without rebasing first (see §1).

---

## 4. Other branches of note (cross-reference)

- `salesforceyetagain` / `salesforceagain`: each 5 commits ahead of `main`, carry the Salesforce training files above. `salesforceagain-v3` exists on remote only (`79868dccd2f Add Salesforce DevOps deep-dive research to forreviews folder`).
- `gh-pages`: 2 commits ahead of local (deployed site).
- Long-lived feature branches from 2026-06 (e.g. `feat/b5-forward-track-tool-...`, `worktree-equity-reachability-tp-2026-06-13`) still have open PRs against `main` — candidates for closure or rebase.

---

## 5. Recommendations / action items

1. **Re-base `nova-currency`** onto current `main` (2632 commits behind) before landing review-driven changes.
2. **Review the 7 November PRs (750–766)** first; they are the most current and least likely to conflict.
3. **Triage/close stale June 2026 PRs** (581, 562, 564, 595, 600, 657, 665, 666, 667) unless actively being worked.
4. **Complete the pending Salesforce research notes** (DevOps/release-engineering, navigation/breadcrumbs, labs/design, user-management/data) and store any new dated output under `forreviews_final/` or the `forreviews/<worktree>/<timestamp>/` convention used on `main`.
5. **Coordinate with the other agent** working on this review — post findings here, avoid editing the same files concurrently.

---

## 6. Coordination

This folder (`forreviews_final/2026-11-14T03-09-09Z_nova-currency/`) is the designated output location for this worktree's review feedback. A peer agent is also producing review output; merge rather than overwrite.