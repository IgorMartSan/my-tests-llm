import os

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver


llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "gemma4"),
    base_url=os.getenv("LLM_URL", "http://localhost:8072/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "local"),
    temperature=0.2,
)


async def chatbot(state: MessagesState):
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=InMemorySaver())
