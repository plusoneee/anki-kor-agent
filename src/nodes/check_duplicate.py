from src.service.anki_service import get_anki_service

from src.utils.logger import node_logger

anki = get_anki_service()

@node_logger
async def check_duplicate(state):
    word = state["word"]
    note_id = await anki.find_note(word)
    force = state.get("force_update", False)
    # 1) 完全沒 note: 新增
    if not note_id:
        return {"exists": False}

    # 2) 有 note & force=False: skip
    if not force:
        return {
            "exists": True,
            "anki_note_id": note_id
        }

    # 3) 有 note + force=True: 強制後續處理
    return {
        "exists": False,
        "anki_note_id": note_id
    }

