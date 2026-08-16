from fastapi import APIRouter, HTTPException

from app.schemas.evals import EvalRequest, EvalRun
from app.services import eval_runner

router = APIRouter()


@router.post("", response_model=EvalRun)
async def start_eval(req: EvalRequest) -> EvalRun:
    return await eval_runner.start_run(req.kind, req.model_ref, req.dataset_ref)


@router.get("", response_model=list[EvalRun])
def list_evals() -> list[EvalRun]:
    return eval_runner.list_runs()


@router.get("/{run_id}", response_model=EvalRun)
def get_eval(run_id: str) -> EvalRun:
    run = eval_runner.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return run
