from src.models.state import WordState
from src.utils.template import render_template
from src.utils.logger import node_logger

# POS mapping
POS_MAP = {
    "n": "名詞",
    "v": "動詞",
    "adj": "形容詞",
    "adv": "副詞",
}

# POS color mapping
POS_COLORS = {
    "n": "#3B82F6",
    "v": "#10B981",
    "adj": "#F59E0B",
    "adv": "#8B5CF6",
}

@node_logger
async def build_back(state: WordState) -> WordState:

    pos = state.get("pos")
    pos_zh = POS_MAP.get(pos, "") if pos else ""
    badge_color = POS_COLORS.get(pos, "#6B7280")  # fallback 灰色

    back_html = render_template(
        "back_minimal.html",
        word=state["word"],
        meaning=state["meaning"],
        pos=pos,
        pos_zh=pos_zh,
        badge_color=badge_color,
        examples=state["examples"],
    )

    return {
        "back_html": back_html
    }