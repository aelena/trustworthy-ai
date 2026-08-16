from typing import Literal

from pydantic import BaseModel

EvalKind = Literal["bias", "explainability", "adversarial", "eval_frameworks", "differential_privacy"]
EvalStatus = Literal["queued", "running", "completed", "failed"]


class EvalRequest(BaseModel):
    kind: EvalKind
    model_ref: str
    dataset_ref: str | None = None


class EvalRun(BaseModel):
    run_id: str
    kind: EvalKind
    model_ref: str
    status: EvalStatus
    started_at: float
    finished_at: float | None = None
    summary: dict | None = None
    error: str | None = None
