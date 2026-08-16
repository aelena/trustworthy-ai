from typing import Any

import litellm

from app.config import settings
from app.schemas.chat import Message
from app.schemas.settings import ProviderConfig

SYSTEM_PROMPT_HEADER = (
    "You are tai-lab, an assistant for AI auditors. Answer using the Trustworthy AI "
    "Body of Knowledge below. Cite sources by file path (e.g. pages/bias.md) when you "
    "rely on them. If the BoK does not cover the question, say so."
)


class PrivacyModeViolation(RuntimeError):
    pass


def _ensure_privacy(provider: ProviderConfig) -> None:
    if not provider.privacy_mode:
        return
    if provider.profile != "ollama":
        raise PrivacyModeViolation(
            "Privacy mode requires the 'ollama' profile — no external provider calls allowed."
        )
    base = (provider.api_base or "").lower()
    if not (base.startswith("http://localhost") or base.startswith("http://127.0.0.1")):
        raise PrivacyModeViolation(
            "Privacy mode requires api_base to point at localhost."
        )


def _resolve_model(provider: ProviderConfig) -> str:
    # LiteLLM expects provider-prefixed model ids for non-OpenAI providers.
    # For Anthropic, plain ids work; for Ollama, we require the ollama/ prefix.
    model = provider.model
    if provider.profile == "ollama" and not model.startswith("ollama/"):
        model = f"ollama/{model}"
    return model


def _build_system(bok_text: str, use_cache: bool, provider: ProviderConfig) -> Any:
    """Return a system prompt structured for prompt caching when supported.

    Anthropic supports `cache_control` on system prompt blocks. Other providers
    receive a flat string — they pay full price every call but the call still
    works.
    """
    if not use_cache or provider.profile != "anthropic":
        return f"{SYSTEM_PROMPT_HEADER}\n\n{bok_text}"

    ttl = "1h" if settings.anthropic_cache_ttl == "1h" else "5m"
    return [
        {"type": "text", "text": SYSTEM_PROMPT_HEADER},
        {
            "type": "text",
            "text": bok_text,
            "cache_control": {"type": "ephemeral", "ttl": ttl},
        },
    ]


async def chat_completion(
    messages: list[Message],
    provider: ProviderConfig,
    bok_text: str,
    use_cache: bool = True,
) -> dict:
    _ensure_privacy(provider)

    api_key = provider.api_key or (
        settings.anthropic_api_key if provider.profile == "anthropic" else None
    )

    kwargs: dict[str, Any] = {
        "model": _resolve_model(provider),
        "messages": [
            {"role": "system", "content": _build_system(bok_text, use_cache, provider)},
            *[{"role": m.role, "content": m.content} for m in messages],
        ],
        "max_tokens": settings.max_output_tokens,
    }
    if api_key:
        kwargs["api_key"] = api_key
    if provider.api_base:
        kwargs["api_base"] = provider.api_base

    response = await litellm.acompletion(**kwargs)
    usage = getattr(response, "usage", None) or {}

    return {
        "content": response.choices[0].message.content,
        "input_tokens": getattr(usage, "prompt_tokens", None),
        "output_tokens": getattr(usage, "completion_tokens", None),
        "cache_read_tokens": getattr(usage, "cache_read_input_tokens", None),
        "cache_write_tokens": getattr(usage, "cache_creation_input_tokens", None),
    }
