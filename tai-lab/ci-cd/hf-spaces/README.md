# Hugging Face Spaces — Backend

We deploy the FastAPI backend as a **Docker SDK Space**. HF Spaces serves Docker containers on port 7860 by default; the backend `Dockerfile` honours that.

## Why this layout

- The Dockerfile lives in `tai-lab/backend/Dockerfile` but is built from the **project root** as context — it needs to `COPY` the BoK markdown (`README.md`, `pages/`, `code/`) alongside the backend source.
- The CI workflow (`deploy-backend.yml`) prepares a flat directory in CI, then pushes it to the Space's git repo. HF Spaces then performs its own build.

## Manual first-time setup

You only do this once. Steps live in the gitignored `deployment-guide.md` at the project root:

1. Create an HF account if needed
2. Create a new **Docker** Space
3. Generate a write-scoped token
4. Add `HF_TOKEN`, `HF_USERNAME`, `HF_SPACE_NAME` to GitHub Actions secrets

Subsequent deploys are automatic on push to `main`.

## Space-side environment variables

Set these in the Space **Settings → Variables and secrets**:

- `BOK_ROOT=/app/bok`
- `CORS_ORIGINS` — your Vercel frontend URL, e.g. `https://tai-lab.vercel.app`
- `MAX_OUTPUT_TOKENS=2048`
- `ANTHROPIC_CACHE_TTL=5m`

Do **not** set `ANTHROPIC_API_KEY` here — keys come from the user per-request via the BYOK flow.
