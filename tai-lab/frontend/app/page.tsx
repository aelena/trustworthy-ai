import { Chat } from "@/components/chat";

export default function Page() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Chat</h1>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Grounded in the Trustworthy AI Body of Knowledge. Configure your provider in{" "}
        <a className="underline" href="/settings">Settings</a>.
      </p>
      <Chat />
    </div>
  );
}
