# 02 — Blockers

Ordered by "how many other things this unblocks". Each has evidence and a verification command.

## B1 — `main` is red, and the pin says so

**Severity:** S1. Blocks every PR's test signal.

**Symptom.** `CI Tests` fails on `main` on every push. All 8 open PRs that ran `test` inherit the same failure.

**Evidence.** `requirements.txt:2` pins `pandas==2.1.4`. `tests/test_combined_book_sleeves.py:17` uses:

```python
_MONTH_ENDS = pd.date_range("2025-01-31", periods=13, freq="ME")
```

`"ME"` (month-end) exists in pandas ≥ 2.2. On 2.1.4 `pd.date_range` raises
`KeyError: 'ME'` from `pandas._libs.tslibs.offsets._get_offset`, at **collection** time, so pytest
reports an ERROR and the whole file contributes 0 tests.

**Proof it is the pin and not the code.** Run against 2.1.4 to reproduce; run against 2.2.3 and it passes.
This machine has 2.2.3, so `pytest tests/test_combined_book_sleeves.py -q` returns `6 passed` locally
while CI returns `ERROR`. That divergence is the signature of a version-pin defect, not a flaky test.

**Fix.** Pick one, and only one:

- **Preferred:** `freq="ME"` → `freq="M"` in `tests/test_combined_book_sleeves.py:17`. `M` is accepted by
  both 2.1.4 and 2.2.x, so the test works under the pin and under any future bump. One character.
- Alternative: bump the pin to `pandas==2.2.3`. Correct if the code genuinely needs 2.2 semantics — but
  then every other file in the repo must be re-validated against 2.2, which is a bigger change than the
  one-character fix.

Do **not** "fix" it by loosening the pin to `pandas>=2.1`. That is what let the drift happen in the first
place, and `requirements-worldclass.txt:6` already carries `pandas>=2.0.0` — an unpinned second source of
truth for the same dependency.

**Verify after fix:**

```bash
pip install 'pandas==2.1.4'
python3 -m pytest tests/test_combined_book_sleeves.py -q     # must be 6 passed
```

**Why this is the top blocker:** until it is fixed, no PR's red `test` job means anything. Every per-PR
review below has to discount it. Fixing it is what makes the rest of the queue readable.

## B2 — `detect-duplicate-large-blobs` cannot fail on findings

**Severity:** S2. A gate that looks like a gate and is not.

**Evidence, from the workflow itself.**

`FAIL_ON_FINDINGS` defaults to `false` for `push` events:

```yaml
FAIL_ON_FINDINGS: ${{ github.event.inputs.fail_on_findings || (github.event_name == 'workflow_dispatch' && 'true' || 'false') }}
```

So the `if [ "${HAS_FINDINGS}" = "true" ] && [ "${FAIL_ON_FINDINGS}" = "true" ]` block at line ~180 is
unreachable on a branch push. The job can only fail by being **cancelled**.

And it is cancelled constantly, because of the concurrency group:

```yaml
concurrency:
  group: branch-large-file-dup-guard
  cancel-in-progress: true
```

One global group, every non-main branch push, and the scan walks every branch tree (2–3 h). Any other
branch push cancels the in-flight run.

**Proof.** Every failing instance I examined reports `cancelled`, never `findings`:

| PR | Job conclusion | Started | Ended |
|---|---|---|---|
| 749 | `cancelled` | 03:10:52 | 03:13:55 |
| 756 | `cancelled` | 23:24:11 | 23:26:58 |
| 757 | `cancelled` | 23:37:39 | 23:39:11 |
| 700 | `cancelled` | 04:53:51 | 04:58:32 |
| 696 | `cancelled` | 22:28:09 | 04:28:24 (+6 h) |
| 761 | `cancelled` | 04:34:32 | 04:37:17 |

The job's own log confirms `HAS_FINDINGS:` was **empty** — the scan never reached the output step:

```
FAIL_ON_FINDINGS: false
...
##[error]The operation was canceled.
...
HAS_FINDINGS:
```

**Step-level proof.** From the job API, the scan step is the one that dies, and the enforcement step
"passes" on an empty value:

```
conclusion: cancelled
   1 success    Set up job
   2 success    Checkout (partial clone)
   3 success    Fetch branch refs
   4 cancelled  Scan for duplicated large blobs across non-main branches
   5 skipped    Update job health page with timestamped alert
   6 success    Enforce fail-on-findings policy      <-- passed with HAS_FINDINGS empty
   7 success    Upload findings artifact
```

So `Enforce fail-on-findings policy` is **not** where the red X comes from. It exits 0 because
`HAS_FINDINGS` is empty and `FAIL_ON_FINDINGS` is `false`. The job conclusion is `cancelled`, which the
check-runs API reports as `fail`. That distinction matters: the gate is not reporting findings, and the
enforcement step has never once run against a populated `HAS_FINDINGS` on a push event.

**Fix options, in order of preference:**

1. **Stop running it on push.** Make it `workflow_dispatch` + schedule only. It is a repo-wide hygiene
   scan, not a per-commit gate. This removes the red X from every PR immediately.
2. If it must stay on push: drop `cancel-in-progress`, scope the group per-branch, and add a `timeout-minutes`
   so a stuck scan cannot hold the group.
3. Either way, set `FAIL_ON_FINDINGS` to `true` deliberately — otherwise the failure branch is dead code
   and the artifact step is the only output. And fix the step-6 default so it fails when the scan was
   cancelled rather than treating an empty output as "no findings".

**Do not** treat any PR's dupguard red X as a finding about that PR until this is fixed. It is a
cancellation.

## B3 — `wiring` carries a deliberate defect and a workflow that publishes it

**Severity:** S2, with an S1 side effect if merged.

Two commits on `wiring` exist only to test that a broken Mermaid diagram fails:

```
4294fd835f1 test: deploy broken mermaid diagram to GH pages
1d9354ab9e2 simulation: deploy broken mermaid diagram for swarm audit
```

`4294fd835f1` adds `.github/workflows/mermaid-test-deploy.yml`:

```yaml
on:
  push:
    branches: [ wiring ]
...
      - name: Deploy to GH Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/mermaid_tests
```

`publish_dir` is `./docs/mermaid_tests`, which contains `broken.html` — a page with three deliberate
Mermaid errors (duplicate node id `E` with conflicting text, an invalid `--invalid-arrow-->`, and an
unclosed `[Incomplete` bracket). The workflow publishes it to GitHub Pages **with no `keep_files: false`,
no clean step, and no test assertion**. `peaceiris/actions-gh-pages` force-publishes the directory
contents, so the broken page becomes the site's Mermaid test surface.

Three separate problems:

1. **A push to `wiring` publishes a known-broken page.** That is the workflow's stated purpose, but there
   is no guard that the page is only ever the test fixture — if `docs/mermaid_tests/` ever gains a real
   page, it gets published alongside or replaced.
2. **The trigger is a feature branch, not a test.** Branch-scoped deploy triggers couple the site to
   whoever is working on that branch. `wiring` is also the branch that carries the 36-file Inception
   retirement, so a routine retirement push publishes a broken page to production Pages.
3. **No `concurrency` group.** Two pushes to `wiring` race, and `peaceiris` force-pushes — last writer
   wins, silently.

**Fix.** Delete both commits from `wiring`, or move the fixture to a `workflow_dispatch`-only workflow
with `if: github.ref == 'refs/heads/wiring'` plus a `concurrency` group and an explicit assertion that the
published tree is the fixture. If the goal was "verify the audit detects a broken diagram", that
verification belongs in a test that runs on the audit tooling, not in a publish step.

**Blocking effect on the retirement:** `wiring` is the branch carrying the Inception retirement — the only
live engineering change in the 21 unmerged branches. Anything that merges the retirement merges these two
commits unless they are separated first.

## B4 — `forreviews/salesforceyetagain-v4` publishes an invented credential

**Severity:** S2. On `main`, in a folder that reads as authoritative.

`forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/certifications.md` lists:

> `| Specialized | ServiceNow Certified Salesforce Admin | Integration with ServiceNow workflows |`

No such certification exists. This is not a naming quibble — it is a credential a job candidate could put
on a résumé and be caught by.

**Correct list** — verified against the DevOps guide's own Certifications section
(`docs/salesforce/devops-engineer.md`, "Certifications"), which is the authoritative source for this track:

| Real credential | What the guide says it maps to |
|---|---|
| Platform Developer I | "The PD1 the posting names. Apex, tests, and the platform model you deploy" |
| Platform App Builder | "Metadata you move every week: objects, Flow, security" |
| Platform Administrator II | "The posting's name [Advanced Admin]. Salesforce renamed this credential to Platform Administrator II. Study the current exam guide and use both names in conversation" |

And the guide is explicit on the point the file gets wrong:

> "A Salesforce 'DevOps Engineer' cert — **There is not an official one to list as if it existed.** Copado,
> Gearset, and AutoRABIT offer their own certificates. Those show tool time. They do not replace PD1."

**Fix.** Delete the "ServiceNow Certified Salesforce Admin" row. Replace the table with the three above,
plus the guide's own caveat that vendor certs exist but are not a substitute.

**Note on a claim I did not make.** Two of the peer bundles in the learning repo claim the
"Development Lifecycle and Deployment Architect" credential fills the DevOps gap. That credential does
exist, but the DevOps guide does not name it, so I am not asserting it here — it would need its own
verification against the official credential page before entering a curriculum. Flagging it as a follow-up
rather than repeating it.

## B5 — No owner and no record for the `job-search-*` overlap

**Severity:** S3, but it will cost review time.

Five branches (`job-search-2026-11-03`, `-fresh-48h`, `-jd-scoring`, `-ledger`, `-rounds21-27`) carry
42–45 commits each and overlap heavily. No consolidation note says which is canonical. Reviewing them
individually duplicates work; merging more than one risks conflicting ledgers.

**Fix.** One of them is canonical; the others are deleted or marked superseded in a single
`updates/2026-11-14-job-search-branch-consolidation.md`.

## B6 — The four tool branches merge with zero test evidence

**Severity:** S2. Not a defect in the code — a hole in the gate.

`ci-tests.yml` has a `paths:` filter (lines 13–22 for push, 24–33 for PR) that does not include `tools/**`
or `config/**`. Verified by matching each path against the filter:

| Changed file | CI runs? |
|---|---|
| `audit_trail/universal_pick_resolver.py` | yes |
| `tools/safe_patch.py` | **no** |
| `tools/check_retired_providers.py` | **no** |
| `config/api_model_roster.json` | **no** |

So all four small tool branches (`feat/safe-patch-helper-2026-11-12`,
`feat/retired-provider-guard-2026-11-12`, `feat/ast-reviewer-codemod-2026-11-12`,
`feat/hermes-web-menu-entry-2026-11-12`) and the `wiring` retirement's `config/api_model_roster.json`
change merge **without a single test running**.

Worse: `ci-tests.yml:203` executes `tools/tests/` in its run step, and `tools/tests/` exists with two files
(`test_edge_filter_engine.py`, `test_forex_unblock_tracker.py`) — but `tools/tests/**` is not in the filter
either. Two test files that can never be triggered by a change to the code they cover.

**Fix.** Add `tools/**` and `config/**` to both `paths:` blocks. Four lines. Until then, the correct review
verdict on those branches is "unverified by CI, reviewed by reading only" — which is what
`01_cross_reference_matrix.md` records for them.

**Why it matters for the Salesforce framing:** this is the guide's §2 in its purest form. The guide says a
deploy fails when "the payload references something the target does not have, and you did not include it."
Here the test payload does not include the code it tests, and nothing fails — it silently does not run.