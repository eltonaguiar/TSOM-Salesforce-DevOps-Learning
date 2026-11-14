#!/usr/bin/env python3
"""Parallel local-model benchmark.

Same task to vLLM and Ollama simultaneously; score against SubQ-derived
ground truth. Tests whether any local model can do usefully large work.

Task: classify 10 job-description topics against a documentation corpus as
COVERED / PARTIAL / MISSING, returning strict JSON.
"""
from __future__ import annotations
import json, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

VLLM = "http://localhost:8000/v1/chat/completions"
OLLAMA = "http://localhost:11434/api/chat"

DOCS = open("/tmp/sam_condensed.txt", encoding="utf-8").read()
JD = json.load(open("/tmp/sam_jd.json"))
GT = json.load(open("/tmp/subq/sam_gt_full.json"))

TOPICS = list(JD)

PROMPT = f"""You are auditing ServiceNow SAM documentation against a BMO SAM Administrator job description.

For EACH of the 10 topics below, decide whether the documentation covers it:
  COVERED  = explains the mechanism well enough to act on
  PARTIAL  = mentioned but thin, or only one aspect
  MISSING  = not present

Return ONLY a JSON object mapping each topic key to one of COVERED, PARTIAL, MISSING.
No prose, no markdown fences.

TOPICS:
{chr(10).join(f'- {k}: {v}' for k, v in JD.items())}

DOCUMENTATION:
{DOCS}

JSON:"""


def post(url: str, payload: dict, timeout: int = 300) -> tuple[dict | None, float, str | None]:
    t0 = time.time()
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode()), time.time() - t0, None
    except urllib.error.HTTPError as e:
        return None, time.time() - t0, f"HTTP {e.code}: {e.read().decode()[:160]}"
    except Exception as e:  # noqa: BLE001
        return None, time.time() - t0, f"{type(e).__name__}: {str(e)[:120]}"


def run_vllm(model: str) -> dict:
    body = {"model": model, "temperature": 0, "max_tokens": 400,
            "messages": [{"role": "user", "content": PROMPT}]}
    r, dt, err = post(VLLM, body)
    if err:
        return {"model": model, "backend": "vllm", "error": err, "secs": round(dt, 1)}
    try:
        txt = r["choices"][0]["message"]["content"]
        usage = r.get("usage", {})
    except Exception:
        return {"model": model, "backend": "vllm", "error": "bad response shape", "secs": round(dt, 1)}
    return {"model": model, "backend": "vllm", "secs": round(dt, 1), "text": txt,
            "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens")}


def run_ollama(model: str) -> dict:
    body = {"model": model, "stream": False, "options": {"temperature": 0, "num_predict": 400},
            "messages": [{"role": "user", "content": PROMPT}]}
    r, dt, err = post(OLLAMA, body)
    if err:
        return {"model": model, "backend": "ollama", "error": err, "secs": round(dt, 1)}
    try:
        txt = r["message"]["content"]
    except Exception:
        return {"model": model, "backend": "ollama", "error": "bad response shape", "secs": round(dt, 1)}
    return {"model": model, "backend": "ollama", "secs": round(dt, 1), "text": txt,
            "prompt_tokens": r.get("prompt_eval_count"), "completion_tokens": r.get("eval_count")}


def parse(text: str) -> dict:
    """Extract the topic->verdict map from loosely-formatted model output."""
    m = re.search(r"\{[^{}]*\}", text, re.S)
    if not m:
        return {}
    try:
        d = json.loads(m.group(0))
    except Exception:
        # repair: pull key:VERDICT pairs
        d = dict(re.findall(r'"?([a-z_]+)"?\s*:\s*"?(COVERED|PARTIAL|MISSING)"?', text))
    out = {}
    for k in TOPICS:
        v = d.get(k)
        if isinstance(v, str) and v.upper() in ("COVERED", "PARTIAL", "MISSING"):
            out[k] = v.upper()
    return out


def score(pred: dict) -> dict:
    exact = sum(1 for k in TOPICS if pred.get(k) == GT[k]["verdict"])
    # adjacency: PARTIAL is half-right against either neighbour
    order = {"MISSING": 0, "PARTIAL": 1, "COVERED": 2}
    adj = 0.0
    for k in TOPICS:
        p, g = pred.get(k), GT[k]["verdict"]
        if not p:
            continue
        d = abs(order[p] - order[g])
        adj += 1.0 if d == 0 else (0.5 if d == 1 else 0.0)
    return {"exact": exact, "adjacent": round(adj / len(TOPICS), 3),
            "answered": len(pred), "of": len(TOPICS)}


def main() -> None:
    targets = [("vllm", "Qwen/Qwen2.5-14B-Instruct"),
               ("ollama", "qwen3.5:4b"),
               ("ollama", "qwen2.5:14b"),
               ("ollama", "qwen2.5:32b"),
               ("ollama", "llama3.1:8b"),
               ("ollama", "qwen2.5-coder:14b"),
               ("ollama", "gemma3:12b"),
               ("ollama", "deepseek-r1:32b")]
    print(f"Firing {len(targets)} models in parallel. Input: {len(DOCS):,} chars (~{len(DOCS)//4:,} tokens)")
    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=len(targets)) as ex:
        futs = {ex.submit(run_vllm if b == "vllm" else run_ollama, m): (b, m) for b, m in targets}
        for f in as_completed(futs):
            results.append(f.result())
    wall = time.time() - t0
    for r in results:
        if "error" in r:
            r["score"] = {"exact": 0, "adjacent": 0, "answered": 0, "of": len(TOPICS)}
        else:
            r["parsed"] = parse(r["text"])
            r["score"] = score(r["parsed"])
    results.sort(key=lambda r: (-r["score"]["adjacent"], r["secs"]))
    print(f"\nwall clock (parallel): {wall:.1f}s\n")
    print(f"{'model':30} {'backend':8} {'exact':>6} {'adj':>6} {'ans':>5} {'secs':>6} {'tok':>6}")
    print("-" * 74)
    for r in results:
        s = r["score"]
        tok = r.get("completion_tokens") or 0
        print(f"{r['model'][:30]:30} {r['backend']:8} {s['exact']:>3}/10 {s['adjacent']:>6.2f} "
              f"{s['answered']:>2}/{s['of']:<2} {r['secs']:>6.1f} {tok:>6}")
    json.dump({"wall_secs": round(wall, 1), "results": results,
               "ground_truth": {k: v["verdict"] for k, v in GT.items()}},
              open("/tmp/local_bench.json", "w"), indent=1)
    print("\nwrote /tmp/local_bench.json")


if __name__ == "__main__":
    main()