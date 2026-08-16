"use client";

import { useEffect, useState } from "react";
import { api, type EvalRun } from "@/lib/api";

const KINDS = [
  { value: "bias", label: "Bias Testing (AIF360 / Fairlearn)" },
  { value: "explainability", label: "Explainability (SHAP / LIME)" },
  { value: "adversarial", label: "Adversarial (ART / PyRIT)" },
  { value: "eval_frameworks", label: "Eval Frameworks (Inspect AI)" },
  { value: "differential_privacy", label: "Differential Privacy (Opacus)" },
];

export function EvalRunner() {
  const [kind, setKind] = useState("bias");
  const [modelRef, setModelRef] = useState("synthetic-credit-model");
  const [runs, setRuns] = useState<EvalRun[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      setRuns(await api.listEvals());
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 2000);
    return () => clearInterval(t);
  }, []);

  async function start() {
    setBusy(true);
    setError(null);
    try {
      await api.startEval(kind, modelRef);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="mb-3 font-medium">Start a run</h2>
        <div className="grid gap-3 sm:grid-cols-3">
          <select
            className="rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
            value={kind}
            onChange={(e) => setKind(e.target.value)}
          >
            {KINDS.map((k) => (
              <option key={k.value} value={k.value}>
                {k.label}
              </option>
            ))}
          </select>
          <input
            className="rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
            placeholder="model ref"
            value={modelRef}
            onChange={(e) => setModelRef(e.target.value)}
          />
          <button
            onClick={start}
            disabled={busy}
            className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-white disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
          >
            {busy ? "Starting…" : "Run"}
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      </div>

      <div>
        <h2 className="mb-3 font-medium">Recent runs</h2>
        <div className="space-y-2">
          {runs.length === 0 && <p className="text-sm text-zinc-500">No runs yet.</p>}
          {runs.map((r) => (
            <div
              key={r.run_id}
              className="rounded-md border border-zinc-200 p-3 text-sm dark:border-zinc-800"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs">{r.run_id}</span>
                <span
                  className={
                    r.status === "completed"
                      ? "text-green-600"
                      : r.status === "failed"
                        ? "text-red-600"
                        : "text-zinc-500"
                  }
                >
                  {r.status}
                </span>
              </div>
              <div className="mt-1 text-zinc-600 dark:text-zinc-400">
                {r.kind} · {r.model_ref}
              </div>
              {r.summary && (
                <pre className="mt-2 overflow-x-auto rounded bg-zinc-50 p-2 text-xs dark:bg-zinc-900">
{JSON.stringify(r.summary, null, 2)}
                </pre>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
