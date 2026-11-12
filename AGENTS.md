# Regras de Desenvolvimento — Codex

## 1. Arquitetura obrigatória

Antes de modificar o código de um módulo:

- Localizar e ler o arquivo `architecture.md` ou `ARCHITECTURE.md` do módulo afetado.
- Consultar também as instruções aplicáveis de `AGENTS.md`.
- Identificar a estrutura de pastas, responsabilidades, dependências e padrões existentes.
- Respeitar a arquitetura definida e a organização atual dos arquivos.
- Não criar novas camadas, diretórios ou padrões arquiteturais sem necessidade.
- Se o arquivo de arquitetura não existir, analisar a estrutura atual e seguir as convenções estabelecidas. Não inventar regras arquiteturais.
- Se a alteração modificar a arquitetura, atualizar sua documentação.

## 2. Análise antes da implementação

Antes de criar qualquer funcionalidade:

- Procurar implementações semelhantes no módulo e em componentes compartilhados.
- Verificar se já existem funções, classes, serviços ou utilitários reutilizáveis.
- Identificar os arquivos realmente necessários para a alteração.
- Priorizar a reutilização em vez da duplicação.
- Evitar modificações fora do escopo solicitado.

## 3. Princípios obrigatórios

- **DRY:** evitar duplicação de regras de negócio e implementações.
- **KISS:** preferir soluções simples, legíveis e de fácil manutenção.
- **YAGNI:** não criar funcionalidades, abstrações ou configurações para necessidades hipotéticas.
- **Single Responsibility:** manter responsabilidades claras, sem fragmentar excessivamente o código.
- **Consistência:** seguir nomenclatura, organização e convenções do projeto.

Evitar interfaces desnecessárias, wrappers sem benefício, abstrações prematuras e funções auxiliares que aumentem a complexidade sem melhorar a clareza.

## 4. Implementação

- Realizar a menor alteração possível que resolva corretamente o problema.
- Manter compatibilidade com contratos e comportamentos existentes.
- Evitar dependências novas quando as atuais forem suficientes.
- Não refatorar código não relacionado à tarefa.
- Manter a solução simples, testável e coerente com o módulo.

## 5. Revisão obrigatória de redundância e simplicidade

Depois da implementação e antes de finalizar, realizar uma revisão do código alterado.

Verificar:

- Existe código duplicado que pode ser reutilizado?
- Foram criadas funções, classes ou arquivos desnecessários?
- Alguma abstração pode ser removida?
- Existe lógica mais simples para resolver o mesmo problema?
- Há condicionais, validações ou transformações redundantes?
- A implementação respeita a arquitetura do módulo?
- O código pode ficar mais legível sem alterar o comportamento?

Aplicar simplificações seguras e diretamente relacionadas à tarefa. Não remover validações necessárias, tratamento de erros ou funcionalidades existentes apenas para reduzir linhas de código.

## 6. Testes e validação

- Executar os testes relacionados à modificação.
- Criar ou atualizar testes quando houver alteração de comportamento.
- Executar os verificadores de lint, formatação e tipos disponíveis e relevantes.
- Verificar se as simplificações não introduziram regressões.
- Não considerar a tarefa concluída sem relatar o resultado das verificações.
- Caso algum teste não possa ser executado, informar o motivo.

## 7. Fluxo obrigatório

Seguir esta sequência:

**ANALISAR → LER ARQUITETURA → PROCURAR REUTILIZAÇÃO → IMPLEMENTAR → TESTAR → REVISAR REDUNDÂNCIA → SIMPLIFICAR → VALIDAR → FINALIZAR**

Antes de finalizar, confirmar que:

- A arquitetura foi respeitada.
- Não há duplicações desnecessárias introduzidas.
- O código está tão simples quanto possível sem prejudicar a manutenção.
- Os testes e verificações relevantes foram executados ou suas limitações foram informadas.
- Nenhuma alteração desnecessária foi realizada.

## 8. Resumo final

Ao concluir, informar brevemente:

1. O que foi modificado.
2. Qual documentação arquitetural foi consultada.
3. Quais reutilizações ou simplificações foram feitas.
4. Quais testes e verificações foram executados e seus resultados.
5. Quais pendências permanecem, se houver.

Evitar relatórios extensos quando a alteração for simples.