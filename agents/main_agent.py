from config import llm
from langchain.agents import create_agent
import tools.calculator_tool as calculator_tool_module
import tools.wikipedia as wikipedia_module
import tools.weather as weather_module
import tools.web_search as web_search_module

tools = [
    calculator_tool_module.calculator_tool,
    wikipedia_module.wikipedia_tool,
    weather_module.weather_tool,
    web_search_module.web_search_tool
]

agent = create_agent(
    llm,
    tools,
    system_prompt = (
    "You are a helpful assistant. "
    "Use the calculator tool when the user asks for arithmetic or percentage calculations. "
    "Use the wikipedia_tool when the user asks for factual, encyclopedic information. "
    "Call tools one at a time with a single query only — never pass multiple queries "
    "or a list in one tool call. If you need multiple lookups, call the tool multiple times, "
    "once per query."
    "For questions about recent events, current data, or anything time-sensitive, "
    "always rely strictly on the web_search_tool results and do not use your own "
    "prior knowledge, since your training data may be outdated."
    )
)