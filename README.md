# TechGear Plus Customer Support Agent

A simple customer support chatbot built with the Gemini File Search API.

This project demonstrates how to build a RAG (Retrieval-Augmented Generation) agent that can answer questions based on your document knowledge base.



NOTE: This agent uses only semantic search. For some uses cases this works but in other cases you may also want a more advanced RAG strategy such as 

1. Reading the full referenced documents to avoid missing context
2. Using a hybrid search strategy for keyword matching.

## Quick Start

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) package manager
- Gemini AI API Key ([get one here](https://aistudio.google.com/app/apikey))

### 2. Installation

```
uv sync
```

### 3. Setup Environment

Create a `.env` file with your API key:

```bash
GEMINI_API_KEY="your-api-key-here"
STORE_NAME="your-store-name-here"
```

### 4. Create File Search Store

Run the setup script to create a new store and upload documents to it:

```bash
uv run setup.py
```

This will:
- Create a file search store
- Upload all PDFs from the `docs/` directory
- Run a sample query
- Output the store name (save this for your `.env` file)

### 5. Run the App Locally

```bash
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
03-gemini-files-api/
├── app/
│   ├── agent.py              # FAQAgent class
│   └── services/
│       ├── file_service.py   # File search operations
│       └── store_service.py  # Store management
├── docs/                     # Knowledge base PDFs
├── app.py                    # Streamlit application
├── setup.py                  # Setup script for creating stores
├── pyproject.toml           # Project dependencies
```

## API Reference

See the official Gemini File Search API documentation:
https://ai.google.dev/gemini-api/docs/file-search
