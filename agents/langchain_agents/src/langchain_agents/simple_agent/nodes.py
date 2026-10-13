from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage

from langgraph.graph import MessagesState
from langgraph.runtime import Runtime

from src.agents.rsa.prompts import SYSTEM_PROMPT


@dataclass
class AgentContext:
    llm: BaseChatModel


async def agent_node(
    state: MessagesState,
    runtime: Runtime[AgentContext],
):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = await runtime.context.llm.ainvoke(messages)

    return {
        "messages": [response],
    }
