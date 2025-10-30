# Livro: Dominando Agentes de IA

**Guia Prático para Construção de Sistemas Inteligentes e Autônomos para Produção**

> Produção de livro sobre AI Agents para Pessoas Engenheiras de Software focado em Python, LangChain e LangGraph, ChromaDB, SQLite, RAG, Chain of Thought, LLM, privacidade e segurança com modelos locais com Ollama e remotos com OpenAI e Gemini.

---

## Dependências

- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [Quarto](https://quarto.org/docs/get-started/)

## Iniciando

```bash
# Clone o repositório
git clone git@github.com:woliveiras/dominando-agentes-ia.git
cd dominando-agentes-ia

# Instale as dependências
uv sync
quarto install tinytex
```

## Construindo o Livro

```bash
# Navegue até o diretório do livro
cd book

# Preview
quarto preview

# Renderize o livro para PDF e HTML
quarto render --to pdf
quarto render --to html

# Ou diretamente 
quarto render
```
