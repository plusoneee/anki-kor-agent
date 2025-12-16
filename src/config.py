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
    vocab_model_name: str = "Korean_Vocab_Auto"  # 系統自動生成的 Vocabulary model
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="ANKI_", extra="ignore"
    )

    tag_default: str = "korean_auto"
    tag_native: str = "native_kor"

    # Vocabulary model card templates and CSS
    card_css: str = """
.card-root {
    font-family: 'Noto Sans KR', sans-serif;
    text-align: center;
    padding: 20px;
}
.word {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 10px;
}
.meaning-pos {
    margin: 15px 0;
}
.meaning {
    font-size: 1.3em;
}
.pos-badge {
    display: inline-block;
    padding: 2px 8px;
    margin-left: 8px;
    border-radius: 4px;
    font-size: 0.8em;
    background-color: #e0e0e0;
}
.ex-block {
    margin-top: 15px;
    text-align: center;
}
.ex-item {
    margin: 10px 0;
}
.ex-kr {
    font-size: 1.1em;
    margin-bottom: 3px;
}
.ex-zh {
    color: #555;
    font-size: 0.95em;
}
"""
    card_front: str = """
<div class="card-root">
    <div class="word">{{Word}}</div>
    {{Audio}}
</div>
"""
    card_back: str = """
<div class="card-root">
    <div class="word">{{Word}}</div>
    {{Audio}}
    <hr>
    <div class="meaning-pos">
        <span class="meaning">{{Meaning}}</span>
        <span class="pos-badge">{{POS}}</span>
    </div>
    <hr>
    <div class="ex-block">
        <div class="ex-item">
            <div class="ex-kr">{{ExampleKorean1}}</div>
            <div class="ex-zh">{{ExampleChinese1}}</div>
        </div>
        <div class="ex-item">
            <div class="ex-kr">{{ExampleKorean2}}</div>
            <div class="ex-zh">{{ExampleChinese2}}</div>
        </div>
    </div>
</div>
"""


class ListeningSettings(BaseSettings):
    deck_name: str = "Korean::Listening"
    model_name: str = "Listening"
    tag_default: str = "listening_auto"
    card_css: str = """
        .card { text-align: center; }
        .korean { font-size: 24px; margin: 10px 0; }
        .chinese { font-size: 18px; color: #666; }
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="ANKI_LISTENING_", extra="ignore"
    )


class AppSettings(BaseSettings):
    word_list_dir: str = "data"
    default_word_list: str = "korean_words.txt"
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )


class CORSSettings(BaseSettings):
    origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="CORS_", extra="ignore"
    )


@lru_cache()
def get_env_settings():
    return AzureOpenAISettings()


@lru_cache()
def get_anki_settings() -> AnkiSettings:
    return AnkiSettings()


@lru_cache()
def get_listening_settings() -> ListeningSettings:
    return ListeningSettings()


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache()
def get_cors_settings() -> CORSSettings:
    return CORSSettings()
