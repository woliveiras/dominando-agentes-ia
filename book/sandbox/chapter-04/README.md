# Capítulo 4: Fundamentos de Prompting e Raciocínio

Este diretório contém **três exercícios práticos completos** do Capítulo 4 do livro "Dominando Agentes de IA", focando em técnicas avançadas de prompt engineering e raciocínio com LLMs.

## 📚 Tópicos Abordados

- **In-Context Learning (ICL)**:
  - Zero-shot, few-shot e many-shot learning
  - Seleção dinâmica de exemplos via embeddings semânticos
  - Estratégias de ordenação e diversidade

- **Chain-of-Thought (CoT) Prompting**:
  - Zero-shot CoT: "Let's think step by step"
  - Few-shot CoT: exemplos com raciocínio explícito
  - Self-consistency: voting com múltiplas cadeias de raciocínio
  - Trade-offs: acurácia vs. custo vs. latência

- **ReAct Framework**:
  - Reasoning + Acting
  - Implementação de agentes com ferramentas
  - Loop Pensamento-Ação-Observação

---

## 🚀 Instalação

### Dependências Necessárias

```bash
uv pip install sentence-transformers scikit-learn numpy
```

### APIs Opcionais (para produção)

```bash
uv pip install openai anthropic
```

**Nota:** Os exercícios incluem simulação de LLMs para execução **sem API keys**. Para uso em produção, configure:

```bash
export OPENAI_API_KEY="sk-..."         # Para GPT-4
export ANTHROPIC_API_KEY="sk-ant-..."  # Para Claude
```

---

## 📝 Exercícios Práticos

### Exercício 1: Few-Shot Dynamic Classifier

**Arquivo:** `01-few-shot-classifier.py`  
**Dataset:** `../../datasets/sentiment_examples.jsonl`

**Objetivo:** Implementar classificador de sentimento com seleção dinâmica de exemplos baseada em similaridade semântica.

**Conceitos:**
- In-Context Learning (ICL)
- Embeddings para seleção de exemplos
- Comparação: seleção aleatória vs. semântica

**Execução:**
```bash
python 01-few-shot-classifier.py
```

**Output esperado:**
```
Avaliação: Seleção Aleatória
Acurácia: 65.0% (13/20)

Avaliação: Seleção Semântica
Acurácia: 85.0% (17/20)

Melhoria com seleção semântica: +20.0%
```

**Desafios adicionais:**
1. Experimentar diferentes valores de `k` (3, 5, 10 exemplos)
2. Comparar modelos de embedding (all-MiniLM-L6-v2 vs. multilingual-e5-base)
3. Implementar diversidade nos exemplos selecionados (evitar redundância)
4. Adicionar cache de embeddings em disco

---

### Exercício 2: Chain-of-Thought Math Solver

**Arquivo:** `02-cot-math-solver.py`  
**Dataset:** `../../datasets/math_problems.jsonl`

**Objetivo:** Implementar solver de problemas matemáticos usando Chain-of-Thought com self-consistency.

**Conceitos:**
- Zero-shot CoT: "Let's think step by step"
- Few-shot CoT: exemplos com raciocínio passo a passo
- Self-consistency: geração de múltiplas soluções + voting
- Análise de custo vs. acurácia

**Execução:**
```bash
python 02-cot-math-solver.py
```

**Output esperado:**
```
Zero-Shot CoT:
Acurácia: 60.0% (9/15)
Custo estimado: $0.003

Few-Shot CoT:
Acurácia: 73.3% (11/15)
Custo estimado: $0.005

Self-Consistency (N=5):
Acurácia: 86.7% (13/15)
Custo estimado: $0.025
Confiança média: 0.85
```

**Desafios adicionais:**
1. Implementar extração robusta de resposta numérica (regex aprimorado)
2. Adicionar detecção de erros de raciocínio (contradições)
3. Experimentar prompt variations ("Think step by step" vs. "Solve carefully")
4. Medir token usage real e calcular custo exato (com APIs)

---

### Exercício 3: Simple ReAct Agent

**Arquivo:** `03-simple-react-agent.py`

**Objetivo:** Implementar agente ReAct básico com ferramentas simples (calculadora, temperatura, conversor de moeda).

**Conceitos:**
- ReAct framework (Reasoning + Acting)
- Parsing de Pensamento/Ação/Observação
- Tool usage e registry
- Loop iterativo com limite de passos

**Ferramentas implementadas:**
- `calculator`: Avalia expressões matemáticas
- `get_temperature`: Retorna temperatura de cidades (mock)
- `convert_currency`: Converte entre moedas (mock)

**Execução:**
```bash
python 03-simple-react-agent.py
```

**Output esperado:**
```
Pergunta: Qual a temperatura em São Paulo?

Pensamento: Preciso obter informações sobre temperatura
Ação: get_temperature("São Paulo")
Observação: 28°C

Pensamento: Tenho a informação necessária
Resposta Final: A temperatura em São Paulo é 28°C.
```

---

## 🔧 Implementação em Produção

### Substituindo Simulação por APIs Reais

Todos os exercícios incluem funções `simulate_*` para execução sem API keys. Para produção:

**OpenAI (GPT-4):**
```python
from openai import OpenAI

client = OpenAI(api_key="sua-api-key")

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
```

**Anthropic (Claude):**
```python
import anthropic

client = anthropic.Anthropic(api_key="sua-api-key")

def call_llm(prompt: str) -> str:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

---

## 📊 Métricas e Análise

### Exercício 1: Few-Shot Classifier

| Método | Acurácia | Tokens/Req | Custo/1K |
|--------|----------|------------|----------|
| Random | ~65% | 350 | $0.0007 |
| Semantic | ~85% | 350 | $0.0007 |

**Insight:** Seleção semântica melhora acurácia em 20-30% sem custo adicional.

### Exercício 2: CoT Math Solver

| Método | Acurácia | Tokens/Req | Custo/1K |
|--------|----------|------------|----------|
| Zero-Shot CoT | ~60% | 200 | $0.0004 |
| Few-Shot CoT | ~73% | 400 | $0.0008 |
| Self-Consistency (N=5) | ~87% | 2000 | $0.0040 |

**Insight:** Self-consistency aumenta acurácia em +14%, mas com 5× no custo.

### Exercício 3: ReAct Agent

| Tipo de Pergunta | Passos | Tokens | Sucesso |
|------------------|--------|--------|---------|
| Single-tool | 1-2 | 300 | 95% |
| Multi-tool | 3-5 | 800 | 85% |
| Raciocínio puro | 2-3 | 400 | 90% |

**Insight:** Agentes ReAct adicionam overhead (2-3× tokens), mas permitem uso de ferramentas externas.

---

## � Conceitos-Chave

### In-Context Learning (ICL)

ICL permite modelos aprenderem novas tarefas a partir de exemplos no prompt, sem fine-tuning:

```python
# Zero-shot: apenas instrução
prompt = "Classifique o sentimento: 'Adorei este produto!'"
# Output: "Positivo"

# Few-shot: instrução + exemplos
prompt = """
Classifique o sentimento:

"Produto incrível!" → Positivo
"Péssima qualidade." → Negativo
"Produto ok." → Neutro

"Adorei este produto!" →
"""
# Output: "Positivo" (mais consistente e confiável)
```

**Quando usar:**
- **Zero-shot:** Tarefas simples, modelos grandes (GPT-4, Claude)
- **Few-shot:** Tarefas complexas, domínios específicos, modelos médios
- **Many-shot:** Tarefas sutis, alta acurácia necessária, contexto longo disponível

### Chain-of-Thought (CoT)

CoT força o modelo a raciocinar passo-a-passo antes de gerar a resposta final:

```python
# Sem CoT (frequentemente falha)
prompt = "Roger tem 5 bolas. Compra 2 latas de 3 bolas cada. Quantas bolas tem agora?"
# Output: "8 bolas" (ERRADO: 5 + 2 = 7? Confundiu latas com bolas)

# Com CoT (sucesso)
prompt = """
Roger tem 5 bolas. Compra 2 latas de 3 bolas cada. Quantas bolas tem agora?

Let's think step by step:
"""
# Output: "1. Roger inicialmente tem 5 bolas
#          2. Ele compra 2 latas
#          3. Cada lata contém 3 bolas
#          4. Total de bolas novas: 2 × 3 = 6
#          5. Total final: 5 + 6 = 11
#          Resposta: 11 bolas" (CORRETO)
```

**Quando usar CoT:**
- ✅ Raciocínio matemático, lógica, planejamento multi-etapa
- ✅ Problemas onde o modelo erra frequentemente no direct answer
- ❌ Classificação simples (overhead desnecessário)
- ❌ Tarefas de alta latência crítica (CoT dobra tokens)

### Self-Consistency

Gera múltiplas cadeias de raciocínio independentes e usa voting majoritário:

```python
# Problema: "João tem 3 maçãs. Compra o dobro. Quantas tem?"

# Gera 5 soluções com CoT (diferentes samples via temperature > 0)
respostas = [
    "3 + (3 × 2) = 9",    # Interpretação 1: dobro = adiciona 6
    "3 × 2 = 6",          # Interpretação 2: dobro = multiplica total
    "3 + (3 × 2) = 9",    # Maioria concorda
    "3 + (3 × 2) = 9",
    "3 × 2 = 6"
]

# Voting: "9" aparece 3×, "6" aparece 2×
final = "9"  # Resposta mais comum (maior confiança)
```

**Trade-off:**
- **Custo:** 5-10× mais chamadas de API
- **Acurácia:** +5-15% em problemas difíceis (GSM8K, MATH)
- **Quando usar:** Decisões críticas (médica, financeira), problemas ambíguos

---

## 🔬 Experimentos Sugeridos

Após completar os exercícios base, explore:

1. **Comparar Modelos**:
   - Teste GPT-4, Claude 3.5, Gemini 2.0, Llama 3.1 70B
   - Compare zero-shot vs few-shot em cada modelo
   - Identifique quando CoT melhora (e quando não melhora)

2. **Otimizar Seleção de Exemplos**:
   - Experimente k = {1, 3, 5, 10} exemplos
   - Teste ordenações: aleatória, cronológica, por similaridade
   - Implemente diversidade (evitar exemplos redundantes)

3. **Domínios Diversos**:
   - **Matemática:** GSM8K, MATH dataset
   - **Código:** HumanEval, debugging tasks
   - **Texto:** classificação multi-label, extração de entidades
   - **Raciocínio:** ARC Challenge, StrategyQA

4. **Custo vs. Qualidade**:
   - Calcule custo real por tarefa (tokens × preço)
   - Compare: GPT-4 zero-shot vs. Llama 3 few-shot
   - Encontre ponto ótimo para seu caso de uso

---

## 💡 Questões para Reflexão

Após completar os exercícios, considere:

1. **ICL vs. Fine-Tuning:**
   - Quando cada abordagem é mais apropriada?
   - Como calcular ROI de fine-tuning vs. few-shot?
   - Em quais cenários ICL é superior?

2. **Custo vs. Qualidade:**
   - Qual a acurácia mínima aceitável para seu domínio?
   - Self-consistency vale 5× no custo?
   - Como otimizar sem sacrificar qualidade?

3. **Robustez:**
   - Como lidar com formatos inesperados de output?
   - O que fazer quando o modelo se recusa a responder?
   - Como detectar e mitigar alucinações?

4. **Escalabilidade:**
   - Como otimizar para alto volume (cache, batching)?
   - Quando migrar para fine-tuning?
   - Como monitorar qualidade em produção?

---

## 📚 Recursos Adicionais

### No Livro
- **Capítulo 3:** Fine-Tuning e Otimização (alternativa ao ICL)
- **Capítulo 5:** Embeddings e Retrieval (para dynamic selection)
- **Capítulo 6:** Tools e Function Calling (expansão do ReAct)
- **Apêndice A:** Comparação de Modelos
- **Apêndice E:** Padrões de Prompts

### Papers de Referência
- Brown et al. (2020): "Language Models are Few-Shot Learners" (GPT-3)
- Wei et al. (2022): "Chain-of-Thought Prompting Elicits Reasoning"
- Wang et al. (2022): "Self-Consistency Improves Chain of Thought"
- Yao et al. (2022): "ReAct: Synergizing Reasoning and Acting"

### Ferramentas
- **LangChain:** Framework para construção de aplicações com LLMs
- **DSPy:** Programação declarativa para prompts
- **Guidance:** Prompting estruturado com templates
- **LMQL:** Query language para LLMs

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'sentence_transformers'"
```bash
uv pip install sentence-transformers
```

### Erro: "FileNotFoundError: [Errno 2] No such file or directory: '../../datasets/...'"
Certifique-se de executar os scripts a partir do diretório `book/sandbox/chapter-04/`:
```bash
cd book/sandbox/chapter-04
python 01-few-shot-classifier.py
```

### Erro: API key inválida (ao usar produção)
```bash
# Verifique se a key está definida
echo $OPENAI_API_KEY

# Se vazia, defina:
export OPENAI_API_KEY="sk-..."
```

### Performance ruim com seleção semântica
1. Verifique qualidade dos embeddings (modelo muito pequeno?)
2. Confirme que dataset de treino tem exemplos diversos
3. Aumente `k` (número de exemplos) de 3 para 5-7

---

**Última atualização:** 2025-01-05  
**Exercícios testados com:** Python 3.11, sentence-transformers 2.2.2, scikit-learn 1.3.0
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
