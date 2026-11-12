# Arquitetura do agente Langfuse

## Objetivo

Projeto independente para validar um agente LangGraph conectado a uma LLM local
compatível com a API da OpenAI e instrumentado com Langfuse.

## Estrutura

```text
langchain_agent_langfuse_test/
├── src/
│   ├── main.py       # loop interativo e encerramento do Langfuse
│   ├── service.py    # caso de uso de execução do agente e tracing
│   └── agent.py      # modelo e grafo LangGraph
├── tests/evals/
│   └── test_agent.py
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Responsabilidades

- `src/main.py` carrega o ambiente, recebe mensagens e delega a execução para
  `run_agent`.
- `src/service.py` cria o callback Langfuse, propaga os atributos do trace e
  invoca o grafo.
- `src/agent.py` configura o `ChatOpenAI`, define o nó `chatbot` e compila o
  `StateGraph` com `InMemorySaver`.
- `tests/evals/test_agent.py` define um `EvaluationDataset` com `Golden`, executa
  as perguntas e avalia as respostas com DeepEval.

## Contratos e execução

O serviço expõe `run_agent(message, thread_id, user_id)`, que retorna o conteúdo
textual da última mensagem do grafo. O modelo é configurado por `LLM_MODEL`,
`LLM_URL` e `OPENAI_API_KEY`; os dados do Langfuse são lidos das variáveis
`LANGFUSE_*`.

Para manter compatibilidade entre execução local e Docker, os módulos são
importados pelo pacote `src`:

```bash
uv run python src/main.py
uv run deepeval test run tests/evals/test_agent.py
```

O `Dockerfile` executa o mesmo ponto de entrada como módulo:
`python -m src.main`.

## Limites atuais

O checkpoint é apenas em memória e não persiste conversas após o processo. O
teste de avaliação usa a LLM real e o avaliador configurado pelo DeepEval; ele
precisa dos serviços locais e das credenciais necessárias para ser executado.

## Manutenção

Manter o projeto independente, evitar abstrações desnecessárias e atualizar este
documento caso sejam alterados o contrato de `run_agent`, o fluxo do grafo ou a
integração com Langfuse.
