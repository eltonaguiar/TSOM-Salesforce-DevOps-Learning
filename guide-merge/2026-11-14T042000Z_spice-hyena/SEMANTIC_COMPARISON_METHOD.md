# Semantic coverage comparison — method, results, and what it cannot do

**Goal:** compare two independent documentation sources (a whole repo of mixed files each) and produce a
ranked list of concepts where one is thinner than the other.
**Built:** 2026-11-14 · `subq/semantic.py`, `subq/retrieval_judge.py`, `subq/repo_compare.py`
**Model:** SubQ `subq-snap-1.2` (decision model, not chat)

---

## The pipeline

```
repo (mixed .md/.html/.xml/.json/code)
   -> flatten + strip markup / extract comments
   -> split into passages at file headers and paragraph breaks
   -> reject junk (TOCs, nav, agent meta-headers, bullet skeletons)
   -> retrieve top-k passages per concept by term density, with a penalty for
      link-heavy and number-free passages
   -> SubQ forced binary: which excerpt gives the reader more?
   -> aggregate wins -> ranked gap list
```

Four files, ~250 lines, no external deps beyond `urllib`.

---

## Three iterations, and why the first two were worthless

I am recording the failures because they are the useful part.

### v1 — whole documents, no retrieval → 10/10 TIE

Fed each source in full (108K and 1.66M chars, truncated) and asked which covered each concept better.
**Every concept returned TIE.** Cause: the model cannot compare what it cannot see. With a TIE option
available, uncertainty collapses into it. A result of 10/10 TIE is not a finding, it is a broken instrument.

### v2 — retrieval, but no TIE option → 10/10 B at ~0.50

Forced a binary. Now every concept went to the corpus, but every probability sat between 0.46 and 0.59.
**A coin flip.** Removing the escape hatch replaced "all TIE" with "all B, barely" — the bias moved, the
signal did not.

### v3 — retrieval fixed → real discrimination, and a real limitation

The retrieval was the actual bug. Two defects, both worth naming:

1. **The passage splitter never populated its buffer.** `passages()` reset `buf = []` on every match and
   never appended the text between matches, so it always returned **zero** passages, and every call fell
   through to an unfiltered fallback. That is why v2 was still surfacing tables of contents.
2. **No junk rejection.** Keyword density scores a table of contents highly — it is dense with the terms and
   contains no prose. Fixed with a junk filter (anchor-link count, worktree/timestamp meta-headers, bullet
   skeletons with no sentences) plus a link-density and number-free penalty.

After the fix: 387 passages from 5 files, 5,120 from 85. Excerpts became real content — the page's actual
limits table against the corpus's actual limits taxonomy.

**v3 result — corpus wins 10/10, most at 0.82–0.93:**

| Concept | Winner | Prob |
|---|---|---|
| destructive_changes | corpus | 0.934 |
| test_execution_trigger | corpus | 0.906 |
| governor_limit_numbers | corpus | 0.858 |
| payload_ceilings | corpus | 0.849 |
| conflict_resolution | corpus | 0.846 |
| coverage_rules | corpus | 0.823 |
| sandbox_masking | corpus | 0.653 |
| release_branching | corpus | 0.651 |
| quick_deploy_window | corpus | 0.427 |
| audit_pack | corpus | 0.371 |

---

## The limitation that matters: it measures breadth, not truth

I know the corpus contains documented falsehoods — it is where the wrong heap figure (6/12 MB) and the
non-existent "1% coverage rule" came from. I checked whether the judge was rewarding them:

| Concept | What the corpus excerpt actually contained | Verdict |
|---|---|---|
| `governor_limit_numbers` | **No numbers at all** — a list of error symptoms ("Too many SOQL queries: 101") | Broader in context, thinner in quotable limits |
| `coverage_rules` | Explicitly "Trigger coverage: **1% minimum per trigger**" — the false claim | **The judge preferred a passage containing a known falsehood (0.823)** |

And on the page side, the "1%" string it matched was inside the page's own **negation** — "There is **no**
'1%' per class rule." The retrieval could not tell an assertion from its refutation.

So the instrument measures **how much a source says about a concept**, not whether what it says is correct.
That is a real and useful thing to measure — but only if you never let it decide facts.

**The correct workflow, and the one used for the actual page merge:**

1. Semantic comparison → *where is a source thin?* (breadth)
2. Primary source documents → *what is true?* (correctness)
3. Merge only what survives step 2

Step 1 localises the work. It must never supply the content. In the earlier merge, this is exactly what
happened: the tool pointed at "which payloads force a test run", and the primary source then revealed that the
candidate answer (the 24-type list) had been stale since API 34.0.

---

## When this is worth running

**Good use:** "source A covers 8 concepts, source B covers 12 — which 4 am I missing?" Breadth discovery
across large mixed-format repos, where reading everything is infeasible.

**Bad use:** "which source is right?" "is this claim true?" "what should the page say?" The tool has no
ground truth and will happily prefer a confident, wrong, richly-written passage over a terse correct one.

**Practical guard:** require a numeric or quotable anchor before merging anything the tool surfaces, and treat
a low margin (<0.6) as "no signal" rather than a weak preference. In v3, `quick_deploy_window` (0.427) and
`audit_pack` (0.371) are effectively ties; only the 0.82+ rows are worth acting on.

---

## Reproduction

```bash
export SUBQ_TOKEN_API_KEY=...
cd /tmp/subq
python3 repo_compare.py --a "pages:/path/to/pages" --b "corpus:/path/to/bundles" \
        --concepts concepts2.json --out result.json
```

`concepts2.json` maps each concept to its retrieval terms and a statement of what a reader needs. That
"need" line is what makes the question answerable — without it the model has no criterion.

## Files

| File | Role |
|---|---|
| `semantic.py` | one decision call: state + options → choice + probabilities |
| `retrieval_judge.py` | flatten-aware passage split, junk filter, density retrieval, forced-binary compare |
| `repo_compare.py` | repo flattening (md/html/xml/json/code), shrink to budget, aggregate wins |