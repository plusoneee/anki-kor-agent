import yaml
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompt"

def load_prompt(name: str) -> dict:
    path = PROMPT_DIR / f"{name}.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)