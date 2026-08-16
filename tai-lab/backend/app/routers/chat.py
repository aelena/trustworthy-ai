from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.bok import bok_index
from app.services.llm import PrivacyModeViolation, chat_completion

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        result = await chat_completion(
            messages=req.messages,
            provider=req.provider,
            bok_text=bok_index.full_text,
            use_cache=req.use_bok_cache,
        )
    except PrivacyModeViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"provider error: {e!r}")

    return ChatResponse(**result)
