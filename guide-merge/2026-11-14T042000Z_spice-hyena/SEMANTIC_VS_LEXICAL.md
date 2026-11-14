# Semantic vs lexical comparison — and what changes

**The distinction that matters: a semantic comparison asks what a passage *means*, not which words it
contains.** Most of the earlier pipeline was lexical. This file records what happens when it is done properly.

Model: `all-MiniLM-L6-v2` (384-dim), mean-pooled chunk vectors, cosine in a shared meaning space.
5,239 repo chunks + 60 site chunks embedded in 6 seconds on CPU.

---

## Why lexical failed, concretely

Four failures, each a different way that token overlap misleads:

| Failure | What happened | Cause |
|---|---|---|
| TOC matched a concept | a table of contents scored highest for "governor" | the word appeared, the meaning did not |
| Assertion ≡ refutation | "there is **no** 1% rule" and "the rule is 1%" scored identically | negation is invisible to bag-of-words |
| Paraphrase scored zero | two documents on certifications shared no 5-word sequence | independent writing shares no verbatim n-grams |
| Wrong passage retrieved | a trigger code sample won a question about coverage rules | topical words present, subject absent |

**Sanity check on the fix:**

```
"the heap size limit is ten megabytes"          vs  "memory available to a transaction is capped at 10 MB"
  cosine 0.586   <- paraphrase, almost no shared vocabulary

vs  "the weather is nice today"
  cosine 0.017   <- unrelated
```

The paraphrase pair shares almost no words and scores 0.586. That separation is what lexical methods cannot
produce.

---

## Result 1 — depth and completeness (semantic)

For each concept, mean of the top-5 chunk similarities per source. No keywords, no model opinion — geometric.

| Concept | Site top-5 | Repo top-5 | Winner |
|---|---|---|---|
| heap | 0.354 | **0.659** | repo |
| coverage | 0.389 | **0.635** | repo |
| payload | 0.294 | **0.694** | repo |
| test_trigger | 0.418 | **0.650** | repo |
| quick_deploy | 0.470 | **0.764** | repo |
| destructive | 0.438 | **0.602** | repo |
| sandbox | 0.397 | **0.682** | repo |
| branching | 0.422 | **0.683** | repo |
| audit | 0.393 | **0.594** | repo |
| conflict | 0.467 | **0.684** | repo |

**Repo wins 10/10**, with a mean margin of ~0.24.

This *agrees* with the earlier retrieval-judge result (repo 10/10) — but the evidence is far stronger. The
judge produced a model opinion at 0.75–0.93 confidence; this produces a reproducible geometric measurement.
Two independent instruments agreeing is the corroboration that was missing.

`payload` shows the largest gap (0.294 vs 0.694) and is the one concept the site has **zero** coverage of —
matching the earlier direct search that found no `39 MB` or `600 MB` anywhere on the site.

**Length bias, and how I handled it.** `max` similarity rewards the source with more chunks (5,239 vs 60), so
I used mean-of-top-5 and also reported the fraction of chunks above 0.35. The fraction is noisy for a small
source — the site shows *higher* fractions on `test_trigger` (16.7% vs 10.8%) because 10 of 60 chunks is a
large share — so mean-of-top-5 is the number to trust.

## Result 2 — duplicates, and a correction

**Semantic near-duplicate detection contradicts the lexical result.**

| Method | Pairs flagged |
|---|---|
| Concept-set Jaccard ≥ 0.55 (lexical) | **203** |
| Shingle Jaccard ≥ 0.25 (verbatim) | 4 |
| **Document embedding cosine ≥ 0.60** | **1** |
| Document embedding cosine ≥ 0.70 | **0** |

Distribution over all 3,570 pairs: **max 0.675, mean 0.225, median 0.219**.

The single pair above 0.60 is `salesforceyetagain-v2-README.md` vs its flat twin — a genuine duplicate, and
one of the four the exact-hash pass already found.

### This corrects `DUPLICATES_AND_OVERLAP.md`

I wrote that the eight broad entries (59–66 concepts, mutual overlap 0.53–0.58) were "the same survey
performed eight times" and that ~6 of 8 were redundant. **The semantic evidence does not support that.**

They converge on *topic* and diverge in *content*. They share a concept profile; they do not share meaning.
Different agents made different choices about what to emphasise, which errors to reproduce, and which
examples to use. That is why they disagree on the heap figure and the 1% rule — if they were copies they
would agree, wrongly but consistently.

**Corrected conclusion:** the corpus is *topically* redundant and *semantically* distinct. The redundancy is
in what it covers, not in what it says. Consolidation should merge by **topic** (one authoritative treatment
per concept) while preserving the **disagreements** as evidence of where the underlying sources conflict —
which is exactly what the polarity pass is for.

## Result 3 — retrieval

Semantic retrieval fixed the failure that had been silently corrupting every model-judged run.

The query *"What is the maximum heap size for synchronous and asynchronous Apex?"* under keyword scoring
returned the document header. Under embedding retrieval it returns the governor-limits section (sim 0.518) in
3.4 seconds.

Three keyword-retrieval defects were found and fixed during this work — tables rejected as junk, no paragraph
breaks in markup-stripped text, and a passage buffer that never populated. Semantic retrieval makes that whole
bug class disappear, because it does not depend on the passage boundaries being well-formed.

## What is still lexical, and why that is correct

**Concept presence** stayed regex-based, deliberately. "Does this document mention sandboxing" is a question
about vocabulary, and answering it semantically would be over-engineering. The failure mode of lexical
presence is known and was measured: it under-reports synonyms (`lookup relationship` → `field history`) and
over-reports short patterns (`ai` matching *email*). Both were caught by hand.

**Claims** use the model (polarity), because "asserts vs denies" is a semantic distinction that no amount of
token counting can recover.

So the pipeline is now: **semantic** for retrieval, depth and near-duplicates; **lexical** for presence, where
it is the right tool; **model** for polarity, where only meaning will do.

## Files

| File | Role |
|---|---|
| `semantic_embed.py` | chunking, embedding, semantic retrieval, doc vectors |
| `semantic_depth.json` | per-concept depth scores |
| `semantic_dups.json` | semantic near-duplicate pairs |

## Caveat

A mean-pooled document vector is a coarse summary — it captures topic and register, not argument. Two
documents at 0.65 are not "65% the same document"; they are close in a topic space that is much flatter than
meaning really is. Treat these numbers as *ordering* evidence, not as quantities.