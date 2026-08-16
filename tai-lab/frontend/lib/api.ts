export type ProviderProfile = "anthropic" | "openai" | "ollama" | "openai_compat";

export interface ProviderConfig {
  profile: ProviderProfile;
  model: string;
  api_key?: string | null;
  api_base?: string | null;
  privacy_mode: boolean;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  content: string;
  cache_read_tokens: number | null;
  cache_write_tokens: number | null;
  input_tokens: number | null;
  output_tokens: number | null;
}

export interface EvalRun {
  run_id: string;
  kind: string;
  model_ref: string;
  status: "queued" | "running" | "completed" | "failed";
  started_at: number;
  finished_at: number | null;
  summary: Record<string, unknown> | null;
  error: string | null;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  chat: (messages: Message[], provider: ProviderConfig, useBokCache = true) =>
    jsonFetch<ChatResponse>("/chat", {
      method: "POST",
      body: JSON.stringify({ messages, provider, use_bok_cache: useBokCache }),
    }),
  listEvals: () => jsonFetch<EvalRun[]>("/evals"),
  startEval: (kind: string, modelRef: string, datasetRef?: string) =>
    jsonFetch<EvalRun>("/evals", {
      method: "POST",
      body: JSON.stringify({ kind, model_ref: modelRef, dataset_ref: datasetRef ?? null }),
    }),
  getEval: (runId: string) => jsonFetch<EvalRun>(`/evals/${runId}`),
  searchKnowledge: (q: string) =>
    jsonFetch<{ query: string; hits: { path: string; title: string; excerpt: string }[] }>(
      `/knowledge/search?q=${encodeURIComponent(q)}`,
    ),
};
