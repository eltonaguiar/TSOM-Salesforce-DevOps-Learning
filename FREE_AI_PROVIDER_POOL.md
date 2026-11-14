# Free AI provider pool — verified shortlist

Source: the 7 repos from the DEV article, checked by four parallel research agents on 2026-11-14.
These are **discovery** yields — each still needs a quick smoke-test before you rely on it.

---

## The 7 repos and what they're for

| Repo | Type | Practical value |
|---|---|---|
| `mnfst/awesome-free-llm-apis` | permanent free tiers | best single source for always-free API keys |
| `cheahjs/free-llm-api-resources` | free + trial | wider net (repo deleted; `tiennm99` fork read) |
| `CYBIRD-D/FREE-LLM-API-Provider` | provider directory | cross-check; includes CN platforms, rate limits |
| `Alishahryar1/free-claude-code` | Claude Code proxy | operational (not curation) |
| `zebbern/no-cost-ai` | broad no-cost | chat/image/video/voice + keyless APIs |
| `eudk/awesome-ai-tools` | very large directory | wide discovery, mostly paid/enterprise |
| `ShaikhWarsi/free-ai-tools` | whole-stack | best builder-focused list |

---

## Best NEW signups (permanent free, no card)

| Provider | Models | Free limit | OpenAI-compatible | Note |
|---|---|---|---|---|
| **Google AI Studio (Gemini)** | Gemini 3.8/3.6/3.5/3.1 Flash, Flash-Lite, Gemma 4 | Flash-Lite ~500 req/day/15rpm; Flash 20 req/day; **Gemma 4 30rpm/14.4k RPD** | yes (OpenAI-compat endpoint) | most reliable free tier |
| **NVIDIA NIM** | Nemotron 3 Ultra 550B, GPT-OSS-120b, Llama, 100+ | ~40 rpm per model | yes `integrate.api.nvidia.com/v1` | phone verify; eval/NDA only |
| **Cloudflare Workers AI** | GPT-OSS-120b, Llama, GLM-4.7, Qwen, DeepSeek | 10,000 neurons/day | yes | some top models require billing method anyway |
| **Mistral La Plateforme** | Large 3, Small 3.1, Nemo | ~1 rps, up to 1B tokens/mo | yes `api.mistral.ai/v1` | data-training opt-in + phone verify |
| **SambaNova** | DeepSeek-V3.1/3.2, Llama 3.3 70B, gpt-oss-120b | 20 RPM but **20 req/day** | yes | tiny daily cap |
| **Aion Labs** | Aion 2/3/3.5, RPa-Llama-8B | 15 rpm, 20K tok/day | yes | small, third-party fine-tunes |
| **GitHub Models** | GPT-OSS, Llama, Mistral | tier-dependent | yes | **one agent reports retired 2026-07-30; verify** |

## Keyless (no key at all — usable in code)

| Provider | Offers | Limits | Compat |
|---|---|---|---|
| **Pollinations.ai** `pollinations.ai` | openai, gemini-2.5-flash-lite, mistral, qwen-coder, deepseek + image/audio | "unlimited" (community-shared, throttles) | partial (OpenAI-style) |
| **LLM7.io** `api.llm7.io/v1` | GPT-OSS-20b, Mistral-Nemo, Codestral | 60 rpm, 250 req/hr, 100K tok/24h | yes |
| **Kilo Gateway** `api.kilo.ai/api/gateway` | Nemotron, north-mini-code, openrouter/free | 200 req/hr per IP | yes |
| **OVHcloud AI Endpoints** (already have) | Qwen3.6-27B, Llama-70B, gpt-oss-120b | 2 rpm/IP | yes |
| **Index-Translate** | translation 150+ langs | ~30 rpm | translation only |

## Trial-only (expiring — not "permanent free")

Baseten $30 · Nebius $1 · Novita $0.50 · AI21 $10/3mo · Upstage $10/3mo · NLP Cloud $15 · Alibaba Studio 1M tokens/90d · SambaNova $5/3mo · Hyperbolic $1 · DeepInfra $1.80 · Scaleway 1M tokens · Mistral/Cohere trial.

## What we already have (verified this session) — excluded

Groq (free, 1,000 req/window) · OpenRouter (keyed) · OVH (keyless) · **Cerebras (no free — $5/account)** · **Fireworks (suspended)** · Ollama local · Z.ai (rate-limits immediately, one-shot fallback only).

## Coding agents/CLIs that route through our LiteLLM :4000

**OpenCode** (standout, BYOK → LiteLLM/OpenRouter/local) · **Roo Code** · **Goose** · **Aider** · **OpenClaw** · ForgeCode (10K tok/day via OpenRouter) · Gemini CLI (1,500 req/day).

**Free Claude Code (FCC) — verdict: skip.** It's a redundant second translation layer next to our LiteLLM proxy, adds a heavy desktop app, carries Anthropic ToS risk, and would run on ARM64 but the benefit is marginal (full assessment in agent report).

## Top recommended wiring (if you want to expand the pool)

1. **NVIDIA NIM** — one signup, 40 rpm, huge catalog, OpenAI-compatible.
2. **Google AI Studio** — best steady quota (Gemma 4 at 30rpm).
3. **Cloudflare Workers AI** — 10K neurons/day durable fallback.
4. **Pollinations.ai** — the one keyless endpoint worth real use.
5. **Mistral La Plateforme** — high monthly token allowance.

## Caution

- Directory claims churn fast: since mid-2026 — Ollama cloud went pay-as-you-go, GitHub Models possibly retired, Together lost free tier, iFlow died, Cerebras went paid, Vercel became trial-only.
- **Don't build production on any of these.** They're for experimentation/low-volume. Smoke-test each endpoint before relying on it (same discipline we applied to Groq/OpenRouter/OVH).
