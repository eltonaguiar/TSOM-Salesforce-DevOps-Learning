# Which source is more complete, and which is more accurate

**The final question, and the two halves pull in opposite directions.**

Completeness and accuracy were measured separately, because a source can be broad and wrong at the same time —
which is exactly what happens here.

---

## Method

**Completeness** — depth of treatment per topic, via retrieval-then-judge (which excerpt gives a reader more
of what they need), plus concept presence against a 75-concept external taxonomy.

**Accuracy** — a **known-answer test**. Eight claims, each with a ground truth verified against a primary
Salesforce document earlier in this session. For each source, ask its *polarity* on each claim: does it
ASSERT, DENY, or not address it?

All eight claims are **FALSE**. A source that DENIES them is correct; one that ASSERTS them is wrong.

| # | Claim (all false) | Ground truth | Primary source |
|---|---|---|---|
| 1 | Heap is 6 MB sync / 12 MB async | heap is **10 MB / 25 MB**; 6/12 is callout request size | `apex-gov-limits.html` |
| 2 | 1% coverage per class/trigger | no per-item floor; 75% org-wide, or per-item 75% under `RunSpecifiedTests` | `apex_code_coverage_intro.htm` |
| 3 | Max compressed payload is 400 MB | **≈39 MB** compressed / ≈600 MB uncompressed | `meta-deploy.html` |
| 4 | `NoTestRun` is valid for prod with Apex | development environments only | CLI reference |
| 5 | A deactivated user cannot be reactivated | they can | — |
| 6 | Named system properties exist (`org.wideSharing.default`) | no general-purpose property store | — |
| 7 | Apex Jobs / Scheduled Jobs are separate Setup pages | consolidated into `Setup > Background Jobs` | — |
| 8 | An official "Salesforce DevOps Engineer" cert exists | no such credential | guide's own Certifications section |

## Results

| Source | Correctly denies | **Falsely asserts** | Silent |
|---|---|---|---|
| **live webpages** | 2 / 8 | **4 / 8** | 2 |
| **merged pages** | 5 / 8 | **0 / 8** | 3 |
| **repo bundles** | 0 / 8 | **3 / 8** | 5 |

### Live webpages

Falsely asserts: heap 6/12 MB · deactivated users cannot be reactivated · named system properties exist ·
Apex Jobs/Scheduled Jobs as separate pages.

These are all pre-merge defects — the merged pages fix every one of them.

### Merged pages

**Zero false assertions.** The five it denies are the five it was built to deny. The three silent ones
(`no_test_run_prod`, `deactivated_cannot_reactivate`, `devops_cert_none`) are cases where the retrieved
passage did not take a position — for two of them the merged page does address the topic elsewhere, so
"silent" is partly a retrieval artefact and should not be read as "absent".

### Repo bundles

Falsely asserts: heap 6/12 MB · the 1% rule · Apex Jobs as a live Setup path.

Three errors, all of which propagated from the same upstream source — the crash-course page. This is the
propagation pattern documented in `DEDUPE_MANIFEST.md`: five bundles reproduced the heap figure because they
copied it from the page that was supposed to be authoritative.

---

## The answer

**Completeness: the repository.** Broader on 10/10 depth topics (0.75–0.93), covering more of the external
concept taxonomy, with deeper treatment of limits, deploy mechanics, and release engineering.

**Accuracy: the merged pages.** Zero false assertions on the known-answer set, against 4 for the live site and
3 for the repo.

**They are not the same source, and that is the point.**

| | Complete? | Accurate? |
|---|---|---|
| Live webpages | no | no (4 false) |
| Repo bundles | **yes** | **no** (3 false) |
| Merged pages | yes | **yes** (0 false) |

The most complete source is among the least accurate. The repo has 1.66M characters against the site's 84K,
and it uses that volume to state more things — including three that are wrong.

**This is why the workflow is three steps and not one.** Coverage ranking found where to look. Polarity
established who was right. Primary sources decided. A single "which is better" question asked of any one
instrument would have produced a confident wrong answer:

- asked for coverage → the repo wins, and you import its errors
- asked for accuracy alone → the site's silence on hard topics reads as caution, and you conclude the site is fine

Neither is true. The repo is broader and wronger; the site is narrower and was wronger still, until the merge.

## Caveats that matter

**"Falsely asserts 0/8" is not "verified correct on everything."** It means the detector found no false
assertion among eight specific claims on the passages it retrieved. Eight is a sample, not a proof, and a
source could be wrong on claims outside the set.

**Silence is not correctness.** A source that never addresses a claim scores the same as one that denies it
correctly. That is why the scoring reports three buckets rather than a single accuracy percentage.

**Retrieval still limits everything.** Every `silent` verdict is partly a retrieval outcome — the detector can
only judge what it was shown. Three separate retrieval defects surfaced while building this (tables rejected
as junk, no paragraph breaks in markup-stripped text, and a buffer that never populated). Expect more.

## Files

| File | Role |
|---|---|
| `polarity.py` | ASSERTS / DENIES / NOT_ADDRESSED per claim |
| `ground_truth.json` | the eight claims with verified answers and sources |
| `accuracy.json` | per-source scores and per-claim detail |