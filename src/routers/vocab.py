from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from pathlib import Path

from src.graph.vocab_loader import get_vocab_graph_app
from src.service.vocab_anki_service import get_vocab_anki_service
from src.config import get_app_settings

router = APIRouter(prefix="/vocab", tags=["vocab"])
graph_app = get_vocab_graph_app()
vocab_service = get_vocab_anki_service()
app_settings = get_app_settings()

# Word list directory
WORD_LIST_DIR = Path(__file__).parent.parent.parent / app_settings.word_list_dir


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
    audio_filename: str | None
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
                    "audio_filename": "vocab_abc123def456.mp3",
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
    audio_filename: Optional[str] = None
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
            audio_filename=None,
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
        audio_filename=result.get("audio_filename"),
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
                    audio_filename=result.get("audio_filename"),
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


# ============== New Endpoints: Query & Coverage ==============


class VocabWordsResponse(BaseModel):
    """Response model for listing all vocab words."""
    total_count: int
    words: List[str]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "total_count": 3,
                    "words": ["학생", "선생님", "학교"]
                }
            ]
        }
    )


class TargetsResponse(BaseModel):
    """Response model for listing available target word list files."""
    files: List[str]
    default: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "files": ["korean_words.txt", "beginner.txt", "intermediate.txt"],
                    "default": "korean_words.txt"
                }
            ]
        }
    )


class CoverageResponse(BaseModel):
    """Response model for coverage check."""
    target_word_count: int
    existing_count: int
    missing_count: int
    coverage_percentage: float
    missing_words: List[str]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "target_word_count": 5,
                    "existing_count": 3,
                    "missing_count": 2,
                    "coverage_percentage": 60.0,
                    "missing_words": ["도서관", "친구"]
                }
            ]
        }
    )


@router.get("/words", response_model=VocabWordsResponse)
async def get_vocab_words():
    """Get all vocabulary words from Anki deck."""
    words = await vocab_service.get_all_vocab_words()
    sorted_words = sorted(list(words))

    return VocabWordsResponse(
        total_count=len(sorted_words),
        words=sorted_words
    )


@router.get("/targets", response_model=TargetsResponse)
async def list_target_word_lists():
    """List all available target word list files in the data directory."""
    if not WORD_LIST_DIR.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Word list directory not found: {WORD_LIST_DIR}"
        )

    # Get all .txt files in the directory
    txt_files = sorted([f.name for f in WORD_LIST_DIR.glob("*.txt")])

    if not txt_files:
        raise HTTPException(
            status_code=404,
            detail=f"No target word list files found in {WORD_LIST_DIR}"
        )

    return TargetsResponse(
        files=txt_files,
        default=app_settings.default_word_list
    )


@router.get("/coverage", response_model=CoverageResponse)
async def check_coverage(file: str = None, top_k: int = 10):
    """Check coverage of word list against existing Anki vocab cards.

    Args:
        file: Word list filename (default: korean_words.txt)
        top_k: Number of missing words to return (default: 10, set to 0 for all)
    """
    # Use default file if not specified
    filename = file if file else app_settings.default_word_list
    word_list_file = WORD_LIST_DIR / filename

    # Check if word list file exists
    if not word_list_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Target word list file not found: {filename}. Use /vocab/targets to see available files."
        )

    # Read word list from file
    try:
        with open(word_list_file, 'r', encoding='utf-8') as f:
            word_list = [line.strip() for line in f if line.strip()]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read word list file: {str(e)}"
        )

    # Get all existing vocab words from Anki
    existing_words = await vocab_service.get_all_vocab_words()

    # Convert to set for efficient comparison
    input_words = set(word_list)

    # Calculate coverage
    found = input_words & existing_words
    missing = input_words - existing_words

    coverage_pct = (len(found) / len(input_words) * 100) if input_words else 0.0

    # Sort missing words and limit by top_k
    sorted_missing = sorted(list(missing))
    limited_missing = sorted_missing if top_k <= 0 else sorted_missing[:top_k]

    return CoverageResponse(
        target_word_count=len(input_words),
        existing_count=len(found),
        missing_count=len(missing),
        coverage_percentage=round(coverage_pct, 2),
        missing_words=limited_missing
    )
