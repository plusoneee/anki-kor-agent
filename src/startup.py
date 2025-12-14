"""
API 啟動時的初始化邏輯：
1. 檢查 Anki 是否在運行
2. 確保 Vocab 和 Listening 的 Deck/Model 存在
"""

from src.utils.anki import invoke_anki, AnkiConnectionError
from src.config import get_anki_settings, get_listening_settings
from src.utils.logger import console


async def check_anki_connection():
    """檢查 Anki 是否在運行"""
    try:
        await invoke_anki("version", {})
        console.log("[Startup] Anki 連線成功", style="green")
        return True
    except AnkiConnectionError as e:
        console.log(f"[Startup] Anki 連線失敗: {e}", style="red")
        raise


async def ensure_vocab_model():
    """確保 Vocab 的 Deck 和 Model 存在"""
    settings = get_anki_settings()
    model_name = settings.vocab_model_name
    deck_name = settings.deck_name

    # Ensure deck exists
    decks = await invoke_anki("deckNames", {})
    if deck_name not in decks:
        await invoke_anki("createDeck", {"deck": deck_name})
        console.log(f"[Startup] 建立 Deck: {deck_name}", style="green")

    # Check if model exists
    models = await invoke_anki("modelNames", {})

    if model_name in models:
        console.log(f"[Startup] Vocab Model 已存在: {model_name}", style="green")
        return

    # Create the Vocabulary model with 8 fields
    model_def = {
        "modelName": model_name,
        "inOrderFields": [
            "Word", "Audio", "Meaning", "POS",
            "ExampleKorean1", "ExampleChinese1",
            "ExampleKorean2", "ExampleChinese2",
        ],
        "css": settings.card_css,
        "cardTemplates": [
            {
                "Name": "Vocabulary Card",
                "Front": settings.card_front,
                "Back": settings.card_back,
            }
        ],
    }

    await invoke_anki("createModel", model_def)
    console.log(f"[Startup] 建立 Vocab Model: {model_name}", style="green")


async def ensure_listening_model():
    """確保 Listening 的 Deck 和 Model 存在"""
    settings = get_listening_settings()
    model_name = settings.model_name
    deck_name = settings.deck_name

    # Ensure deck exists
    decks = await invoke_anki("deckNames", {})
    if deck_name not in decks:
        await invoke_anki("createDeck", {"deck": deck_name})
        console.log(f"[Startup] 建立 Deck: {deck_name}", style="green")

    # Check if model exists
    models = await invoke_anki("modelNames", {})

    if model_name in models:
        console.log(f"[Startup] Listening Model 已存在: {model_name}", style="green")
        return

    # Create the Listening model
    model_def = {
        "modelName": model_name,
        "inOrderFields": ["Audio", "Korean", "Chinese"],
        "css": settings.card_css,
        "cardTemplates": [
            {
                "Name": "Listening Card",
                "Front": "{{Audio}}",
                "Back": """
{{FrontSide}}
<hr id=answer>
<div class="korean">{{Korean}}</div>
<div class="chinese">{{Chinese}}</div>
""",
            }
        ],
    }

    await invoke_anki("createModel", model_def)
    console.log(f"[Startup] 建立 Listening Model: {model_name}", style="green")


async def initialize():
    """API 啟動時執行的初始化"""
    console.log("[Startup] 開始初始化...", style="bold blue")

    # 1. 檢查 Anki 連線
    await check_anki_connection()

    # 2. 確保 Models 存在
    await ensure_vocab_model()
    await ensure_listening_model()

    console.log("[Startup] 初始化完成!", style="bold green")
