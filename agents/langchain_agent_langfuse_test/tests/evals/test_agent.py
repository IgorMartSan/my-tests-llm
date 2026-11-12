import asyncio
import os
import uuid

import pytest
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import GEval
from deepeval.models import OpenAIModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

from src.service import run_agent


@pytest.fixture(scope="module")
def agent_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


dataset = EvaluationDataset(
    goldens=[
        Golden(input="Qual é o seu nome?", expected_output="Informar que o nome do agente é RSA."),
        Golden(input="Quem é você?", expected_output="Explicar que é o RSA, um assistente virtual de inteligência artificial."),
        Golden(input="O que você faz?", expected_output="Explicar que pode responder perguntas, fornecer informações e realizar tarefas baseadas em texto."),
    ]
)


# Cria um teste independente para cada pergunta
@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.input)
def test_agent(golden, agent_loop):
    # Executa o agente real
    response = agent_loop.run_until_complete(run_agent(message=golden.input, thread_id=str(uuid.uuid4()), user_id="deepeval_test"))

    # Registra pergunta, resposta e expectativa
    test_case = LLMTestCase(input=golden.input, actual_output=response, expected_output=golden.expected_output)

    # Configura o LLM avaliador
    metric = GEval(
        name="Qualidade da resposta",
        criteria=("Avalie se a resposta atende ao comportamento esperado, é correta, clara e objetiva."),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=0.8,
        model=OpenAIModel(model=os.getenv("LLM_MODEL", "gemma4"), base_url=os.getenv("LLM_URL", "http://localhost:8072/v1"), api_key=os.getenv("OPENAI_API_KEY", "local"), temperature=0),
        verbose_mode=True,
    )

    print(f"\nPergunta: {golden.input}")
    print(f"Resposta do agente: {response}")
    assert_test(test_case=test_case, metrics=[metric])
