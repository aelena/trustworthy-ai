from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bok_root: Path = Path(__file__).resolve().parents[2].parent
    cors_origins: str = "http://localhost:3000"
    anthropic_api_key: str = ""
    max_output_tokens: int = 2048
    anthropic_cache_ttl: str = "5m"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
