# 02 — Code review findings (line level, on the `jet-slime` diff)

Scope: the 41 files in `git diff origin/main...jet-slime`. Severity: **S1** ship-blocker,
**S2** should-fix, **S3** nice-to-have / note. Line numbers are on-disk `jet-slime` unless noted.

---

## A. `tools/start_litellm_proxy.sh` — the substantive change (good, with nits)

The diff is a genuinely good hardening pass: correct liveness probe, a real start lock, a port
guard, and several root-cause label fixes. The comments are unusually honest (they name the exact
failure they prevent). Findings:

### F-01 · S2 · Executable bit lost
`git diff` shows `old mode 100755 / new mode 100644`, and on disk the file is `-rw-rw-r--`
(verify: `ls -l tools/start_litellm_proxy.sh`).
Impact: any caller that does `./tools/start_litellm_proxy.sh` or a systemd `ExecStart` pointing at
the path directly will `Permission denied`. Callers that use `bash tools/...` are unaffected, which
is why it can pass a smoke test and still fail in the unit that matters.
Fix: `git update-index --chmod=+x tools/start_litellm_proxy.sh` (or restore `100755` in the commit).

### F-02 · S2 · `OPENCODE_API_KEY_ALT` is written by two different labels
Lines 309 and 339:
```
309: parse_key "OPENCODE_API_KEY_ALT"                                   OPENCODE_API_KEY_ALT
339: parse_key "OPENCODE.AI API KEY test (try Big Pickle or other free models)"  OPENCODE_API_KEY_ALT
```
Both map to the same env var. If `dbpasses.txt` contains both labels, **the last one parsed wins
silently** and there is no log line saying which credential was chosen. The comment at 301–305 also
relies on ordering ("Added AFTER the stale line so it wins") for `OPENCODE_API_KEY`.
Impact: a reviewer cannot tell which OpenCode key is live; a future re-order silently swaps it.
Fix: give each label a distinct env var, or log the winning label, or assert exactly one match.

### F-03 · S3 · `parse_key` label set is now very wide and typo-fragile
New labels include `"EXA API KEY for serach"` (typo "serach"), `"HYPERBOLIC API KEY :"` (space
before colon), `"MODELSCOPE API KEY :"`, `"INFRON API KEY(FREE 1000 requests a day ):"`. Because
`parse_key()` matches **whole lines**, these only work if the `dbpasses.txt` spelling is byte-exact
— which is exactly the class of bug F-01's sibling (the OpenRouter label) already was.
Fix: add a boot-time check that each `parse_key` label matched exactly once, and fail loud (or warn)
on zero-match for the providers that matter. This is the single highest-leverage change: it converts
a whole category of silent-degradation bugs into a startup error.

### F-04 · S3 · `[[ -v $v ]]` is bash-version dependent
Line 409 replaces `${!v:-}` with `[[ -v $v ]]`. `-v` on a name is bash ≥ 4.2; on macOS's stock
bash 3.2 it errors. The repo is Linux/systemd, so fine here, but the shebang is `#!/usr/bin/env bash`
and the script is now non-executable (F-01) — document the bash floor or use a portable check.

### F-05 · note · the `/health/readiness` and `9>&-` lock fixes are correct
`proxy_healthy()` (line 66) now probes `/health/readiness` (line 72) — right call, `/health` fans
out. The `exec 9>` lock (89–96) with `flock -w` and the `9>&-` in the child (436, 472, 478) so the
long-lived proxy does not inherit the lock — this is the correct pattern and the comments explain the
exact race. No change needed; calling it out so a reviewer does not "simplify" it away.

---

## B. `tools/verify_all_keys.py` + 5 more — literal `[REDACTED]` shipped into source (S1)

**This is the ship-blocker.** The Mercury-retirement commit's redaction pass wrote the literal
string `[REDACTED]` over env-var names and endpoint URLs in **six source files**. `origin/main` has
the real names; `jet-slime` has `[REDACTED]`. Byte-verified on disk (`xxd` of line 43:
`... 22 5b 52 45 44 41 43 54 45 44 5d 22 ...` = `"[REDACTED]"`).

| File | main | jet-slime | What broke |
|---|---|---|---|
| `tools/verify_all_keys.py` | 0 | **16** | label strings + 3 endpoint URLs (`"[REDACTED]/chat/completions"`) |
| `tools/api_model_roster.py` | 0 | **7** | provider names + key-env names (`ProviderSpec("[REDACTED]", ...)`) |
| `tools/local_swarm_review.py` | 0 | **3** | `"env": "[REDACTED]"`, HF/moonshot key names |
| `tools/model_picks_research.py` | 0 | **2** | moonshot env name |
| `config/api_model_roster.json` | 0 | **3** | `"key_env_hit": "[REDACTED]"` |
| `tools/_graphify_docs_multibackend.py` | 0 | **1** | `os.environ.get("[REDACTED]")` |
| `tools/swarm/api_consult.py` | 1 | 1 | **pre-existing on main — not this branch** |
| `.ruflo/orchestrator.py` | 5 | 5 | **pre-existing on main — not this branch** |

Representative broken lines (on `jet-slime`):
```
verify_all_keys.py:43   ("COHERE_API_KEY",          "[REDACTED]"),
verify_all_keys.py:61   ("OPENROUTER_API_KEY",      "[REDACTED]"),
verify_all_keys.py:364  return t_openai_compat("[REDACTED]/chat/completions", key, "qwen-turbo")
api_model_roster.py:90  ProviderSpec("kimi", ("KIMI_API_KEY", "[REDACTED]"), ...)
api_model_roster.py:108 ProviderSpec("opencode", ("[REDACTED]",), notes="CLI-only ...")
_graphify_docs_multibackend.py:35  os.environ.get("[REDACTED]") or os.environ.get("KIMI_API_KEY") or ""
```

### F-06 · S1 · why it is a ship-blocker (and why it is easy to miss)
The files **still parse** (`ast.parse` succeeds for all five), because `"[REDACTED]"` is a valid Python
string. So there is no syntax error and no import failure — the tools import cleanly and then **silently
do the wrong thing at runtime**: they look up an env var / dbpasses label literally named `[REDACTED]`
(never present), and call `"[REDACTED]/chat/completions"` (a non-URL). This is the worst failure mode:
green import, broken behaviour. It maps exactly to the Crash-Course governor-limit warning — "a deploy
can succeed and the feature can still fall over in prod."

Fix: revert these six files' `[REDACTED]` occurrences to the real values from `origin/main`
(`git checkout origin/main -- <file>` then re-apply only the intended Mercury removals), **or**
re-run the redaction so it does not touch source. Add a CI guard: `git grep -n '\[REDACTED\]' -- '*.py'
'*.json'` must be empty for code paths (reports/session logs are allowed to keep it).

---

## C. Inception/Mercury retirement — is it complete?

The chatlog claims "retire from every registry." Verified by `git grep -in 'inception|mercury'`:
**no live `inception` provider code remains** in `*.py`/`*.yml`/`*.sh` — the removals in
`tools/swarm/api_consult.py`, `swarm_run.py`, `worker_runner.py`, `api_model_roster.py`,
`tools/swarm_v2/swarms/core/llm_client.py`, and `_graphify_docs_multibackend.py` are clean and
consistent (provider entry + sampling defaults + cost table + engine set all removed together).

But the grep also surfaces **three things that are NOT the Inception API and must not be "fixed" by
an over-eager reviewer**:
- `mercury2/*` and `.github/workflows/mercury2-*.yml` — this is the **Mercury 2 model/strategy**
  (a local ML module + its scanner/retrain workflows), unrelated to Inception Labs' API.
- `inception_paper_trading.html` in `audit-dashboard.yml` (lines 1241/1365/1419) — a **dashboard
  filename**, not the API.
- `ai-tournament-pipeline.yml` 117–118 and `second-opinion/scripts/ask.py:47` — **retirement
  comments** that correctly explain the persona now routes via Together.

### F-07 · S3 · the chatlog's grep claim is misleading
`updates/2026-11-12-FREEBUFF-chatlog-1959UTC.md` §8 says `git grep -in 'inception|mercury'` "expect:
retirement comments only." On this branch that grep also returns `mercury2` (strategy) and
`inception_paper_trading.html` (dashboard). A reviewer following the chatlog's reproduction step will
think the retirement is incomplete. Fix the doc's grep to exclude `mercury2` and
`inception_paper_trading`, e.g. `git grep -in 'inceptionlabs|mercury-2|INCEPTION_`.

---

## D. Mermaid-test scaffolding commits — should not ship (S2)

Commits `4294fd835f` and `1d9354ab9e` add a **deliberately broken** mermaid diagram and a deploy
workflow:
- `.github/workflows/mermaid-test-deploy.yml` — triggers on `push: branches: [wiring]`, deploys
  `./docs/mermaid_tests` via `peaceiris/actions-gh-pages@v3`.
- `docs/mermaid_tests/broken.html` + `tests/mermaid_simulation/broken_diagram.{mmd,html}` — the broken
  diagram itself (duplicate node id, `--invalid-arrow--`, unclosed bracket).

### F-08 · S2 · a workflow that publishes a broken page to GitHub Pages
`peaceiris/actions-gh-pages` with `publish_dir` and no `keep_files` **replaces** the target pages
content. If the `wiring` branch is (or becomes) the Pages source, merging this to `main` and pushing
`wiring` would publish a broken page over the docs site. Even if `wiring` is throwaway, committing
deploy-to-Pages test scaffolding to a review branch is the wrong place for it.
Fix: move to a scratch repo or gate behind `workflow_dispatch` + an env flag; never `push`-trigger a
Pages deploy from a review branch. At minimum confirm `wiring` is not a Pages production source.

### F-09 · S3 · "broken" fixtures are fine as fixtures, wrong as committed site content
The `.mmd` is a legitimate mermaid *error-handling* fixture. Keep it under `tests/` only; drop it from
`docs/` (which is the published tree).

---

## E. New tool files — design-level review

Four new tools, all reading `~/dbpasses.txt` and never printing keys. Approach is sound and the
docstrings are good. Design notes:

### F-10 · S2 · four overlapping tools, no single entry point
`litellm_dynamic_models.py` (merge free models into config at boot), `free_model_discovery.py`
(emit a YAML fragment), `free_provider_audit.py` (audit which creds serve free inference),
`model_capability_probe.py` (vision/web capability). `free_model_discovery.py` and
`litellm_dynamic_models.py` **both discover free models and emit config** — overlapping
responsibility. A reviewer should ask which is canonical.
Fix: one discovery core, thin CLIs; or document the boundary (discovery = offline report, dynamic =
boot-time merge) in a README.

### F-11 · S3 · `requests` import is a hard dependency in tools that "fail open"
`litellm_dynamic_models.py` and `free_provider_audit.py` `raise SystemExit(1)` if `requests` is
missing — that is fail-*closed* for the whole proxy start path if discovery is wired in. The shell
wrapper falls back to static config on non-zero exit (good), so blast radius is contained, but the
tool's own docstring says "fail-open" while the import is fail-closed. Align the wording or wrap the
import to degrade gracefully.

### F-12 · S3 · probe traffic is real inference spend on free tiers
`free_provider_audit.py` does a live 8-token completion per provider, and `free_model_discovery.py`
probes every candidate. On metered free tiers (OpenRouter 50 req/day no-credit) a full sweep can
burn the daily budget. The OpenRouter note in `start_litellm_proxy.sh` already flags this; make the
auditors default to `--no-probe` or rate-limit, and never run them on a cron that overlaps the proxy.

---

## F. `litellm_config.yaml` (+816) — not line-reviewed

The config grew by ~816 lines (new provider groups, dynamic-model fallbacks). I did not line-review
the YAML. Two review gates a reviewer should run:
- **YAML parses** after the dynamic merge (the tool writes `litellm_config.runtime.yaml`).
- **No secret literals** in the committed YAML (`grep -iE 'sk-|key|token|password' litellm_config.yaml`
  should show only `${ENV}` references, never values).

### F-13 · S2 · gate: prove the committed config has no secret literals
This is the Salesforce-lens "secrets never in Git" check applied to the actual changed file. It is a
verification step, not a known defect — but it is the one that matters most for a config that grew
816 lines.