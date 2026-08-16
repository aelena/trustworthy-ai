from typing import Literal

from pydantic import BaseModel

from app.schemas.settings import ProviderConfig


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    provider: ProviderConfig
    use_bok_cache: bool = True


class ChatResponse(BaseModel):
    content: str
    cache_read_tokens: int | None = None
    cache_write_tokens: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
