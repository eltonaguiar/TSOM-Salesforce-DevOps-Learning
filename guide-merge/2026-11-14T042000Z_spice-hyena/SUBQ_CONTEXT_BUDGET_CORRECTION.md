# Correction: SubQ's real context budget is large

**This file corrects `SUBQ_CONTEXT_BUDGET.md`.** The earlier "plateau at 4,100–4,600 tokens" was an artefact
of the measurement, not a property of the model.

---

## What was wrong

I filled `state` with a repeated sentence (`"Salesforce metadata deployment and release engineering notes. "`
repeated). Reported `input_tokens` plateaued at ~4,100–4,600 regardless of how many copies I sent.

**That is compression, not a context limit.** Identical filler is cheap to encode. Unique content is not.

The claim I had published — "it silently truncates at 32–40K characters" — is **false**. The A/B test that
showed heap flipping from wrong to right with "more context" was still valid (more unique content *did*
improve the answer), but the ceiling I inferred from the plateau was not.

## Needle-in-haystack, unique content

A unique fact (`ZEBRA-7741`) was inserted at 10%, 50%, and 90% of a filler-of-similar-sentences state of
increasing size. The question was a forced choice: is the codename `ZEBRA-7741`, `none mentioned`, or `other`?

| State size | Reported tokens | Needle at 10% | 50% | 90% |
|---|---|---|---|---|
| 40,000 chars | 5,909 | found, 0.919 | found, 0.913 | found, 0.906 |
| 400,000 chars | 57,776 | found, 0.956 | found, 0.923 | found, 0.952 |
| **1,200,000 chars** | **173,036** | found, 0.950 | found, 0.950 | found, **0.970** |

**It processed 173K tokens and found a needle at the 90% position of a 1.2-million-character state.**
Confidence did not degrade with depth or size. The 384K-token claim is consistent with this; I did not push
to 384K in this run.

Unknown fields (`context`, `documents`, `corpus`, `input`, …) are **silently accepted and ignored** —
`input_tokens` stays at 93 regardless of what is put in them. `state` is the only context channel. That is
why probing for an alternate field returned nothing useful.

## What this changes

| Earlier claim | Corrected |
|---|---|
| Silently truncates at ~32–40K chars / ~4.5K tokens | **False.** That was filler compression |
| Retrieval is necessary because the corpus is 1.66M chars | **Weaker.** 1.66M chars ≈ 400K tokens, near the 384K cap; a slightly trimmed corpus **fits in `state`** |
| My 1.1K excerpts were starving it | **Still true** — the A/B test stands. But the right fix is "put the corpus in `state`", not "retrieve 12 chunks" |
| Decision-record results are provisional pending a re-run at 34K | **They should be re-run with the full corpus in `state`** |

## Corrected architecture

```
put the documents in `state`          (up to ~384K tokens / ~1.5M chars)
        ↓
questions[] with structured criteria  (the measurements, if any)
        ↓
one batched call
        ↓
choice + confidence per question
```

Retrieval is a fallback for when the corpus exceeds the cap, not the default. For *this* comparison
(84K-char live site + 1.66M-char repo ≈ 430K tokens) a modest trim of the longest bundle files brings it
under 384K.

## What still holds

- Confidence is an evidence-sufficiency signal (no-evidence → 0.059).
- Criteria evidence drives the choice (flipping evidence flips the answer).
- Many-option ranking degrades; pairwise / Yes-No / best-match with few options work.
- Unknown fields are silently ignored — never assume a field is "accepted" because the call succeeded.
- Measuring the limit with *unique* content is mandatory. Repeated filler will always understate it.

## Files this corrects

| File | What changes |
|---|---|
| `SUBQ_CONTEXT_BUDGET.md` | the 32–40K / 4.5K-token ceiling is withdrawn |
| `DECISION_RECORD.md` | should be re-run with the corpus in `state` |
| `COMPLETENESS_VS_ACCURACY.md` | polarity numbers were from 1.1K excerpts; a full-state re-run is the next measurement |