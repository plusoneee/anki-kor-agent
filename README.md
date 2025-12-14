# Anki Kor Agent

A Korean learning agent that uses LangGraph and Azure OpenAI to automatically create Anki flashcards.

## Documentation

- **English**: [docs/README.md](docs/README.md)
- **繁體中文**: [docs/README.zh-TW.md](docs/README.zh-TW.md)

## Quick Start

### Docker (Recommended)

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env with your Azure OpenAI credentials
# 3. Start Anki on your computer
# 4. Run with Docker Compose
docker-compose up -d
```

### Local Development

```bash
# 1. Install dependencies
uv sync

# 2. Create and edit .env file
cp .env.example .env

# 3. Start Anki
# 4. Run the server
uv run uvicorn main:app --reload
```

## Features

- **Vocabulary Cards**: Automatic Korean word parsing with TTS, examples, and structured fields
- **Listening Cards**: Generate audio flashcards from Korean sentences
- **LangGraph Pipeline**: Robust workflow with duplicate detection and error handling
- **Docker Support**: Easy deployment with Docker Compose

For detailed documentation, installation instructions, and API usage, please see:
- [Full English Documentation](docs/README.md)
- [完整中文文檔](docs/README.zh-TW.md)
