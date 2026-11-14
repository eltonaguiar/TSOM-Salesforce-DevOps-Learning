# Duplicate and overlapping documents

**Question:** which documents are duplicates, or cover overlapping material.

Two different questions that need two different instruments, and conflating them was the first mistake.

| Tier | Instrument | What it finds |
|---|---|---|
| Verbatim | MD5, then 5-word shingle Jaccard | byte-identical and lightly-edited copies |
| Topical | concept-set Jaccard (75-concept taxonomy) | same material, different words |

---

## Tier 1 — verbatim duplication

| Measure | Count |
|---|---|
| Exact duplicate groups | 3 |
| Near-duplicate pairs (shingle Jaccard ≥ 0.60) | 4 |
| Near-duplicate clusters | 4 |
| Overlap pairs (0.25–0.60) | **0** |

All four near-duplicate clusters are the same pattern — the `salesforceyetagain-v2` folder and its flat twins:

| Group | Documents |
|---|---|
| `e313a409` | `2026-11-14T0210Z-salesforceyetagain-v2-01_certifications-curriculum.md` ≡ `.../2026-11-14T0210Z-salesforceyetagain-v2/01_certifications-curriculum.md` |
| `654cc741` | `...-02_crash-course.md` ≡ `.../02_crash-course.md` |
| `e520cc88` | `...-README.md` ≡ `.../README.md` |
| near | `...-00_planning-salesforce-principles.md` ≡ `.../00_planning-salesforce-principles.md` |

**Four documents, two copies each, one pattern.** Someone wrote the research into a folder and then
concatenated a copy at the flat `forreviews/` root, and never reconciled them. Fixing one leaves the other
live — which is the specific hazard the dedupe pass exists to catch.

## Tier 2 — topical overlap

Shingle Jaccard found **0** overlap pairs. That is not because the corpus is un-duplicated; it is because
shingling measures verbatim text, and two documents written independently about certifications share almost
no 5-word sequences even when they cover identical ground.

Switching to concept-set Jaccard:

| Measure | Count |
|---|---|
| Pairs with concept overlap ≥ 0.55 | **203** |
| Pairs at 1.000 (identical concept sets) | 4 |
| Pairs at 0.80–0.94 | 11 |

### Entry-level redundancy

Mean concept overlap of each entry against all the others:

| Entry | Files | Concepts | Mean overlap |
|---|---|---|---|
| `2026-11-14T0210Z-salesforceyetagain-v2` | 4 | 63 | 0.583 |
| `2026-11-14T023507_salesforcemore-v2.md` | 1 | 59 | 0.579 |
| `2026-11-14T023507_salesforcemore-v2` | 24 | 59 | 0.579 |
| `20261114-020852-salesforcemore` | 12 | 66 | 0.564 |
| `2026-11-14T023241_salesforceagain-v2.md` | 1 | 64 | 0.561 |
| `20261114-023241_salesforceagain-v2` | 10 | 64 | 0.561 |
| `20261114-020300-salesforceagain-kilo` | 13 | 64 | 0.553 |
| `salesforceagain-v4-2026-11-14-0230` | 3 | 45 | 0.531 |
| `2026-11-14T023312_salesforcemore-v3` | 8 | 41 | 0.496 |
| `..._devops-metadata-dependencies-deep-dive.md` | 1 | 34 | 0.420 |
| `..._devops-governor-limits-deep-dive.md` | 1 | 30 | 0.413 |
| `..._devops-gearset-ui-deep-dive.md` | 1 | 27 | 0.385 |
| `...-01_certifications-curriculum.md` | 1 | 25 | 0.377 |
| `...-00_planning-salesforce-principles.md` | 1 | 22 | 0.362 |
| `..._devops-github-cicd-pipeline.md` | 1 | 12 | 0.223 |
| `2026-11-14T021036_salesforceyetagain-v3.md` | 1 | 8 | 0.169 |
| `...-README.md` | 1 | 1 | 0.013 |

**The gradient is the finding.** The eight broad entries each cover 59–66 concepts and overlap each other at
0.53–0.58 — they are the same survey performed eight times. The narrow deep-dives cover 8–34 concepts and
overlap at 0.17–0.42 — they are the differentiated material.

## What is actually redundant, and what is not

| Disposition | Documents | Reason |
|---|---|---|
| **Delete outright** | the 4 flat twins of `salesforceyetagain-v2` | byte-identical or near-identical to their folder copies |
| **Keep one of** | the 8 broad survey entries (59–66 concepts, mutual overlap 0.53–0.58) | any one or two covers the same ground. `salesforceagain-kilo` and `salesforcemore-v2` are the two with correct numbers and correction logs |
| **Keep all** | the narrow deep-dives (8–34 concepts, overlap 0.17–0.42) | low overlap — this is where the unique material is |

So of 85 files: **4 are pure duplicates, ~6 of the 8 broad entries are redundant, and the ~9 narrow
deep-dives are all worth keeping.** That is the opposite of the usual assumption that "the big files are the
valuable ones" — here the big files are the duplicated ones.

## A caution on the concept-set instrument

The concept taxonomy has 75 entries, so two documents that each cover 60 of them will score ≥0.55 almost by
arithmetic, regardless of whether their *treatment* overlaps. The high mean overlaps at the top of the table
are partly a ceiling effect.

That does not invalidate the gradient — the narrow deep-dives really are different, and the flat twins really
are identical — but the absolute numbers should be read as "same coverage profile", not "same content".

## Files

| File | Role |
|---|---|
| `duplicates.py` | exact hash + shingle Jaccard + union-find clustering |
| `duplicates_result.json` | tier-1 results |
| `concepts.py` | the concept-set instrument used for tier 2 |