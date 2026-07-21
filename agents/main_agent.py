from config import llm
from langchain.agents import create_agent
import tools.calculator_tool as calculator_tool_module

tools = [calculator_tool_module.calculator_tool]

agent = create_agent(
    llm,
    tools,
    system_prompt="You are a helpful assistant. Use the calculator tool when the user asks for arithmetic or percentage calculations.",
)