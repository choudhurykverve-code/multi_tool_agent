from langchain_core.messages import HumanMessage

from agents.main_agent import agent

_session_history = {}


def chat_with_agent(message: str, session_id: str | None = None) -> str:
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")

    key = session_id or "default"
    history = _session_history.setdefault(key, [])
    history.append(HumanMessage(content=message))

    try:
        result = agent.invoke({"messages": history})

        messages = result.get("messages")

        if not messages:
            raise RuntimeError("Agent returned no messages.")

        response = messages[-1].content

        if not response:
            raise RuntimeError("Agent returned an empty response.")

        _session_history[key] = messages
        return response

    except ValueError:
        raise
    except Exception as exc:
        raise RuntimeError(f'Agent execution failed: {exc}') from exc
