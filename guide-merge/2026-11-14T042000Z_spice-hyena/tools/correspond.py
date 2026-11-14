#!/usr/bin/env python3
"""Repository-file -> webpage correspondence.

Two mappings, different confidence:

  1. GUIDE REPO -> PAGE. Deterministic: the guide repo publishes
     docs/salesforce/<name>.md at /docs/salesforce/<name>/. No inference needed.

  2. TSOM BUNDLE FILE -> PAGE. Not declared anywhere. Inferred by scoring each
     bundle file's vocabulary against each page's vocabulary (TF-IDF cosine),
     then assigning to the best match. This is a similarity claim, not a
     declared mapping -- report the margin so a weak assignment is visible.

Outputs, per page: which files feed it, how much input it got, and which files
are orphans (match no page above threshold).
"""
from __future__ import annotations
import glob, json, math, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_compare import flatten, strip_markup  # noqa: E402

TOKEN = re.compile(r"[a-z][a-z0-9_.]{2,}")
STOP = set("""the a an and or of to in is are was were be been for on with as at by from this that these those it its
not no if then than so such can will would should could may might must do does did has have had you your we our they
their there here what which who whom when where why how all any both each few more most other some only own same too
very s t just don now also into over under about after before between during out up down off again further once
https http www com github io org docs md html setup salesforce page pages guide guides lab labs""".split())


def toks(text: str) -> Counter:
    return Counter(t for t in TOKEN.findall(text.lower()) if t not in STOP and len(t) > 2)


def idf(ptoks: dict[str, Counter]) -> dict[str, float]:
    """Downweight terms common to all pages; keep terms that distinguish a page."""
    n = len(ptoks)
    df = Counter()
    for c in ptoks.values():
        for t in c:
            df[t] += 1
    return {t: math.log((n + 1) / (d + 0.5)) for t, d in df.items()}


def cosine(a: Counter, b: Counter, weights: dict[str, float] | None = None) -> float:
    if not a or not b:
        return 0.0
    w = weights or {}
    num = sum(w.get(t, 1.0) * a[t] * b[t] for t in set(a) & set(b))
    da = math.sqrt(sum(w.get(t, 1.0) * v * v for t, v in a.items()))
    db = math.sqrt(sum(w.get(t, 1.0) * v * v for t, v in b.items()))
    if not da or not db:
        return 0.0
    return max(0.0, min(1.0, num / (da * db)))


def guide_mapping(guide_dir: str) -> list[dict]:
    rows = []
    for p in sorted(glob.glob(os.path.join(guide_dir, "docs/salesforce/*.md"))):
        name = os.path.basename(p)[:-3]
        rows.append({"file": os.path.relpath(p, guide_dir),
                     "page": f"/docs/salesforce/{name}/",
                     "kind": "declared",
                     "confidence": 1.0})
    return rows


def bundle_mapping(bundle_dir: str, page_texts: dict[str, str]) -> tuple[list[dict], list[dict]]:
    ptoks = {k: toks(v) for k, v in page_texts.items()}
    weights = idf(ptoks)
    rows, orphans = [], []
    for p in sorted(glob.glob(os.path.join(bundle_dir, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, bundle_dir)
        try:
            raw = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if len(raw.strip()) < 200:
            continue
        ft = toks(raw)
        scores = sorted(((cosine(ft, pt, weights), k) for k, pt in ptoks.items()), reverse=True)
        best_score, best_page = scores[0]
        runner_up = scores[1][0] if len(scores) > 1 else 0.0
        margin = best_score - runner_up
        row = {"file": rel, "page": best_page, "score": round(best_score, 4),
               "runner_up": round(runner_up, 4),
               "margin": round(margin, 4), "chars": len(raw), "kind": "inferred"}
        if best_score < 0.02 or margin < 0.002:
            row["weak"] = True
            orphans.append(row)
        rows.append(row)
    return rows, orphans


if __name__ == "__main__":
    print("module")