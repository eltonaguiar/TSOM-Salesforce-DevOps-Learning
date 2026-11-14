# 07 — Updated work, informed by the Salesforce training guides

This is the synthesis. It takes the findings from `01`–`03` and re-expresses them with the Salesforce
guides' vocabulary, gates, and discipline — then states what changes as a result.

**The core shift.** I reviewed this repo as a code review. The guides review it as a **release-engineering**
problem. Those produce different priorities, and the release-engineering one is correct:

| Code-review framing | Release-engineering framing (after the guides) |
|---|---|
| "PR #749 has a good fix with a missing consumer" | "PR #749 is a release with an incomplete audit pack and no rollback target" |
| "`main` is red because of a pandas pin" | "`main` is the production org and it rejects every deploy; the validation gate is not validating the payload that ships" |
| "462 branches is messy" | "No branching model, so hotfixes have no defined origin and no release can be tagged" |
| "CI has a broken gate" | "One of the four required pipeline stages is missing entirely, and a second is a no-op" |

## 1. Re-prioritised work queue

Re-derived using the guide's ordering: *validate before you release; tag before you can roll back;
one payload, parent and child together.*

| Rank | Item | Guide principle it comes from | Was |
|---|---|---|---|
| 1 | **Fix B1** (`freq="ME"` → `"M"`) | §9 "A green Dev sandbox is not evidence. The validation that counts is against the org you are about to change" — here: CI validates a different pandas than production runs | #4 in my first pass |
| 2 | **Create release tags from now on** | §4 "Tag production after a successful deploy… That tag is the rollback target" and "If you do not have a tag from the last good prod deploy, you do not have a rollback" | **not on my list at all** |
| 3 | **Add the missing validate stage** | §5 "Validate / Integrate / Stage / Release" — four stages, one of which does not exist here | not on my list |
| 4 | **Write the branching model down** | §4, including "A feature branch lives days, not weeks" | implicit in §3 of `04` |
| 5 | **Fix B2** (dupguard no-op gate) | §9 "validation vs quick deploy vs real deploy" — a stage that cannot fail is not a stage | #2 |
| 6 | **Separate the mermaid commits from `wiring`** | §8 "Packages… unpackaged metadata deployed from Git is still the right default" — the release unit must be the retirement, not the retirement + a deliberate defect | #3 |
| 7 | **PR #749 — add the status consumer** | §2 "If the payload references something the target does not have, and you did not include it, the deploy fails" — a new status value with no reader | #1 |
| 8 | **PR #761 — make credential precedence explicit** | §1 "Secrets never go in Git" + the guide's precision standard | not on my list |
| 9 | **Batch rebase the queue** | §7 conflict clinic — "You have a fix for each, not just the symptom" | last |
| 10 | **B4 — correct the invented credential** | Guides' Certifications section | #5 |

The two new entries at ranks 2–4 are the point of this exercise. Neither is a defect in the code. Both are
absences of release-engineering structure, and the guides name them explicitly.

## 2. What "done" means now

The guide's method is that every item ends in a checkable test. Applying that to the work:

| Item | Guide's "done when" | This repo's version |
|---|---|---|
| B1 | "You can run a dry-run and read the failure" | `pip install pandas==2.1.4 && pytest tests/test_combined_book_sleeves.py -q` → `6 passed` |
| B2 | "You can explain dry-run vs quick deploy vs a real prod deploy" | `gh run view <id>` on a branch push shows `success`, not `cancelled`, for the scan step |
| B3 | — | A push to `wiring` does not publish `broken.html`, or the workflow does not exist |
| Tags | "That tag is the rollback target" | `git tag -l 'release-*'` is non-empty and points at a known-good commit |
| Validate stage | "A human cannot push to prod without a green validation, a named test run, and a ticket id" | A prod deploy requires a green run against the deploying commit, and the run id is in the record |
| Branching | "A hotfix is cut from `main`, and it merges back into `main` and any open release branch" | Written in `AGENTS.md`, and the 21-branch backlog is closed or consolidated |
| B4 | — | `forreviews/salesforceyetagain-v4/certifications.md` lists only real credentials |

## 3. Corrections to my own earlier findings

A review that only finds other people's errors is not a review. Three of my first-pass claims were wrong or
imprecise, and the guides are what caught them:

1. **I wrote that the dupguard red X means "findings".** It does not. Step-level API output shows the scan
   step `cancelled` and `Enforce fail-on-findings policy` **succeeding** on an empty `HAS_FINDINGS`. The red
   X is the job conclusion, not a policy failure. Corrected in `02_blockers.md` B2.

2. **I wrote that CI "does not surface a coverage number".** It does — `ci-tests.yml:246` runs
   `coverage report`, `:238` uploads `coverage.xml`, and `:212` gates at `--cov-fail-under=10`. What is
   missing is the *record*, not the number. Corrected in `04_salesforce_alignment.md` §6.

3. **I initially treated the two mermaid commits as a code-quality problem.** Under the guides' framing they
   are a **release-pipeline** problem: a push-triggered deploy that force-publishes a known-broken page.
   The fix is different (remove the trigger, not clean the fixture).

## 4. The one structural change worth making

If only one thing from this pass is adopted, it should be the guide's §1 opening sentence:

> "Production is not the source of truth. Git is. The org is a target you deploy to."

This repo inverts it in one specific place: `TORONTOEVENTS_ANTIGRAVITY/index.html` is in Git (4,845 lines,
canonical), but `_next/static/chunks/*.js` is **only on the production FTP server**. The `AGENTS.md`
gotcha list already records this — tests fail locally because the bundled chunks are absent from the repo.

That is a source-of-truth inversion. Two consequences follow, and both are documented symptoms in this repo:

- A local checkout cannot be validated against what is actually deployed. "Green locally" and "green in
  production" are different claims about different artifacts — the guide's honest-rehearsal rule, violated
  structurally.
- A rollback means re-uploading from a backup, not deploying a previous commit. That is the guide's
  "you cannot undelete records" case, applied to the frontend.

**Recommendation:** commit the built chunks, or record their sha in a manifest that the deploy verifies.
Either makes the deployed artifact a deploy target rather than a source of truth.

## 5. What I did not do, and why

- **I did not fix B1.** It is a one-character change to `tests/test_combined_book_sleeves.py:17`, and it is
  on the critical path for every PR. But it changes `main`, and this session's brief was to review and
  report, not to alter the shared branch. It is written up with the exact edit and the verification command
  so it can be applied deliberately.
- **I did not merge or rebase any PR.** Same reason, plus the queue needs the batch pass described in §1.
- **I did not write to `forreviews/salesforceyetagain-v4/`.** That folder is on `main`, is the other agent's
  working set, and the repo rule is that a fix record goes in `updates/`. B4 is recorded here instead.
- **I did not attempt the Salesforce labs.** They require Developer Edition orgs and credentials, which are
  out of scope for a code review session. They are specified in `05_salesforce_curriculum_v1.md` with
  terminal exercises so they can be executed by whoever picks up the track.

## 6. Effect on the Salesforce track

The guides' DevOps track is built from requisition 276046. Applying it to this repo produces a concrete
result: **this repo is a working demonstration of about 40% of that job description, and a counter-example
for the other 60%.**

What the repo demonstrates:
- Git as the record, with a commit-message convention that carries ticket ids
- CI with a real test gate, a quarantine mechanism for known drift, and coverage reporting
- A fix-record convention (`updates/*.md`) that is genuinely good — the Freebuff chatlog's §9 is a
  hand-built audit pack
- Defensive engineering: `safe_patch.py` (anchored, syntax-gated, atomic), `check_retired_providers.py`
  (structural JSON scanning rather than text grep), `check_batch_closes.py` (an operational gate with a
  baseline defect count)

What it lacks, and what the track must therefore teach by other means:
- No environment path (Dev/QA/UAT/Pre-Prod/Prod)
- No release tags, no rollback target
- No validate-only deploy stage
- No segregation of duties — one person authors and merges
- No masking/refresh equivalent for the production data path
- No packaging story — the retirement is one 4,254-line blob

That split is the useful output. The curriculum in `05` is ordered so that the learner builds the missing
half first, in Developer Edition orgs, where a mistake costs nothing.