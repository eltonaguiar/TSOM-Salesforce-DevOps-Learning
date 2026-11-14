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
---

# Addendum — webpage source, and the precision number

## Extending to webpages

A webpage source is not a directory of files. Added `web_source.py`: fetch each URL, keep only
`<main>`/`<article>` when present, strip `nav/header/footer/aside/script/style`, flatten to the same text
shape the repo adapter produces. All five Salesforce pages fetched cleanly (84,078 chars).

**The live site is stale relative to the merged pages** — verified, not assumed:

| Marker | Live site | Merged pages |
|---|---|---|
| Heap `6 MB / 12 MB` (wrong) | present | absent |
| Heap `10 MB / 25 MB` (correct) | absent | present |
| `39 MB` payload ceiling | absent | present |
| `RunRelevantTests` | absent | present |
| `Setup > Apex Jobs` (stale path) | present | absent |
| `Setup > Background Jobs` | absent | present |

So the merge has not been ported. Every comparison against the live site is a comparison against the
pre-merge pages.

## Run: live webpages vs repo bundles

All ten concepts went to the repo, most at high confidence:

| Concept | Repo wins | Prob |
|---|---|---|
| payload_ceilings | B | 0.928 |
| destructive_changes | B | 0.926 |
| governor_limit_numbers | B | 0.913 |
| release_branching | B | 0.909 |
| coverage_rules | B | 0.904 |
| quick_deploy_window | B | 0.889 |
| conflict_resolution | B | 0.874 |
| test_execution_trigger | B | 0.846 |
| sandbox_masking | B | 0.833 |
| audit_pack | B | 0.752 |

## Then I checked whether the repo's extra coverage was *correct*

This is the step that turns a ranking into something usable. I inspected the retrieved repo excerpt for the
four highest-ranked concepts and checked for known-bad values:

| Concept | Repo excerpt contained | Verdict |
|---|---|---|
| `payload_ceilings` (0.928) | **39 MB**, with the base64/50 MB/22% explanation | **Genuine gap — correct content** |
| `destructive_changes` (0.926) | `destructiveChanges.xml`, `--pre-` / `--post-` distinction | **Genuine gap — correct content** |
| `governor_limit_numbers` (0.913) | **No numbers at all** — error symptoms ("Too many SOQL queries: 101") | **False positive.** Broader in symptoms, thinner in quotable limits |
| `coverage_rules` (0.904) | **"1% minimum per trigger"** — the documented falsehood | **False positive.** The repo is wrong |

**Measured precision at the top of the ranking: 2 of 4 (50%).**

Both genuine gaps (`payload_ceilings`, `destructive_changes`) are already closed in the merged pages — they
are gaps against the *live site*, not against the merge. So the actionable output of this run is: **port the
merge**, which was already known.

## What this means for using the tool

- The ranking is a **candidate generator**, not a verdict. Half the top-ranked items did not survive a
  correctness check.
- **High confidence is not evidence of correctness.** `coverage_rules` scored 0.904 and the repo's content was
  wrong. Confidence measures how decisively the model preferred one excerpt, not whether either is true.
- The verification step is cheap: grep the retrieved excerpt for the specific value you expect. It took one
  command to reject two of four.
- **Always name the source precisely.** "Repo vs webpages" is only meaningful once you say which revision of
  each. Here the webpages were pre-merge, which is why the repo won everything.

---

# Addendum 2 — conflict detection, and a bug in my own tooling

## The gap this fills

Coverage asks "who says more". Neither answers the question that produces wrong
documentation: **where do the two sources contradict each other?**

Six detection strategies were built. Five failed in instructive ways.

| # | Strategy | Result | Failure mode |
|---|---|---|---|
| 1 | whole documents, TIE allowed | 10/10 TIE | cannot compare what it cannot see |
| 2 | retrieval + forced binary | 10/10 B at ~0.50 | coin flip; bias replaced signal |
| 3 | retrieval fixed + judge | 10/10 B at 0.75–0.93 | worked for breadth |
| 4 | model-judged AGREE/CONFLICT/DIFFERENT | 10/10 DIFFERENT | narrow excerpts hide the conflict |
| 5 | value-set substring scan | false AGREE | assertion vs refutation |
| 6 | **polarity per claim** | **works** | see below |

**#5 is the important one.** Comparing "does this string appear" found that the merged page and the repo both
contain `6 MB` and `12 MB` — and reported AGREE. But the page uses them for *callout request size* (correct)
and the repo uses them for *heap size* (wrong). Substring presence cannot tell an assertion from its
refutation, and the tool produced a false "no conflict here" on the single most important discrepancy in the
whole corpus.

**#6 fixes it** by asking for the source's *polarity* on a specific claim — ASSERTS / DENIES / NOT_ADDRESSED —
then comparing polarities. Reading the claim, not the token.

## A bug in my own tooling

The first polarity run returned `NOT_ADDRESSED` for all 8 claims. That was not a finding.

SubQ returns `choice: "option_1"` and `probabilities: {"option_0": ..., "option_1": ...}` — **not** the option
text. `pick()` returned `"option_1"`, and the comparison `ch.startswith("ASSERTS")` was false for every
option index, so every verdict fell through to the `NOT_ADDRESSED` branch.

Resolution required mapping the index back to the option list:

```python
key = max(pr.items(), key=lambda x: x[1])[0]      # "option_1"
if key.startswith("option_"):
    return options[int(key.split("_")[1])], pr[key]   # "DENIES the claim"
```

**This also affected the coverage runs (#2, #3).** They happened to produce the correct outcome because B was
always `option_1` and the fallback branch also mapped to B — the bug was masked by the answer. It was luck,
not soundness. Any run where A won would have been silently reported as B.

Lesson: when a model returns an indexed choice, resolve the index against the option list you supplied. Never
compare the returned key against a label prefix.

## Corrected results

### Contradictions (merged pages vs repo bundles)

| Claim | Merged | Repo | Verdict |
|---|---|---|---|
| Heap size is 6 MB sync / 12 MB async | **DENIES** | **ASSERTS** | **CONTRADICTION** |
| There is a 1% minimum coverage per class/trigger | **DENIES** | **ASSERTS** | **CONTRADICTION** |
| Max compressed payload is 400 MB | DENIES | not addressed | no signal |
| Named system properties exist (`org.wideSharing.default`) | DENIES | not addressed | no signal |
| Apex Jobs / Scheduled Jobs are separate Setup pages | DENIES | not addressed | no signal |

The two contradictions are **exactly the two false claims the merge corrected**, verified against primary
sources (`apex-gov-limits.html`, `apex_code_coverage_intro.htm`). The detector reproduced known ground truth
without being told the answer — that is the validation that matters.

The three `NO_SIGNAL` rows are retrieval misses, not absences: the repo does contain `400 MB`, and does
address deactivation, but the topical window did not surface the asserting passage. Claim-targeted retrieval
with a wider window is the next fix.

### Coverage (live site vs repo) — unchanged and still valid

Repo broader on 10/10, 0.75–0.93. Confirmed the outcome is unchanged after the fix, because B was genuinely
the higher-probability option in all ten.

## What is now reliable, and what is not

| Capability | State |
|---|---|
| Breadth ranking ("who covers more") | Works. Measures volume, **not** correctness. Measured precision 2/4 at the top |
| Contradiction detection | Works for claims with a crisp testable form. Reproduced 2/2 known ground-truth conflicts |
| Automatic adjudication | **Does not exist.** A conflict is a pointer to a primary source, never a verdict |
| Narrow-topic retrieval | Still the weak link. Every `NO_SIGNAL` above is a retrieval miss |

## Rules for use

1. **Rank with coverage, decide with polarity, adjudicate with primary sources.** Three separate steps; do not
   collapse them.
2. **Name the source revision.** "Live site vs repo" was uninterpretable until the site was established as
   pre-merge.
3. **Resolve indexed choices.** Always map `option_N` back to the supplied label.
4. **Treat a low margin as no signal.** Under 0.6 is a tie, not a weak preference.
5. **A conflict is a search task, not an answer.** Expect roughly half of top-ranked items to fail a
   correctness check.
