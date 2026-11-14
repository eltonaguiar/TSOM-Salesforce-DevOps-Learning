#!/usr/bin/env python3
"""Repository-scale semantic coverage comparison.

A "source" is a directory tree of mixed documentation files (.md, .html, .xml,
.json, source code). This module flattens a repo into comparable text, then asks
SubQ per-concept which source covers it more substantively.

Usage:
    python3 repo_compare.py --a <dirA> --b <dirB> --concepts concepts.json
"""
from __future__ import annotations
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic import compare  # noqa: E402

TEXT_EXT = {".md", ".markdown", ".txt", ".rst"}
MARKUP_EXT = {".html", ".htm", ".xml", ".svg", ".mdx"}
CODE_EXT = {".py", ".js", ".ts", ".java", ".apex", ".cls", ".trigger", ".sh", ".yaml", ".yml", ".json"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
MAX_BYTES = 900_000  # keep the state within SubQ's practical input budget


def strip_markup(t: str) -> str:
    t = re.sub(r"(?is)<(script|style|nav|footer|header)\b.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def strip_code(t: str) -> str:
    """Keep comments and string literals that carry documentation; drop the rest."""
    out = []
    for line in t.splitlines():
        s = line.strip()
        if s.startswith(("#", "//", "/*", "*", "--")) or re.search(r'"""|\'\'\'', s):
            out.append(s)
    return "\n".join(out)


def flatten(root: str) -> tuple[str, list[str]]:
    chunks, files = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (TEXT_EXT | MARKUP_EXT | CODE_EXT):
                continue
            try:
                raw = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if not raw.strip():
                continue
            if ext in MARKUP_EXT:
                body = strip_markup(raw)
            elif ext in CODE_EXT:
                body = strip_code(raw)
            else:
                body = raw
            body = body.strip()
            if len(body) < 40:
                continue
            chunks.append(f"\n===== {os.path.relpath(p, root)} =====\n{body}")
            files.append(os.path.relpath(p, root))
    text = "\n".join(chunks)
    return text, files


def shrink(text: str, limit: int = MAX_BYTES) -> str:
    if len(text) <= limit:
        return text
    # keep every file's header + an even slice, so no file disappears entirely
    parts = text.split("\n===== ")
    head, rest = parts[0], parts[1:]
    budget = max(1, limit - len(head))
    per = max(1, budget // max(1, len(rest)))
    out = [head]
    for p in rest:
        out.append(p[:per])
    return "\n===== ".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="label/dir, e.g. merged:/path")
    ap.add_argument("--b", required=True, help="label/dir, e.g. corpus:/path")
    ap.add_argument("--concepts", required=True)
    ap.add_argument("--out", default="semantic_result.json")
    args = ap.parse_args()

    la, da = args.a.split(":", 1)
    lb, db = args.b.split(":", 1)
    ta, fa = flatten(da)
    tb, fb = flatten(db)
    ta, tb = shrink(ta), shrink(tb)
    print(f"{la}: {len(fa)} files, {len(ta):,} chars")
    print(f"{lb}: {len(fb)} files, {len(tb):,} chars")

    concepts = json.load(open(args.concepts))
    rows = compare(la, ta, lb, tb, concepts)

    wins_a = sum(1 for r in rows if r["winner"] == "A")
    wins_b = sum(1 for r in rows if r["winner"] == "B")
    ties = sum(1 for r in rows if r["winner"] == "TIE")
    errs = sum(1 for r in rows if r["winner"] == "ERROR")

    print(f"\n{'concept':34} {'winner':7} {'prob':>6}  confidence")
    for r in rows:
        print(f"{r['concept']:34} {r['winner']:7} {r['prob']:>6}  {r.get('confidence')}")

    print(f"\n{la} wins {wins_a} | {lb} wins {wins_b} | ties {ties} | errors {errs}")
    print(f"\nConcepts where {lb} is still BETTER covered than {la} (residual gap):")
    gaps = [r for r in rows if r["winner"] == "B"]
    for r in sorted(gaps, key=lambda x: -x["prob"]) or []:
        print(f"  {r['prob']:.2f}  {r['concept']}")

    json.dump({"meta": {"a": la, "b": lb, "files_a": len(fa), "files_b": len(fb)},
               "rows": rows, "wins": {"A": wins_a, "B": wins_b, "TIE": ties}},
              open(args.out, "w"), indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()