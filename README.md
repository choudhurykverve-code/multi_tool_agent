# Multi Tool Agent with API and FastAPI

A multi-tool AI assistant built with Python, LangChain, and FastAPI. It can answer questions by routing requests to specialized tools such as a calculator, Wikipedia search, weather lookup, web search, and document-based RAG over local PDFs.

The project includes both:

- a terminal chat interface in `app.py`
- a REST API built with FastAPI in `api/`

## Overview

This project is designed to behave like an intelligent agent that decides which tool best matches a user request. For example:

- arithmetic questions → calculator tool
- general knowledge questions → Wikipedia tool
- weather questions → weather tool
- current events / fresh information → web search tool
- content-based questions from uploaded PDFs → RAG tool

The main agent is configured in `agents/main_agent.py` and uses a Groq LLM to decide when to call a tool.

## Features

- Calculator for arithmetic and percentage operations
- Wikipedia lookup for factual and encyclopedic questions
- OpenWeatherMap integration for local weather queries
- Tavily-powered web search for real-time and time-sensitive information
- RAG over PDF documents using FAISS + embeddings
- FastAPI-based chat endpoint for integration into web apps or frontends
- CORS enabled for browser-based clients
- CLI chat experience for local testing and demos

## Tech Stack

- Python 3.11+
- LangChain
- LangGraph agent tooling
- FastAPI
- Pydantic
- Groq LLM
- Google Generative AI for embeddings
- FAISS for vector search
- Tavily for web search
- OpenWeatherMap for weather data
- Wikipedia API and document parsing via Python libraries

## Project Structure

```text
multi_tool_agent/
├── app.py
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
└── .gitignore
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or newer
- pip installed
- API keys for the services you want to use

## Environment Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd multi_tool_agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:

```bash
copy .env.example .env
```

or on macOS/Linux:

```bash
cp .env.example .env
```

5. Fill in the required keys in `.env`:

```env
GROQ_API_KEY=your_groq_key
OPENWEATHER_API_KEY=your_weather_key
TAVILY_API_KEY=your_tavily_key
GOOGLE_API_KEY=your_google_key
```

You can get keys from:

- Groq: https://console.groq.com
- OpenWeatherMap: https://openweathermap.org/api
- Tavily: https://tavily.com
- Google AI Studio: https://aistudio.google.com

## Running the CLI Agent

Start the interactive terminal app:

```bash
python app.py
```

Example:

```text
You: What is 15% of 240?
AI: 36.0

You: What is the weather in Mumbai?
AI: The current weather in Mumbai is light rain and 27.5°C.

You: Who is Marie Curie?
AI: Marie Curie was a physicist and chemist known for her pioneering research on radioactivity.
```

Type `exit`, `quit`, or `bye` to end the session.

## Running the FastAPI Server

Start the API from the project root:

```bash
uvicorn api.main:app --reload
```

The server will run at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Usage

### Chat endpoint

Endpoint:

```http
POST /chat/
```

Request body:

```json
{
  "message": "What is the weather in London?"
}
```

Example with curl:

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the weather in London?"}'
```

Example response:

```json
{
  "response": "The weather in London is currently cloudy with a temperature of 18°C."
}
```

## RAG and Document Support

The RAG tool can answer questions based on PDF files placed in the `documents/` directory.

Steps:

1. Add your PDF files into `documents/`
2. Run a question through the agent or API that references the document
3. The system builds or updates the FAISS vector index automatically

Notes:

- The vector store is saved in `vectorstore/faiss_index/`
- Rebuilding the index may be needed if you add new PDFs
- PDFs with scanned images may not work properly unless OCR support is added

## Tool Behavior

The agent is instructed to route user requests to the correct tool based on the request type:

- calculator → arithmetic, percentages, math operations
- Wikipedia → general factual information
- weather → current or forecast weather for a city
- web search → news, current events, recent facts
- RAG → uploaded document questions and summarization

## Error Handling

The system includes safeguards for:

- missing or empty messages
- API rate limiting
- network failures
- invalid input
- missing document indexes
- empty or unsupported queries

## Notes

- The repository uses local environment variables stored in `.env`
- Sensitive API keys should never be committed to version control
- The project is intended for learning, demos, and custom AI workflows

## Troubleshooting

### FastAPI server won't start

Check that dependencies are installed and that the virtual environment is active:

```bash
pip install -r requirements.txt
```

### Agent returns errors

Confirm that your `.env` file contains valid API keys and that the selected service has available quota.

### RAG does not work

- verify that the PDF file exists in `documents/`
- make sure the file is readable and text-based
- remove the FAISS folder if you want to rebuild the index

## License

This project does not currently define a license file. If you plan to use it publicly, add a license before distribution.
