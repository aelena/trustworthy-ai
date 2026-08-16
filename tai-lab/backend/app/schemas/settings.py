from typing import Literal

from pydantic import BaseModel, Field

ProviderProfile = Literal["anthropic", "openai", "ollama", "openai_compat"]


class ProviderConfig(BaseModel):
    """Per-request provider configuration sent by the frontend.

    The frontend stores these in browser localStorage and forwards them per
    request. The backend does NOT persist them.
    """

    profile: ProviderProfile = "anthropic"
    model: str = Field(
        default="claude-haiku-4-5",
        description="Model id, in LiteLLM-compatible form (e.g. 'claude-haiku-4-5', 'ollama/llama3.2', 'gpt-4o-mini').",
    )
    api_key: str | None = None
    api_base: str | None = Field(
        default=None,
        description="For Ollama or any OpenAI-compatible endpoint. e.g. 'http://localhost:11434'.",
    )
    privacy_mode: bool = Field(
        default=False,
        description="When true, the backend refuses any non-local provider call for the request.",
    )
