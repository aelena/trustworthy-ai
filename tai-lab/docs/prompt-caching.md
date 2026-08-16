# Prompt caching, BYOK economics, and when to opt out

This doc covers exactly **how the Body of Knowledge gets cheaply attached to every chat turn**, and what changes when the user picks a non-Anthropic provider.

---

## 1. The mechanic

Anthropic prompt caching gives a **90% discount on the cached portion** of an input prompt for a limited time after a successful "cache write." The mechanic, in the form tai-lab uses it:

1. The backend builds a system prompt with two blocks:
   - A short instruction header
   - The full BoK markdown (~50–80K tokens), marked with `cache_control: {"type": "ephemeral", "ttl": "5m"}`
2. The first request after a cold start (or after the TTL expires) is a **cache write** — Anthropic charges 1.25× base input for the BoK block.
3. Every subsequent request within the TTL is a **cache read** — Anthropic charges 0.1× base input for the BoK block. Your live user message and the assistant's output are billed at full normal rates.

The cached prefix must be **byte-identical** across calls. Any change (a per-user name, the current date, a config flag) invalidates the cache and triggers a fresh write. Keep dynamic data strictly *after* the cached prefix.

## 2. Concrete numbers

BoK ≈ 60K tokens. Haiku 4.5 input is ~$1/M tokens.

| | Per BoK-attached call |
|---|---|
| Uncached input (no caching) | 60K × $1/M = **$0.060** |
| Cache **write** (5m TTL) | 60K × $1.25/M = **$0.075** |
| Cache **read** (subsequent calls) | 60K × $0.10/M = **$0.006** |

A red-teaming session firing 500 prompts in 10 minutes:

- Uncached: ~**$30** in BoK costs alone
- Cached: 2 writes + 498 reads ≈ **$3.10**

A roughly **10× saving**, not a free lunch. Output tokens and the live user message are unaffected — they're outside the cached prefix.

## 3. The TTL trade-off

Anthropic offers two TTL flavours. The choice is governed by the env var `ANTHROPIC_CACHE_TTL` on the backend:

| TTL | Write multiplier | Read multiplier | Best for |
|---|---|---|---|
| `5m` (default) | 1.25× | 0.10× | Bursty interactive use — chat sessions, eval runs that finish in a few minutes |
| `1h` | 2× | 0.10× | Long-running batch jobs, sparse polling, multi-stage workflows that span ~30 min |

**Rule of thumb**: if your call cadence is faster than once every ~3 minutes, `5m` wins. If you make occasional calls spaced 10–45 minutes apart, `1h` amortises better. If your call pattern is slower than ~1/hour, **don't enable caching** — write fees dominate.

## 4. When the BYOK user picks a non-Anthropic provider

tai-lab uses LiteLLM as a provider abstraction. Every provider is callable, but **caching economics are not portable**.

| Provider | Caching behaviour | What this means for the BoK |
|---|---|---|
| **Anthropic** | Explicit `cache_control` blocks, 5m or 1h TTL, 90% read discount | Full benefit. tai-lab applies caching automatically. |
| **OpenAI** | Automatic prefix caching (no API knob). 50% discount on cached input. Smaller cache, no SLA on hit rate. | Best-effort. Your OpenAI bill will be roughly 2× an Anthropic-cached run for the same workload, but still cheaper than uncached. tai-lab does not set `cache_control` for OpenAI — the platform handles it transparently. |
| **Groq, Together, OpenRouter, etc.** (OpenAI-compatible) | Varies by upstream. Most do not currently expose caching. | Pay full input price every call. Cheap models per-token, but no BoK discount. |
| **Ollama (local)** | No caching whatsoever. Your local GPU/CPU does the work. | "Cost" is your machine's electricity. Latency is the bottleneck, not API spend. |

The Settings UI labels Anthropic as "recommended for cached BoK" so users picking a different provider understand why their bill differs.

## 5. When to opt out of caching

Even on Anthropic, caching is the wrong choice in three scenarios:

1. **One-shot calls.** A single isolated query pays a 1.25× write fee with no subsequent reads to amortise it. Net effect: 25% *more* expensive than no caching.
2. **Sparse usage** (calls > TTL apart). Same reasoning — every call is a fresh write.
3. **Frequently-changing system prompt.** If you splice user-specific or time-specific data into the cached prefix, the cache invalidates on every request.

Set `use_bok_cache: false` on the `/chat` request body to bypass caching for a single call. The backend will fall back to a flat string system prompt.

## 6. When to leave Anthropic entirely

| Reason | Better destination |
|---|---|
| Privacy / data residency | Ollama (privacy mode). Zero external calls. |
| Per-token cost (low BoK use) | OpenAI's `gpt-4o-mini` or Groq's free tier of Llama 3.x |
| Higher RPM at low cost | Groq, Together |
| Specific model capabilities | Whichever provider hosts that model |

In all cases, set the provider in Settings; the backend automatically stops applying `cache_control` blocks and routes through LiteLLM.

## 7. What the backend reports back

Every `/chat` response body includes:

```json
{
  "input_tokens": 280,
  "output_tokens": 412,
  "cache_read_tokens": 60123,
  "cache_write_tokens": 0
}
```

A healthy cached session looks like: `cache_write_tokens=0` after the first call, `cache_read_tokens` close to your BoK token estimate. If you see `cache_read_tokens=0` on an Anthropic call after the first request, the cache was invalidated — usually because something dynamic snuck into the prefix. Inspect the system prompt builder in `backend/app/services/llm.py`.

## 8. Mental model

Think of caching as a paid bet: you stake 25% extra on the first call to win 90% off on the next ones. The bet pays out when you make ≥ 2 calls within the TTL. For the chat-with-BoK and red-teaming workloads tai-lab is built for, that bet wins in nearly every realistic session — but only on Anthropic.
