from agents.main_agent import agent
from langchain_core.messages import HumanMessage

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
        used_tools = get_used_tools(messages)
        used_tools = list(dict.fromkeys(used_tools)) 
        
        if used_tools:
            print(f"[Tool used] {', '.join(used_tools)} was invoked.")

        if messages:
            print(f"AI: {messages[-1].content}")
        else:
            print(f"AI: {response}")

