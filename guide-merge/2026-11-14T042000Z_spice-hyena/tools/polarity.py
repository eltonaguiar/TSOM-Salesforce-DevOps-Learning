#!/usr/bin/env python3
"""Polarity-aware claim checking.

Every method above shares one flaw: substring presence cannot distinguish an
assertion from its refutation. A page saying "there is NO 1% per class rule"
scores identically to a page saying "the rule is 1% per class".

Fix: for each (source, claim), ask the model for the source's POLARITY on that
claim -- ASSERTS / DENIES / NOT_ADDRESSED -- then compare polarities.

  both ASSERT, same value   -> agree
  both ASSERT, diff value   -> conflict
  one ASSERTS, other DENIES -> direct contradiction
  anything NOT_ADDRESSED    -> no signal

This is the only variant that can catch a contradiction, because it reads the
claim rather than the token.
"""
from __future__ import annotations
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic import decide, pick  # noqa: E402
from retrieval_judge import retrieve  # noqa: E402


def polarity(la: str, ta: str, lb: str, tb: str, concepts: dict) -> list[dict]:
    rows = []
    for name, spec in concepts.items():
        terms = spec["terms"]
        ae, be = retrieve(ta, terms), retrieve(tb, terms)
        out = {"concept": name, "claim": spec["claim"]}
        for tag, label, excerpt in (("A", la, ae), ("B", lb, be)):
            state = (f"SOURCE ({label}) excerpt on '{name}':\n{excerpt}\n\n"
                     f"CLAIM UNDER TEST: {spec['claim']}")
            instr = ("Does this source ASSERT the claim, DENY the claim, or NOT ADDRESS it? "
                     "Judge only the excerpt. If it mentions the topic but never takes a position "
                     "on this specific claim, choose NOT ADDRESSED.")
            opts = ["ASSERTS the claim", "DENIES the claim", "NOT ADDRESSED"]
            try:
                r = decide(state, instr, opts)
                ch, p = pick(r, opts)
            except RuntimeError as e:
                out[tag] = {"polarity": "ERROR", "err": str(e)[:100]}
                continue
            pol = ("ASSERTS" if ch.startswith("ASSERTS")
                   else "DENIES" if ch.startswith("DENIES") else "NOT_ADDRESSED")
            out[tag] = {"polarity": pol, "prob": round(p, 3)}
        pa, pb = out["A"]["polarity"], out["B"]["polarity"]
        if "ERROR" in (pa, pb):
            verdict = "ERROR"
        elif pa == "NOT_ADDRESSED" or pb == "NOT_ADDRESSED":
            verdict = "NO_SIGNAL"
        elif pa == "DENIES" and pb == "DENIES":
            verdict = "AGREE"
        elif pa == "ASSERTS" and pb == "ASSERTS":
            verdict = "AGREE"
        elif {pa, pb} == {"ASSERTS", "DENIES"}:
            verdict = "CONTRADICTION"
        else:
            verdict = "MIXED"
        out["verdict"] = verdict
        rows.append(out)
    return rows


if __name__ == "__main__":
    print("module")