# Livro: Dominando Agentes de IA

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Guia Prático para Construção de Sistemas Inteligentes e Autônomos para Produção**

> Livro sobre AI Agents para Pessoas Engenheiras de Software focado em Python, LangChain e LangGraph, ChromaDB, SQLite, RAG, Chain of Thought, LLM, privacidade e segurança com modelos locais com Ollama e remotos com OpenAI e Gemini.

---

## 📖 Sobre Este Livro

**"Dominando Agentes de IA"** é um livro open source mantido pela comunidade, escrito em português com exemplos práticos e executáveis.

### Licença e Uso

Este livro está licenciado sob **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

**Em resumo:**

- Você pode ler, copiar e compartilhar gratuitamente
- Você pode contribuir via pull requests
- Você pode usar em cursos/tutoriais não-comerciais (com atribuição)
- Você pode criar traduções e adaptações (com mesma licença)
- Você **não pode vender** este conteúdo sem autorização
- Você **não pode usar** comercialmente sem autorização

**Venda Comercial:** A venda comercial deste livro (Amazon, editoras, etc.) é **exclusiva do autor**. Para uso comercial, entre em contato.

**Contribuições:** Ao submeter um pull request, você concorda que suas contribuições sejam licenciadas sob os mesmos termos e permite que o autor as inclua em versões comerciais futuras.

📄 **Licenças completas:** [English](LICENSE.md) | [Português](LICENSE.pt-BR.md) | [Español](LICENSE.es.md)

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
