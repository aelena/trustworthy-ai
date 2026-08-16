# CI/CD

Two pipelines, one per deploy target.

| Target | What it deploys | Free tier home | Workflow file |
|---|---|---|---|
| Vercel | Next.js frontend | vercel.com | `.github/workflows/deploy-frontend.yml` |
| Hugging Face Spaces | FastAPI backend (Docker) | huggingface.co/spaces | `.github/workflows/deploy-backend.yml` |

The workflow YAMLs live at `.github/workflows/` (where GitHub Actions reads them). Provider-specific config that *isn't* a workflow lives here under `ci-cd/`:

- `vercel/vercel.json` — Next.js project config consumed by the Vercel CLI
- `hf-spaces/README.md` — notes on the Space-side environment

Each workflow runs on push to `main` for paths in its scope, plus a manual `workflow_dispatch` trigger.

## Required GitHub Actions secrets

Configure under **Settings → Secrets and variables → Actions**:

| Secret | Used by | Notes |
|---|---|---|
| `VERCEL_TOKEN` | Vercel | Personal token from vercel.com/account/tokens |
| `VERCEL_ORG_ID` | Vercel | From `.vercel/project.json` after first local link |
| `VERCEL_PROJECT_ID` | Vercel | Same |
| `HF_TOKEN` | HF Spaces | Write-scoped HF access token from huggingface.co/settings/tokens |
| `HF_USERNAME` | HF Spaces | Your HF username |
| `HF_SPACE_NAME` | HF Spaces | The Space repo name (e.g. `tai-lab-backend`) |

The full step-by-step is in the gitignored `deployment-guide.md` at the project root — that's your private setup walkthrough. This README is the public surface.

## Local validation before pushing

```bash
# Frontend
cd frontend && npm run build

# Backend
cd backend && pytest && docker build -f Dockerfile -t tai-lab-backend ../
```

The backend Dockerfile is run from the **project root** as build context so it can `COPY` the BoK markdown alongside the backend code.
