# RAG Document Assistant

A customizable RAG (Retrieval-Augmented Generation) assistant built with the Gemini File Search API. Upload your documents and get instant, grounded answers with citations.


## Features
- 🔍 **Semantic Search** — Find relevant information based on meaning, not just keywords
- 📄 **Citation Support** — Answers include references to source documents
- 💬 **Conversation Memory** — Follow-up questions understand context

> **Note:** This agent uses semantic search only. For advanced use cases, consider:
> 1. Reading full referenced documents to avoid missing context
> 2. Using a hybrid search strategy for keyword matching

## Quick Start

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) package manager
- Gemini AI API Key ([get one here](https://aistudio.google.com/app/apikey))

### 2. Installation
```bash
uv sync
```

### 3. Setup Environment
Create a `.env` file:
```bash
GEMINI_API_KEY=your-api-key-here
STORE_NAME=your-store-name-here
```

### 4. Add Your Documents
Place your PDF files in the `docs/` directory.

### 5. Create File Search Store
```bash
uv run setup.py
```
This will:
- Create a file search store
- Upload all PDFs from `docs/`
- Run a sample query
- Output the store name (save this for your `.env` file)

### 6. Run the App
```bash
uv run chainlit run app.py
```
The app will open at `http://localhost:8000`

## Customization

### Change the System Prompt
Edit `app/agent.py` and modify `SYSTEM_PROMPT` to match your use case:

```python
SYSTEM_PROMPT = """
Your custom instructions here...
"""
```

### Change the Welcome Message
Edit `app.py` and update the welcome message in `@cl.on_chat_start`.

## Project Structure
```
├── app/
│   ├── agent.py              # RAG agent with system prompt
│   └── services/
│       ├── file_service.py   # File upload/management
│       └── store_service.py  # Store CRUD operations
├── docs/                     # Your PDF documents
├── app.py                    # Chainlit UI
├── setup.py                  # Setup script
└── pyproject.toml            # Dependencies
```

## API Reference
[Gemini File Search API Documentation](https://ai.google.dev/gemini-api/docs/file-search)
