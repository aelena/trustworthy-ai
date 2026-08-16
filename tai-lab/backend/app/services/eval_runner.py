import asyncio
import time
import uuid
from pathlib import Path

from app.config import settings
from app.schemas.evals import EvalKind, EvalRun

_RUNS: dict[str, EvalRun] = {}

# Map eval kind -> path to the canonical script in the trustworthy-ai/code dir.
_SCRIPT_MAP: dict[EvalKind, str] = {
    "bias": "bias_testing.py",
    "explainability": "explainability.py",
    "adversarial": "adversarial_testing.py",
    "eval_frameworks": "eval_frameworks.py",
    "differential_privacy": "differential_privacy.py",
}


def list_runs() -> list[EvalRun]:
    return sorted(_RUNS.values(), key=lambda r: r.started_at, reverse=True)


def get_run(run_id: str) -> EvalRun | None:
    return _RUNS.get(run_id)


async def start_run(kind: EvalKind, model_ref: str, dataset_ref: str | None) -> EvalRun:
    run_id = uuid.uuid4().hex[:12]
    run = EvalRun(
        run_id=run_id,
        kind=kind,
        model_ref=model_ref,
        status="queued",
        started_at=time.time(),
    )
    _RUNS[run_id] = run
    asyncio.create_task(_execute(run, dataset_ref))
    return run


async def _execute(run: EvalRun, dataset_ref: str | None) -> None:
    run.status = "running"
    script = settings.bok_root.resolve() / "code" / _SCRIPT_MAP[run.kind]
    if not script.exists():
        run.status = "failed"
        run.error = f"script not found: {script}"
        run.finished_at = time.time()
        return

    # PoC executes the canonical script as a subprocess. Real sandboxing
    # (e2b/Modal/Docker-per-job) is deferred until users can upload arbitrary
    # model code — see design-specs.md.
    try:
        proc = await asyncio.create_subprocess_exec(
            "python",
            str(script),
            cwd=str(script.parent),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        run.summary = {
            "exit_code": proc.returncode,
            "stdout_tail": stdout.decode(errors="replace")[-2000:],
            "stderr_tail": stderr.decode(errors="replace")[-1000:],
            "model_ref": run.model_ref,
            "dataset_ref": dataset_ref,
        }
        run.status = "completed" if proc.returncode == 0 else "failed"
    except Exception as e:
        run.status = "failed"
        run.error = repr(e)
    finally:
        run.finished_at = time.time()
