# Concept coverage — does document A cover concept X?

**The fifth shape: per-document, per-concept coverage.** Binary, batchable, decisive.

This is what I originally did with regex presence, which was lexical and had measured failure modes. Redone
semantically: the model reads the document and judges whether the concept is actually covered.

---

## Method

One call per document. Twelve concept questions in a single batch, each with the concept stated in plain
language rather than as a keyword.

```python
questions = {f"q{i}": {"instructions": f"Does this document cover: {concept_description}?",
                       "type": "choice",
                       "criteria": {"options": ["Yes","No"], "option_0": "Yes", "option_1": "No"}}
             for i, concept_description in enumerate(concepts, 1)}
```

Each page scored separately, then unioned — because a concept covered anywhere in a page counts as covered.

## Result — live webpages vs merged pages

| Concept | Merged | Live | |
|---|---|---|---|
| heap_limits | Yes | Yes | |
| payload_ceilings | **Yes** | No | **gained** |
| coverage_rules | **Yes** | No | **gained** |
| validate_window | **Yes** | No | **gained** |
| deploy_queue | **Yes** | No | **gained** |
| test_levels | Yes | Yes | |
| destructive_changes | Yes | Yes | |
| sandbox_masking | Yes | Yes | |
| branch_model | Yes | Yes | |
| conflict_clinic | Yes | Yes | |
| audit_pack | No | Yes | *see caveat* |
| source_tracking | No | No | |

**Merged 10/12, live 7/12.**

### The four gained concepts corroborate every earlier independent finding

| Concept | Corroborated by |
|---|---|
| `payload_ceilings` | direct search: zero `39 MB` / `600 MB` on the live site, while it mentions deploy payloads 13 times |
| `coverage_rules` | the three-rule correction, verified against `apex_code_coverage_intro.htm` |
| `validate_window` | `sf project deploy validate` — "valid for 10 days" |
| `deploy_queue` | Metadata API: one deploy at a time, not FIFO |

Four separate instruments — direct string search, primary-source verification, CLI reference, and API behaviour
— agree with the coverage matrix. That is the strongest corroboration in the whole exercise, because the
failure modes are unrelated.

## The truncation caveat, which is the real lesson

`audit_pack` reads "live Yes, merged No," which would mean the merge deleted §11. It did not. The cause is the
context budget:

```
devops-engineer.md: 44,014 chars
  ## 9. Tests and validation      at char 28,588   WITHIN 33K
  ## 10. Releases                 at char 33,313   BEYOND 33K CUTOFF
  ## 11. Banking change control   at char 35,460   BEYOND 33K CUTOFF
  ## 12. Design patterns          at char 36,662   BEYOND 33K CUTOFF
```

**The merged devops-engineer page is larger than the context budget by itself.** Sections 10–12 were never
visible to the model, so `audit_pack` could not be found.

**Therefore the merged 10/12 is a lower bound, not a measurement.** The true figure is at least 11/12, and
probably 12/12 once §10–12 are readable.

## The method this implies

A document larger than ~34K characters cannot be assessed in one call. The correct procedure:

```
document > 34K chars
   -> chunk to <= 33K
   -> score each chunk against the concept set
   -> union the chunk results
```

That is what I did *across* pages (one call each, then union) but not *within* a page. Doing it within
`devops-engineer.md` would require 2 calls and would resolve `audit_pack` correctly.

**This is the same constraint surfacing at a third level:** first per question (my 1.1K excerpts), then per
document pair (33K split between two documents), now per document (44K page against a 33K budget). Each time
the fix is the same — measure the budget, then size the unit of work to it.

## What this shape is good for

- **Per-concept gap analysis across a set of documents** — exactly the "which concepts are missing" question,
  now answered semantically
- **Batchable**: 12 concepts in one call, ~8–9K input tokens
- **Decisive**: answers came back at 0.5–0.99 confidence, with the low ones correctly flagging thin coverage

## What it cannot do

It cannot tell you *how well* a concept is covered — only whether it is covered at all. A single sentence
counts the same as a chapter. For depth, use the retrieval-judge or the embedding depth scores; for truth, use
polarity against a primary source.

## Files

| File | Role |
|---|---|
| `coverage_final.json` | per-page results, unioned, with the live comparison |
| `coverage_live.json` | the live per-page baseline |
| `SUBQ_CONTEXT_BUDGET.md` | the limit that produced the truncation caveat |