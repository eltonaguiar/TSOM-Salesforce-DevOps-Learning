#!/usr/bin/env python3
"""Concept inventory and set comparison across two sources.

Distinct from claim checking: this asks whether a concept is *present at all*,
not whether the source is right about it. Presence is a substring question and
keyword matching is adequate -- a page mentioning "sandbox" covers the concept
even if it describes it badly. (For claims, see polarity.py.)

Outputs three sets:
  BOTH      - the shared curriculum core
  ONLY_A    - what source A uniquely contributes
  ONLY_B    - what source B uniquely contributes

Plus per-source counts, so a concept present in neither is visible rather than
silently dropped from the taxonomy.
"""
from __future__ import annotations
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def present(text: str, patterns: dict[str, str]) -> dict[str, bool]:
    return {name: bool(re.search(pat, text, re.I)) for name, pat in patterns.items()}


def compare(la: str, ta: str, lb: str, tb: str, concepts: dict) -> dict:
    pa = present(ta, concepts)
    pb = present(tb, concepts)
    both = sorted(k for k in pa if pa[k] and pb[k])
    only_a = sorted(k for k in pa if pa[k] and not pb[k])
    only_b = sorted(k for k in pa if pb[k] and not pa[k])
    neither = sorted(k for k in pa if not pa[k] and not pb[k])
    return {
        "sources": {"A": la, "B": lb},
        "counts": {"A": sum(pa.values()), "B": sum(pb.values()),
                   "both": len(both), "only_A": len(only_a),
                   "only_B": len(only_b), "neither": len(neither),
                   "total": len(concepts)},
        "both": both, "only_A": only_a, "only_B": only_b, "neither": neither,
        "detail": {k: {"A": pa[k], "B": pb[k]} for k in sorted(concepts)},
    }


if __name__ == "__main__":
    print("module")