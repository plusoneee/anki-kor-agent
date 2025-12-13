import base64
from src.models.listening_state import ListeningState
from src.utils.anki import invoke_anki
from src.utils.logger import node_logger


@node_logger
async def store_audio(state: ListeningState):
    """Store audio file in Anki media collection via storeMediaFile API."""
    audio_bytes = state["audio_bytes"]
    filename = state["audio_filename"]

    # Base64 encode the audio data for AnkiConnect
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    await invoke_anki("storeMediaFile", {"filename": filename, "data": audio_b64})
    return {"audio_stored": True}
