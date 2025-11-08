# Configuração Claude

Este diretório contém as instruções customizadas para o Claude AI trabalhar neste repositório.

## 📄 Arquivo Principal

- **`instructions.md`**: Contém todas as diretrizes de desenvolvimento para este livro

## 🔧 Como Funciona

### Claude Desktop App

O Claude Desktop lê automaticamente arquivos `.claude/instructions.md` quando você:

1. Configura o projeto nas Preferências
2. Abre conversas relacionadas a este diretório

### Claude via API/MCP

Se você usa Claude via API ou Model Context Protocol:

- Referencie este arquivo como contexto do projeto
- Configure o MCP server para incluir este diretório

## ✅ Verificação

Para testar se Claude está lendo estas instruções:

```
Pergunta: "Quais são os padrões de código para este projeto?"

Resposta esperada: Claude deve mencionar:
- Formato Quarto Markdown (.qmd)
- Português brasileiro
- Código executável (copy-paste-run)
- Estrutura de capítulos específica
```

## 🔗 Mais Informações

- Documentação oficial: https://www.anthropic.com/claude
- Model Context Protocol: https://modelcontextprotocol.io

---

**Última atualização**: 2025-01-04
