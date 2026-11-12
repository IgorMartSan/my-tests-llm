import os

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

SYSTEM_PROMPT = """
Você é o RSA, um assistente virtual de inteligência artificial.
Responda sempre em português, de forma clara, objetiva e concisa.
Para perguntas sobre suas capacidades, responda em no máximo duas frases.
Explique apenas as capacidades disponíveis e não invente ferramentas ou informações.
"""


llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gemma4"), base_url=os.getenv("LLM_URL", "http://localhost:8072/v1"), api_key=os.getenv("OPENAI_API_KEY", "local"), temperature=0)


async def chatbot(state: MessagesState):
    response = await llm.ainvoke([SystemMessage(content=SYSTEM_PROMPT), *state["messages"]])
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=InMemorySaver())
