"use client";

import { useState } from "react";
import { api, type ChatResponse, type Message } from "@/lib/api";
import { loadProvider } from "@/lib/storage";

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [usage, setUsage] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function send() {
    if (!input.trim() || busy) return;
    const next: Message[] = [...messages, { role: "user", content: input.trim() }];
    setMessages(next);
    setInput("");
    setBusy(true);
    setError(null);
    try {
      const provider = loadProvider();
      const res = await api.chat(next, provider);
      setMessages([...next, { role: "assistant", content: res.content }]);
      setUsage(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        {messages.length === 0 && (
          <p className="text-sm text-zinc-500">
            Ask anything grounded in the Trustworthy AI Body of Knowledge.
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : ""}>
            <div
              className={
                m.role === "user"
                  ? "inline-block max-w-[85%] rounded-lg bg-zinc-900 px-3 py-2 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900"
                  : "inline-block max-w-[85%] whitespace-pre-wrap rounded-lg bg-zinc-100 px-3 py-2 text-sm dark:bg-zinc-800"
              }
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          placeholder="What does demographic parity mean?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
          disabled={busy}
        />
        <button
          onClick={send}
          disabled={busy || !input.trim()}
          className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-white disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {busy ? "…" : "Send"}
        </button>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}
      {usage && (
        <p className="text-xs text-zinc-500">
          tokens — input: {usage.input_tokens ?? "?"} · output: {usage.output_tokens ?? "?"} · cache read: {usage.cache_read_tokens ?? 0} · cache write: {usage.cache_write_tokens ?? 0}
        </p>
      )}
    </div>
  );
}
