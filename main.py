from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routers import vocab_router, listening_router
from src.utils.anki import AnkiConnectionError

app = FastAPI(
    title="Korean Anki Loader API",
    description="A Korean learning tool that creates Anki flashcards for vocabulary and listening practice.",
    version="1.0.0",
)


# Exception handlers
@app.exception_handler(AnkiConnectionError)
async def anki_connection_error_handler(_request: Request, exc: AnkiConnectionError):
    return JSONResponse(
        status_code=503,
        content={
            "status": "error",
            "error": "anki_connection_error",
            "message": str(exc),
            "hint": "請開啟 Anki 應用程式，並確認 AnkiConnect 外掛已安裝並啟用。",
        },
    )


# Include routers
app.include_router(vocab_router)
app.include_router(listening_router)


@app.get("/")
async def root():
    return {
        "message": "Korean Anki Loader API",
        "docs": "/docs",
        "endpoints": {
            "vocab": "/vocab",
            "vocab_batch": "/vocab/batch",
            "listening": "/listening",
            "listening_batch": "/listening/batch",
        },
    }
