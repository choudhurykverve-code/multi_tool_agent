import os
from langchain.tools import tool
from langchain_tavily import TavilySearch

API_KEY = os.getenv("TAVILY_API_KEY")

@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for recent or current information.

    Use this tool when the user asks about recent events,
    news, current data, or anything that requires up-to-date
    information not likely known from general knowledge.
    """

    if not query or not query.strip():
        return "Error: Query can not be empty."

    if not API_KEY:
        return "Error: Web search api key not configured."

    try:
        search=TavilySearch(max_result=3)
        result=search.invoke(query.strip())
        return str(result)
    except Exception as e:
        return f"Error: Could not complete web search. ({e})"
 