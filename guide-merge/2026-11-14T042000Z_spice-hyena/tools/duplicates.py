#!/usr/bin/env python3
"""Duplicate and overlap detection across a document set.

Three tiers, cheapest first:
  1. EXACT      - identical bytes (hash)
  2. NEAR       - high shingle Jaccard (copy, light edit, folder/flat twin)
  3. OVERLAP    - moderate shingle Jaccard (same material, different framing)

Near vs overlap is a threshold choice, not a discovery: >0.60 means "one is
largely redundant", 0.25-0.60 means "they overlap, both may be worth keeping".

Also reports a REPRESENTATIVE per cluster -- the longest document, which is the
one to keep when consolidating.
"""
from __future__ import annotations
import glob, hashlib, itertools, os, re, sys

TOKEN = re.compile(r"[a-z][a-z0-9_]{2,}")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def shingles(text: str, k: int = 5) -> set[str]:
    t = tokens(text)
    if len(t) < k:
        return {" ".join(t)} if t else set()
    return {" ".join(t[i:i + k]) for i in range(len(t) - k + 1)}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load(paths: list[str]) -> list[dict]:
    docs = []
    for p in paths:
        try:
            raw = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if len(raw.strip()) < 50:
            continue
        docs.append({"path": p, "sha": hashlib.md5(raw.encode()).hexdigest(),
                     "chars": len(raw), "sh": shingles(raw)})
    return docs


def analyse(docs: list[dict], near: float = 0.60, overlap: float = 0.25) -> dict:
    exact = {}
    for d in docs:
        exact.setdefault(d["sha"], []).append(d["path"])

    pairs = []
    for a, b in itertools.combinations(docs, 2):
        s = jaccard(a["sh"], b["sh"])
        if s >= overlap:
            pairs.append({"a": a["path"], "b": b["path"], "jaccard": round(s, 4),
                          "a_chars": a["chars"], "b_chars": b["chars"],
                          "tier": "NEAR" if s >= near else "OVERLAP"})

    # union-find over near-duplicate pairs -> clusters
    parent = {d["path"]: d["path"] for d in docs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for p in pairs:
        if p["tier"] == "NEAR":
            union(p["a"], p["b"])

    clusters = {}
    for d in docs:
        clusters.setdefault(find(d["path"]), []).append(d)
    cl = [sorted(v, key=lambda d: -d["chars"]) for v in clusters.values() if len(v) > 1]
    cl.sort(key=lambda c: -len(c))

    return {
        "exact": {k: v for k, v in exact.items() if len(v) > 1},
        "pairs": sorted(pairs, key=lambda p: -p["jaccard"]),
        "near_clusters": [{"representative": c[0]["path"],
                           "members": [d["path"] for d in c],
                           "chars": c[0]["chars"]} for c in cl],
        "counts": {"docs": len(docs),
                   "exact_groups": sum(1 for v in exact.values() if len(v) > 1),
                   "near_pairs": sum(1 for p in pairs if p["tier"] == "NEAR"),
                   "overlap_pairs": sum(1 for p in pairs if p["tier"] == "OVERLAP"),
                   "near_clusters": len(cl)},
    }


if __name__ == "__main__":
    print("module")