
# Instruções Copilot para o livro Dominando Agentes de IA

## Projeto

Este repositório é um livro prático para construção de sistemas inteligentes e autônomos para produção, com foco em orquestração de multi-agentes no mundo real e integração com LLMs.


## Arquitetura & Estrutura

- **Agentes**: A lógica principal está em `agents/` (ex: triage, scheduling, matching, notification, optimization, orchestrator). Cada agente é um módulo especializado; a orquestração é feita em `agents/orchestrator/`.
- **Packages**: Ferramentas compartilhadas, templates de prompt, gerenciamento de memória e avaliadores estão em `packages/`.
- **CLI**: Ferramentas de desenvolvimento e depuração estão em `cli/` (ex: `chat.py`, `test_agent.py`, `debug.py`).
- **Shared**: Código comum (modelos de banco de dados, schemas) está em `shared/`.
- **Infrastructure**: API (`infrastructure/api/`), web (`infrastructure/web/`) e configs Docker

## Convenções Principais

- **Agentes comunicam via orquestrador**: Workflows multi-agentes são coordenados em `agents/orchestrator/`.
- **Ferramentas são modulares**: Defina novas ferramentas em `packages/tools/` e prompts em `packages/prompts/`.
- **Memória e avaliação**: Use `packages/memory/` para estado dos agentes e `packages/evaluators/` para checagem de qualidade.
- **Testes**: Use scripts CLI (`cli/test_agent.py`) para testar e depurar agentes.
- **Compliance & Segurança**: O tratamento de dados deve estar em conformidade com requisitos de privacidade e regulamentação (ex: LGPD, CFM) conforme descrito na documentação do projeto.

## Fluxos de Trabalho do Desenvolvedor

- **Desenvolvimento de agentes**: Implemente novos agentes em `agents/`, registre-os no orquestrador e exponha ferramentas via `packages/tools/`.
- **Testes**: Execute testes de agentes e sessões de depuração usando scripts CLI.
- **Engenharia de prompts**: Armazene e atualize templates de prompt em `packages/prompts/`.
- **Gerenciamento de memória**: Persista e recupere o estado dos agentes usando `packages/memory/`.

## Exemplos

- Para adicionar um agente de triagem: crie `agents/triage/triage_agent.py`, registre no orquestrador e defina ferramentas/prompts conforme necessário.
- Para adicionar uma nova ferramenta: implemente em `packages/tools/` e atualize a lógica do agente para utilizá-la.
- Para testar um agente: execute `python cli/test_agent.py --agent triage`.

## Referências

- Veja `docs/projeto_guia.md` para detalhes de arquitetura e workflows.
- Veja `docs/estrutura.md` para filosofia do projeto e escopo de aprendizado.
- Veja `docs/sumario.md` para teoria de agentes e técnicas práticas.
- Veja `docs/quick_start.md` para configuração rápida e primeiros passos.
