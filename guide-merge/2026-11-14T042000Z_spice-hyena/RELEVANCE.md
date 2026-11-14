# Relevance scoring — and its limits

**The fourth decision shape: how relevant is document A to document B.**

Distinct from best-match (select one from many) and Yes/No (binary). Two things make it different: it is
**graded** (not binary) and **directional** (A→B is not B→A).

---

## Direction is real, and symmetric measures cannot express it

Tested with a pair chosen so the two directions *should* differ — a narrow deep-dive (8 concepts) and a broad
survey (64 concepts):

| Direction | Verdict | Confidence |
|---|---|---|
| narrow deep-dive → broad survey | **Marginally relevant** | 0.644 |
| broad survey → narrow deep-dive | **Relevant** | 0.566 |

That is the correct asymmetry. A broad survey gives a reader of a narrow deep-dive useful context; a narrow
deep-dive is a subset of what the survey already covers, so it adds little to a reader of the survey.

**Every similarity measure I used earlier is symmetric by definition.** `cosine(A,B) == cosine(B,A)`,
`jaccard(A,B) == jaccard(B,A)`. So the entire depth and duplicate analysis in this folder was direction-blind.
It was answering "are these similar", which is a legitimate question — but not "is A useful to B".

SubQ is the only instrument in this set that can express direction, because the question is posed asymmetrically.

## Applying it: how relevant is each bundle to the devops-engineer page

One call per bundle, direction fixed as *bundle → page*.

| Bundle | Relevance | Confidence |
|---|---|---|
| `salesforceagain-v4-2026-11-14-0230` | Highly relevant | 0.672 |
| `..._devops-gearset-ui-deep-dive.md` | Relevant | 0.658 |
| `20261114-020300-salesforceagain-kilo` | Highly relevant | 0.614 |
| `2026-11-14T023241_salesforceagain-v2` | Relevant | 0.575 |
| `..._devops-governor-limits-deep-dive.md` | Relevant | 0.546 |
| `2026-11-14T0210Z-salesforceyetagain-v2-00_planning...` | Highly relevant | 0.546 |
| `..._devops-github-cicd-pipeline.md` | Relevant | 0.513 |
| `2026-11-14T0210Z-salesforceyetagain-v2` | Highly relevant | 0.451 |
| `2026-11-14T023507_salesforcemore-v2` | Highly relevant | 0.442 |
| `2026-11-14T023312_salesforcemore-v3` | Highly relevant | 0.462 |
| `20261114-020852-salesforcemore` | Highly relevant | 0.409 |
| `2026-11-14T021036_salesforceyetagain-v3.md` | Marginally relevant | 0.399 |

**Mean confidence 0.49.** Every value sits below the 0.6 gate.

## This is the weakest instrument in the set, and the numbers show why

| Limitation | Consequence |
|---|---|
| **No batching** | Relevance needs both documents in `state`, so each pair is its own call. 18 bundles = 18 calls. Every other shape batched N questions into one |
| **Low confidence** | Mean 0.49, max 0.67. The model hedges on a 4-point graded scale |
| **Coarse scale** | Four labels cannot separate bundles that differ by a little. Most landed on "Highly relevant" |
| **Context split** | Both documents compete for the ~34K budget, so each gets less than it would alone |

The low confidence is not a failure of this particular run. It is structural: asking "how relevant" invites a
hedge, where asking "which one" or "yes or no" forces a commitment. **Graded judgments are inherently less
decisive than choices.**

## What it is still good for

Two uses survive the weakness:

**1. Direction-sensitive questions.** If the question is genuinely asymmetric — "is this narrow note useful to a
reader of the broad survey?" — relevance is the only instrument that can answer it. Similarity cannot.

**2. A coarse first pass.** "Marginally relevant" at 0.399 for the narrow `salesforceyetagain-v3.md` is
informative even at low confidence: it is the one bundle that is not a good match for this page, and it is also
the one that `FILE_PAGE_CORRESPONDENCE.md` independently mapped with the weakest margin (0.169).

Two instruments with different failure modes agreeing on the same outlier is worth more than either alone.

## Recommendation

Do not use relevance for ranking. Use it for **pairwise triage** where direction matters, and treat anything
under 0.6 as unresolved. For "which bundle should I read", best-match is better: fewer calls, higher confidence,
and a decision at the end.

## Files

| File | Role |
|---|---|
| `relevance.json` | the per-bundle relevance scores |
| `BEST_MATCH.md` | the stronger selection instrument |
| `SEMANTIC_VS_LEXICAL.md` | the symmetric measures this is contrasted with |