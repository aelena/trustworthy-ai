import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "tai-lab",
  description: "Trustworthy AI evaluation lab",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b border-zinc-200 dark:border-zinc-800">
          <nav className="mx-auto flex max-w-5xl items-center gap-6 px-6 py-4">
            <Link href="/" className="font-semibold">tai-lab</Link>
            <Link href="/" className="text-sm text-zinc-600 hover:underline dark:text-zinc-300">Chat</Link>
            <Link href="/evals" className="text-sm text-zinc-600 hover:underline dark:text-zinc-300">Evals</Link>
            <Link href="/settings" className="ml-auto text-sm text-zinc-600 hover:underline dark:text-zinc-300">Settings</Link>
          </nav>
        </header>
        <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
