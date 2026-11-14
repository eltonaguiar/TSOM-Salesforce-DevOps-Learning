# SubQ decision trail — what to prioritise in the Salesforce guides

**Purpose:** use SubQ (a decision model, not a chat model) to rank which Salesforce training section has the
most missing content, then narrow it with follow-up questions.
**Model:** `subq-snap-1.2` · `POST https://api.subq.ai/v1/systemone`
**Run:** 2026-11-14 04:30 UTC
**Client:** `/tmp/subq/client.py` (direct, no proxy)
**Total cost:** 5 calls, ~3,400 input tokens. Not a verified billing debit.

---

## Why SubQ and not a chat model

SubQ is a **decision** model. You give it a state (context) and a choice question with explicit options; it
returns a choice, per-option probabilities, and a confidence. That is the right tool for ranking, and it is
strictly better than asking a chat model "which is worst?" — because the chat model will produce fluent prose
regardless of whether the answer is grounded.

The trade-off is that SubQ cannot **verify** anything. It ranks the options you give it. Every factual claim
still has to be checked against a primary source, which is what caught the important error below.

---

## The five questions

### Q1 — which page has the most genuinely missing content

State: measured coverage of 43 release-engineering topics across the 5 pages, plus the caveat that the pages
have different audiences and a beginner page is not supposed to carry DevOps depth.

| Option | Probability |
|---|---|
| **devops-engineer** | **0.906** |
| options (meta) | 0.072 |
| crash-course | 0.008 |
| labs-design | 0.006 |
| navigation-breadcrumbs | 0.005 |
| user-management-data | 0.003 |

**Choice: devops-engineer · confidence 0.887.** Decisive.

This agrees with the raw measurement, but for the *right* reason: the beginner pages score badly on DevOps
topics by design. `devops-engineer` is the one page where a gap is actually a defect.

### Q2 — which section of devops-engineer is most incomplete

| Option | Probability |
|---|---|
| **2. Metadata that breaks releases** | **0.449** |
| 9. Tests and validation | 0.293 |
| options (meta) | 0.215 |
| 3. Environments and sandboxes | 0.024 |
| 11. Banking change control | 0.008 |
| 5. CI/CD | 0.006 |
| 7. Conflict clinic | 0.003 |
| 12. Design patterns | 0.002 |

**Choice: §2 · confidence 0.370.** Low confidence — genuinely split between §2 and §9. That low number is
information: it said "narrow this", not "I'm sure".

### Q3 — head-to-head, §2 vs §9

Framed as "which has more content genuinely missing for someone who must *run or review* a production release",
with the full current contents of both sections in the state.

| Option | Probability |
|---|---|
| **2. Metadata that breaks releases** | **0.855** |
| options (meta) | 0.080 |
| 9. Tests and validation | 0.060 |

**Choice: §2 · confidence 0.782.** Decisive once forced.

### Q4 — what specifically is missing from §2

Five candidate additions, each described with what it would add and what it would cost.

| Option | Probability |
|---|---|
| **C) metadata types that force a full local test run** | **0.390** |
| A) governor limit numbers table | 0.315 |
| options (meta) | 0.164 |
| B) org-wide / per-24-hour limits | 0.118 |
| E) source tracking | 0.010 |
| D) Apex code size / storage | 0.003 |

**Choice: C · confidence 0.268.** Low — split between C and A.

### Q5 — head-to-head, A vs C

| Option | Probability |
|---|---|
| **C) metadata types that force a full local test run** | **0.804** |
| options (meta) | 0.135 |
| A) governor limit numbers table | 0.060 |

**Choice: C · confidence 0.706.** Decisive.

---

## The decision

```
Q1  which page           -> devops-engineer            (0.906, conf 0.887)
Q2  which section        -> §2 vs §9 split             (0.449, conf 0.370)
Q3  head-to-head         -> §2 Metadata that breaks    (0.855, conf 0.782)
Q4  what content         -> C vs A split               (0.390, conf 0.268)
Q5  head-to-head         -> C metadata types / tests   (0.804, conf 0.706)
```

**Verdict: §2 "Metadata that breaks releases" is the weakest section, and the most valuable addition is the
rule for which payloads force a test run.**

The pattern in the confidence scores is worth noting: the model was confident when choosing between pages
and between content items, and unsure when choosing between sections. Two forced head-to-heads resolved it.
That is a reasonable way to use a decision model — let it rank, then narrow with binary questions rather
than trusting a single low-confidence multi-way choice.

---

## What verification changed

SubQ selected "the metadata types that force a full local test run". The candidate content for that was the
**24-type list** that appears in the research bundles (`ApexClass`, `CustomField`, `CustomObject`, `Profile`,
`Flow`, `ValidationRule`, `Workflow`, and 17 others).

**That list is correct only for Metadata API 33.0 and earlier.** Verified against the primary source, which
states both things:

> "When deploying to production, all tests, except those that originate from managed packages, are executed if
> your deployment package contains **Apex classes or triggers**. If your package doesn't contain Apex
> components, no tests are run by default."

> "if your package contains a custom object, all tests are run in API version **33.0 and earlier**. In
> contrast, **starting with API version 34.0, no tests are run for this package.**"

So the 24-type list is a decade-stale artefact that has been copied forward across training material and into
the bundles. On any supported API version, a `CustomField`/`Profile`/`Flow`/`ValidationRule` payload alone runs
**zero tests**.

**Had the bundle claim been merged unverified, the page would have taught a rule that has been wrong since
2015.** This is the strongest argument for the verify-before-merge discipline: SubQ correctly identified *where*
the gap was, and only the primary source could say *what* the correct content is.

The merged page now carries the version distinction, the official example, and the practical consequence — a
config-only deploy that looks validated is not, because nothing ran.

Source: [Running Tests in a Deployment](https://developer.salesforce.com/docs/platform/api-metadata/guide/meta-deploy-running-tests.html)

---

## Reproduction

```bash
export SUBQ_TOKEN_API_KEY=$(awk '/^SUBQ Token/{getline; print; exit}' ~/dbpasses.txt | tr -d ' \r')
cd /tmp/subq && python3 client.py q1.json   # then q2..q5
```

The five question specs are in `/tmp/subq/q{1..5}.json` and are reproducible: temperature 0, fixed options,
fixed state. They are not committed here because they reference a local key path; the states and options are
transcribed in this file.

## Caveat

SubQ's output is an **opinion about which gap is largest**, given the framing I supplied. It is not evidence
that the gap exists — the coverage measurement is. And it is not a source of facts; every number in the merged
pages came from a primary document. Treat the SubQ run as a prioritisation aid, which is what it was used for.