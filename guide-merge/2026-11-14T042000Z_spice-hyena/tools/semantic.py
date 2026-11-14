#!/usr/bin/env python3
"""Semantic coverage comparison between two documentation sources.

For each concept, ask SubQ which source covers it more substantively.
Aggregates to a per-source win count -> a ranked gap list.

This is deliberately different from keyword presence: a page can contain the word
"coverage" and still not teach the rule. SubQ judges the substance, not the token.
"""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error

API = "https://api.subq.ai/v1/systemone"
MODEL = "subq-snap-1.2"


def key() -> str:
    k = os.environ.get("SUBQ_TOKEN_API_KEY") or os.environ.get("SUBQ_FREE_API_KEY")
    if not k:
        sys.exit("no SubQ key")
    return k


def decide(state: str, instructions: str, options: list[str], temperature: float = 0.0) -> dict:
    criteria = {"options": options}
    for i, o in enumerate(options):
        criteria[f"option_{i}"] = o
    payload = {"model": MODEL, "state": state,
               "questions": {"q1": {"instructions": instructions, "type": "choice", "criteria": criteria}},
               "temperature": temperature}
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}") from e


def pick(resp: dict) -> tuple[str, float]:
    a = resp.get("answers", {}).get("q1", {})
    pr = a.get("probabilities", {}) or {}
    if not pr:
        return a.get("choice", "?"), 0.0
    best = max(pr.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else -1)
    return best[0], best[1]


def compare(label_a: str, text_a: str, label_b: str, text_b: str, concepts: dict[str, str]) -> list[dict]:
    """concepts: {name: what 'substantive coverage' means for this concept}"""
    rows = []
    for name, definition in concepts.items():
        state = (f"SOURCE A = {label_a}\n---\n{text_a}\n---\n\n"
                 f"SOURCE B = {label_b}\n---\n{text_b}\n---\n\n"
                 f"CONCEPT: {name}\nSUBSTANTIVE COVERAGE MEANS: {definition}")
        instr = (f"For the concept '{name}', which source covers it more substantively? "
                 f"Choose A if A teaches it well enough to act on, B if B does, or TIE if both are "
                 f"equally thin or equally complete.")
        opts = [f"A: {label_a}", f"B: {label_b}", "TIE: equally thin or equally complete"]
        try:
            r = decide(state, instr, opts)
            ch, p = pick(r)
        except RuntimeError as e:
            rows.append({"concept": name, "winner": "ERROR", "prob": 0.0, "err": str(e)})
            continue
        winner = "A" if ch.startswith("A") else ("B" if ch.startswith("B") else "TIE")
        rows.append({"concept": name, "winner": winner, "prob": round(p, 3),
                     "choice": ch, "confidence": r.get("answers", {}).get("q1", {}).get("confidence")})
    return rows


if __name__ == "__main__":
    print("import as a module")