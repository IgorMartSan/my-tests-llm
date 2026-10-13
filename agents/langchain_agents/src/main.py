import asyncio


from config import settings
from core.registry import get_agent
from core.observability import observability


async def main():
    try:
        # Inicializa as conexões compartilhadas
        async with create_connections() as connections:
            # Seleciona e compila o agente
            graph = get_agent(
                name=settings.agent_name,
                checkpointer=InMemorySaver(),
            )

            # Configuração da conversa
            conversation_id = "conversation_123"
            user_id = "user_123"

            while True:
                message = await asyncio.to_thread(input, "Você: ")

                if message.lower() in {"sair", "exit"}:
                    break

                # Callback do Langfuse
                handler = observability.get_handler()

                # Executa o agente
                with observability.trace(
                    agent_id=settings.agent_name,
                    user_id=user_id,
                    conversation_id=conversation_id,
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
                            "callbacks": [handler] if handler else [],
                        },
                        context=connections,
                    )

                print("Agente:", result["messages"][-1].content)

    finally:
        observability.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
