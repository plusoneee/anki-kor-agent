from typing import TypedDict, Optional, List, Literal


class ListeningState(TypedDict, total=False):
    # Input
    korean_sentence: str
    chinese_translation: Optional[str]

    # Translation node output
    translation: str
    translation_source: Literal["user", "llm"]

    # TTS node output
    audio_bytes: bytes
    audio_filename: str

    # Store audio node output
    audio_stored: bool

    # Ensure model node output
    model_exists: bool

    # Build card node output
    front_html: str
    back_html: str

    # Send to Anki node output
    anki_note_id: Optional[int]

    # Control flags
    force_update: bool
    exists: Optional[bool]

    # Tags
    tags: List[str]
