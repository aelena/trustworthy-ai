import { EvalRunner } from "@/components/eval-runner";

export default function Page() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Evaluations</h1>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Run canonical Trustworthy AI test suites (bias, explainability, adversarial, framework, privacy).
        v1 executes the scripts in the repo&apos;s <code>code/</code> folder against bundled examples.
      </p>
      <EvalRunner />
    </div>
  );
}
