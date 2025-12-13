from typing import Literal, List
from pydantic import BaseModel, Field


class ExampleItem(BaseModel):
    type: Literal["casual", "formal"] = Field(
        description="例句語氣類型：casual= 요體（口語），formal= ㅂ니다體（正式）。"
    )
    kr: str = Field(description="韓文例句，使用現在式。")
    zh: str = Field(description="中文翻譯。")


class WordParseOutput(BaseModel):
    word: str = Field(description="韓文單字原形（以 다 結尾）。")
    meaning: str = Field(description="單字的中文意思。")
    pos: Literal["n","v","adj","adv","p"] = Field(description="詞性")
    examples: List[ExampleItem] = Field(
        description="兩句例句：第一句 casual（요體），第二句 formal（ㅂ니다體）。"
    )
