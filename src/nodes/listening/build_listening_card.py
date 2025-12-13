from src.models.listening_state import ListeningState
from src.utils.template import render_template
from src.config import get_listening_settings
from src.utils.logger import node_logger


@node_logger
async def build_listening_card(state: ListeningState):
    """Build front and back HTML for the listening card."""
    settings = get_listening_settings()

    # Front: Audio player reference
    front_html = f'[sound:{state["audio_filename"]}]'

    # Back: Korean sentence + Chinese translation
    back_html = render_template(
        "listening_back.html",
        korean=state["korean_sentence"],
        chinese=state["translation"],
    )

    # Tags
    tags = [settings.tag_default, "listening"]
    if state.get("translation_source") == "llm":
        tags.append("auto_translated")

    return {"front_html": front_html, "back_html": back_html, "tags": tags}
