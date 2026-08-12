from langchain_core.messages import HumanMessage

from agents.main_agent import agent

def chat_with_agent(message:str) -> str:
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")
    try:
        result = agent.invoke(
            {
                "messages":[
                    HumanMessage(content=message)
                ]
            }
        )

        messages = result.get("messages")

        if not messages:
            raise RuntimeError("Agent returned no messages.")

        response = messages[-1].content

        if not response:
            raise RuntimeError("Agent returned an empty response.")

        return response

    except ValueError:
        raise
    except Exception as exc:
        raise RuntimeError(f'Agent execution failed: {exc}') from exc
    