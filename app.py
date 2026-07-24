from agents.main_agent import agent
from langchain_core.messages import HumanMessage
import time


def get_used_tools(messages):
    used_tools = []

    for message in messages:
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                name = call.get("name", "unknown_tool")
                used_tools.append(name)

        additional_kwargs = getattr(message, "additional_kwargs", {})
        if isinstance(additional_kwargs, dict) and additional_kwargs.get("tool_calls"):
            for call in additional_kwargs["tool_calls"]:
                name = call.get("function", {}).get("name", "unknown_tool")
                used_tools.append(name)

    return used_tools


def get_ai_text(message):
    content = message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        return "\n".join(texts) if texts else str(content)

    return str(content)


def safe_invoke(agent, messages, retries=2):
    for attempt in range(retries + 1):
        try:
            return agent.invoke({"messages": messages})
        except Exception as e:
            error_text = str(e)

            if "rate_limit" in error_text.lower() or "429" in error_text:
                return {"messages": [], "error": "Rate limit reached. Please wait a few minutes and try again."}

            if attempt < retries:
                print(f"[Retrying... attempt {attempt + 1}]")
                time.sleep(2)
                continue

            return {"messages": [], "error": f"Something went wrong: {error_text}"}

    return {"messages": [], "error": "Unknown error occurred."}


print("=" * 35)
print("     Multi-Tool AI Agent")
print("=" * 35)

conversation_history = []

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        break

    if not user_input.strip():
        print("AI: Please enter a valid question.")
        continue

    conversation_history.append(HumanMessage(content=user_input))

    response = safe_invoke(agent, conversation_history)

    if "error" in response:
        print(f"AI: {response['error']}")
        continue

    messages = response.get("messages", [])
    conversation_history = messages

    used_tools = get_used_tools(messages)
    used_tools = list(dict.fromkeys(used_tools))

    if used_tools:
        print(f"[Tool used] {', '.join(used_tools)} was invoked.")

    if messages:
        print(f"AI: {get_ai_text(messages[-1])}")
    else:
        print(f"AI: {response}")