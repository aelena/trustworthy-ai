# tai-lab frontend

Next.js 15 (App Router) + React 19 + Tailwind. Pure client-side persistence for BYOK keys (browser localStorage). The backend is the source of truth for chat orchestration, knowledge lookup, and eval execution.

## Local run

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000.

## Pages

- `/` — Chat with the BoK-grounded assistant
- `/evals` — Start eval runs and inspect history
- `/settings` — Provider profile (Anthropic / OpenAI / Ollama / OpenAI-compatible) + BYOK + privacy mode

## API client

`lib/api.ts` is the only place that talks to the backend. Use it from components.
