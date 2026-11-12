# Agente RSA com Langfuse

## Executar o agente

Na raiz deste projeto, execute:

```bash
cd agents/langchain_agent_langfuse_test
uv run python src/main.py
```

Ou:

```bash
uv run python -m src.main
```

## Executar os testes

Os testes devem ser executados na raiz do projeto:

```bash
cd /home/igor/Projetos/DockerLLMTest/agents/langchain_agent_langfuse_test
uv run deepeval test run tests/evals/test_agent.py
```

Não execute `uv run pytest -q` dentro de `src/`, pois os testes ficam em
`tests/evals/`.

O terminal exibirá as perguntas e respostas. O DeepEval executará a métrica
`GEval` usando a LLM local como juíza. Para detalhes dos traces e justificativas,
use `deepeval inspect` após a execução.
