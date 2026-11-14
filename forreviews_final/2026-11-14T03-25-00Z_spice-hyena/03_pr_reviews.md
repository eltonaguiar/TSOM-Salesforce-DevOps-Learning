# 03 — Per-PR review

20 open PRs. All figures verified from the API, not from the PR body.

## Summary table

| PR | Title (short) | Files | Base | Real blockers | CI | Recommendation |
|---|---|---|---|---|---|---|
| 749 | resolver: true TP/SL exit time | 6 | stale | 1 design gap | inherited red + cancelled dupguard | **Merge after 2 fixes** — highest value |
| 756 | DSR>1 + resolver hit-ts | 7 | stale | 1 overlap with 749 | same | **Merge after rebasing on 749** |
| 757 | audit evidence cards + readiness | 33 | stale | 1 design risk | same | Review, then merge |
| 760 | fund walk-forward review fixes | 11 | stale | none found | same | **Merge** |
| 761 | rotated FTP credentials | 16 | stale | 1 precedence bug | same | **Merge after 1 fix** |
| 763 | sci-fi TV watchlist | 2 | current | none | — | Merge (low risk) |
| 758 | BTC evaluator drawdown | 6 | stale | **conflicts with main** | cancelled only | Needs rebase first |
| 759 | 95-fund durability (research) | 7 | stale | none | inherited red | Merge (docs) |
| 750 | Nemotron bond yield test | 7 | stale | none | inherited red | Merge (research) |
| 713 | CI backup-verify + dupguard | 3 | stale | none | inherited red | Merge — fixes B2 |
| 711 | per-class staleness defects | 1 | stale | none | inherited red | Merge |
| 745 | audit smart_picks gate + empty state | 4 | stale | none | inherited red | Merge |
| 746 | KPI page spec (spec only) | 1 | stale | none | inherited red | Merge |
| 744 | forward_validator blacklist | 13 | stale | none | inherited red | Merge |
| 735 | symbol→asset-class cache | 11 | stale | none | inherited red | Merge |
| 736 | fc category persist + weather | 20 | stale | none | inherited red | Merge |
| 701 | pick rationale passthrough | 13 | stale | none | inherited red + scan | Merge |
| 700 | LLM free-first + Discord failure | 16 | stale | **1 conflict with main** | inherited red + masking | **Do not merge as-is** |
| 696 | Discord webhook rotation | 9 | stale | **superseded by 700/761** | masking + scan | Close as superseded |
| 765 | kilo additional skills | 1 | current | none | — | Merge |
| 766 | kilo jobs scan 2026-11-02 | 1 | current | none | — | Merge as dated snapshot |

## Detailed findings

### PR #749 — resolver true exit time · recommended: merge after 2 fixes

The most valuable PR in the set. It fixes a real measurement defect: every resolution path stamped
`resolved_at = resolver run-time`, so 73 MomentumEMA picks all closed at `2026-10-20T00:02:50Z` while
actually hitting TP/SL on different bars. That is not a cosmetic timestamp — it poisons any
per-bar or per-minute analysis of closes.

What it does:
- `_exit_ts_str()` — new helper; uses `pick['_intrabar_exit_ms']` (the hitting bar's ms) when present.
- `_check_tp_sl_intrabar` — records the current bar's timestamp as a side-channel before returning.
- `TIME_EXIT` no-live-price path — status becomes `UNRESOLVED_NO_PRICE`, never `0.0`.
- Adds `tools/check_batch_closes.py`, `tools/export_closed_picks_full.py`,
  `tests/test_batch_close_exit_time.py`.

**Fix 1 — the new status value has no consumer.** `UNRESOLVED_NO_PRICE` is written by the resolver, but
nothing downstream knows it. Verified on `main`:

- `audit_trail/dashboard_generator.py:1831` filters closed picks by an explicit allowlist:
  `("CLOSED","RESOLVED","WON","LOST","SL_HIT","TP_HIT")`. `UNRESOLVED_NO_PRICE` is not in it, so those
  picks silently vanish from symbol track stats instead of being counted as "unmeasured".
- `_build_strategy_symbol_track_stats` (defined at line 5661; the `TIME_EXIT`/`CLOSED` branch is at line
  5672) and `_track_win_loss` (defined at 5714; same branch at 5732) both key on
  `exit_reason == "TIME_EXIT" or status == "CLOSED"`. `TIME_EXIT` + `UNRESOLVED_NO_PRICE` still matches
  on the `exit_reason` half, so it falls into the `pnl > 0.01 / pnl < -0.01` branch — but `pnl` is
  `None`, so `float(None or 0)` = `0.0`, and it lands in **neither** win nor loss. Correct outcome by
  accident, but the intent is not expressed anywhere.
- `_resolve_status` (defined at line 7451; the early return is at 7455) returns `caller_status` unchanged
  unless it is exactly `CLOSED`, so `UNRESOLVED_NO_PRICE` propagates to the dashboard verbatim — and the
  dashboard's JS has no branch for it.

This is the guide's "deploy the parent and the child in one payload" problem in a different costume: a
new value introduced without the readers. **Fix:** add `UNRESOLVED_NO_PRICE` to the closed-status
allowlist at line 1831, and add an explicit branch in both track-stats functions that counts it as
neither win nor loss (and optionally surfaces a separate "unmeasured" counter). Without that, the fix
is half-landed.

**Fix 2 — the comment claims a guarantee the code does not make.** The PR adds, in `_check_tp_sl_intrabar`:

```python
pick["_intrabar_exit_ms"] = bar.get("timestamp")
```

with a comment saying "at return this is always the hitting bar's timestamp". That is true only if the
loop returns on the first hit. Read the loop on `main`: it does `if sl_hit: return ...` /
`if tp_hit: return ...` — so yes, it returns immediately. But `bar.get("timestamp")` may be `None` for
unstamped sources, and the helper's `isinstance(_ms, (int, float)) and _ms > 0` guard silently falls back
to run time. That fallback is correct behaviour, but the test asserts `len(distinct) == 20` — an
unstamped source would produce 1 distinct value and fail the test with a confusing message. **Fix:**
assert `>= 15` only (which the test also does) and drop the `== 20` line, or add an explicit
"all bars stamped" precondition assertion.

**Not a blocker but worth a follow-up:** the PR leaves `TIME_EXIT` run-time-stamped rows as-is and flags
them `exit_time_estimated=true`, which is honest. It does not wire a historical-bar exit price. The PR
body says this. Fine — just do not let the flag be forgotten; nothing consumes
`exit_time_estimated` either.

### PR #756 — DSR>1 + resolver hit-ts · recommended: rebase on 749

Overlaps 749 in `audit_trail/universal_pick_resolver.py` and introduces a **different** mechanism for the
same problem:

| | 749 | 756 |
|---|---|---|
| Side-channel key | `pick['_intrabar_exit_ms']` | `pick['_hit_bar_ts']` |
| Set when | every loop iteration, before the SL/TP check | only when `sl_hit or tp_hit` |
| Helper | `_exit_ts_str()` | `_hit_ts_iso()` |

Two keys, two helpers, one bug. Merging both leaves the resolver with two representations of "the bar
that hit" and two code paths that must agree.

756 also carries a genuinely separate fix that 749 does not have — `_per_pick_price` gaining an
`as_of_ms` parameter so TIME_EXIT prices use the *latest* bar at/before expiry, not the *first* bar
at/after entry:

```
-        for b in bars:
-            if ts is not None and ts >= entry_ms:
-                 close = b.get("close")
-                 if close: return float(close)
+        best = None
+        for b in bars:
+            ...
+            if as_of_ms is not None and ts > as_of_ms: continue
+            if close and (best is None or ts > best[0]): best = (ts, float(close))
```

This matters, and it is correct: on `main` the helper returns the **first** post-entry bar, so a pick
held for three days is priced at its entry bar's close. The docstring on `main` (line 693 onward) even
says "Prefers the latest intrabar OHLC bar whose open time is >= the pick's entry timestamp" while the
code returns the first match — docstring and code disagree on `main` today. 756 fixes the code.

**Recommendation:** land 749 first (or 756's `_per_pick_price` hunk first), then rebase the other,
collapsing the two side-channels to one. Do not merge both as-is.

### PR #757 — audit evidence cards · 33 files · review then merge

Largest diff in the set and it touches all three deploy paths. Two things to check before merging:

1. It modifies `.github/workflows/audit-dashboard.yml`, and this repo's own `AGENTS.md` records that the
   `push:` trigger was deliberately removed from that workflow on 2026-05-19 because of a cancel-cascade.
   Confirm the PR does not reintroduce a push trigger.
2. 33 files with dashboard HTML/JS is the class of change that silently breaks the `/audit/` page. There
   is no screenshot or Playwright evidence in the body. Ask for one before merging — the repo has a
   Playwright setup and `tests/mental-health-resources.spec.ts` is known to pass locally.

### PR #761 — FTP credential rotation · recommended: merge after 1 fix

`tools/ftp_credentials.py` is well built: `FTPCredentials` dataclass with `password: field(repr=False)`,
control-character validation, no hardcoded secret, and a test that asserts the password is absent from
`repr()`. That is the right shape.

**The fix — precedence is wrong when both env and file agree on host/user:**

```python
password = env.get("FTP_PASS") or env.get("FTP_PASSWORD")
path = Path(credential_file or env.get("FTP_CREDENTIAL_FILE") or Path.home()/"dbpasses.txt")
if path.is_file() and host == HOST and user == USER:
    password = read_local_password(path)     # <-- file unconditionally wins
```

If the host and user are the defaults, the **file always overrides `FTP_PASS`** — even when the operator
deliberately set `FTP_PASS` for a one-off deploy. The PR's own test is named
`test_rotated_local_value_supersedes_stale_50webs_environment`, which tells you this was intentional. But
"stale env beats fresh env" is a guess about operator intent. A CI job that sets `FTP_PASS` explicitly
will be silently overridden by a file on the runner — and if that file is stale, the deploy fails with a
confusing auth error rather than a clear "env ignored" signal.

**Fix:** make the precedence explicit and documented, and make the choice visible:

- If `FTP_PASS` is set **and** the file also has a value → raise, naming both sources, unless
  `FTP_PREFER_FILE=1` is set. Silent precedence between two credentials is how you get a wrong deploy.
- Or invert it: env wins, file is the fallback. That matches the 12-factor convention and the rest of this
  repo's env handling.

Either way, log which source was used (never the value).

**Secondary:** `read_local_password` matches `"50WEBS_FTP" in label and "PASS" in label` and then reads
`next(source)`. A line like `50WEBS_FTP host` would not match (no PASS) — good. But `50WEBS_FTP PASSWORD
RESET` would match and return the next line. Low risk, but tightening to an exact label set would be
better than substring matching, which is exactly the bug the Freebuff chatlog records for
`OPEN ROUTER API KEY (OPENROUTER)`.

### PR #700 — LLM free-first routing · do not merge as-is

Two problems:

1. **It conflicts with `main` on `litellm_config.yaml`.** The PR is cut from a 346-line version of the
   config; `main` now has a 790-line version with a different group structure
   (`ULTRA_FREE_*`, `ULTRA_PAID_MODE_*`, `ZZZ_BAD_LEGACY_MIXED_F_*`). The PR's chain edits target group
   names (`free-mode`, `free-mode-large`, `free-mode-tools`) that **do not exist on `main`**. Merging this
   would either conflict or, worse, silently apply nothing.
2. **Its central idea is already on `main`.** The PR's policy note says "exhaust EVERY free group before
   touching a paid one." The `main` config has `ULTRA_FREE_*` groups with `ULTRA_PAID_MODE_*` as the
   terminal fallback — same intent, different (and newer) naming.

**Recommendation:** re-derive the free-first policy against the current group names, or close it. The
Discord webhook loud-failure half of the PR (in `coinglass_strategies/discord_notify.py` and
`shared/failover_notifications.py`) is separable and may still be valuable — split it out.

### PR #696 — Discord webhook rotation · close as superseded

Cut from the same 346-line `litellm_config.yaml` era, and its `lint-masking` + `scan-new-additions` jobs
fail. `#700` and `#761` cover the same ground (secret rotation, no embedded defaults). Close it and keep
the rotation record in `updates/`.

### PR #758 — BTC evaluator drawdown · rebase required

The only PR with `mergeable=CONFLICTING` / `mergeStateStatus=DIRTY`. Its target is stated in the body as
`oc-winning-candidate`, not `main` — so a conflict against `main` is expected, not a defect. Confirm the
PR is retargeted deliberately; if it is meant for `main`, rebase.

### PRs 711, 713, 735, 736, 744, 745, 746, 750, 759, 763, 765, 766 — no substantive findings

All are stale relative to `main` and all show the same inherited-red pattern. Individually low risk.
The only one that needs a second look is **#713**, because its stated purpose is fixing the dupguard
false-failure — the B2 blocker. Read it before fixing B2 yourself, to avoid duplicating the fix.

### Cross-PR observation

Every PR is cut from a `main` that has moved substantially since (the repo carries heavy bot traffic —
`origin/main` is 84,138 commits deep). I measured this two ways:

- **Directly, for the 8 PRs I fetched** (749, 756, 757, 759, 760, 761, 700, 696): each head is 84,138
  commits behind `origin/main`.
- **By creation date, for the rest:** #711/#713 were opened 2026-10-04, #735/#736 on 10-18, #744–#750 on
  10-20, #759 on 10-23, #763 on 11-01, #765/#766 on 11-02. Against a repo whose `main` receives dozens of
  bot commits per hour, all of these are structurally stale even where I did not fetch the head.

None of them shows a rebase in CI, and CI will not catch it: the `paths:` filter on `ci-tests.yml` means a
conflicting change outside `paper_trading/`, `alpha_engine/`, `audit_trail/`, `tests/`, or the pinned
requirements files never triggers a test run at all.

The queue therefore is not reviewable one-by-one. It needs a batch rebase pass **after B1 is fixed** —
otherwise every rebase lands on a red `main` and re-confirms the inherited failure.