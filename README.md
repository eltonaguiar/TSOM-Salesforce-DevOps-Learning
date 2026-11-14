# TSOM-Salesforce-DevOps-Learning

Learning resources and training items for the **Salesforce DevOps Engineer** role at Toronto School of Management (TSOM) / Scotiabank.
---

## Findings summary (2026-11-14)

This repo also hosts the verified findings of a local-model capability study (the GX10/GB10 machine) and the
cross-referenced ServiceNow + Salesforce documentation reviews. Full write-ups:
[LOCAL_MODEL_FINDINGS.md](LOCAL_MODEL_FINDINGS.md), [servicenow-jd-reviews/](servicenow-jd-reviews/),
[guide-merge/](guide-merge/).

### TL;DR

Local models are genuinely useful for real work. A 10-topic classification scored 0.80–0.85.
The LiteLLM proxy survives concurrent mixed-model calls — 6 distinct models at once, 6/6, no restart.
But the best classifier (`gemma3:12b`) cannot call tools; use `qwen2.5:14b` or `:32b` for agentic work.
On MiniWoB browser tasks, `qwen2.5:14b` got 55%, `:32b` 70% — real task completion, 0 action-parse failures.
Diffusion LMs (DiffuSeq / Diffusion-LM / SSD-LM) are not recommended on this box: research code, slower for
short generation.

### ELI5

Think of the local AI models like a small team on your own computer. Some are great at reading a page and
sorting facts (gemma3) but cannot press buttons or search the web. Others (qwen2.5) can both reason and act, so
they are the ones you send to actually *do* a task in a browser. We tested all of them at once on the same job:
they agreed with the "correct answer" about 80–85% of the time. We also hammered the server with many models at
once — it stayed up, just got a bit slower. The fancy "diffusion" text models everyone is talking about are not
ready to help here yet, so we did not install them.

### Overall conclusion

Use **`qwen2.5:14b`** as the default local model (accuracy + tools + 100% on simple browser tasks), elevate to
**`qwen2.5:32b`** for multi-step work (80% on checkbox tasks), use **`deepseek-r1:32b`** for reasoning with a
≥600-token budget, and keep **`gemma3:12b`** only for classification where no tool is needed. Run fan-out
through the **LiteLLM proxy on :4000** (deliberate local-only groups `TOPNOTCH_LOCALONLY*`), cap concurrent
mixed calls at ~12, and strip JSON fences for `coder/deepseek/7b`. Everything above is measured; the raw data
and harnesses are in the repo.
