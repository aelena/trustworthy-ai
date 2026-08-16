"use client";

import { useEffect, useState } from "react";
import type { ProviderConfig } from "@/lib/api";
import { defaultProvider, loadProvider, saveProvider } from "@/lib/storage";

export function SettingsForm() {
  const [cfg, setCfg] = useState<ProviderConfig>(defaultProvider);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setCfg(loadProvider());
  }, []);

  function update<K extends keyof ProviderConfig>(k: K, v: ProviderConfig[K]) {
    setCfg((c) => ({ ...c, [k]: v }));
    setSaved(false);
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    saveProvider(cfg);
    setSaved(true);
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium">Provider</label>
        <select
          value={cfg.profile}
          onChange={(e) => update("profile", e.target.value as ProviderConfig["profile"])}
          className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
        >
          <option value="anthropic">Anthropic (recommended for cached BoK)</option>
          <option value="openai">OpenAI</option>
          <option value="ollama">Ollama (local — privacy mode)</option>
          <option value="openai_compat">OpenAI-compatible (Groq, OpenRouter, …)</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium">Model</label>
        <input
          value={cfg.model}
          onChange={(e) => update("model", e.target.value)}
          placeholder="claude-haiku-4-5 / ollama/llama3.2 / gpt-4o-mini"
          className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
        />
      </div>

      {cfg.profile !== "ollama" && (
        <div>
          <label className="block text-sm font-medium">API key (BYOK)</label>
          <input
            type="password"
            value={cfg.api_key ?? ""}
            onChange={(e) => update("api_key", e.target.value)}
            placeholder="sk-…"
            className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          />
          <p className="mt-1 text-xs text-zinc-500">
            Stored only in your browser&apos;s localStorage. Sent per-request to the backend, never persisted server-side.
          </p>
        </div>
      )}

      {(cfg.profile === "ollama" || cfg.profile === "openai_compat") && (
        <div>
          <label className="block text-sm font-medium">API base</label>
          <input
            value={cfg.api_base ?? ""}
            onChange={(e) => update("api_base", e.target.value)}
            placeholder="http://localhost:11434"
            className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          />
        </div>
      )}

      <div className="flex items-center gap-2">
        <input
          id="privacy"
          type="checkbox"
          checked={cfg.privacy_mode}
          onChange={(e) => update("privacy_mode", e.target.checked)}
        />
        <label htmlFor="privacy" className="text-sm">
          Privacy mode — refuse any non-localhost provider call
        </label>
      </div>

      <button
        type="submit"
        className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900"
      >
        Save
      </button>
      {saved && <span className="ml-3 text-sm text-green-600">Saved.</span>}
    </form>
  );
}
