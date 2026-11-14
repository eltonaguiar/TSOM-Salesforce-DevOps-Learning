# Full-state re-run — 354K tokens, and what it did not improve

**Follows `SUBQ_CONTEXT_BUDGET_CORRECTION.md`.** The 384K-token claim is real. I put the live site, the
merged pages, and the repo (minus four exact-duplicate twins) in `state` in one call.

| | |
|---|---|
| State | 1,421,668 characters |
| Payload | 1,479,564 bytes |
| Reported `input_tokens` | **354,526** |
| Output tokens | 0 |
| Questions | 8, batched |

354K tokens is inside the 384K cap. The call succeeded. The needle-test prediction held.

---

## Results

| # | Question | Answer | Confidence |
|---|---|---|---|
| 1 | Live asserts heap 6/12 MB? | **Yes** | 0.425 |
| 2 | Merged asserts heap 10/25 MB? | **Yes** | 0.730 |
| 3 | Repo contains the 6/12 MB false claim? | **Yes** | 0.444 |
| 4 | Live states 39 MB payload? | **No** | 0.622 |
| 5 | Merged states 39 MB payload? | **Yes** | 0.772 |
| 6 | Port the merge? | **No** | **0.467** |
| 7 | Which is more complete? | repo bundles | 0.456 |
| 8 | Which is more accurate on limits/coverage? | repo bundles | **0.206** |

q1–q5 are **fact-finding** and they are right (q1/q3/q4 match independent verification; q2/q5 match the
merged text). q6–q8 are **decisions** and they are worse than the evidence-based run:

| Decision | Evidence-as-criteria (earlier) | Full corpus in `state` |
|---|---|---|
| Port the merge? | **Yes, 0.949** | No, 0.467 |
| More complete? | repo, 0.964 | repo, 0.456 |
| More accurate? | merged (known-answer: 0 false) | **repo, 0.206** |

The full-state run **flipped "port the merge" from Yes to No** and **called the repo more accurate**, which
the known-answer test contradicts (repo: 5 of 8 false assertions; merged: 0 of 8). Both of those full-state
answers sit below the 0.6 gate, so they should not be acted on — but they would have been, if confidence were
ignored.

## What this means

**Large context helps the model find facts. It does not replace structured evidence for decisions.**

The needle test showed it can retrieve a unique string from 1.2M characters. q1–q5 show it can answer
presence questions about three large documents in one call. That is the 384K-token design working.

q6–q8 show the other half: a decision ("should we port?") asked against raw text, with no measurements as
criteria, returns a low-confidence coin flip — and in two cases the wrong way. The evidence-as-criteria run
of the same decision, with `live_false_assertions: 4` and `merged_false_assertions: 0` supplied as numbers,
returned Yes at 0.949.

**Do not substitute the corpus for the measurements.** Put the documents in `state` when the question is
"does this text contain X". Put the measurements in `criteria` when the question is "what should we do".

That is the same layering as `SUBQ_NATIVE_APPROACH.md`, now confirmed at the advertised context size:

| Question type | Where the content goes | What we saw |
|---|---|---|
| Fact / presence | documents in `state` | q1–q5 correct, 354K tokens |
| Decision / what to do | measurements in `criteria` | 0.949 vs 0.467 on the same question |

## What still holds after the correction

- 384K tokens is real; the 4.5K plateau was filler compression.
- Unknown API fields are silently ignored.
- Confidence below ~0.6 means "do not act".
- Criteria evidence drives decisions; raw text does not substitute for it.
- The A/B test (starved vs fuller unique context improving answers) still holds — it was about unique
  content volume, not about a 32K ceiling.

## Files

| File | Role |
|---|---|
| `SUBQ_CONTEXT_BUDGET.md` | withdrawn ceiling; see the correction file |
| `SUBQ_CONTEXT_BUDGET_CORRECTION.md` | the needle test |
| `fullstate_run.json` | this run's raw answers |
| `DECISION_RECORD.md` | the evidence-based decisions, which this run does **not** overturn |