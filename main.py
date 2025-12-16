from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routers import vocab_router, listening_router, status_router
from src.utils.anki import AnkiConnectionError
from src.startup import initialize


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 生命週期管理：啟動時初始化 Anki 連線和 Models"""
    await initialize()
    yield
    # 關閉時的清理（目前不需要）


app = FastAPI(
    title="Korean Anki Loader API",
    description="A Korean learning tool that creates Anki flashcards for vocabulary and listening practice.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(status_router)


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
