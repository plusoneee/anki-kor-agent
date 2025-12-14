from src.models.listening_state import ListeningState
from src.service.listening_anki_service import get_listening_anki_service
from src.utils.logger import node_logger

anki = get_listening_anki_service()


@node_logger
async def check_duplicate(state: ListeningState):
    """Check if a listening card for this sentence already exists."""
    sentence = state["korean_sentence"]
    note_id = await anki.find_listening_note(sentence)
    force = state.get("force_update", False)

    if not note_id:
        return {"exists": False}

    if not force:
        return {"exists": True, "anki_note_id": note_id}

    return {"exists": False, "anki_note_id": note_id}
