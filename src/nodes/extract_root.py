from typing import Dict, Any
from langchain_core.output_parsers import PydanticOutputParser

from src.models.root_schema import RootOutput
from src.models.state import WordState
from src.utils.llm import ask_llm
from src.utils.prompt_loader import load_prompt
from src.utils.logger import node_logger

# Load config from YAML
CNF = load_prompt("extract_root")
parser = PydanticOutputParser(pydantic_object=RootOutput)


@node_logger
async def extract_root(state: WordState) -> Dict[str, Any]:
    """
    解析單字字源：
      - 若為漢字詞: 回傳一個漢字（如 學）
      - 若為純韓語詞（고유어）: 回傳 'N'
    後續自動轉為 Tag（root_學 / native_kor）
    """
    word = state["word"]
    user_prompt = CNF["user_prompt"].format(
        word=word, format_instructions=parser.get_format_instructions()
    )
    try:
        result = await ask_llm(
            model=CNF["parameters"]["model"],
            system_prompt=CNF["system_prompt"],
            user_prompt=user_prompt,
            temperature=CNF["parameters"]["temperature"],
            max_tokens=CNF["parameters"]["max_tokens"],
        )
    except Exception as e:
        return {
            "root": None,
            "root_tag": None,
            "root_error": str(e),
        }

    parsed: RootOutput = parser.parse(result)
    root_value = parsed.root.strip()

    return {
        "root": root_value,
        "root_tag": "native_kor" if root_value == "N" else f"root_{root_value}",
    }
