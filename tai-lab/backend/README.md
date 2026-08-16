# tai-lab backend

FastAPI service that powers the Trustworthy AI evaluation lab.

## Routes

| Method | Path | Purpose |
|---|---|---|
| GET  | `/healthz` | Liveness |
| GET  | `/readyz` | BoK load status + token estimate |
| POST | `/chat` | Chat with the BoK-grounded assistant |
| GET  | `/knowledge/search?q=…` | Grep the BoK |
| GET  | `/knowledge/files` | List all BoK files |
| POST | `/evals` | Start an eval run (subprocess against `code/*.py`) |
| GET  | `/evals` | List runs |
| GET  | `/evals/{run_id}` | Get run status & summary |

## Local run

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for the auto-generated OpenAPI explorer.

## Provider config

The backend is provider-agnostic via [LiteLLM](https://github.com/BerriAI/litellm). Per-request, the frontend sends a `ProviderConfig`:

- `profile`: `"anthropic" | "openai" | "ollama" | "openai_compat"`
- `model`: LiteLLM-style model id
- `api_key`: BYOK — never persisted server-side
- `api_base`: required for Ollama / OpenAI-compatible endpoints
- `privacy_mode`: when true, the backend rejects any non-local provider call

Only the `anthropic` profile gets prompt caching applied. See `../docs/prompt-caching.md`.

## Tests

```bash
pytest
```

The smoke test loads the BoK from the repo root (`../`) and asserts a non-empty index.
