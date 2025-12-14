from src.models.vocab_state import VocabState
from src.utils.logger import node_logger

# 詞性英文轉中文對照表
POS_MAP = {
    "n": "名詞",
    "v": "動詞",
    "adj": "形容詞",
    "adv": "副詞",
    "pron": "代名詞",
    "prep": "介詞",
    "conj": "連接詞",
    "interj": "感嘆詞",
    "num": "數詞",
    "aux": "助動詞",
    "det": "限定詞",
    "part": "助詞",
    "suffix": "詞尾",
    "prefix": "詞頭",
    "phrase": "片語",
    "expr": "慣用語",
}


@node_logger
async def build_examples(state: VocabState) -> dict:
    """Convert examples list to 4 separate fields and convert POS to Chinese."""
    examples = state.get("examples", [])
    pos = state.get("pos", "")

    # 詞性轉中文
    pos_zh = POS_MAP.get(pos.lower(), pos) if pos else "" 

    ex1 = examples[0] if len(examples) > 0 else {}
    ex2 = examples[1] if len(examples) > 1 else {}

    return {
        "example_korean_1": ex1.get("kr", ""),
        "example_chinese_1": ex1.get("zh", ""),
        "example_korean_2": ex2.get("kr", ""),
        "example_chinese_2": ex2.get("zh", ""),
        "pos_zh": pos_zh,
    }
