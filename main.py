# src/api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.graph.anki_loader import get_graph_app

from typing import List, Optional


app = FastAPI(title="Word Parser API")
graph_app = get_graph_app()


class WordRequest(BaseModel):
    word: str
    force_update: bool = True


class WordResponse(BaseModel):
    status: str
    meaning: str
    pos: str
    examples: list[dict]
    anki_note_id: int
    tags: list[str]
    root: str | None
    force_update: bool


class BatchWordRequest(BaseModel):
    words: List[str]
    force_update: bool = False


class BatchWordItem(BaseModel):
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


class BatchWordResponse(BaseModel):
    status: str
    results: List[BatchWordItem]
    success_count: int
    fail_count: int


@app.post("/parse")
async def parse_word_api(req: WordRequest):
    initial_state = {"word": req.word, "force_update": req.force_update}
    result = await graph_app.ainvoke(initial_state)
    return WordResponse(
        status="success",
        meaning=result["meaning"],
        pos=result["pos"],
        examples=result["examples"],
        anki_note_id=result["anki_note_id"],
        tags=result.get("tags", []),
        root=result.get("root"),
        force_update=req.force_update,
    )


@app.post("/parse-batch", response_model=BatchWordResponse)
async def parse_word_batch(req: BatchWordRequest):
    results = []

    for word in req.words:
        try:
            initial_state = {
                "word": word,
                "force_update": req.force_update,
            }
            result = await graph_app.ainvoke(initial_state)

            item = BatchWordItem(
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
            item = BatchWordItem(
                word=word,
                status="failed",
                error=str(e),
                force_update=req.force_update,
            )

        results.append(item)

    success = sum(1 for r in results if r.status == "success")
    fail = len(results) - success

    return BatchWordResponse(
        status="completed",
        results=results,
        success_count=success,
        fail_count=fail,
    )
