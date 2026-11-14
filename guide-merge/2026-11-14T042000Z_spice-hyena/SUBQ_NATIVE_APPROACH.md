# How SubQ Snap would approach this

**Framing:** SubQ is a **decision** model, not a text model. Its native call is `state` + `questions` +
`criteria`, and it returns a choice with per-option probabilities and a confidence. Asking it to *compare two
documents* misuses it. The correct question is *"given these measurements, which do you choose?"*

That inverts the pipeline I had built. I was using SubQ as an oracle for individual claims, which is the least
interesting thing it can do.

---

## What I had wrong

I made **five separate API calls** for what is one decision, each carrying a single question. SubQ accepts an
array of questions and answers them in one round trip. And I was passing *prose* as criteria, when criteria are
meant to be **structured evidence the model weighs**.

## What SubQ actually does with criteria

Tested directly: same question, same options, criteria evidence flipped.

| Criteria | Choice | Confidence |
|---|---|---|
| evidence favours A (`A_depth 0.71 / B_depth 0.42`, `A_false 0 / B_false 3`) | **A** (0.971) | **0.968** |
| evidence favours B (mirror) | **B** (0.988) | **0.987** |
| **no evidence** (options only) | coin flip (0.372 / 0.373) | **0.059** |

The third row is the important one. **Without evidence it abstains rather than guessing.** Confidence is a
measure of *evidence sufficiency*, not of rhetorical force. That is a property no chat model gives you — a chat
model produces fluent prose at any confidence level.

So SubQ's confidence is usable as a gate: below ~0.6, the measurements do not separate the options, and the
correct action is to measure better, not to act.

## The SubQ-native pipeline

```
measurements (embeddings, known-answer tests, presence)
        ↓
structured criteria per decision  (one question = one decision)
        ↓
one batched SubQ call             (N questions, 1 round trip)
        ↓
choice + confidence per decision
        ↓
low confidence  ->  measure better, do not act
high confidence ->  commit
```

The model is the **aggregation layer**. It does not read the documents; it weighs the numbers.

## Demonstrated on the real problem

Ten concepts, each with measured semantic depth for both sources, batched into a single call:

```python
questions = {
  f"q{i}": {"instructions": f"For '{concept}', which source covers it more thoroughly?",
            "type": "choice",
            "criteria": {"options": ["site","repo"],
                         "site_depth": 0.354, "repo_depth": 0.659,
                         "gap": 0.305,
                         "site_coverage_frac": 0.033, "repo_coverage_frac": 0.018}}
  for i, concept in enumerate(concepts, 1)
}
```

**Result — one call, 1,198 input tokens, 0 output tokens:**

| Concept | Choice | Confidence | site | repo |
|---|---|---|---|---|
| heap | repo | 0.957 | 0.354 | 0.659 |
| coverage | repo | 0.943 | 0.389 | 0.635 |
| payload | repo | 0.961 | 0.294 | 0.694 |
| test_trigger | repo | 0.947 | 0.418 | 0.650 |
| quick_deploy | repo | 0.944 | 0.470 | 0.764 |
| destructive | repo | 0.986 | 0.438 | 0.602 |
| sandbox | repo | 0.988 | 0.397 | 0.682 |
| branching | repo | 0.988 | 0.422 | 0.683 |
| audit | repo | 0.986 | 0.393 | 0.594 |
| conflict | repo | 0.961 | 0.467 | 0.684 |

10/10 correct, mean confidence **0.966**. Against ten separate calls, this is one round trip, no output tokens,
and the same evidence always yields the same answer.

## What does not work, and why

| Attempt | Result |
|---|---|
| Rank 10 options in one question by criteria | **Degrades** — returned a criteria *key* as the choice, confidence 0.516 |
| Global "which is better" over two 100K-char documents | 10/10 TIE |
| Compare narrow excerpts without the specific claim | 8/8 NOT_ADDRESSED |

**SubQ is a choice model, not a ranking model.** It reliably answers binary and few-option questions. Asking it
to order ten options by evidence produces an ill-formed answer. Pairwise decisions, batched, are the pattern
that works.

Two smaller artefacts worth knowing:
- Criteria keys receive probability mass of their own (`A_depth_score: 0.006`) — the format treats each key as
  a pseudo-option. Harmless for the main choice, but it means the probability vector is not a clean
  distribution over the options.
- `options` (the array itself) also appears in `probabilities`. Ignore it.

## Where SubQ fits, and where it does not

| Layer | Instrument | Why |
|---|---|---|
| Measure depth | embeddings | geometric, reproducible, no opinion |
| Measure accuracy | known-answer polarity test | needs meaning, not tokens |
| Measure presence | lexical | it is a vocabulary question |
| **Decide and aggregate** | **SubQ** | weighs multi-criteria evidence, abstains when evidence is thin |

SubQ cannot discover a fact nobody measured. If the depth score is wrong, SubQ will confidently choose on the
strength of a wrong number. It is a decision layer, not an oracle — which is the same conclusion the polarity
work reached from the other direction: **a conflict is a pointer to a primary source, never a verdict.**

## The one-line answer

SubQ Snap would not be asked to compare the documentation. It would be handed the measurements — depth per
concept, assertions per claim, presence per topic — and asked to commit to a decision for each, in one batched
call, with its confidence used as the evidence-sufficiency gate. Measurement finds the facts; SubQ decides what
to do about them; primary sources adjudicate.