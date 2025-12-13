from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AzureOpenAISettings(BaseSettings):
    api_key: str
    api_version: str = "2025-01-01-preview"
    deployment: str = "gpt-4o-mini-0"
    endpoint: str
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="AZURE_OPENAI_", extra="ignore"
    )


class AnkiSettings(BaseSettings):
    url: str = "http://127.0.0.1:8765"
    deck_name: str = "Korean::Auto"
    model_name: str = "Basic"
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="ANKI_", extra="ignore"
    )

    tag_default: str = "korean_auto"
    tag_native: str = "native_kor"

@lru_cache()
def get_env_settings():
    return AzureOpenAISettings()

@lru_cache()
def get_anki_settings() -> AnkiSettings:
    return AnkiSettings()