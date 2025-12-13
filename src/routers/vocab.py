from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from src.graph.vocab_loader import get_vocab_graph_app

router = APIRouter(prefix="/vocab", tags=["vocab"])
graph_app = get_vocab_graph_app()


# ============== Request/Response Models ==============


class VocabRequest(BaseModel):
    word: str
    force_update: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"word": "학생", "force_update": False},
                {"word": "감사합니다", "force_update": True},
            ]
        }
    )


class VocabResponse(BaseModel):
    status: str
    meaning: str
    pos: str
    examples: list[dict]
    anki_note_id: int
    tags: list[str]
    root: str | None
    force_update: bool

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "success",
                    "meaning": "學生",
                    "pos": "n",
                    "examples": [
                        {"type": "formal", "kr": "저는 학생입니다.", "zh": "我是學生。"},
                        {"type": "casual", "kr": "나는 학생이야.", "zh": "我是學生。"},
                    ],
                    "anki_note_id": 1234567890,
                    "tags": ["korean_auto", "root_學", "pos_n"],
                    "root": "學",
                    "force_update": False,
                }
            ]
        }
    )


class BatchVocabRequest(BaseModel):
    words: List[str]
    force_update: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"words": ["학생", "선생님", "학교"], "force_update": False},
            ]
        }
    )


class BatchVocabItem(BaseModel):
    word: str
    status: str
    meaning: Optional[str] = None
    pos: Optional[str] = None
    examples: Optional[list] = None
    anki_note_id: Optional[int] = None
    tags: list[str] = []
    root: Optional[str] = None
    error: Optional[str] = None
    force_update: bool = False


class BatchVocabResponse(BaseModel):
    status: str
    results: List[BatchVocabItem]
    success_count: int
    fail_count: int


# ============== Endpoints ==============


@router.post("", response_model=VocabResponse)
async def create_vocab_card(req: VocabRequest):
    """Create a single vocabulary Anki card."""
    initial_state = {"word": req.word, "force_update": req.force_update}
    result = await graph_app.ainvoke(initial_state)

    # Handle case when card already exists (skipped)
    if result.get("exists") is True:
        return VocabResponse(
            status="skipped",
            meaning="(已存在)",
            pos="",
            examples=[],
            anki_note_id=result["anki_note_id"],
            tags=[],
            root=None,
            force_update=req.force_update,
        )

    return VocabResponse(
        status="success",
        meaning=result["meaning"],
        pos=result["pos"],
        examples=result["examples"],
        anki_note_id=result["anki_note_id"],
        tags=result.get("tags", []),
        root=result.get("root"),
        force_update=req.force_update,
    )


@router.post("/batch", response_model=BatchVocabResponse)
async def create_vocab_cards_batch(req: BatchVocabRequest):
    """Create multiple vocabulary Anki cards."""
    results = []

    for word in req.words:
        try:
            initial_state = {
                "word": word,
                "force_update": req.force_update,
            }
            result = await graph_app.ainvoke(initial_state)

            # Handle case when card already exists (skipped)
            if result.get("exists") is True:
                item = BatchVocabItem(
                    word=word,
                    status="skipped",
                    meaning="(已存在)",
                    anki_note_id=result["anki_note_id"],
                    force_update=req.force_update,
                )
            else:
                item = BatchVocabItem(
                    word=word,
                    status="success",
                    meaning=result["meaning"],
                    pos=result["pos"],
                    examples=result["examples"],
                    anki_note_id=result["anki_note_id"],
                    tags=result.get("tags", []),
                    root=result.get("root"),
                    force_update=req.force_update,
                )
        except Exception as e:
            item = BatchVocabItem(
                word=word,
                status="failed",
                error=str(e),
                force_update=req.force_update,
            )

        results.append(item)

    success = sum(1 for r in results if r.status == "success")
    skipped = sum(1 for r in results if r.status == "skipped")
    fail = len(results) - success - skipped

    return BatchVocabResponse(
        status="completed",
        results=results,
        success_count=success,
        fail_count=fail,
    )
