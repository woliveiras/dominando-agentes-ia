# Capítulo 4: Fundamentos de Prompting e Raciocínio

Este diretório contém exemplos práticos do **Capítulo 4** do livro "Dominando Agentes de IA", focando em técnicas de prompt engineering e raciocínio com LLMs.

## 📚 Tópicos Abordados

- **In-Context Learning (ICL)**:
  - Zero-shot learning
  - Few-shot learning
  - Many-shot learning
  - Dynamic example selection com embeddings
  - Estratégias de ordenação e seleção de exemplos

- **Chain-of-Thought (CoT) Prompting**:
  - Zero-shot CoT: "Let's think step by step"
  - Few-shot CoT: exemplos com raciocínio
  - Self-consistency: voting com múltiplas cadeias
  - Quando usar CoT vs. raciocínio direto

- **ReAct**: Reasoning + Acting (introdução básica)

## 🚀 Pré-requisitos

### Instalação de Dependências

```bash
uv pip install anthropic openai sentence-transformers scikit-learn numpy
```

### Variáveis de Ambiente

```bash
# API Keys (escolha uma ou ambas)
export ANTHROPIC_API_KEY="sk-ant-..."  # Para usar Claude
export OPENAI_API_KEY="sk-..."         # Para usar GPT-4

# Verificar
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

## 📝 Exemplos (Em Desenvolvimento)

Este capítulo está em desenvolvimento ativo. Os seguintes exemplos serão adicionados:

### 01-zero-shot-vs-few-shot.py
Demonstração de zero-shot vs few-shot learning em classificação de sentimentos.

### 02-dynamic-example-selection.py
Implementação de seleção dinâmica de exemplos usando embeddings semânticos.

### 03-chain-of-thought.py
Comparação de raciocínio direto vs. CoT em problemas matemáticos.

### 04-self-consistency.py
Implementação de self-consistency com voting majoritário.

### 05-react-basic.py
Introdução básica ao padrão ReAct (Reasoning + Acting).

## 🎯 Conceitos-Chave

### In-Context Learning

ICL é a capacidade de modelos grandes aprenderem novas tarefas a partir de exemplos no prompt, sem atualizar pesos:

```python
# Zero-shot
prompt = "Classifique o sentimento: 'Adorei este produto!'"
# Output: "Positivo"

# Few-shot
prompt = """
Classifique o sentimento:

Texto: "Produto incrível!" → Positivo
Texto: "Péssima qualidade." → Negativo
Texto: "Produto ok." → Neutro

Texto: "Adorei este produto!" →
"""
# Output: "Positivo" (mais consistente)
```

### Chain-of-Thought

CoT força o modelo a raciocinar passo-a-passo antes de gerar a resposta final:

```python
# Sem CoT (frequentemente falha)
prompt = "Roger tem 5 bolas. Compra 2 latas de 3. Quantas tem?"
# Output: "8" (ERRADO)

# Com CoT (sucesso)
prompt = """
Roger tem 5 bolas. Compra 2 latas de 3. Quantas tem?
Let's think step by step:
"""
# Output: "1. Roger tem 5 bolas
#          2. Compra 2 latas de 3 = 6 bolas
#          3. Total: 5 + 6 = 11
#          Resposta: 11" (CORRETO)
```

### Self-Consistency

Gera múltiplas cadeias de raciocínio e usa voting para escolher a resposta mais comum:

```python
# Gera 5 respostas com CoT
respostas = ["11", "11", "12", "11", "11"]  # Uma errada
# Voting: 11 aparece 4x, 12 aparece 1x
final = "11"  # Resposta mais comum
```

## 🔬 Experimentos Sugeridos

1. **Comparar Modelos**:
   - Teste GPT-4, Claude, e modelos menores
   - Compare performance em zero-shot vs few-shot
   - Verifique quando CoT melhora a acurácia

2. **Otimizar Exemplos**:
   - Teste diferentes quantidades de exemplos (1, 3, 5, 10)
   - Experimente ordenações diferentes
   - Use dynamic selection vs exemplos fixos

3. **Testar Domínios**:
   - Matemática: problemas aritméticos
   - Código: debugging e análise
   - Texto: classificação, extração de informações
   - Lógica: raciocínio de senso comum

## 📊 Métricas de Avaliação

Para avaliar a eficácia das técnicas de prompting:

```python
# Acurácia simples
accuracy = correct / total

# F1-Score para classificação
from sklearn.metrics import f1_score
f1 = f1_score(y_true, y_pred, average='weighted')

# Cost-Accuracy trade-off
cost_per_token = 0.003  # Claude Sonnet input pricing
total_tokens = sum([len(tokenizer.encode(p)) for p in prompts])
cost = total_tokens * cost_per_token / 1000
cost_efficiency = accuracy / cost
```

## 💡 Dicas Práticas

### Quando usar Zero-Shot
- ✅ Tarefas comuns (tradução, resumo)
- ✅ Minimizar latência e custo
- ✅ Testar rapidamente se o modelo sabe

### Quando usar Few-Shot
- ✅ Formato específico não-trivial
- ✅ Zero-shot inconsistente
- ✅ Ensinar estilo ou tom
- ✅ Domínio específico

### Quando usar Many-Shot
- ✅ Tarefas muito complexas
- ✅ Context window grande disponível
- ✅ Fine-tuning não é viável
- ✅ Alta precisão necessária

### Quando usar CoT
- ✅ Problemas matemáticos/lógicos
- ✅ Raciocínio multi-etapa
- ✅ Debugging de código
- ✅ Planejamento complexo
- ❌ Classificação simples
- ❌ Geração criativa
- ❌ Lookup factual

### Quando usar Self-Consistency
- ✅ Problemas críticos (custo < acurácia)
- ✅ Decisões de alto impacto
- ✅ Inferências paralelas disponíveis
- ❌ Tarefas simples (desperdício)

## 🐛 Troubleshooting

### Erro: "API key not found"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# ou
export OPENAI_API_KEY="sk-..."
```

### CoT não melhora resultados
- Verifique tamanho do modelo (precisa ~10B+ parâmetros)
- Teste variantes de prompt ("Let's think step by step" vs outras)
- Considere few-shot CoT com exemplos de raciocínio

### Few-shot inconsistente
- Aumente número de exemplos (3 → 5 → 10)
- Use dynamic selection com embeddings
- Verifique diversidade dos exemplos

### Custo alto
- Use zero-shot quando possível
- Reduza número de exemplos few-shot
- Evite self-consistency em tarefas simples
- Considere caching de exemplos

## 📖 Referências

### Papers Fundamentais

1. **GPT-3 (Brown et al., 2020)**: Introduziu few-shot ICL
   - [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)

2. **Chain-of-Thought (Wei et al., 2022)**: CoT prompting
   - [Chain-of-Thought Prompting Elicits Reasoning](https://arxiv.org/abs/2201.11903)

3. **Self-Consistency (Wang et al., 2022)**: Voting com múltiplas cadeias
   - [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171)

4. **ReAct (Yao et al., 2022)**: Reasoning + Acting
   - [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)

### Documentação

- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering Guide (DAIR.AI)](https://www.promptingguide.ai/)

## 🤝 Contribuindo

Encontrou formas melhores de estruturar prompts? Compartilhe!

1. Documente suas descobertas
2. Compare com baseline (zero-shot direto)
3. Meça acurácia e custo
4. Abra PR com exemplos

---

**Status**: 🚧 Em desenvolvimento
**Última atualização**: 2025-01-07
