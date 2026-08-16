from fastapi import APIRouter

from app.services.bok import bok_index

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@router.get("/readyz")
def readyz() -> dict:
    return {
        "status": "ok" if bok_index.is_loaded else "loading",
        "bok_files": bok_index.file_count,
        "bok_tokens_estimate": bok_index.token_estimate,
    }
