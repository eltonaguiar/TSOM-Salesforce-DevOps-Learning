#!/usr/bin/env python3
"""Semantic (embedding-based) comparison -- replaces the lexical instruments.

Why this exists: the earlier pipeline matched tokens. A table of contents scored
highly for "governor" because the word appeared in it. An assertion and its
refutation scored identically because both contain "1%". A paraphrase scored zero
because it shares no 5-word sequences.

Embeddings map text to a meaning space, so:
  - retrieval is by meaning, not by token overlap
  - "the heap is 10 MB" and "memory is capped at ten megabytes" are close
  - a TOC is far from the concept it merely names

Model: all-MiniLM-L6-v2 (384-dim, CPU-friendly).
"""
from __future__ import annotations
import os, re, sys
import numpy as np

_MODEL = None
CHUNK = 220  # words per embedded chunk


def model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def chunk_text(text: str, chunk_words: int = CHUNK) -> list[str]:
    """Split into word-bounded chunks; keeps tables and lists intact-ish."""
    out = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        words = block.split()
        if len(words) <= chunk_words:
            if len(block) > 40:
                out.append(block)
            continue
        for i in range(0, len(words), chunk_words):
            piece = " ".join(words[i:i + chunk_words])
            if len(piece) > 40:
                out.append(piece)
    return out


def embed(texts: list[str], batch: int = 64) -> np.ndarray:
    if not texts:
        return np.zeros((0, 384))
    m = model()
    v = m.encode(texts, batch_size=batch, show_progress_bar=False,
                 normalize_embeddings=True, convert_to_numpy=True)
    return v


def top_passages(query: str, chunks: list[str], k: int = 3,
                 min_sim: float = 0.0) -> list[tuple[float, str]]:
    """Semantic retrieval: rank chunks by cosine similarity to the query meaning."""
    if not chunks:
        return []
    qv = embed([query])[0]
    cv = embed(chunks)
    sims = cv @ qv                      # both normalised -> dot = cosine
    order = np.argsort(-sims)
    out = []
    for i in order[:k * 3]:
        if len(out) >= k:
            break
        if sims[i] < min_sim:
            continue
        out.append((float(sims[i]), chunks[i]))
    return out


def doc_vector(chunks: list[str]) -> np.ndarray:
    """Mean-pooled chunk vectors = a document embedding."""
    if not chunks:
        return np.zeros(384)
    v = embed(chunks)
    return v.mean(axis=0)


def sim(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na and nb else 0.0


if __name__ == "__main__":
    print("module; call embed()/top_passages()/doc_vector()")