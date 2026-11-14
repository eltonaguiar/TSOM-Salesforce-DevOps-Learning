#!/usr/bin/env python3
"""Conflict detection between two documentation sources.

Coverage asks "who says more". This asks "where do they disagree" -- which is the
question that matters, because a disagreement is where one of them is wrong.

Three verdicts per concept:
  AGREE      - both excerpts teach the same thing
  CONFLICT   - they assert incompatible things (one is wrong)
  DIFFERENT  - they cover different facets, no contradiction

A CONFLICT is only actionable once you check it against a primary source; this
module flags, it does not adjudicate.
"""
from __future__ import annotations
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic import decide, pick  # noqa: E402
from retrieval_judge import retrieve  # noqa: E402


def classify(la: str, ta: str, lb: str, tb: str, concepts: dict) -> list[dict]:
    rows = []
    for name, spec in concepts.items():
        terms = spec["terms"]
        ae, be = retrieve(ta, terms), retrieve(tb, terms)
        state = (f"SOURCE A ({la}) on '{name}':\n{ae}\n\n"
                 f"SOURCE B ({lb}) on '{name}':\n{be}\n\n"
                 f"SPECIFIC VALUES TO CHECK: {spec.get('values','(none given)')}")
        instr = ("Do these two excerpts AGREE, CONFLICT, or cover DIFFERENT facets? "
                 "Choose CONFLICT only if they assert incompatible specific values or rules "
                 "that cannot both be true. Judge only the excerpts shown.")
        opts = ["AGREE: same facts",
                "CONFLICT: incompatible facts or rules",
                "DIFFERENT: non-overlapping facets, no contradiction"]
        try:
            r = decide(state, instr, opts)
            ch, p = pick(r, opts)
        except RuntimeError as e:
            rows.append({"concept": name, "verdict": "ERROR", "prob": 0.0, "err": str(e)[:120]})
            continue
        v = ("AGREE" if ch.startswith("AGREE")
             else "CONFLICT" if ch.startswith("CONFLICT") else "DIFFERENT")
        rows.append({"concept": name, "verdict": v, "prob": round(p, 3),
                     "confidence": r.get("answers", {}).get("q1", {}).get("confidence"),
                     "a_excerpt": ae[:400], "b_excerpt": be[:400]})
    return rows


if __name__ == "__main__":
    print("module")