"use client";

import type { ProviderConfig } from "./api";

const KEY = "tai-lab.provider";

export const defaultProvider: ProviderConfig = {
  profile: "anthropic",
  model: "claude-haiku-4-5",
  api_key: "",
  api_base: null,
  privacy_mode: false,
};

export function loadProvider(): ProviderConfig {
  if (typeof window === "undefined") return defaultProvider;
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return defaultProvider;
    return { ...defaultProvider, ...JSON.parse(raw) };
  } catch {
    return defaultProvider;
  }
}

export function saveProvider(cfg: ProviderConfig): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, JSON.stringify(cfg));
}
