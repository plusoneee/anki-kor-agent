# Anki Kor Agent

[繁體中文](README.zh-TW.md)

A Korean learning agent that uses LangGraph and Azure OpenAI to automatically create Anki flashcards. Supports both vocabulary cards and listening cards with TTS audio.

## Features

### Vocabulary Cards (`/vocab`)
- Parse Korean words with LLM to extract meaning, part of speech, and example sentences
- Extract word roots and hanja (Chinese characters) information
- Generate TTS audio for word pronunciation
- Automatically create or update Anki flashcards with structured fields (Word, Audio, Meaning, POS, Examples)
- Duplicate detection to avoid creating redundant cards

### Listening Cards (`/listening`)
- Generate TTS audio from Korean sentences using Google TTS (gTTS)
- Auto-translate Korean to Chinese if translation not provided
- Create listening-focused cards (audio front, text back)
- Automatically create Anki deck and note type

## Architecture

### Vocabulary Pipeline

```mermaid
flowchart LR
    A[START] --> B[check_duplicate]
    B -->|exists| C[END]
    B -->|continue| D[fanout]
    D --> E[parse_word]
    D --> F[extract_root]
    E --> G[build_tags]
    F --> G
    G --> H[build_examples]
    H --> I[generate_tts]
    I --> J[store_audio]
    J --> K[send_to_anki]
    K --> C
```

### Listening Pipeline

```mermaid
flowchart LR
    A[START] --> B[check_duplicate]
    B -->|exists| C[END]
    B -->|continue| D[translate_sentence]
    D --> E[generate_tts]
    E --> F[store_audio]
    F --> G[build_card]
    G --> H[send_to_anki]
    H --> C
```

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- [Anki](https://apps.ankiweb.net/) with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin installed
- Azure OpenAI API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/plusoneee/anki-kor-agent.git
cd anki-kor-agent
```

2. Install dependencies:
```bash
uv sync
```

3. Create your environment file:
```bash
cp .env.example .env
```

4. Edit `.env` with your credentials:
```
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

## Docker Deployment (Recommended)

The easiest way to run the application is using Docker Compose.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- Anki running on your host machine with AnkiConnect plugin

### Quick Start

1. Create `.env` file from example:
```bash
cp .env.example .env
```

2. Edit `.env` with your Azure OpenAI credentials:
```bash
# Required: Add your Azure OpenAI credentials
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

3. Start Anki on your host machine

4. Run with Docker Compose:
```bash
docker-compose up -d
```

5. Access the API at http://localhost:8000

### Docker Commands

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

**Notes:**
- Docker automatically connects to host Anki using `host.docker.internal:8765`
- Audio files persist in `./audio` directory
- Same `.env` file works for both Docker and local development

## Local Development

### Usage

> **Important:** Make sure Anki is running before starting the server. AnkiConnect only works when Anki is open.

1. Start Anki application

2. Run the FastAPI server:
```bash
uv run uvicorn main:app --reload
```

3. The API will be available at http://127.0.0.1:8000

### API Endpoints

#### Vocabulary - Single Word
```bash
curl -X POST http://127.0.0.1:8000/vocab \
  -H "Content-Type: application/json" \
  -d '{"word": "학생", "force_update": false}'
```

#### Vocabulary - Batch
```bash
curl -X POST http://127.0.0.1:8000/vocab/batch \
  -H "Content-Type: application/json" \
  -d '{"words": ["학생", "선생님"], "force_update": false}'
```

#### Listening - Single Sentence
```bash
# With user-provided translation
curl -X POST http://127.0.0.1:8000/listening \
  -H "Content-Type: application/json" \
  -d '{"korean_sentence": "안녕하세요", "chinese_translation": "你好"}'

# Auto-translate with LLM
curl -X POST http://127.0.0.1:8000/listening \
  -H "Content-Type: application/json" \
  -d '{"korean_sentence": "오늘 날씨가 좋아요"}'
```

#### Listening - Batch
```bash
curl -X POST http://127.0.0.1:8000/listening/batch \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {"korean_sentence": "안녕하세요", "chinese_translation": "你好"},
      {"korean_sentence": "감사합니다"}
    ]
  }'
```

### Vocabulary Coverage Check

Track your learning progress by checking how many words from your target list are already in your Anki deck.

#### List Available Target Word Lists
```bash
curl http://127.0.0.1:8000/vocab/targets
```

Response:
```json
{
  "files": ["korean_words.txt", "beginner.txt"],
  "default": "korean_words.txt"
}
```

#### Check Coverage
```bash
# Check default word list (korean_words.txt) with top 10 missing words
curl http://127.0.0.1:8000/vocab/coverage

# Check specific word list
curl http://127.0.0.1:8000/vocab/coverage?file=beginner.txt

# Customize number of missing words returned
curl http://127.0.0.1:8000/vocab/coverage?file=beginner.txt&top_k=20

# Get all missing words (set top_k=0)
curl http://127.0.0.1:8000/vocab/coverage?top_k=0
```

Response:
```json
{
  "target_word_count": 1668,
  "existing_count": 119,
  "missing_count": 1549,
  "coverage_percentage": 7.13,
  "missing_words": ["가게", "가격", "가구", ...]
}
```

#### Get All Vocab Words
```bash
curl http://127.0.0.1:8000/vocab/words
```

**Setting up Target Word Lists:**

1. Create the `data/` directory in your project root (if it doesn't exist)
2. Add your target word list files (one word per line, UTF-8 encoded):
   ```
   data/
   ├── korean_words.txt       # Default target list
   ├── beginner.txt           # Beginner level words
   └── intermediate.txt       # Intermediate level words
   ```
3. You can customize the directory and default file in `.env`:
   ```
   WORD_LIST_DIR=data
   DEFAULT_WORD_LIST=korean_words.txt
   ```

## Configuration

Environment variables (see `.env.example`):

### Azure OpenAI Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | (required) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | (required) |
| `AZURE_OPENAI_API_VERSION` | API version | `2025-01-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | `gpt-4o-mini-0` |

### Anki Vocabulary Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `ANKI_URL` | AnkiConnect URL | `http://127.0.0.1:8765` |
| `ANKI_DECK_NAME` | Target Anki deck | `Korean::Auto` |
| `ANKI_VOCAB_MODEL_NAME` | Anki note type (auto-created) | `Korean_Vocab_Auto` |

### Anki Listening Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `ANKI_LISTENING_DECK_NAME` | Listening deck | `Korean::Listening` |
| `ANKI_LISTENING_MODEL_NAME` | Listening note type | `Listening` |
| `ANKI_LISTENING_TAG_DEFAULT` | Default tag | `listening_auto` |

## Project Structure

```
src/
├── routers/                   # FastAPI routers
│   ├── vocab.py               # /vocab endpoints
│   └── listening.py           # /listening endpoints
├── graph/
│   ├── vocab_loader.py        # Vocabulary LangGraph pipeline
│   └── listening_loader.py    # Listening LangGraph pipeline
├── models/
│   ├── vocab_state.py         # Vocabulary state definition
│   └── listening_state.py     # Listening state definition
├── nodes/
│   ├── vocab/                 # Vocabulary processing nodes
│   └── listening/             # Listening processing nodes
├── service/
│   ├── vocab_anki_service.py
│   └── listening_anki_service.py
├── prompt/                    # LLM prompt YAML files
└── utils/
    ├── anki.py                # AnkiConnect client
    ├── llm.py                 # Azure OpenAI wrapper
    └── tts.py                 # Google TTS wrapper
```
