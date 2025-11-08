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

### Código

- No corpo do texto, somente o trecho importante para o contexto
- No final do capítulo, código completo

Regras:

- Todos os imports incluídos
- Docstrings em funções
- Comentários `# uv pip install ...` para dependências
- Código também em arquivo separado em `book/sandbox/chapter-XX/`

Exemplo: 

**SEMPRE executável (copy-paste-run):**
```python
# uv pip install transformers torch  # Dependências no topo

import torch
from transformers import AutoModelForCausalLM

def exemplo_funcional():
    """Docstring clara."""
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    return model

# Exemplo de uso
model = exemplo_funcional()
```

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
