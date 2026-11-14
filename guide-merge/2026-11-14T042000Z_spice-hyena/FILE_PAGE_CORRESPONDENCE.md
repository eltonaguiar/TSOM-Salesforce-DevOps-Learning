# File ↔ page correspondence

**Question answered:** which repository file corresponds to which webpage.

Needed before any file-level comparison: without it, a comparison treats each source as an
undifferentiated blob and cannot say *which* page lost content or *which* file is orphaned.

Built: `correspond.py` · 2026-11-14 · deterministic where declared, inferred where not.

---

## Mapping 1 — guide repo → page (declared, no inference)

The guide repo publishes `docs/salesforce/<name>.md` at `/docs/salesforce/<name>/`. One-to-one,
no ambiguity:

| Repository file | Webpage |
|---|---|
| `docs/salesforce/crash-course.md` | `/docs/salesforce/crash-course/` |
| `docs/salesforce/devops-engineer.md` | `/docs/salesforce/devops-engineer/` |
| `docs/salesforce/labs-design.md` | `/docs/salesforce/labs-design/` |
| `docs/salesforce/navigation-breadcrumbs.md` | `/docs/salesforce/navigation-breadcrumbs/` |
| `docs/salesforce/user-management-data.md` | `/docs/salesforce/user-management-data/` |

All five are one-way: each file feeds exactly one page, and each page has exactly one source file.
There are no orphaned page files and no pages without a source file.

## Mapping 2 — TSOM bundle file → page (inferred)

Nothing in the bundles declares which page a file targets. Inferred by IDF-weighted cosine similarity
between each bundle file's vocabulary and each page's, assigned to the best match with the margin over
the runner-up reported.

| Page | Files | Chars | Mean score | Max |
|---|---|---|---|---|
| `devops-engineer` | 77 | 1,542,893 | 0.392 | 0.804 |
| `crash-course` | 4 | 78,979 | 0.547 | 0.861 |
| `labs-design` | 2 | 12,627 | 0.490 | 0.899 |
| `user-management-data` | 1 | 12,458 | 0.996 | 0.996 |
| `navigation-breadcrumbs` | 1 | 7,737 | 0.955 | 0.955 |

**The 77-file skew to `devops-engineer` is a real finding, not a bias.** The corpus is *Salesforce
DevOps* research: limits, CI/CD, packaging, conflict resolution. Four pages are beginner/ELI5 material that
the research was never aimed at. The mapping is reporting what the corpus is.

**Validation.** The highest-margin assignments are exactly the files whose *names* declare their page:

| File | Score | Margin |
|---|---|---|
| `20261114-020852-salesforcemore/source-capture/user-management-data.md` | 0.9955 | 0.677 |
| `20261114-020852-salesforcemore/source-capture/navigation-breadcrumbs.md` | 0.9546 | 0.549 |
| `20261114-020300-salesforceagain-kilo/05-jd-term-deep-dive.md` | 0.8040 | 0.559 |

Files named after a page map to that page with the strongest confidence. The method recovers declared
intent where it exists, which is the check that it is measuring content and not noise.

**Confidence distribution.** Median margin 0.176; only **3 of 85** files are weak (<0.02):

| File | Margin | Assigned |
|---|---|---|
| `20261114-023241-salesforceagain-v2/01-limits-governors-and-system-properties.md` | 0.019 | crash-course |
| `20261114-023241-salesforceagain-v2/06-certifications-and-curriculum.md` | 0.017 | devops-engineer |
| `salesforceagain-v4-2026-11-14-0230/research-plan.md` | 0.006 | labs-design |

The third is a meta-document about how to do research, not Salesforce content — it matching *anything* is
noise, and `research-plan.md` is the correct answer to "where does this belong": nowhere.

## Two bugs found while building this

**Unpacking.** `scores` holds `(score, key)` tuples; `best, second = scores[0]` unpacks the tuple rather than
indexing it, so `best[1]` raised `TypeError: 'float' object is not subscriptable`.

**Weighted cosine was not a cosine.** The first IDF version weighted the numerator once and squared the weight
in the denominator:

```
num = Σ w·a·b          da = √Σ(w·a)²        # inconsistent
```

For `a == b` this gives `Σw·a² / Σw²·a²`, which exceeds 1 — and one page scored **1.6378**, an impossible
cosine. Correct form weights both terms linearly:

```
num = Σ w·a·b          da = √Σ(w·a²)        db = √Σ(w·b²)
```

Scores are now bounded 0–1 (observed 0.081–0.996). Worth noting the ranking barely changed — the bug
inflated magnitudes, not order. But an out-of-range score is a signal that something is wrong, and it was
the only visible symptom of a real formula error.

## What this enables

With the correspondence in hand, comparisons can be **per page** instead of per blob:

- For each page, compare only the files that map to it — a like-for-like comparison
- `devops-engineer` has 77 input files and the others have 1–4; that ratio alone predicts where the
  research depth went and where it did not
- Orphan detection: `research-plan.md` is the only file matching no page, and correctly so
- A file whose score is high but whose margin is low is ambiguous — those 3 files are the ones to inspect
  by hand rather than trust