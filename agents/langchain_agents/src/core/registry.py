from src.agents.rsa.graphs import create_graph as rsa_graph
from src.agents.support.graphs import create_graph as support_graph


AGENTS = {
    "rsa": rsa_graph,
    "support": support_graph,
}


def get_agent(name: str, checkpointer=None):
    factory = AGENTS.get(name)

    if factory is None:
        raise ValueError(f"Agente não encontrado: {name}")

    return factory(checkpointer=checkpointer)
