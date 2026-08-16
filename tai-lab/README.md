# tai-lab

A proof-of-concept tool for **Trustworthy AI model evaluation** built on top of the Trustworthy AI Body of Knowledge in the parent repo.

Two surfaces:

1. **Chat** — a BoK-grounded assistant that answers auditor-style questions, citing the markdown pages it draws from.
2. **Evals** — a runner that executes the canonical Python tests under `../code/` (bias, explainability, adversarial, eval frameworks, differential privacy) against a chosen model.

## Architecture

```
Next.js (Vercel free)              FastAPI (HF Spaces Docker, free)
  Chat / Evals / Settings   ────►    /chat  → LiteLLM ──► Anthropic / OpenAI / Ollama
                                     /evals → subprocess → ../code/*.py
                                     /knowledge → grep over ../pages/*.md
```

- **Provider abstraction** via [LiteLLM](https://github.com/BerriAI/litellm). One backend, many providers (Anthropic, OpenAI, Ollama, any OpenAI-compatible endpoint).
- **BYOK**: API keys live in browser `localStorage` and are forwarded per-request. Never persisted server-side.
- **Privacy mode**: a hard switch that refuses any non-localhost provider call — used with Ollama for fully local operation.
- **Cached BoK**: on Anthropic, the entire BoK is sent as a `cache_control`-marked system prompt, paying ~10% of base input rates after the first call. See [docs/prompt-caching.md](./docs/prompt-caching.md).
- **No vector DB**. The BoK is small enough (~50–80K tokens) to fit comfortably as cached context. RAG is deferred until paper-PDF ingestion lands.

## Layout

```
tai-lab/
├── backend/            FastAPI app (LiteLLM, BoK loader, eval runner)
│   ├── app/
│   ├── tests/
│   └── Dockerfile      Used by HF Spaces (port 7860)
├── frontend/           Next.js 15 + Tailwind
│   ├── app/
│   ├── components/
│   └── lib/
├── ci-cd/
│   ├── vercel/         Frontend deploy via GitHub Actions
│   └── hf-spaces/      Backend deploy via GitHub Actions
└── docs/
    └── prompt-caching.md
```

## Quick start (local, no deploy)

```bash
# Backend
cd tai-lab/backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd tai-lab/frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000, configure your provider in **Settings**, and start chatting.

### Privacy-mode quick start (no external API calls)

```bash
ollama pull llama3.2
ollama serve
```

In **Settings**: profile `ollama`, model `llama3.2`, api_base `http://localhost:11434`, privacy mode **on**.

## What v1 does

- BoK-grounded chat with citations (Anthropic with caching; OpenAI / Ollama / OpenAI-compatible without)
- BYOK provider profiles persisted in browser `localStorage`
- Privacy mode that refuses any non-localhost provider call
- Knowledge search endpoint (`/knowledge/search`) — grep over the BoK
- Eval runner that subprocess-executes the five canonical scripts in `../code/`
- Run history with status / stdout tail / stderr tail

## What v1 deliberately does NOT do (deferred)

| Feature | Why deferred |
|---|---|
| Sandboxed user-code execution (e2b/Modal) | PoC trusts only the canonical scripts; no user-uploaded model code yet |
| Real PDF report generation | Markdown summaries are enough for the demo |
| Paper-PDF ingestion + RAG | The BoK alone fits in cached context; defer until corpus > context window |
| Model registry UI | Hardcoded zoo of 3–5 examples is enough |
| Auth & multi-user persistence | Single-user demo; SQLite + browser localStorage suffice |

## Cost ceiling

With Anthropic Haiku 4.5 + cached BoK and the deferred items above, expect **under ~$15/month** of casual usage. Set a hard spend cap in the Anthropic console as the real safety net. See [docs/prompt-caching.md](./docs/prompt-caching.md) for the per-provider economics and when to opt out of caching.

## Considerations

- **HF Spaces sleeps after inactivity.** First request after a quiet period takes ~30s to wake. Fine for a demo, not for production.
- **Prompt caching is Anthropic-specific.** Switching to OpenAI, Ollama, or any other LiteLLM-supported backend will pay full input price every call. The frontend surfaces this in Settings.
- **Privacy mode breaks caching.** Ollama has no caching of any kind, and external calls are refused. That's the intended trade-off.
- **The backend treats the canonical scripts as trusted code.** Do not extend the eval runner to execute user-uploaded Python without first introducing real sandboxing — see `design-specs.md` for the v2 plan.

## See also

- Parent repo — `../README.md` (the BoK itself)
- Caching guide — [`docs/prompt-caching.md`](./docs/prompt-caching.md)
- CI/CD — [`ci-cd/README.md`](./ci-cd/README.md)
