from src.models.listening_state import ListeningState
from src.service.listening_anki_service import get_listening_anki_service
from src.utils.logger import node_logger

anki = get_listening_anki_service()


@node_logger
async def send_listening_to_anki(state: ListeningState):
    """Add or update the listening card in Anki."""
    sentence = state["korean_sentence"]
    audio_filename = state["audio_filename"]
    translation = state["translation"]
    tags = state.get("tags", [])

    note_id = await anki.find_listening_note(sentence)

    if note_id:
        await anki.update_listening_note(
            note_id, audio_filename, sentence, translation, tags
        )
        return {"anki_note_id": note_id}

    new_id = await anki.add_listening_note(audio_filename, sentence, translation, tags)
    return {"anki_note_id": new_id}
