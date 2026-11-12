from langchain_core.messages import HumanMessage
from langfuse import propagate_attributes
from langfuse.langchain import CallbackHandler

if __package__:
    from src.agent import graph
else:
    from agent import graph


async def run_agent(message: str, thread_id: str, user_id: str) -> str:
    handler = CallbackHandler()

    with propagate_attributes(trace_name="langchain_agent_langfuse_test", user_id=user_id, session_id=thread_id, tags=["rsa", "langgraph"]):
        result = await graph.ainvoke({"messages": [HumanMessage(content=message)]}, config={"configurable": {"thread_id": thread_id}, "callbacks": [handler]})

    return str(result["messages"][-1].content)
