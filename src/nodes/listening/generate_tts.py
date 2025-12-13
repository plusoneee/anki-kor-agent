import hashlib
from src.models.listening_state import ListeningState
from src.utils.tts import generate_korean_tts
from src.utils.logger import node_logger


@node_logger
async def generate_tts(state: ListeningState):
    """Generate TTS audio from Korean sentence using gTTS."""
    sentence = state["korean_sentence"]

    # Generate unique filename based on sentence hash
    sentence_hash = hashlib.md5(sentence.encode()).hexdigest()[:12]
    filename = f"listening_{sentence_hash}.mp3"

    audio_bytes = await generate_korean_tts(sentence)
    return {"audio_bytes": audio_bytes, "audio_filename": filename}
