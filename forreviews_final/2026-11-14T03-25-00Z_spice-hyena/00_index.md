# forreviews_final — cross-referenced review (spice-hyena)

**Reviewer:** `spice-hyena` (Kilo worktree)
**Session:** 2026-11-14T03:25:00Z
**Repo:** `eltonaguiar/findtorontoevents_antigravity.ca`
**Scope:** every review artifact reachable from `origin/main`, all remote branches, and all open PRs — then re-scoped against the Salesforce training guides.

## How to read this folder

| File | What it answers |
|---|---|
| `00_index.md` | This file. Scope, method, headline numbers, reading order. |
| `01_cross_reference_matrix.md` | Every review item → where it lives → state → verdict. The map. |
| `02_blockers.md` | Defects that must be fixed before anything merges. Evidence attached. |
| `03_pr_reviews.md` | Per-PR review of the 20 open PRs (correctness, staleness, CI, overlap). |
| `04_salesforce_alignment.md` | The Salesforce-guide pass: what this repo's DevOps story is missing versus the guide. |
| `05_salesforce_curriculum_v1.md` | The corrected 8-module curriculum, rebuilt from the guides' actual content. |
| `06_salesforce_runbook_template.md` | The guide's runbook/audit-pack rendered against this repo's real surfaces. |
| `07_updated_work_based_on_salesforce.md` | The *updated work* — findings rewritten with guide vocabulary and gates. |

Files 04–07 are the Salesforce pass. Files 01–03 are the pure cross-reference and stand alone.

---

## Method

1. Enumerated `origin/main`, all 191 remote branch refs, and every worktree registered in `git worktree list`.
2. Separated bot/CI traffic (`[skip ci]`, `github-actions[bot]`, `deploy:`) from human review artifacts by commit subject.
3. Pulled every open PR's head, merge state, check rollup, changed-file list, and — where the diff touched a file that already exists on `main` — the actual numstat overlap.
4. Read the failing job logs for every PR, rather than trusting the red X. That distinguished real failures from a broken gate.
5. Fetched all five Salesforce guides from the learning site and extracted the section structure and the checklists.
6. Re-read the review artifacts themselves (`updates/2026-11-12-*.md`, `forreviews/salesforceyetagain-v4/*`, the PR bodies) and checked their claims against the code.

## Headline numbers

| Measure | Value |
|---|---|
| Branches on origin | 191 (21 ahead of `main`; 1 is `gh-pages` deploy output) |
| Human-authored branches ahead of `main` | 20 (excluding `gh-pages`) |
| Open PRs | 20 |
| PRs whose `test` job fails | 8 of 8 that ran (all from B1) |
| PRs with a real conflict with `main` | 1 (`#758`) |
| Distinct root causes behind those 8 red test jobs | **1** |
| Distinct root causes behind those 8 red `detect-duplicate-large-blobs` jobs | **1** (gate bug, not findings) |
| `forreviews/` items on `main` | 5 files, one folder (`salesforceyetagain-v4`) |
| Review artifacts with no prior `forreviews_final` entry | 3 groups: the `wiring` mermaid commits, the 4 small tool branches, and `docs/freebuff-handoff-2026-11-13` |

## The five things worth acting on first

1. **`main` is red and nothing is allowed to be blocked on that.** `test (3.11)` and `test (3.12)` fail on `main` itself, on every push, because `tests/test_combined_book_sleeves.py:17` uses `freq="ME"` (pandas ≥2.2) while `requirements.txt` pins `pandas==2.1.4`. Every PR inherits this. No PR's test result is evidence about that PR until this is fixed.
2. **`detect-duplicate-large-blobs` is not a gate — it is a coin flip.** `FAIL_ON_FINDINGS` is always `false` on `push`, and the concurrency group cancels the newest run whenever any other branch is pushed. Every "failure" I examined was `cancelled`, never `findings` — and the `Enforce fail-on-findings policy` step *succeeded* on an empty value. Treat it as noise, or fix the concurrency group; do not treat it as a review signal.
3. **Four tool branches merge with zero tests running.** `ci-tests.yml`'s `paths:` filter excludes `tools/**` and `config/**`, so `safe_patch.py`, `check_retired_providers.py`, `ast_reviewer_codemod.py`, and `hermes_web.sh` merge unverified — even though `ci-tests.yml:203` runs `tools/tests/`, which can itself never be triggered by a `tools/` change.
4. **The `wiring` branch has two commits that intentionally deploy a broken Mermaid page to GitHub Pages, and no reason to exist.** Either delete them or add a guard. Right now a green-looking branch carries a deliberate defect into `docs/`, and because `wiring` also carries the Inception retirement, merging the retirement merges the defect.
5. **`forreviews/salesforceyetagain-v4` is an unfinished skeleton, not a deliverable.** Five files, four of which are meta-documents about doing research. Zero DevOps content — the one topic the whole track exists for. The index marks the DevOps doc "Pending" while the folder name claims v4. It also invents a "ServiceNow Certified Salesforce Admin" credential.

## Reproduce

```bash
git fetch --prune origin
gh pr list --state open --limit 50 --json number,title,headRefName,mergeStateStatus
for p in $(gh pr list --state open --limit 50 --json number --jq '.[].number'); do
  gh pr checks "$p" | awk -F'\t' '$2=="fail"{print FILENAME": "$1}'
done
python3 -m pytest tests/test_combined_book_sleeves.py -q   # PASSES on pandas 2.2.3 (local); FAILS on pandas 2.1.4 (CI pin)
```

## Verification note (why the reproduction command misleads)

This machine has pandas **2.2.3**; CI installs the pinned **2.1.4** (`requirements.txt:2`) and that is
exactly the axis the bug sits on. Local green + CI red is the signature of a version-pinned failure,
not of a flaky test. Confirmed from the job log: `KeyError: 'ME'` raised inside
`pandas._libs.tslibs.offsets._get_offset` at collection time, after `Successfully installed ... pandas-2.1.4`.

```bash
pip install 'pandas==2.1.4' && python3 -m pytest tests/test_combined_book_sleeves.py -q   # reproduces
```