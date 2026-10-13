from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)

from langgraph.checkpoint.memory import InMemorySaver

from src.agents.rsa.nodes import (
    AgentContext,
    agent_node,
)


def create_graph(checkpointer=None):
    builder = StateGraph(
        MessagesState,
        context_schema=AgentContext,
    )

    builder.add_node("agent", agent_node)

    builder.add_edge(START, "agent")
    builder.add_edge("agent", END)

    return builder.compile(
        checkpointer=checkpointer,
    )
