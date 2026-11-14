#!/usr/bin/env python3
"""Value-set conflict detection.

Coverage asks "who says more". Conflict asks "where do they disagree" -- and a
disagreement is only detectable if you look for the specific competing values.

Retrieval-by-topic fails here: a 1,100-char topical window often contains neither
competing number, so the model defaults to "different facets". So: for each
concept, scan BOTH sources for each candidate value, report which source asserts
which value, and flag a conflict only when the sources assert incompatible
members of the same value set.

Detection is deterministic (regex). The model is not used to find the conflict;
it is used only afterwards, if at all, to judge whether a difference matters.
"""
from __future__ import annotations
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_compare import flatten  # noqa: E402
from web_source import flatten_urls  # noqa: E402


def find(text: str, pat: str, window: int = 140) -> list[str]:
    """Return short contexts for every match of pat."""
    out = []
    for m in re.finditer(pat, text, re.I):
        s = max(0, m.start() - window)
        ctx = re.sub(r"\s+", " ", text[s:m.end() + window]).strip()
        if ctx not in out:
            out.append(ctx)
        if len(out) >= 3:
            break
    return out


def compare_values(la: str, ta: str, lb: str, tb: str, concepts: dict) -> list[dict]:
    rows = []
    for name, spec in concepts.items():
        row = {"concept": name, "values": {}, "a": {}, "b": {}}
        for vname, vpat in spec["values"].items():
            a_hits = find(ta, vpat)
            b_hits = find(tb, vpat)
            row["values"][vname] = vpat
            if a_hits:
                row["a"][vname] = a_hits
            if b_hits:
                row["b"][vname] = b_hits
        av, bv = set(row["a"]), set(row["b"])
        row["shared"] = sorted(av & bv)
        row["only_a"] = sorted(av - bv)
        row["only_b"] = sorted(bv - av)
        if av and bv and (av - bv) and (bv - av):
            row["status"] = "CONFLICT"      # both assert, but different values
        elif av and not bv:
            row["status"] = "A_ONLY"
        elif bv and not av:
            row["status"] = "B_ONLY"
        elif av and bv:
            row["status"] = "AGREE"
        else:
            row["status"] = "NO_SIGNAL"
        rows.append(row)
    return rows


if __name__ == "__main__":
    print("module")