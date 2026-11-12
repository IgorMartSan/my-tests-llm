import asyncio

from dotenv import load_dotenv

load_dotenv()

from langfuse import get_client
from src.service import run_agent


async def main():
    langfuse = get_client()

    conversation_id = "conversation_123"
    user_id = "user_123"

    try:
        while True:
            message = await asyncio.to_thread(input, "Você: ")

            if message.lower() in {"sair", "exit"}:
                break

            response = await run_agent(message=message, thread_id=conversation_id, user_id=user_id)

            print("Agente:", response)

    finally:
        langfuse.flush()


if __name__ == "__main__":
    asyncio.run(main())
