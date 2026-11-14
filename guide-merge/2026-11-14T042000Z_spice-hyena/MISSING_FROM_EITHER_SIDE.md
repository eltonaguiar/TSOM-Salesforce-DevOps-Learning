# Concepts missing from either side

**Question:** which Salesforce concepts are missing from one or both sources.

This is the question the previous result could not answer, and the reason is worth stating plainly.

---

## First: the previous result was circular

`CONCEPT_INTERSECTION.md` reported **48 of 49 concepts in both sources**. That number was guaranteed by
construction: I derived the 49-concept taxonomy *from the five pages themselves*. A taxonomy built out of
source A cannot find concepts missing from A — the pages trivially cover a list made from their own contents.

So that run answered "do the pages cover what the pages cover," which is not a question. It is recorded here
because the mistake is instructive: **a gap analysis needs a taxonomy from outside both sources.**

## Second: an external taxonomy

Rebuilt from the wider Salesforce platform and the DevOps role's requirements — not from either source:
objects, security, automation, integration, deployment, monitoring, and adjacent clouds. 75 concepts.

### Result at face value

| Set | Count |
|---|---|
| In both | 65 |
| Only in webpages | 0 |
| Only in repo | 8 |
| **Missing from both** | **2** |

### Then validated each of the 8 by hand

Face-value set differences are not trustworthy — two were taxonomy errors:

| Concept | Raw result | After direct check | Verdict |
|---|---|---|---|
| `lookup_relationship` | only repo | site has 14 "lookup" / "master-detail" hits | **taxonomy false negative** — semantically present |
| `field_audit_trail` | only repo | site has 1 hit ("field history") | **taxonomy false negative** — present |
| `sosl` | only repo | site has 7 "search" hits but never SOSL | real gap, narrow — search is covered, SOSL is not |
| `mfa` | only repo | 0 hits, no 2FA/authenticator either | **genuinely missing** |
| `source_tracking` | only repo | 0 hits | **genuinely missing** |
| `big_objects` | only repo | 0 hits | **genuinely missing** |
| `mulesoft` | only repo | 0 hits | **genuinely missing** |
| `einstein` | only repo | 0 hits | **genuinely missing** |

## The answer

**Missing from the webpages (5, plus one narrow):**

`mfa` · `source_tracking` · `big_objects` · `mulesoft` · `einstein`
— and `sosl` in the narrow sense that search is covered but SOSL specifically is not.

**Missing from the repo:** none. The repo is broader than the pages on every concept it addresses.

**Missing from both sides (2):**

`heroku` · `tableau_crm`

Neither source covers Heroku or Tableau CRM. For a Salesforce DevOps curriculum aimed at a commercial-banking
release-engineering role, that is defensible rather than a defect — neither is core to metadata release
engineering. But it is a real boundary of the curriculum and worth stating rather than leaving implicit.

## The regex bugs, again

Three separate pattern errors surfaced in this exercise alone, all of the same class:

| Pattern | Bug | Effect |
|---|---|---|
| `einstein\|ai` | bare `ai` matches *email, domain, available, maintain* | **142 false hits** — the single worst defect found |
| `10,000\s*(rows\|DML)` | misses "10,000 **records per** DML" | false negative on `dml_limit` (previous file) |
| `field audit trail` | misses "field history", the current UI name | false negative on `field_audit_trail` |

The `ai` case is the one to remember: a two-letter alternative in a regex alternation is effectively
unbounded. `\bAI\b` or nothing.

## Why the threshold approach failed

I tried requiring ≥2 and ≥3 occurrences to filter coincidental matches. It made things **worse**, not better:

| Min occurrences | both | only site | only repo | missing both |
|---|---|---|---|---|
| 1 | 65 | 0 | 8 | 2 |
| 2 | 62 | 0 | 11 | 2 |
| 3 | 57 | 0 | 12 | 6 |

Raising the threshold moved concepts *out* of the site's coverage — `communities` and `event_monitoring`
became "only in repo" even though I had directly observed 2 site hits for each. Longer documents accumulate
mentions faster, so a raw-count threshold systematically penalises the smaller source.

**Presence must be measured at threshold 1, with the term itself validated.** Density normalisation
(hits per 1,000 chars) is the correct fix if a graded comparison is ever needed; raw counts are not comparable
across a 20× length difference (84,078 chars vs 1,661,273).

## Files

| File | Role |
|---|---|
| `concepts.py` | presence detection + set comparison |
| `external_taxonomy.json` | 75 externally-derived concepts with validated patterns |
| `external_result.json` | the four sets, face value |

## Caveat

Presence detection is deliberately shallow, and this run showed both of its failure modes: it under-reports
when a pattern misses a synonym (`lookup relationship`, `field history`) and over-reports when a pattern is too
loose (`ai`). Neither is fixable by tuning alone — the terms have to be checked against real text. Budget for
that step; it caught 3 defects here.