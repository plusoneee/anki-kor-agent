from src.config import get_anki_settings
from src.utils.logger import node_logger

@node_logger
async def build_tags(state):
    settings = get_anki_settings()
    tags = [settings.tag_default]  # e.g. korean_auto

    # --- root tag ---
    root = state.get("root")
    pos = state.get("pos")

    if root == "N":
        tags.append(settings.tag_native)      # native_kor
    elif root:
        tags.append(f"root_{root}")           # root:漢字

    if pos:
        tags.append(f"pos_{pos}")             # pos:v

    return {
        "tags": tags
    }
