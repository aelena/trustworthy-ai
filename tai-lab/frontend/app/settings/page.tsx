import { SettingsForm } from "@/components/settings-form";

export default function Page() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Settings</h1>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        BYOK provider configuration. Anthropic gets prompt caching applied for the BoK system prompt; other providers do not. See{" "}
        <code>docs/prompt-caching.md</code> for the cost implications.
      </p>
      <SettingsForm />
    </div>
  );
}
