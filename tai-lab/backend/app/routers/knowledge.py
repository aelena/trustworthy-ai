from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.bok import bok_index

router = APIRouter()


class KnowledgeHit(BaseModel):
    path: str
    title: str
    excerpt: str


class KnowledgeResponse(BaseModel):
    query: str
    hits: list[KnowledgeHit]


@router.get("/search", response_model=KnowledgeResponse)
def search(q: str, limit: int = 8) -> KnowledgeResponse:
    if not q.strip():
        raise HTTPException(status_code=400, detail="query is empty")
    files = bok_index.grep(q, max_hits=limit)
    hits = [
        KnowledgeHit(
            path=f.path,
            title=f.title,
            excerpt=_excerpt(f.content, q),
        )
        for f in files
    ]
    return KnowledgeResponse(query=q, hits=hits)


@router.get("/files", response_model=list[str])
def list_files() -> list[str]:
    return [f.path for f in bok_index.files]


def _excerpt(content: str, query: str, window: int = 240) -> str:
    idx = content.lower().find(query.lower())
    if idx < 0:
        return content[:window]
    start = max(0, idx - window // 2)
    end = min(len(content), idx + window // 2)
    return ("…" if start > 0 else "") + content[start:end] + ("…" if end < len(content) else "")
