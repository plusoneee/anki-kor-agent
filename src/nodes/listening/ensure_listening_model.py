from src.models.listening_state import ListeningState
from src.utils.anki import invoke_anki
from src.config import get_listening_settings
from src.utils.logger import node_logger


@node_logger
async def ensure_listening_model(state: ListeningState):
    """Ensure the Listening Note Type and Deck exist in Anki, create if not."""
    settings = get_listening_settings()
    model_name = settings.model_name
    deck_name = settings.deck_name

    # Ensure deck exists
    decks = await invoke_anki("deckNames", {})
    if deck_name not in decks:
        await invoke_anki("createDeck", {"deck": deck_name})

    # Check if model exists
    models = await invoke_anki("modelNames", {})

    if model_name in models:
        return {"model_exists": True}

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
    return {"model_exists": True}
