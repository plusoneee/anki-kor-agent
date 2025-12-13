from src.models.listening_state import ListeningState
from src.utils.llm import ask_llm
from src.utils.prompt_loader import load_prompt
from src.utils.logger import node_logger

CNF = load_prompt("translate_sentence")


@node_logger
async def translate_sentence(state: ListeningState):
    """Translate Korean sentence to Chinese using LLM if not provided."""
    user_translation = state.get("chinese_translation")

    if user_translation and user_translation.strip():
        return {"translation": user_translation.strip(), "translation_source": "user"}

    korean = state["korean_sentence"]
    user_prompt = CNF["user_prompt"].format(sentence=korean)

    result = await ask_llm(
        model=CNF["parameters"]["model"],
        system_prompt=CNF["system_prompt"],
        user_prompt=user_prompt,
        temperature=CNF["parameters"]["temperature"],
        max_tokens=CNF["parameters"]["max_tokens"],
    )
    return {"translation": result.strip(), "translation_source": "llm"}
