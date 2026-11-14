#!/usr/bin/env python3
"""Retrieval-then-judge semantic comparison.

Why this exists: asking a model "which of these two 100K-char documents covers X
better" produces a degenerate answer -- it cannot compare what it cannot see.
So: retrieve the most relevant passage from each source for each concept, then
ask the model to compare only those two excerpts.

Forced binary (no TIE option): a TIE escape hatch absorbs every uncertain case,
which is what made the naive version return 10/10 TIE.
"""
from __future__ import annotations
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic import decide, pick  # noqa: E402

WINDOW = 1100


def passages(text: str) -> list[tuple[int, str]]:
    """Split into passages at file headers, then on paragraph breaks."""
    out = []
    # split at file headers, keeping offsets
    marks = [(m.end(), m.start()) for m in re.finditer(r"\n?===== .*?=====\n", text)]
    if not marks:
        bounds = [(0, len(text))]
    else:
        bounds = []
        prev = 0
        for body_start, hdr_start in marks:
            if hdr_start > prev:
                bounds.append((prev, hdr_start))
            bounds.append((body_start, None))
            prev = body_start
        bounds.append((prev, len(text)))
        # resolve the None ends
        fixed = []
        for i, (s, e) in enumerate(bounds):
            if e is None:
                e = bounds[i + 1][0] if i + 1 < len(bounds) else len(text)
            fixed.append((s, e))
        bounds = fixed

    refined = []
    for s, e in bounds:
        body = text[s:e]
        if len(body.strip()) < 40:
            continue
        if len(body) <= WINDOW * 1.4:
            refined.append((s, body))
            continue
        for p in re.split(r"\n\s*\n", body):
            if len(p.strip()) < 40:
                continue
            refined.append((s, p))
    return refined


JUNK = re.compile(r"(Worktree:\*\*|Timestamp:\*\*|^\s*[-*] \[.*?\]\(#|Contents\n|Next Steps|## Sources|Source Repo:|Agent:\*\*)", re.M)


def _is_junk(body: str) -> bool:
    """Reject navigation, TOCs, and agent meta-headers: they match keywords but teach nothing."""
    low = body.lower()
    if len(re.findall(r"\]\(#", body)) > 3:          # TOC / anchor links
        return True
    if re.search(r"\|\s*---", body) and len(body) < 400:  # front-matter table
        return True
    if low.count("worktree:") + low.count("timestamp:") + low.count("source repo:") > 1:
        return True
    if len(re.findall(r"^\s*[-*]\s", body, re.M)) > 12 and len(re.findall(r"[.!?]\s", body)) < 3:
        return True                                      # bullet skeleton, no prose
    if JUNK.search(body) and len(body) < 600:
        return True
    return False


def retrieve(text: str, terms: list[str], k: int = 2, want_number: bool = True) -> str:
    ps = [(o, b) for o, b in passages(text) if len(b.strip()) > 80 and not _is_junk(b)]
    if not ps:
        ps = passages(text)
    if not ps:
        return text[:WINDOW]
    scored = []
    for off, body in ps:
        low = body.lower()
        hits = sum(low.count(t.lower()) for t in terms if t)
        if not hits:
            continue
        density = hits / max(1.0, (len(body) / 1000.0) ** 0.6)
        if want_number and not re.search(r"\d", body):
            density *= 0.35
        # penalise passages that are mostly links
        links = len(re.findall(r"\]\(|https?://", body))
        density /= (1.0 + links / 40.0)
        scored.append((density, off, body))
    if not scored:
        return ps[0][1][:WINDOW]
    scored.sort(key=lambda x: -x[0])
    seen, out = set(), []
    for density, off, body in scored:
        if any(abs(off - s) < WINDOW // 2 for s in seen):
            continue
        seen.add(off)
        out.append(body.strip()[:WINDOW])
        if len(out) >= k:
            break
    return ("\n[...]\n".join(out))[: WINDOW * k]


def run(la: str, ta: str, lb: str, tb: str, concepts: dict[str, dict]) -> list[dict]:
    rows = []
    for name, spec in concepts.items():
        terms = spec["terms"]
        a_ex = retrieve(ta, terms)
        b_ex = retrieve(tb, terms)
        state = (f"SOURCE A ({la}) says, on '{name}':\n{a_ex}\n\n"
                 f"SOURCE B ({lb}) says, on '{name}':\n{b_ex}\n\n"
                 f"WHAT A READER NEEDS: {spec['need']}")
        instr = ("Which source gives a reader more of what they need for this concept? "
                 "Judge only the excerpts above, not what you assume the full documents contain.")
        opts = [f"A: {la} excerpt is more complete", f"B: {lb} excerpt is more complete"]
        try:
            r = decide(state, instr, opts)
            ch, p = pick(r)
        except RuntimeError as e:
            rows.append({"concept": name, "winner": "ERROR", "prob": 0.0, "err": str(e)[:120]})
            continue
        w = "A" if ch.startswith("A") else "B"
        rows.append({"concept": name, "winner": w, "prob": round(p, 3),
                     "a_excerpt_chars": len(a_ex), "b_excerpt_chars": len(b_ex)})
    return rows


if __name__ == "__main__":
    print("module")