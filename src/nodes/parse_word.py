from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from src.models.state import WordState
from src.models.word_schema import WordParseOutput
from src.utils.prompt_loader import load_prompt
from src.utils.llm import ask_llm
from typing import Dict, Any
from src.utils.logger import node_logger


CNF = load_prompt("parse_word")
output_parser = PydanticOutputParser(pydantic_object=WordParseOutput)

parse_word_prompt = PromptTemplate(
    template=CNF["user_prompt"],
    input_variables=["word"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)

@node_logger
async def parse_word(state: WordState) -> Dict[str, Any]:
    word = state["word"]
    user_prompt = parse_word_prompt.format(word=word)

    try:
        response = await ask_llm(
            model=CNF["parameters"]["model"],
            system_prompt=CNF["system_prompt"],
            user_prompt=user_prompt,
            temperature=CNF["parameters"]["temperature"],
            max_tokens=CNF["parameters"]["max_tokens"],
        )

        parsed: WordParseOutput = output_parser.parse(response)

    except Exception as e:
        raise RuntimeError(f"[parse_word] LLM Error: {e}")

    return {
        "meaning": parsed.meaning,
        "pos": parsed.pos,
        "examples": [ex.model_dump() for ex in parsed.examples],
    }
