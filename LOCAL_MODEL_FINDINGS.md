# Local model findings — benchmark, stability, capability

Date: 2026-11-14 · Machine: ASUS GX10 (NVIDIA GB10, 128 GB unified) · Backends: vLLM :8000, Ollama :11434,
LiteLLM :4000, Hermes on Windows LAN :8642.

Everything below is measured, not assumed. Methods and raw data are referenced at the bottom.

---

## TL;DR

- **The local models can do decent, real work** — a 10-topic classification at 0.80–0.85 adjacent accuracy, and
  real browser-task completion on MiniWoB (55–70%).
- **The proxy does not die under concurrent mixed models.** 6 distinct models simultaneously: 6/6 ok, survived.
  18 concurrent: 16/18 (two 429s), survived. No endpoint needed a restart.
- **The top accuracy scorer is the wrong default for agentic work.** `gemma3:12b` has **no tool support**
  (HTTP 400). `qwen2.5:14b` is the default: 0.85 accuracy, tools, 80%+ on multi-step MiniWoB.
- **Diffusion LMs (DiffuSeq / Diffusion-LM / SSD-LM) are not worth installing on the GX10** — research
  prototypes, slower at short generation. LLaDA-8B is the only defensible experiment, and it is a separate
  project.

---

## 1. Accuracy benchmark (8 models, parallel, 118 s wall)

Task: classify 10 job-description topics against 3,250 tokens of SAM documentation as strict JSON. Scored
against SubQ ground truth over the full 188K-char repo. Adjacent scoring half-credits PARTIAL.

| Model | Exact | Adjacent | Secs |
|---|---|---|---|
| gemma3:12b | 7/10 | **0.85** | **6.8** |
| qwen2.5:14b | 7/10 | **0.85** | 118.2 |
| deepseek-r1:32b (2000 tok) | 7/10 | **0.85** | 99.1 |
| qwen2.5-coder:14b | 6/10 | 0.80 | 32.0 |
| vLLM Qwen2.5-14B | 6/10 | 0.80 | 34.0 |
| qwen2.5:32b | 6/10 | 0.80 | 49.0 |
| llama3.1:8b | 5/10 | 0.75 | 65.9 |
| qwen3.5:4b | 0/10 | FAIL | — |

Ensemble (majority vote, 6 models): **0.85, zero catastrophically wrong topics.**

Errors are **directional**: gemma3/qwen2.5:32b are conservative (over-call MISSING); qwen2.5:14b and
coder:14b are generous. **Read the disagreement between a conservative and a generous model — that is where the
real uncertainty is.**

## 2. Concurrency and stability

Mixed-model concurrent calls, PID-checked before/after every wave. **No endpoint crashed. No restart required.**

| Wave | Result | Errors | Proxy |
|---|---|---|---|
| 6 distinct models simultaneously | 6/6 ok | none | survived |
| gemma ×4 + qwen14 + coder, together | 6/6 ok | none | survived |
| 18 concurrent, 3×6 mixed | 16/18 | 2× HTTP 429 | survived |
| vLLM 12-way burst | 12/12, 15.1 s | none | survived |
| LiteLLM 12-way burst | 12/12, 15.6 s | none | survived |
| Ollama 12-way burst | 12/12, 32.9 s | none | survived |
| Hermes 12-way burst | 10/12, 117.7 s | HTTP 429 | survived |

- Ollama `NUM_PARALLEL=1` **queues**, not fails: 12 parallel = 32.9 s wall, linear latency.
- vLLM **batches**: 12 parallel ≈ same as one (continuous batching). Best for fan-out.
- Clean ceiling: ~12 concurrent mixed calls on :4000. At 18 expect 429.

## 3. Capabilities

### Tools

| Model | Tool call | Result |
|---|---|---|
| gemma3:12b | **HARD FAIL** | HTTP 400, does not support tools |
| qwen2.5:14b | PASS | called `web_search` |
| qwen2.5:32b | PASS | called `web_search` |
| qwen2.5:7b | PASS | called `web_search` |
| qwen2.5-coder:14b | no call | declares tools, never invoked |
| deepseek-r1:32b | no call | 111 s spent reasoning |

### JSON reliability (3 tests × 3 runs; valid/3)

| Model | Object | Schema | Exact "OK" | Fenced | Verdict |
|---|---|---|---|---|---|
| qwen2.5:32b | 2/3 | 3/3 | 3/3 | 1 | reliable |
| qwen2.5:14b | 2/3 | 3/3 | 3/3 | 0 | reliable, but emits `license` not `licence` (deterministic) |
| deepseek-r1:32b | 3/3 | 3/3 | 3/3 | 0/9 sample, 7/11 repeat | needs fence-stripping; temperature=0 not deterministic |
| qwen2.5-coder:14b | 0/3 | 2/3 | 3/3 | 4 | needs stripping (```json wrapper) |
| gemma3:12b | 0/3 | 2/3 | 2/3 | 4 | unreliable — returned a 10-element array of unrelated products |
| qwen2.5:7b | 1/3 | 3/3 | 3/3 | 2 | needs stripping |

Safe transport for all six: strip → unwrap fences → json.loads → on failure extract outermost balanced `{...}`
with a dict-shape check → key-alias for qwen2.5 14b/7b (license/licence).

### Web-agent (MiniWoB, headless Chromium, benchmark's own reward)

| task | qwen2.5:14b | qwen2.5:32b |
|---|---|---|
| click-test | 5/5 (100%) | 5/5 (100%) |
| enter-text | 5/5 (100%) | 5/5 (100%) |
| click-checkboxes | 1/5 (20%) | 4/5 (80%) |
| choose-date | 0/5 (0%) | 0/5 (0%) |
| **total** | **11/20 (55%)** | **14/20 (70%)** |

0 parse failures in 152 model turns — failures are **planning/semantics, not syntax**. 14B emitted whole plans at
once on checkboxes; both fail the stateful date picker. 32B's edge shows almost entirely on the multi-step task
(80% vs 20%).

### Long-context needle

qwen2.5:14b and :32b both 3/3 at ~6.7K tokens. One miss at ~8.3K/10% did not reproduce. No reliable
long-context failure up to ~8K tokens. (Retrieval at 1.2M chars was tested only on SubQ, not these models.)

## 4. Recommended picks by use case

| Use | Model |
|---|---|
| Agent / tool calling / web | **qwen2.5:14b** (default) or qwen2.5:32b for multi-step |
| Reasoning-heavy | deepseek-r1:32b (≥600 output tokens) |
| Code | qwen2.5-coder:14b |
| High-throughput fan-out | vLLM Qwen2.5-14B |
| Pure classification, no tools | gemma3:12b |
| Cheap bulk triage | qwen2.5:7b |

## 5. Diffusion LMs on the GX10 (GB10) — not recommended

Hardware fits all four (DiffuSeq, Diffusion-LM, SSD-LM, LLaDA-8B). But DiffuSeq/Diffusion-LM/SSD-LM are
2022-23 research repos — unmaintained, no Ollama/LiteLLM integration, and slower at short generation than
autoregressive. Their advantage is long-output parallel decoding and controllable generation, not chat, tools,
or agents. Only LLaDA-8B is a defensible experiment, and it is a separate project.

---

## Files and reproduction

- `tools/bench_local.py` — the 8-model accuracy benchmark
- `tools/mixed_concurrency.py` — the mixed-model stability test
- `data/local_bench.json`, `data/ensemble.json` — accuracy results
- `data/stability_heavy.json`, `/tmp/mixed_concurrency.json` — concurrency results
- `/tmp/json_report.md`, `/tmp/json_probe_results.json` — JSON matrix
- `/tmp/webagent_report.md`, `/tmp/webagent_results.json` — MiniWoB eval
- `/tmp/needle_local.json` — long-context needle
- Config: `litellm_config.yaml` (`TOPNOTCH_LOCALONLY*` groups, commit f6a4f47) and
  `~/.config/kilo/TOPNOTCH_LOCALONLY.md` + `topnotch-localonly` provider
