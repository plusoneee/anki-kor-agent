import asyncio
from io import BytesIO
from gtts import gTTS


async def generate_korean_tts(text: str) -> bytes:
    """
    Generate TTS audio for Korean text using gTTS.
    Returns MP3 audio bytes.
    """

    def _generate():
        tts = gTTS(text=text, lang="ko")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.read()

    loop = asyncio.get_event_loop()
    audio_bytes = await loop.run_in_executor(None, _generate)
    return audio_bytes
