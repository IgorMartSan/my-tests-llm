# Arquitetura do projeto

## Visão geral

Este repositório reúne uma plataforma para execução local de modelos de linguagem,
agentes baseados em LangChain/LangGraph e, futuramente, serviços MCP. A arquitetura
da raiz é organizada em três áreas padrão:

- `agents/`: código dos agentes e seus componentes de execução;
- `composes/`: infraestrutura Docker Compose, modelos e serviços compartilhados;
- `mcps/`: serviços MCP, reservado para a expansão futura da plataforma.

O arquivo `docker-compose.yml` é o ponto de entrada da infraestrutura e inclui os
serviços de modelos em `composes/models/` e o stack de observabilidade Langfuse em
`composes/langfuse/`.

## Estrutura de diretórios

```text
.
├── docker-compose.yml                 # Composição principal da infraestrutura
├── test-models.sh                      # Smoke test dos endpoints dos modelos
├── composes/
│   ├── models/
│   │   ├── compose.gemma.yaml          # Gemma servido por vLLM/OpenAI API
│   │   └── compose.laya.yaml           # Serviço Laya
│   └── langfuse/
│       └── compose.langfuse.yaml       # Langfuse e dependências locais
└── agents/
    ├── langchain_agents/               # Projeto principal de agentes
    │   ├── src/
    │   │   ├── main.py                 # Entrada interativa do agente
    │   │   ├── core/                   # Registro e componentes compartilhados
    │   │   └── langchain_agents/        # Implementações de agentes
    │   ├── pyproject.toml
    │   └── Dockerfile
    └── langchain_agent_langfuse_test/  # Exemplo isolado com Langfuse
        ├── src/
        ├── pyproject.toml
        └── Dockerfile
```

`agents/`, `composes/` e `mcps/` são as áreas padrão da raiz. Novas funcionalidades
devem ser colocadas na área correspondente, sem misturar código de agentes com
infraestrutura ou serviços MCP.

## Responsabilidades

### Infraestrutura

- `docker-compose.yml` compõe os serviços selecionados e define a rede
  `agent_platform_network`.
- `composes/models/compose.gemma.yaml` executa o modelo Gemma com vLLM e expõe a
  API compatível com OpenAI na porta `8072`.
- `composes/models/compose.laya.yaml` executa o serviço Laya e expõe sua API na
  porta `8003`.
- `composes/langfuse/compose.langfuse.yaml` executa o Langfuse Web/Worker e suas
  dependências: PostgreSQL, Redis, ClickHouse e MinIO.
- `test-models.sh` verifica a disponibilidade do endpoint de chat do Gemma e do
  healthcheck do Laya.

Os arquivos Compose são responsáveis somente pela execução e configuração dos
serviços. A lógica dos agentes permanece nos projetos Python.

### Serviços MCP

`mcps/` será responsável pelos serviços que expõem ferramentas e integrações por
meio do Model Context Protocol (MCP). Cada serviço MCP deverá ficar isolado em seu
próprio subdiretório, com código, dependências, configuração e, quando necessário,
seu arquivo Compose. A área ainda não possui serviços implementados e não deve ser
tratada como dependência dos agentes até que seus contratos sejam definidos.

### Estrutura obrigatória dos agentes

Todos os agentes, independentemente do modelo utilizado ou da integração com
Langfuse, devem seguir a mesma estrutura interna:

```text
<nome_do_agente>/
├── graphs.py     # construção e compilação do StateGraph
├── nodes.py      # nós e regras de execução do fluxo
└── prompts.py    # prompts usados pelo agente
```

`graphs.py` define o grafo e suas transições; `nodes.py` implementa os nós; e
`prompts.py` concentra os prompts, sem lógica de controle. A entrada (`main.py`),
o registro, a observabilidade e a configuração compartilhada ficam fora do
diretório do agente.

O registro deve apontar para uma fábrica `create_graph` de cada agente. Dessa
forma, todos os agentes possuem o mesmo contrato de criação e podem ser
selecionados sem lógica específica no ponto de entrada. Integrações como Langfuse
devem usar os componentes compartilhados, sem criar uma segunda estrutura de
agente.

### Projeto `langchain_agents`

Este é o projeto principal para agentes LangGraph.

- `src/main.py` coordena a execução interativa, seleciona o agente, mantém o
  identificador da conversa e executa o grafo de forma assíncrona.
- `src/core/registry.py` funciona como registro/fábrica de agentes: recebe o nome
  do agente e devolve o grafo compilado correspondente.
- Os agentes devem seguir a estrutura obrigatória descrita acima.
- O estado do fluxo é baseado em `MessagesState`; o contexto de execução pode
  fornecer dependências compartilhadas, como o modelo de linguagem.
- O checkpoint padrão usado nos exemplos atuais é `InMemorySaver`, adequado para
  testes locais e sem persistência entre reinicializações.
- A observabilidade é integrada no ponto de entrada, por meio do componente
  compartilhado de observabilidade, quando disponível.

### Projeto `langchain_agent_langfuse_test`

Este projeto é um exemplo independente de um agente LangGraph com Langfuse e deve
seguir a mesma estrutura obrigatória dos demais agentes.

- O agente deve separar a configuração do modelo, o grafo, os nós e os prompts em
  seus respectivos módulos; `src/agent.py` só pode permanecer como compatibilidade
  temporária durante a migração da estrutura atual.
- `src/main.py` fornece o loop interativo e cria os callbacks/traces do Langfuse.
- Configurações variáveis, como `LLM_MODEL`, `LLM_URL` e `OPENAI_API_KEY`, são
  obtidas do ambiente; o `.env` é carregado na entrada da aplicação.

Esse projeto não deve ser tratado como dependência interna do projeto principal.
Ele existe para testes e validação da integração com Langfuse.

## Fluxo de execução

```text
Usuário
  │
  ▼
Entrada interativa (main.py)
  │
  ├── seleciona o agente pelo registry (projeto principal)
  │
  ▼
Grafo LangGraph compilado
  │
  ▼
Nó do agente → modelo compatível com OpenAI
  │
  ├── checkpoint em memória
  └── callback/trace Langfuse, quando configurado
  │
  ▼
Resposta exibida ao usuário
```

Na infraestrutura local, o modelo é acessado por HTTP. O Gemma usa
`http://localhost:8072/v1`; os agentes devem receber a URL do modelo por
configuração, em vez de embutir endpoints específicos em regras de negócio.

## Convenções de desenvolvimento

- Preferir a menor alteração compatível com a estrutura existente.
- Reutilizar o registro, os tipos de estado e os componentes compartilhados antes
  de criar novas implementações.
- Manter a separação entre infraestrutura Docker, entrada da aplicação, registro
  de agentes, grafos, nós, prompts e futuros serviços MCP.
- Respeitar a divisão da raiz: agentes em `agents/`, infraestrutura em `composes/`
  e serviços MCP em `mcps/`.
- Não criar camadas, diretórios ou abstrações apenas por antecipação.
- Usar `uv` para dependências e execução dos projetos Python.
- Usar Ruff conforme a configuração de cada `pyproject.toml`.
- Segredos e credenciais devem permanecer em variáveis de ambiente ou arquivos
  locais não versionados; não devem ser adicionados ao código ou aos Compose.

## Estado atual e limites conhecidos

O repositório está em evolução. O projeto `langchain_agents` contém referências
em `src/main.py` e `src/core/registry.py` para módulos (`config`,
`core.observability` e `src.agents.*`) que ainda não estão representados na
estrutura atual. Além disso, o exemplo `langchain_agent_langfuse_test` ainda
concentra o agente em `src/agent.py`, em vez de usar a estrutura obrigatória.
Essas diferenças devem ser resolvidas em alterações próprias, sem alterar este
documento para ocultar a diferença entre a arquitetura desejada e o estado
implementado.

Não há atualmente uma camada de persistência de conversas: o checkpoint em memória
é perdido quando o processo termina. A rede Docker compartilhada está declarada,
mas os arquivos Compose incluídos ainda devem ser avaliados caso seja necessário
que os containers dos agentes acessem os serviços por nome de rede.

## Alterações arquiteturais

Qualquer mudança que introduza novos serviços, projetos, camadas ou contratos de
integração deve atualizar este documento junto com o código afetado.
