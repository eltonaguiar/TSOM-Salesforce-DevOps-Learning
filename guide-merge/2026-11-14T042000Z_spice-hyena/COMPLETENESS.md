# Which document is more complete?

**"Complete" is not measurable without a target.** That is why the earlier whole-document comparison returned
10/10 TIE: two documents can only be compared for completeness against something they are both trying to
cover.

So: define the target, measure against it, then ask.

---

## Target

The **75-concept external Salesforce platform taxonomy** — built from the wider platform and the DevOps role's
requirements, not from either source. (Using either source's own scope would make the comparison circular,
which is exactly what the first attempt did.)

Completeness = concepts covered out of 75.

## Measurement

| Source | Concepts | Completeness |
|---|---|---|
| **repo bundles** | **73 / 75** | **97.3%** |
| merged pages | 66 / 75 | 88.0% |
| live webpages | 65 / 75 | 86.7% |

The repo misses 2; the merged pages miss 9; the live site misses 10.

**The merge added exactly one concept by presence** (`einstein`). Everything else the merge changed is *within*
concepts the live site already had — numbers, rules, version distinctions. That is the whole point of the
merge, and it is why presence-based completeness barely moves (65 → 66) while depth and accuracy move a great
deal.

## SubQ judgment on the same evidence

| Comparison | Verdict | Confidence |
|---|---|---|
| repo vs merged | **repo more complete** | 0.969 |
| repo vs live | **repo more complete** | 0.964 |
| merged vs live | merged more complete | **0.483** |

The 0.483 is the useful number. 66 vs 65 is a 1.3-point difference — one concept — and the model correctly
declined to call it. That is the gate doing its job: a near-tie is reported as a near-tie, not rounded up into
a decision.

## The answer, split by axis

"Which is more complete" has three defensible answers depending on what completeness means:

| Axis | Winner | Evidence |
|---|---|---|
| **Breadth** — concepts covered | **repo** (73/75) | presence against the external taxonomy |
| **Depth** — how thoroughly each concept is treated | **repo** (10/10 concepts, 0.594–0.764 vs 0.294–0.470) | mean-top-5 embedding similarity |
| **Accuracy** — freedom from false assertions | **merged** (0 of 8) | known-answer polarity test |

**The repo is the most complete document set. It is also the least accurate.** It covers 73 of 75 concepts and
falsely asserts 5 of 8 known-false claims.

**The merged pages are nearly as broad (66/75) and are the only source with zero false assertions.**

So the honest answer to "which is more complete" is: **the repo, on both breadth and depth — but completeness
is the wrong axis to select on.** A document that covers 97% of the concepts while getting specific facts wrong
is worse for a reader than one covering 88% correctly, because the reader cannot tell which 3% to distrust.

That is why the decision record (`DECISION_RECORD.md`) resolves to *merge from the repo's breadth* but *trust
the merged pages' facts* — rather than to "the repo is more complete, use the repo."

## The methodological point

Two attempts failed before this worked:

| Attempt | Result | Why |
|---|---|---|
| compare two documents in one call, no target | 10/10 TIE | nothing to be complete *relative to* |
| presence against a taxonomy derived from the pages | 48/49 | circular — the pages defined their own target |

**Completeness requires an external target.** Once supplied, the measurement is trivial and the judgment is
decisive (0.96+ where the gap is real) or appropriately abstains (0.483 where it is not).

## Files

| File | Role |
|---|---|
| `completeness.json` | the per-source counts |
| `external_taxonomy.json` | the 75-concept target |
| `SEMANTIC_VS_LEXICAL.md` | the depth axis |
| `COMPLETENESS_VS_ACCURACY.md` | the accuracy axis |