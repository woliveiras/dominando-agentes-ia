# Instruções GitHub Copilot

Livro técnico sobre construção de sistemas de agentes inteligentes usando LLMs. Conteúdo em Quarto (`.qmd`), exemplos em `book/sandbox/`, datasets em `book/datasets/`.

---

## Padrões de Escrita

### Formato

- **Quarto Markdown** (`.qmd`)
- **Português brasileiro** (pt-BR)
- Tom técnico mas acessível
- Não utilizar emojis
- Evitar bullet points
- Estrutura: `# Capítulo X: Título {.unnumbered}` → Introdução → Conceitos → Exemplos → Exercícios → Conclusão
- Exercícios em arquivo separado na pasta book/chapters/part-xx/exercises/xx-exercises.qmd

### Exercícios

- Exercícios em arquivo separado na pasta `book/chapters/part-xx/exercises/xx-exercises.qmd`
- No final do capítulo, incluir seção breve referenciando os exercícios

Formato da referência no capítulo:

```markdown
## Exercícios Práticos

Este capítulo possui exercícios práticos hands-on que complementam o conteúdo teórico. Os exercícios cobrem [lista de tópicos]. Para acessar os exercícios completos, consulte o arquivo de exercícios da Parte [X].
```

Estrutura do arquivo de exercícios:

```markdown
# Exercícios Práticos: Título do Capítulo {.unnumbered}

Introdução breve.

## Exercício N: Título

**Objetivo:** O que aprenderá

**Por que?** Relevância prática

**Código:**
\`\`\`python
# Código executável completo
\`\`\`

**Desafios:** (opcionais para aprofundamento)
**Reflexão:** (perguntas sobre aplicação real)
```

### Código

- No corpo do texto, somente o trecho importante para o contexto
- No final do capítulo, código completo em seção "Exemplos Completos de Código"

Regras:

- Todos os imports incluídos
- Docstrings em funções
- Comentários `# uv pip install ...` para dependências
- Código completo no final do capítulo com labels `{#sec-exemplo-nome}`
- Referências no texto usando `@sec-exemplo-nome` dentro de callout-note
- Código executável (copy-paste-run)

Exemplo de referência no texto:

```markdown
::: {.callout-note}
# Implementação Completa
Para o exemplo completo de deduplicação com MinHash, veja o @sec-exemplo-minhash-dedup.
:::
```

Exemplo de código completo no final do capítulo:

```markdown
### Exemplo 1: Título do Exemplo {#sec-exemplo-nome}

Descrição do que o exemplo faz.

\`\`\`python
# uv pip install biblioteca

import biblioteca

def funcao_exemplo():
    """Docstring completa."""
    # Implementação completa
    pass
\`\`\`

**Resultados esperados:**
- Métrica 1: valor
- Métrica 2: valor
```

**IMPORTANTE:** O leitor não tem acesso ao diretório `book/sandbox/`. Nunca referencie este caminho no texto dos capítulos. Use apenas as referências `@sec-exemplo-*` para apontar para código no final do próprio capítulo.

### Callouts Quarto

```markdown
::: {.callout-note}
Contexto adicional, matemática opcional
:::

::: {.callout-tip}
Dicas práticas, otimizações
:::

::: {.callout-warning}
Limitações, trade-offs, armadilhas
:::

::: {.callout-important}
Conceitos críticos
:::
```

### Diagramas

Use Mermaid para fluxogramas, sequências, classes.

```{mermaid}
conteúdo
```

### Referências Bibliográficas

Sempre adicionar referências bibliográficas para trabalhos citados.

```markdown
[@vaswani2017attention] para citação única
[@brown2020language; @devlin2018bert] para múltiplas
```

**Em `references.bib`:**

```bibtex
@inproceedings{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  booktitle={NeurIPS},
  year={2017},
  url={https://arxiv.org/abs/1706.03762}
}
```

**Regras:**

- URL obrigatória (arXiv ou DOI preferencial)
- Múltiplos autores: 3 primeiros + `and others` (NÃO use `and ...`)
- Formato chave: `sobrenome+ano+palavra-chave`

### Exercícios

```markdown
### Exercício N: Título

**Objetivo:** O que aprenderá

**Por que?** Relevância prática

**Código:**
```python
# Código executável completo
```

**Desafios:** (opcionais para aprofundamento)
**Reflexão:** (perguntas sobre aplicação real)
```

---

## Padrões Técnicos

- Itálico para termos em inglês
- "tokenização" (não "tokenization")
- "BPE (Byte-Pair Encoding)" primeira vez, depois "BPE"
- *Fertility rate*: taxa de fertilidade = `Total Tokens / Total Palavras`

---

**Erros comuns a evitar:**

- ❌ Prometer conteúdo não entregue na conclusão
- ❌ Código incompleto sem aviso
- ❌ Citar referências inexistentes
- ❌ Exercícios sem datasets
- ❌ Não faça commit do código no Git, eu reviso tudo antes de commitar

--- 

**Última atualização**: 2025-01-04
**Versão**: 2.0
