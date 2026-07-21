from agents.main_agent import agent
from langchain_core.messages import HumanMessage

def tool_was_used(messages):
    for message in messages:
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            return True

        additional_kwargs = getattr(message, "additional_kwargs", {})
        if isinstance(additional_kwargs, dict) and additional_kwargs.get("tool_calls"):
            return True

    return False

print("=" * 35)
print("     Multi-Tool AI Agent")
print("=" * 35)

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    else:
        response = agent.invoke({"messages": [HumanMessage(content=user_input)]})
        messages = response.get("messages", [])
        used_tool = tool_was_used(messages)

        if used_tool:
            print("[Tool used] calculator tool was invoked.")

        if messages:
            print(f"AI: {messages[-1].content}")
        else:
            print(f"AI: {response}")

