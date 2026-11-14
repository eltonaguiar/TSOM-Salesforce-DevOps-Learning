# Yes / No decision record

**The binary form of the structured decision. One SubQ call, 681 input tokens, 0 output tokens, eight
questions.**

Yes/No is the cleanest structured-decision shape because it forces a commitment: there is no partial credit,
no hedge, and the confidence is the only place uncertainty can live.

| # | Question | Answer | Confidence |
|---|---|---|---|
| 1 | Does the live site contain false assertions? | **Yes** | 0.614 |
| 2 | Do the merged pages contain false assertions? | **No** | 0.781 |
| 3 | Is the repo broader than the site? | Yes | **0.408** |
| 4 | Is the repo accurate? | **No** | 0.837 |
| 5 | Does the site lack the payload limits? | **Yes** | 0.746 |
| 6 | Do duplicates exist that should be deleted? | **Yes** | 0.896 |
| 7 | Do redundant branches exist that should be deleted? | **Yes** | 0.969 |
| 8 | Does the merge improve accuracy? | **Yes** | 0.832 |

Mean confidence 0.760.

---

## Question 3 failed, and that is the useful result

`repo_broader_than_site` came back **Yes at 0.408** — below the 0.6 gate, despite the measurement clearly
showing the repo winning 10/10 on depth.

The cause was mine, not the model's. I supplied `evidence_count: 1` for that question — a scalar count that
carries no information. Every other question had specific named evidence (`"asserts heap 6/12 MB, deactivated
users cannot be reactivated, ..."`, four concrete items).

Re-running the same question with the actual measurements as evidence:

| Evidence supplied | Answer | Confidence |
|---|---|---|
| `evidence_count: 1` (what I sent) | Yes | **0.183** |
| full depth per concept (10 concepts × site/repo scores) | Yes | **0.955** |

Same answer. Confidence moved 0.183 → 0.955.

**The evidence quality determines whether the decision is actionable, and the confidence is how you can tell.**
A scalar count is not evidence; it is a label. This is the same lesson as the context-budget finding one level
down — the instrument is only as good as what you actually put into it.

## What the eight answers say

Read as a set:

- **The live site is wrong** (Q1 yes, Q2 no, Q8 yes) — it carries false assertions the merged pages do not, and
  replacing it improves accuracy.
- **The repo is broad but not trustworthy** (Q3 yes*, Q4 no) — it covers more ground and gets specific facts
  wrong. Useful as a map of *what to cover*; not as a source of *what is true*.
- **Two cleanup actions are unambiguous** (Q6, Q7) — delete the duplicate files, delete the redundant branches.
  Highest confidence in the set (0.896, 0.969), and both are mechanical.
- **One concrete content gap** (Q5) — the payload ceilings are absent from the site.

The `*` on Q3 matters: the answer is right, but at 0.408 it should not have been acted on as supplied. The
correct reading is "unresolved, needs the real measurements" — which the re-run then supplied.

## Why this shape is worth having

| Shape | What it gives you |
|---|---|
| prose comparison | an argument you have to re-verify |
| ranked list | an ordering with no confidence |
| **Yes/No + confidence** | a commitment, plus a gate on whether the evidence supported it |

The gate is the part that earns its keep. Seven of eight cleared 0.6 and can be acted on. The eighth says
"your evidence was a label, not a measurement" — which is exactly the kind of thing a prose answer would have
smoothed over.

## Files

| File | Role |
|---|---|
| `yesno.json` | the eight questions, answers, and confidences |
| `DECISION_RECORD.md` | the multi-option decisions, including the one still open |
| `SUBQ_CONTEXT_BUDGET.md` | the context limit that made these results reproducible |