# Multi Tool Agent

A multi-tool AI assistant built with Python, LangChain, and FastAPI. The project can answer questions by choosing the correct specialized tool automatically, and it supports follow-up conversations using session-based memory.

## Overview

This project combines:

- a LangChain agent with multiple tools
- a FastAPI API for integration with frontend apps or other services
- conversation memory so follow-up questions can use previous context in the same session

The system routes prompts to the most suitable tool, such as:

- calculator for arithmetic or percentage questions
- Wikipedia for factual or encyclopedic knowledge
- weather tool for current weather conditions
- web search for time-sensitive or recent information
- RAG for questions based on uploaded PDF documents

## Features

- Math and percentage calculation support
- Wikipedia knowledge lookup
- Weather lookup using OpenWeatherMap
- Web search using Tavily
- RAG over local PDFs using FAISS + embeddings
- FastAPI chat endpoint with CORS support
- In-memory session conversation history

## Tech Stack

- Python 3.11+
- LangChain
- FastAPI
- Pydantic
- Groq LLM
- Google Generative AI
- FAISS
- Tavily
- OpenWeatherMap
- Wikipedia

## Project Structure

```text
multi_tool_agent/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── agents/
│   └── main_agent.py
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── chat.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py
│   └── services/
│       └── chat_service.py
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculator_tool.py
│   ├── weather.py
│   ├── web_search.py
│   ├── wikipedia.py
│   └── rag.py
├── documents/
├── vectorstore/
│   └── faiss_index/
├── .gitignore
└── venv/
```

## Prerequisites

Make sure you have:

- Python 3.11 or higher
- pip installed
- a virtual environment
- valid API keys for the connected services

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd multi_tool_agent
```

2. Create and activate a virtual environment:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add environment variables in a `.env` file:

```bash
copy .env.example .env
```

or:

```bash
cp .env.example .env
```

Example:

```env
GROQ_API_KEY=your_groq_key
OPENWEATHER_API_KEY=your_openweather_key
TAVILY_API_KEY=your_tavily_key
GOOGLE_API_KEY=your_google_key
```

## Running the FastAPI Server

Start the API:

```bash
uvicorn main:app --reload
```

Then open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## API Usage

### Chat endpoint

```http
POST /chat/
```

Example request:

```json
{
  "message": "What is the weather in London?"
}
```

Example response:

```json
{
  "response": "The weather in London is currently cloudy with a temperature of 18°C."
}
```

The API automatically manages a session cookie named `agent_session_id`, so the user does not need to pass a session ID manually. Conversation history is stored in memory for the same browser session.

## RAG / Document Support

Place PDFs in the `documents/` folder to enable document-based queries.

- The app uses a FAISS vector store
- The index is stored under `vectorstore/faiss_index/`
- The agent can answer questions based on document content after indexing

## Tool Routing Behavior

The agent decides which tool to use based on the request type:

- arithmetic / percentage → calculator
- general knowledge → Wikipedia
- weather conditions → weather tool
- recent or current events → web search
- document content questions → RAG

## Conversation Memory

The project includes in-memory conversation history for follow-up prompts.

Example:

1. “What is the weather in London?”
2. “And tomorrow?”

The second question can use the context of the first one without needing the user to pass a session ID explicitly.

## Troubleshooting

### Install dependencies

```bash
pip install -r requirements.txt
```

### App fails to start

- confirm the virtual environment is active
- ensure the `.env` file contains valid keys
- check that dependencies were installed successfully

### Empty or failing responses

- verify Groq/Tavily/OpenWeatherMap/Google keys are valid
- ensure the service quota is not exhausted
- confirm the document directory contains readable PDF files for RAG

## Notes

- Session memory is currently in-memory only and resets when the server restarts.
- The project is intended for local demo, learning, and API integration use.

## License

This project does not currently include a license file. If you plan to publish it publicly, add one before distribution.
