from pydantic import BaseModel, field_validator
import re

class RootOutput(BaseModel):
    root: str

    @field_validator("root")
    def validate_root(cls, v):
        v = v.strip()

        # case 1: native Korean word
        if v == "N":
            return v

        # case 2: must be 1-4 CJK Han characters
        if 1 <= len(v) <= 4 and re.match(r"^[\u4e00-\u9fff]+$", v):
            return v

        raise ValueError("Invalid root output. Must be 1-4 Han characters or 'N'.")
