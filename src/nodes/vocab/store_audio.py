from src.models.vocab_state import VocabState
from src.utils.anki import store_media_file
from src.utils.logger import node_logger


@node_logger
async def store_audio(state: VocabState) -> dict:
    """Store audio file in Anki media collection."""
    await store_media_file(state["audio_bytes"], state["audio_filename"])
    return {"audio_stored": True}