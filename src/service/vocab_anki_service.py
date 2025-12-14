from typing import List, Optional
from functools import lru_cache
from src.utils.anki import invoke_anki
from src.config import get_anki_settings


from src.utils.logger import console


class VocabAnkiService:
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
            console.log(f"[VocabAnkiService] Removing tags: {tags_str}", markup=False)
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
            console.log(f"[VocabAnkiService] Tags confirmed: {note_tags}", markup=False)

    # 查重
    async def find_note(self, word: str) -> Optional[int]:
        escaped = word.replace('"', '\\"')
        query = f'deck:"{self.settings.deck_name}" Word:"{escaped}"'
        notes = await invoke_anki("findNotes", {"query": query})
        if notes:
            console.log(f"[VocabAnkiService] found existing note: {notes[0]}", markup=False)
            return notes[0]
        console.log(f"[VocabAnkiService] NEW word: {word}", markup=False)
        return None

    # 獲取所有vocab單字（用於涵蓋率檢查）
    async def get_all_vocab_words(self) -> set[str]:
        """Fetch all vocabulary words from Anki deck."""
        query = f'deck:"{self.settings.deck_name}"'
        note_ids = await invoke_anki("findNotes", {"query": query})

        if not note_ids:
            console.log("[VocabAnkiService] No vocab cards found in deck", markup=False)
            return set()

        # Batch fetch all note info
        notes_info = await invoke_anki("notesInfo", {"notes": note_ids})

        # Extract Word field from each note
        words = set()
        for note in notes_info:
            word = note.get("fields", {}).get("Word", {}).get("value", "").strip()
            if word:
                words.add(word)

        console.log(f"[VocabAnkiService] Retrieved {len(words)} vocab words", markup=False)
        return words

    # 建 note 結構（使用 8 個獨立欄位）
    def make_note(
        self,
        word: str,
        audio_filename: str,
        meaning: str,
        pos_zh: str,
        example_korean_1: str,
        example_chinese_1: str,
        example_korean_2: str,
        example_chinese_2: str,
        tags: List[str],
    ):
        return {
            "deckName": self.settings.deck_name,
            "modelName": self.settings.vocab_model_name,
            "fields": {
                "Word": word,
                "Audio": f"[sound:{audio_filename}]",
                "Meaning": meaning,
                "POS": pos_zh,
                "ExampleKorean1": example_korean_1,
                "ExampleChinese1": example_chinese_1,
                "ExampleKorean2": example_korean_2,
                "ExampleChinese2": example_chinese_2,
            },
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
            "tags": tags,
        }

    # 新增 note
    async def add_note(
        self,
        word: str,
        audio_filename: str,
        meaning: str,
        pos_zh: str,
        example_korean_1: str,
        example_chinese_1: str,
        example_korean_2: str,
        example_chinese_2: str,
        tags: List[str],
    ) -> int:
        note = self.make_note(
            word, audio_filename, meaning, pos_zh,
            example_korean_1, example_chinese_1,
            example_korean_2, example_chinese_2,
            tags
        )
        note_id = await invoke_anki("addNote", {"note": note})
        console.log(f"[VocabAnkiService] ADD → {note_id}", markup=False)
        return note_id

    # 更新 note
    async def update_note(
        self,
        note_id: int,
        word: str,
        audio_filename: str,
        meaning: str,
        pos_zh: str,
        example_korean_1: str,
        example_chinese_1: str,
        example_korean_2: str,
        example_chinese_2: str,
        tags: List[str],
    ):
        await invoke_anki(
            "updateNoteFields",
            {
                "note": {
                    "id": note_id,
                    "fields": {
                        "Word": word,
                        "Audio": f"[sound:{audio_filename}]",
                        "Meaning": meaning,
                        "POS": pos_zh,
                        "ExampleKorean1": example_korean_1,
                        "ExampleChinese1": example_chinese_1,
                        "ExampleKorean2": example_korean_2,
                        "ExampleChinese2": example_chinese_2,
                    },
                }
            },
        )
        await self._prune_tags(note_id)
        await self._ensure_tags(note_id, tags)
        return note_id


@lru_cache()
def get_vocab_anki_service() -> VocabAnkiService:
    return VocabAnkiService()
