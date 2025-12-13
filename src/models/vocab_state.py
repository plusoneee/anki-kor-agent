from typing import TypedDict, List, Dict, Optional, Literal


class VocabState(TypedDict, total=False):
    word: str
    meaning: str
    pos: str
    examples: List[Dict[str, str]]  # casual/formal examples

    # build_back node output
    back_html: str

    # send_to_anki node output
    anki_note_id: Optional[int]

    tags: Optional[List[str]]
    root: Optional[Literal["N"] | str]  # "N" 表示純韓語詞，否則為漢字
    root_tag: Optional[str]  # 用於 Anki 的 root 標籤

    # anki update control
    force_update: Optional[bool]  # 是否強制更新已存在的 Anki
    exists: Optional[bool]  # 是否已存在（重複檢查結果）
