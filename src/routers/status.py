from fastapi import APIRouter
from src.utils.anki import invoke_anki, AnkiConnectionError

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/anki")
async def check_anki_status():
    """檢查 Anki 連接狀態"""
    try:
        # 嘗試呼叫 AnkiConnect 的 version action
        version = await invoke_anki("version", {})
        return {
            "connected": True,
            "version": version,
            "message": "Anki 連接正常"
        }
    except AnkiConnectionError as e:
        return {
            "connected": False,
            "error": str(e),
            "message": "無法連接到 Anki"
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "message": "檢查 Anki 連接時發生錯誤"
        }


@router.get("/api")
async def check_api_status():
    """檢查 API 狀態"""
    return {
        "connected": True,
        "message": "API 運行正常"
    }
