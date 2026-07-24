# Multi-Tool AI Agent (LangChain)

An intelligent AI agent built with LangChain that automatically selects the correct tool based on the user's query, from a single CLI chat interface.

## Objective

Build an AI Agent that can understand a user's question and automatically route it to the right tool — calculator, Wikipedia, weather, web search, or a document knowledge base (RAG) — without the user needing to specify which tool to use.

## Features

- **Calculator** — arithmetic expressions and percentage calculations (safe AST-based evaluation, no `eval()`)
- **Wikipedia Search** — retrieves and summarizes factual/encyclopedic information
- **Weather** — fetches current weather conditions for any city (OpenWeatherMap API)
- **Web Search** — searches the web for recent events and time-sensitive information (Tavily API)
- **RAG (Document Search)** — answers questions from PDFs placed in the `documents/` folder, using FAISS + Gemini embeddings
- **Memory** — maintains conversation history so follow-up questions understand prior context
- **Error Handling** — gracefully handles API failures, rate limits, invalid input, and missing documents without crashing

## Tech Stack

- Python 3.11+
- LangChain / LangGraph (`create_agent`)
- Groq (`llama-3.3-70b-versatile`) as the primary LLM
- Google Gemini (`models/gemini-embedding-001`) for embeddings
- FAISS for vector storage
- Tavily for web search
- OpenWeatherMap for weather data
- CLI as the primary interface

## Project Structure

```
multi_tool_agent/
├── app.py                  
├── config.py                
├── .env                     
├── .env.example             
├── requirements.txt
├── README.md
├── agents/
│   └── main_agent.py         
├── tools/
│   ├── calculator.py          
│   ├── calculator_tool.py      
│   ├── wikipedia.py           
│   ├── weather.py               
│   ├── web_search.py             
│   └── rag.py                     
├── vectorstore/
│   └── faiss_index/                
├── documents/                        
└── utils/
```

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd multi_tool_agent
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      
source venv/bin/activate   
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
copy .env.example .env      
cp .env.example .env        
```

Required keys:
```
GROQ_API_KEY=
OPENWEATHER_API_KEY=
TAVILY_API_KEY=
GOOGLE_API_KEY=
```

- Groq: https://console.groq.com
- OpenWeatherMap: https://openweathermap.org/api
- Tavily: https://tavily.com
- Google AI Studio (Gemini): https://aistudio.google.com

### 5. Add a sample PDF for RAG (optional)
Place any `.pdf` file into the `documents/` folder. The vector index will be built automatically the first time a document-related question is asked.

### 6. Run the agent
```bash
python app.py
```

## Usage Examples

```
You: what is 15% of 240
AI: 36.0

You: who is Marie Curie
AI: Marie Curie was a physicist and chemist known for her research on radioactivity...

You: what is the weather in Mumbai
AI: The current weather in Mumbai is light rain with a temperature of 27.5°C...

You: what is the latest news on the champions league final
AI: [uses web search for current information]

You: what is the objective of the project according to the document
AI: [answers using content from the uploaded PDF]
```

Type `exit`, `quit`, or `bye` to end the session.

## How Tool Selection Works

The agent uses a single system prompt that describes when each tool should be used (arithmetic → calculator, factual/encyclopedic → Wikipedia, current weather → weather tool, recent/time-sensitive info → web search, document-specific questions → RAG). The underlying LLM decides which tool (if any) to call based on the user's phrasing, and can call multiple tools across a conversation as needed.

## Error Handling

- API/network failures (Groq rate limits, timeouts) are caught and shown as friendly messages instead of crashing the CLI, with limited automatic retries for transient failures.
- Invalid or empty user input is rejected with a clear message before being sent to the model.
- Missing or empty `documents/` folder is detected by the RAG tool, which returns a clear error instead of failing silently.
- Invalid city names, empty queries, and malformed tool arguments are handled within each individual tool.

## Assumptions & Known Limitations

- The RAG tool only supports PDFs with an actual text layer. Scanned/image-based PDFs (e.g., certificates that are essentially images) are not supported, since no OCR step is implemented.
- The FAISS index is built once from all PDFs present in `documents/` at first use, and cached to `vectorstore/faiss_index/`. Adding new PDFs later requires deleting `vectorstore/faiss_index/` to force a rebuild.
- Free-tier API limits apply (Groq token limits, OpenWeatherMap/Tavily rate limits) — the agent handles rate limit errors gracefully but cannot bypass provider quotas.
- The interface is CLI-only in the current version; a Streamlit UI is an optional future addition.
- Web search accuracy depends on the underlying model correctly prioritizing fresh search results over its own training knowledge; this is mitigated via explicit system prompt instructions but not 100% guaranteed.