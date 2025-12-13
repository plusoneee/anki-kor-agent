from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from src.graph.listening_loader import get_listening_graph_app

router = APIRouter(prefix="/listening", tags=["listening"])
graph_app = get_listening_graph_app()


# ============== Request/Response Models ==============


class ListeningRequest(BaseModel):
    korean_sentence: str
    chinese_translation: Optional[str] = None
    force_update: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "korean_sentence": "오늘 날씨가 좋아요",
                    "chinese_translation": "今天天氣很好",
                    "force_update": False,
                },
                {
                    "korean_sentence": "밥 먹었어요?",
                    "chinese_translation": None,
                    "force_update": False,
                },
            ]
        }
    )


class ListeningResponse(BaseModel):
    status: str
    korean_sentence: str
    chinese_translation: str
    translation_source: str
    audio_filename: str
    anki_note_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "success",
                    "korean_sentence": "오늘 날씨가 좋아요",
                    "chinese_translation": "今天天氣很好",
                    "translation_source": "user",
                    "audio_filename": "listening_abc123def456.mp3",
                    "anki_note_id": 1234567890,
                }
            ]
        }
    )


class ListeningBatchItem(BaseModel):
    korean_sentence: str
    chinese_translation: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"korean_sentence": "안녕하세요", "chinese_translation": "你好"},
                {"korean_sentence": "감사합니다", "chinese_translation": None},
            ]
        }
    )


class BatchListeningRequest(BaseModel):
    sentences: List[ListeningBatchItem]
    force_update: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "sentences": [
                        {"korean_sentence": "안녕하세요", "chinese_translation": "你好"},
                        {"korean_sentence": "감사합니다", "chinese_translation": "謝謝"},
                        {"korean_sentence": "맛있어요"},
                    ],
                    "force_update": False,
                }
            ]
        }
    )


class BatchListeningResultItem(BaseModel):
    korean_sentence: str
    status: str
    chinese_translation: Optional[str] = None
    translation_source: Optional[str] = None
    audio_filename: Optional[str] = None
    anki_note_id: Optional[int] = None
    error: Optional[str] = None


class BatchListeningResponse(BaseModel):
    status: str
    results: List[BatchListeningResultItem]
    success_count: int
    fail_count: int


# ============== Endpoints ==============


@router.post("", response_model=ListeningResponse)
async def create_listening_card(req: ListeningRequest):
    """Create a single listening Anki card with TTS audio."""
    initial_state = {
        "korean_sentence": req.korean_sentence,
        "chinese_translation": req.chinese_translation,
        "force_update": req.force_update,
    }
    result = await graph_app.ainvoke(initial_state)

    # Handle case when card already exists (skipped)
    if result.get("exists") is True:
        return ListeningResponse(
            status="skipped",
            korean_sentence=result["korean_sentence"],
            chinese_translation="(已存在)",
            translation_source="skipped",
            audio_filename="(已存在)",
            anki_note_id=result["anki_note_id"],
        )

    return ListeningResponse(
        status="success",
        korean_sentence=result["korean_sentence"],
        chinese_translation=result["translation"],
        translation_source=result["translation_source"],
        audio_filename=result["audio_filename"],
        anki_note_id=result["anki_note_id"],
    )


@router.post("/batch", response_model=BatchListeningResponse)
async def create_listening_cards_batch(req: BatchListeningRequest):
    """Create multiple listening Anki cards with TTS audio."""
    results = []

    for sentence_req in req.sentences:
        try:
            initial_state = {
                "korean_sentence": sentence_req.korean_sentence,
                "chinese_translation": sentence_req.chinese_translation,
                "force_update": req.force_update,
            }
            result = await graph_app.ainvoke(initial_state)

            # Handle case when card already exists (skipped)
            if result.get("exists") is True:
                item = BatchListeningResultItem(
                    korean_sentence=sentence_req.korean_sentence,
                    status="skipped",
                    chinese_translation="(已存在)",
                    translation_source="skipped",
                    audio_filename="(已存在)",
                    anki_note_id=result["anki_note_id"],
                )
            else:
                item = BatchListeningResultItem(
                    korean_sentence=sentence_req.korean_sentence,
                    status="success",
                    chinese_translation=result["translation"],
                    translation_source=result["translation_source"],
                    audio_filename=result["audio_filename"],
                    anki_note_id=result["anki_note_id"],
                )
        except Exception as e:
            item = BatchListeningResultItem(
                korean_sentence=sentence_req.korean_sentence,
                status="failed",
                error=str(e),
            )

        results.append(item)

    success = sum(1 for r in results if r.status == "success")
    skipped = sum(1 for r in results if r.status == "skipped")
    fail = len(results) - success - skipped

    return BatchListeningResponse(
        status="completed",
        results=results,
        success_count=success,
        fail_count=fail,
    )
