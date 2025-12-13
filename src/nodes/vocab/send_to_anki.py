from src.models.vocab_state import VocabState
from src.service.vocab_anki_service import get_vocab_anki_service
from typing import Dict, Any
from src.utils.logger import node_logger

anki = get_vocab_anki_service()


@node_logger
async def send_to_anki(state: VocabState) -> Dict[str, Any]:
    """
    Node 任務：將解析好的資料寫入 Anki。
    - 先用 service.find_note() 判斷是否存在
    - 若存在 → update
    - 若不存在 → add
    """
    word = state["word"]
    back_html = state["back_html"]
    tags = state.get("tags", [])

    # 1) 檢查是否應該 update
    note_id = await anki.find_note(word)

    # 2) 更新
    if note_id:
        await anki.update_note(note_id, word, back_html, tags)
        return {"anki_note_id": note_id}

    # 3) 新增
    new_id = await anki.add_note(word, back_html, tags)
    return {"anki_note_id": new_id}
