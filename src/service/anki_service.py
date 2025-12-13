from typing import List, Optional
from functools import lru_cache
from src.utils.anki import invoke_anki
from src.config import get_anki_settings


from src.utils.logger import console


class AnkiService:
    def __init__(self):
        self.settings = get_anki_settings()
        self.default_tag = self.settings.tag_default
        self.native_tag = self.settings.tag_native

    async def _prune_tags(self, note_id: int):
        # ====================================================
        # Tag tool：移除舊 tag（保留使用者自加的）
        # ====================================================
        note_info = await invoke_anki("notesInfo", {"notes": [note_id]})
        note_tags = set(note_info[0].get("tags", []))

        # 可移除清單
        removable = {self.default_tag, self.native_tag}
        removable |= {t for t in note_tags if t.startswith("root_")}
        removable |= {t for t in note_tags if t.startswith("pos_")}

        if removable:
            tags_str = " ".join(removable)  # ⚠ MUST be space-separated string
            console.log(f"[AnkiService] Removing tags: {tags_str}", markup=False)
            await invoke_anki("removeTags", {"notes": [note_id], "tags": tags_str})

    async def _ensure_tags(self, note_id: int, tags: List[str]):
        # ====================================================
        # Tag tool：確保 Tag 新增成功
        # ====================================================
        if tags:
            tags_str = " ".join(tags)
            await invoke_anki("addTags", {"notes": [note_id], "tags": tags_str})

        # 再確認
        note_info = await invoke_anki("notesInfo", {"notes": [note_id]})
        note_tags = set(note_info[0].get("tags", []))

        missing = [t for t in tags if t not in note_tags]
        if missing:
            console.log(f"[⚠ Warning] Retrying add tags → {missing}", markup=False)
            retry = " ".join(missing)
            await invoke_anki("addTags", {"notes": [note_id], "tags": retry})
        else:
            console.log(f"[AnkiService] Tags confirmed: {note_tags}", markup=False)
    # 查重
    async def find_note(self, word: str) -> Optional[int]:
        query = f'deck:"{self.settings.deck_name}" front:"{word}"'
        notes = await invoke_anki("findNotes", {"query": query})
        if notes:
            console.log(f"[AnkiService] found existing note: {notes[0]}", markup=False)
            return notes[0]
        console.log(f"[AnkiService] NEW word: {word}", markup=False)
        return None

    # 建 note 結構
    def make_note(self, word: str, back_html: str, tags: List[str]):
        return {
            "deckName": self.settings.deck_name,
            "modelName": self.settings.model_name,
            "fields": {"Front": word, "Back": back_html},
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
            "tags": tags,
        }

    # 新增 note
    async def add_note(self, word: str, back_html: str, tags: List[str]) -> int:
        note = self.make_note(word, back_html, tags)
        note_id = await invoke_anki("addNote", {"note": note})
        console.log(f"[AnkiService] ADD → {note_id}", markup=False)
        return note_id

    # 更新 note
    async def update_note(self, note_id: int, word: str, back_html: str, tags: List[str]):
        await invoke_anki(
            "updateNoteFields",
            {"note": {"id": note_id, "fields": {"Front": word, "Back": back_html}}},
        )
        await self._prune_tags(note_id)
        await self._ensure_tags(note_id, tags)
        return note_id


@lru_cache()
def get_anki_service() -> AnkiService:
    return AnkiService()