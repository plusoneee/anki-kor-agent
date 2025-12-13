from typing import List, Optional
from functools import lru_cache
from src.utils.anki import invoke_anki
from src.config import get_listening_settings
from src.utils.logger import console


class ListeningAnkiService:
    def __init__(self):
        self.settings = get_listening_settings()
        self.default_tag = self.settings.tag_default

    async def find_listening_note(self, sentence: str) -> Optional[int]:
        """Find existing listening note by Korean sentence field."""
        escaped = sentence.replace('"', '\\"')
        query = f'deck:"{self.settings.deck_name}" Korean:"{escaped}"'
        notes = await invoke_anki("findNotes", {"query": query})
        if notes:
            console.log(
                f"[ListeningAnkiService] found existing note: {notes[0]}", markup=False
            )
            return notes[0]
        console.log("[ListeningAnkiService] NEW sentence", markup=False)
        return None

    def make_listening_note(
        self, audio_filename: str, korean: str, chinese: str, tags: List[str]
    ):
        """Create note structure for Listening model."""
        return {
            "deckName": self.settings.deck_name,
            "modelName": self.settings.model_name,
            "fields": {
                "Audio": f"[sound:{audio_filename}]",
                "Korean": korean,
                "Chinese": chinese,
            },
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
            "tags": tags,
        }

    async def add_listening_note(
        self, audio_filename: str, korean: str, chinese: str, tags: List[str]
    ) -> int:
        note = self.make_listening_note(audio_filename, korean, chinese, tags)
        note_id = await invoke_anki("addNote", {"note": note})
        console.log(f"[ListeningAnkiService] ADD -> {note_id}", markup=False)
        return note_id

    async def update_listening_note(
        self,
        note_id: int,
        audio_filename: str,
        korean: str,
        chinese: str,
        tags: List[str],
    ):
        await invoke_anki(
            "updateNoteFields",
            {
                "note": {
                    "id": note_id,
                    "fields": {
                        "Audio": f"[sound:{audio_filename}]",
                        "Korean": korean,
                        "Chinese": chinese,
                    },
                }
            },
        )
        # Update tags
        if tags:
            tags_str = " ".join(tags)
            await invoke_anki("addTags", {"notes": [note_id], "tags": tags_str})
        console.log(f"[ListeningAnkiService] UPDATE -> {note_id}", markup=False)
        return note_id


@lru_cache()
def get_listening_anki_service() -> ListeningAnkiService:
    return ListeningAnkiService()
