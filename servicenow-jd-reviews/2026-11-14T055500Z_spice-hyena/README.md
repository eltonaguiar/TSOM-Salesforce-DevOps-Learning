# Local-model benchmark + two JD reviews

Two questions answered here:

1. **Can the free local models do decently large work?** — yes, at 13–14B, with a known bias.
2. **How do our docs measure against the two job descriptions?** — SAM and ServiceNow dev/retail.

| File | Contents |
|---|---|
| `README.md` | benchmark method, results, verdict |
| `01_sam_vs_bmo_jd.md` | SAM repo vs the BMO SAM Administrator JD |
| `02_servicenow_docs_vs_topics.md` | the 31 guide pages vs your ServiceNow topic list |
| `tools/bench_local.py` | the parallel harness (vLLM + Ollama) |
| `data/` | raw results, ground truth, coverage matrices |

---

# 1. Local-model benchmark

## Setup

**Backends reachable:**

| Backend | Endpoint | Model | Context |
|---|---|---|---|
| vLLM | `localhost:8000` | `Qwen/Qwen2.5-14B-Instruct` | **8,192** (hard cap) |
| Ollama | `localhost:11434` | 27 models, incl. 4B–70B | 8K–131K |

**Task** — a real piece of work, not a toy: given 13,000 chars of SAM documentation (~3,250 tokens) and the
10 BMO job-description topics, classify each topic `COVERED` / `PARTIAL` / `MISSING` as strict JSON.

**Scoring** — against ground truth from SubQ over the **full 188K-char repo** (SubQ handles that; local models
cannot). Adjacent scoring gives half credit for `PARTIAL` vs either neighbour, since `PARTIAL` genuinely sits
between the two.

**Execution** — all 8 models fired **simultaneously** via `ThreadPoolExecutor`.

## Results

| Model | Backend | Exact | Adjacent | Answered | Secs | Out tokens |
|---|---|---|---|---|---|---|
| **gemma3:12b** | ollama | **7/10** | **0.85** | 10/10 | **6.8** | 131 |
| **qwen2.5:14b** | ollama | **7/10** | **0.85** | 10/10 | 118.2 | 105 |
| **deepseek-r1:32b** (2000 tok) | ollama | **7/10** | **0.85** | 10/10 | 99.1 | 566 |
| qwen2.5-coder:14b | ollama | 6/10 | 0.80 | 10/10 | 32.0 | 109 |
| Qwen2.5-14B-Instruct | **vllm** | 6/10 | 0.80 | 10/10 | 34.0 | 105 |
| qwen2.5:32b | ollama | 6/10 | 0.80 | 10/10 | 49.0 | 105 |
| llama3.1:8b | ollama | 5/10 | 0.75 | 10/10 | 65.9 | 105 |
| qwen3.5:4b | ollama | 0/10 | 0.00 | **0/10** | 76.4 | 1500 (all thinking) |

Wall clock for all 8 in parallel: **118 s**. Sequential would have been ~9 minutes.

**Ensemble (majority vote across 6 answering models): 7/10, 0.85** — ties the best single model, but with
**zero catastrophically wrong topics**. Every ensemble error was an adjacent miss.

## The failure modes are directional, not random

| Model | Error pattern | Bias |
|---|---|---|
| `gemma3:12b` | PARTIAL→MISSING ×3 | **conservative** |
| `qwen2.5:32b` | PARTIAL→MISSING ×4 | **conservative** |
| `llama3.1:8b` | PARTIAL→MISSING ×4 | **conservative** |
| `qwen2.5:14b` | MISSING→PARTIAL ×3 | **generous** |
| `qwen2.5-coder:14b` | all 6 PARTIALs correct, MISSING→PARTIAL ×4 | **generous but precise** |

That is usable information. A conservative model tells you "if it says COVERED, believe it." A generous model
tells you "if it says MISSING, believe it." `qwen2.5-coder:14b` is the most interesting: it got **every
PARTIAL right** and only over-called MISSING as PARTIAL — a single, correctable bias.

## Verdict

**Yes — 13–14B local models can do decently large work, and they can do it in parallel.**

- **0.85 adjacent accuracy** on a 10-topic audit over 3,250-token input.
- **6.8 s** for the best model (`gemma3:12b`), warm.
- Fully parallel — 8 models in 118 s.
- Costs nothing and leaves the machine.

**What does not work:**
- **4B is not usable.** `qwen3.5:4b` returned empty output at both 400 and 1,500 token budgets — it spent the
  entire budget on internal reasoning and emitted nothing. Not a tuning issue; a capability issue.
- **Thinking models need headroom.** `deepseek-r1:32b` scored 0/10 at 400 tokens and 0.85 at 2,000. If you run
  a reasoning model, budget ≥600 output tokens or you get an empty answer.
- **vLLM's 8,192 cap** rules out whole-document work there. Ollama's 131K-context models can take much more.

**Practical recipe:** run `gemma3:12b` + `qwen2.5-coder:14b` + one generous model in parallel, majority-vote,
and read the disagreements rather than the votes. That gives you the accuracy of the best model plus a
per-topic dissent signal that flags exactly the topics a human should check.

**What local models are not for:** establishing ground truth. They answer the question you gave them; they
cannot tell you whether the answer is right. That still needs a primary source or a much larger model —
which is why the ground truth here came from SubQ over the full repo, not from the locals.