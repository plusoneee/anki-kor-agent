import base64
from aiohttp import ClientSession, ClientTimeout, ClientConnectorError
from src.config import get_anki_settings

settings = get_anki_settings()


class AnkiConnectionError(Exception):
    """Raised when cannot connect to Anki."""

    pass


async def invoke_anki(action: str, params: dict):
    payload = {"action": action, "version": 6, "params": params}
    timeout = ClientTimeout(total=10)
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(settings.url, json=payload) as resp:
                data = await resp.json()
                if data.get("error"):
                    raise RuntimeError(f"[Anki] Error: {data['error']}")
                return data.get("result")
    except ClientConnectorError:
        raise AnkiConnectionError(
            f"無法連接到 Anki，請確認 Anki 已開啟且 AnkiConnect 外掛已安裝。(URL: {settings.url})"
        )


async def store_media_file(audio_bytes: bytes, filename: str):
    """Store audio file in Anki media collection."""
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    await invoke_anki("storeMediaFile", {"filename": filename, "data": audio_b64})
