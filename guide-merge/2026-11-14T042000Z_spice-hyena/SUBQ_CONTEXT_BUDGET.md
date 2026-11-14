# SubQ's real context budget — and why my excerpts were starving it

**The design claim:** SubQ evaluates a large amount of supplied context and returns structured decisions.

**What I had been doing:** feeding it ~1,100-character excerpts, because I had assumed a context limit and
built retrieval to fit one. That assumption was never measured. It was wrong, and it was costing accuracy.

---

## Measured context limit

Fed a fixed filler text of increasing length, watching reported `input_tokens`:

| State size | Reported input tokens |
|---|---|
| 2,000 chars | 425 |
| 10,000 chars | 1,568 |
| 16,000 chars | 2,427 |
| 20,000 chars | 3,007 |
| 24,000 chars | 3,586 |
| 32,000 chars | 4,123 |
| **40,000 chars** | **4,123** ← plateau |
| 50,000 chars | 4,565 |
| 120,000 chars | 4,565 |
| 250,000 chars | 4,565 |

**It silently truncates at roughly 32–40K characters (~4,100–4,600 tokens).** Beyond that, extra context is
discarded and reported usage does not move — the plateau is the evidence. Nothing errors; nothing warns.

So "large amount of supplied context" is real but bounded: about **32–40K characters per request**, not
unbounded. That is still **~15× the ~2.2K chars** I was sending per question.

## A/B test: excerpt vs full budget

Same questions, same model, same criteria format. Only the supplied context differs.

| Concept | k=2 excerpt (~2K) | Full budget (~34K) |
|---|---|---|
| heap | **site**, conf 0.573 | **repo**, conf **0.848** |
| payload | repo, conf 0.759 | repo, conf **0.882** |
| coverage | repo, conf 0.492 | repo, conf **0.601** |

Reported input tokens rose from 854/596/718 to 2,097/3,126/1,805 — roughly 3–4× more context actually used.

**The heap case is the important one: the answer flipped.** At 2K the model picked the site; at 34K it picked
the repo at 0.848. The narrow excerpt was not merely weaker evidence — it pointed the wrong way. Confidence
rose in all three cases, and `coverage` moved from an uninformative coin flip (0.492) to a real decision (0.601).

**A starved context does not just lower confidence — it can invert the answer.** That is the failure mode I had
been building into every model-judged run.

## Corrected architecture

```
semantic retrieval  ->  select up to ~32-40K chars per decision   (not 1-2K)
        ↓
SubQ, batched       ->  N decisions in one call, evidence as criteria
        ↓
confidence          ->  gate: <0.6 means measure differently, not "guess harder"
```

The retrieval step does not go away — you cannot send 1.66M characters. But its **target** was wrong by an
order of magnitude. The fix is not a better ranker; it is a bigger budget:

- Retrieve **many** chunks per side (8–12), not 2
- Prefer whole sections over snippets — a table with its surrounding prose beats two isolated rows
- Budget to ~34K chars and stop, rather than truncating at 1.1K and hoping

## What this changes about the earlier results

| Result | Status |
|---|---|
| Depth ranking (repo 10/10, mean-top-5) | **Unaffected** — that was embedding geometry, no model context involved |
| Polarity / contradiction detection | **Affected** — ran on ~1.1K excerpts; should be re-run with the full budget |
| Decision record (5 committed, 1 open) | **Provisional** — the open one (canonical bundle, 0.517) may resolve with more context |

The depth measurements stand because they never depended on SubQ's context. Every *model-judged* result is now
provisional until re-run at the correct budget.

## Why this matters beyond this task

The general failure is **optimising to an unmeasured constraint**. I designed retrieval around an assumed
context limit, never checked the real one, and the assumption quietly degraded every model decision by forcing
it to judge from a fragment.

The fix is cheap — measure the limit first, then size the retrieval to it. Measuring took four requests.

## Files

| File | Role |
|---|---|
| `SUBQ_CONTEXT_BUDGET.md` | this file |
| `semantic_embed.py` | the retrieval whose budget needs raising |
| `DECISION_RECORD.md` | the provisional decisions to re-run |