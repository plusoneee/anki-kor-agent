from aiohttp import ClientSession, ClientTimeout
from src.config import get_anki_settings

settings = get_anki_settings()


async def invoke_anki(action: str, params: dict):
    payload = {"action": action, "version": 6, "params": params}
    timeout = ClientTimeout(total=10)
    async with ClientSession(timeout=timeout) as session:
        async with session.post(settings.url, json=payload) as resp:
            data = await resp.json()
            if data.get("error"):
                raise RuntimeError(f"[Anki] Error: {data['error']}")
            return data.get("result")
