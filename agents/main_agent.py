from config import llm
from langchain.agents import create_agent
import tools.calculator_tool as calculator_tool_module
import tools.wikipedia as wikipedia_module
import tools.weather as weather_module
import tools.web_search as web_search_module
import tools.rag as rag_module

tools = [
    calculator_tool_module.calculator_tool,
    wikipedia_module.wikipedia_tool,
    weather_module.weather_tool,
    web_search_module.web_search_tool,
    rag_module.rag_tool,
]

agent = create_agent(
    llm,
    tools,
    system_prompt=(
    "You are a helpful assistant with access to multiple tools. "

    "Use the calculator_tool when the user asks for arithmetic or percentage calculations. "

    "Use the wikipedia_tool when the user asks for factual or encyclopedic information. "

    "Call tools one at a time with a single query only. Never pass multiple queries "
    "or a list in one tool call. If you need multiple lookups, call the tool multiple "
    "times, once per query. "

    "Use the weather_tool when the user asks about current weather conditions, "
    "temperature, or weather forecasts for a specific location. "

    "For questions about recent events, current data, news, or anything time-sensitive, "
    "always use the web_search_tool and rely on its results rather than your own "
    "prior knowledge. "

    "Use the rag_tool when the user asks about the content of an uploaded PDF or document. "
    "This includes requests to summarize, explain, find information, or answer questions "
    "based on a specific uploaded document. If the user mentions a specific PDF filename, "
    "use the rag_tool. If the user says 'the document', 'the PDF', 'according to the "
    "document', or similar, use the rag_tool. "

    "Do not use the rag_tool for general questions about PDFs, PDF software, or document "
    "formats when the question is not asking about the content of an uploaded document."
    )
)