from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper


wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1000
)


@tool
def wikipedia_tool(query: str) -> str:
    """
    Search Wikipedia and return a summary of the topic.

    Use this tool when the user asks for factual information,
    definitions, historical facts, or general knowledge about
    a person, place, event, or concept.
    """

    if not query or not query.strip():
        return "Error: Query cannot be empty."

    try:
        result = wiki_wrapper.run(query.strip())
        if not result:
            return f"No Wikipedia results found for '{query}'."
        return result
    except Exception as e:
        return f"Error while searching Wikipedia: {e}"