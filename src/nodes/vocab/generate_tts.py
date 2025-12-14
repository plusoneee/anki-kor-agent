import hashlib
from src.models.vocab_state import VocabState
from src.utils.tts import generate_korean_tts
from src.utils.logger import node_logger


@node_logger
async def generate_tts(state: VocabState):
    """Generate TTS audio from Korean word using gTTS."""
    word = state["word"]

    # Generate unique filename based on word hash
    word_hash = hashlib.md5(word.encode()).hexdigest()[:12]
    filename = f"vocab_{word_hash}.mp3"

    audio_bytes = await generate_korean_tts(word)
    return {"audio_bytes": audio_bytes, "audio_filename": filename}
