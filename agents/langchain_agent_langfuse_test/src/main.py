import asyncio

from langfuse import get_client, propagate_attributes
from langfuse.langchain import CallbackHandler

from agent import graph


from dotenv import load_dotenv

load_dotenv()


async def main():
    langfuse = get_client()

    conversation_id = "conversation_123"
    user_id = "user_123"

    try:
        while True:
            message = await asyncio.to_thread(
                input,
                "Você: ",
            )

            if message.lower() in {"sair", "exit"}:
                break

            handler = CallbackHandler()

            with propagate_attributes(
                trace_name="langchain_agent_langfuse_test",
                user_id=user_id,
                session_id=conversation_id,
                tags=["rsa", "langgraph"],
            ):
                result = await graph.ainvoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": message,
                            }
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": conversation_id,
                        },
                        "callbacks": [handler],
                    },
                )

            print(
                "Agente:",
                result["messages"][-1].content,
            )

    finally:
        langfuse.flush()


if __name__ == "__main__":
    asyncio.run(main())
