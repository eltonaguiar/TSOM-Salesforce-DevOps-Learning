#!/usr/bin/env python3
"""Webpage source adapter.

A "webpage source" is a set of URLs whose rendered HTML documents a topic.
Differs from a repo source in ways that matter for comparison:

  - content is rendered: nav, breadcrumbs, footers, theme chrome are noise
  - JS-rendered content may be absent without a headless browser
  - the same page can be stale relative to its source markdown

So: fetch, keep only <main>/<article> when present, strip chrome, flatten to the
same text shape repo_compare.py produces.
"""
from __future__ import annotations
import json, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_compare import strip_markup  # noqa: E402

UA = "Mozilla/5.0 (compatible; doc-coverage-audit/1.0)"
CHROME = re.compile(
    r"(?is)<(nav|header|footer|aside|script|style|noscript|svg|form)\b.*?</\1>")


def fetch(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def main_content(html: str) -> str:
    """Prefer <main> or <article>; fall back to <body>. Drops theme chrome either way."""
    html = CHROME.sub(" ", html)
    for tag in ("main", "article"):
        m = re.search(rf"(?is)<{tag}\b[^>]*>(.*?)</{tag}>", html)
        if m and len(strip_markup(m.group(1))) > 500:
            return m.group(1)
    m = re.search(r"(?is)<body\b[^>]*>(.*?)</body>", html)
    return m.group(1) if m else html


def flatten_urls(urls: list[str], label: str) -> tuple[str, list[str]]:
    chunks, ok = [], []
    for u in urls:
        try:
            html = fetch(u)
        except Exception as e:  # noqa: BLE001 - report and continue
            chunks.append(f"\n===== {u} =====\n[FETCH FAILED: {e}]")
            continue
        body = strip_markup(main_content(html)).strip()
        if len(body) < 100:
            chunks.append(f"\n===== {u} =====\n[EMPTY OR JS-RENDERED: {len(body)} chars]")
            continue
        chunks.append(f"\n===== {u} =====\n{body}")
        ok.append(u)
    return "\n".join(chunks), ok


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    text, ok = flatten_urls(spec["urls"], spec.get("label", "web"))
    print(f"fetched {len(ok)}/{len(spec['urls'])} urls, {len(text):,} chars")
    for u in ok:
        print("  ok", u)