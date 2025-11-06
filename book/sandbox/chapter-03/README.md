# Exemplos do Capítulo 3: Fine-Tuning e Otimização

Exemplos práticos de fine-tuning com LoRA, análise de tokenização e avaliação com LLM-as-Judge.

## 📋 Visão Geral dos Exemplos

### 01-lora-fine-tuning.py
**Fine-Tuning com LoRA (Low-Rank Adaptation)**

Demonstra fine-tuning eficiente de LLM para tradução de termos técnicos usando LoRA.

**O que você vai aprender:**
- Configuração de LoRA (rank, alpha, dropout)
- Fine-tuning sem treinar modelo inteiro
- Redução de memória (4-8x menor que full fine-tuning)
- Merge de adapters para deployment

**Instalação:**
```bash
uv pip install transformers peft datasets accelerate bitsandbytes torch
```

**Execução:**
```bash
python 01-lora-fine-tuning.py
```

**Requisitos:**
- Dataset: `../../datasets/tech_terms_pt_en.jsonl`
- GPU recomendada (funciona em CPU, mais lento)
- Memória: ~8GB GPU / ~16GB RAM

**Configuração LoRA:**
```python
LoraConfig(
    r=16,              # Rank (complexidade do adapter)
    lora_alpha=32,     # Scaling factor
    lora_dropout=0.05, # Regularização
    target_modules=["q_proj", "v_proj"]  # Camadas a adaptar
)
```

**Resultados esperados:**
- Training time: ~10-30 min (GPU) / ~2-4h (CPU)
- Model size: Base (500MB) + LoRA adapter (2-5MB)
- Memory footprint: ~6GB GPU

---

### 02-tokenization-analysis.py
**Análise de Tokenização e Custos de API**

Analisa eficiência de tokenização para diferentes idiomas e calcula custos de API.

**O que você vai aprender:**
- Fertility rate por idioma
- Cálculo de custo baseado em tokens
- Comparação de eficiência: inglês vs português vs código
- Otimização de prompts para reduzir tokens

**Instalação:**
```bash
uv pip install tiktoken transformers
```

**Execução:**
```bash
python 02-tokenization-analysis.py
```

**Métricas analisadas:**
- **Tokens**: Quantidade de tokens por texto
- **Fertility rate**: Tokens / Palavras
- **Custo estimado**: Based on GPT-4 pricing
- **Eficiência**: Comparação cross-linguística

**Insights típicos:**
- Inglês: fertility ~1.0 (mais eficiente)
- Português: fertility ~1.3-1.5
- Código: fertility ~0.7-0.9 (muito eficiente)
- Implicação: Mesmo prompt custa mais em PT

---

### 03-llm-as-judge.py
**Avaliação com LLM-as-Judge**

Sistema de avaliação automática de respostas usando LLM como juiz.

**O que você vai aprender:**
- Rubrica estruturada para avaliação
- Análise de viés do juiz
- Comparação entre diferentes modelos
- Métricas de qualidade (relevância, precisão, completude)

**Instalação:**
```bash
uv pip install anthropic
```

**Execução:**
```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
python 03-llm-as-judge.py
```

**Requisitos:**
- Chave de API da Anthropic
- Dataset de exemplos (incluído no script)

**Rubrica de avaliação:**
```python
{
    "relevance": 0-5,      # Resposta aborda a pergunta?
    "accuracy": 0-5,       # Informação está correta?
    "completeness": 0-5,   # Resposta é completa?
    "clarity": 0-5         # Explicação é clara?
}
```

**Análise de viés:**
- Teste com respostas idênticas em ordem diferente
- Detecte preferência por respostas mais longas
- Identifique viés de posição (primeira vs última)

---

## 🎯 Conceitos Aplicados

### Fine-Tuning Eficiente

| Método | Memória | Tempo | Qualidade |
|--------|---------|-------|-----------|
| **Full Fine-Tuning** | 100% | 100% | ⭐⭐⭐⭐⭐ |
| **LoRA (r=8)** | 15% | 30% | ⭐⭐⭐⭐ |
| **LoRA (r=16)** | 20% | 40% | ⭐⭐⭐⭐⭐ |
| **LoRA (r=64)** | 40% | 60% | ⭐⭐⭐⭐⭐ |

**Recomendação**: LoRA r=16 oferece melhor custo-benefício

### Pipeline de Desenvolvimento

```
1. Data Preparation
   ↓
2. Tokenization Analysis (02)
   ↓ (Otimizar custos)
3. Fine-Tuning (01)
   ↓ (Treinar modelo)
4. Evaluation (03)
   ↓ (Validar qualidade)
5. Deployment
```

---

## 🔧 Setup e Configuração

### Instalação Completa

```bash
# Todas as dependências
uv pip install transformers peft datasets accelerate bitsandbytes torch tiktoken anthropic
```

### Preparar Datasets

#### Para Fine-Tuning (01)
```bash
# Criar dataset de exemplo
cat > ../../datasets/tech_terms_pt_en.jsonl << EOF
{"input": "traduza: API", "output": "Application Programming Interface"}
{"input": "traduza: container", "output": "contêiner"}
EOF
```

#### Para LLM-as-Judge (03)
```bash
# Configurar API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Verificar
echo $ANTHROPIC_API_KEY
```

---

## 📊 Benchmarks e Resultados

### Fine-Tuning Performance (01)

**GPT-2 Small (124M params):**
- LoRA r=16: ~2GB GPU memory
- Training: ~15 min (100 examples)
- Inference: ~50ms/response

**Llama-2-7B:**
- LoRA r=16: ~8GB GPU memory
- Training: ~2h (1000 examples)
- Inference: ~200ms/response

### Tokenization Efficiency (02)

**Comparison Table:**

| Text Type | Tokens (EN) | Tokens (PT) | Fertility (EN) | Fertility (PT) |
|-----------|-------------|-------------|----------------|----------------|
| Technical doc | 256 | 384 | 1.0 | 1.5 |
| Code snippet | 128 | 128 | 0.8 | 0.8 |
| Casual text | 200 | 280 | 1.1 | 1.4 |

**Cost Impact (GPT-4):**
- EN: $0.03/1K tokens (input)
- PT: Same $/token → 50% more expensive per word!

### LLM-as-Judge Reliability (03)

**Agreement with human evaluators:**
- Relevance: 85% agreement
- Accuracy: 78% agreement
- Completeness: 82% agreement
- Overall: κ (Cohen's kappa) ~0.75 (substantial agreement)

---

## 🎓 Exercícios Práticos

### 1. Fine-Tuning Experiments

**Objetivo**: Comparar diferentes configurações LoRA

```python
# Experimente diferentes ranks
configs = [
    {"r": 4, "lora_alpha": 8},
    {"r": 8, "lora_alpha": 16},
    {"r": 16, "lora_alpha": 32},
    {"r": 32, "lora_alpha": 64},
]

# Para cada config:
# 1. Treinar modelo
# 2. Avaliar qualidade
# 3. Medir tempo e memória
# 4. Plotar trade-offs
```

**Desafio**: Encontre configuração ótima para seu caso de uso

### 2. Tokenization Optimization

**Objetivo**: Reduzir custo de API em 30%

```python
# Tarefa: Otimizar este prompt
verbose_prompt = """
Por favor, poderia me ajudar a entender o que é machine learning?
Gostaria de uma explicação detalhada sobre os conceitos fundamentais.
"""

# Meta: Reduzir tokens mantendo clareza
optimized_prompt = "Explique machine learning de forma detalhada."

# Medir:
# - Tokens antes: ?
# - Tokens depois: ?
# - Redução: ?%
```

**Desafio**: Otimize 10 prompts diferentes, compare savings

### 3. LLM-as-Judge Calibration

**Objetivo**: Identificar e mitigar viés

```python
# Teste viés de posição
responses = [response_A, response_B]
scores_AB = judge(responses)        # A primeiro, B segundo
scores_BA = judge(reversed(responses))  # B primeiro, A segundo

# Viés de posição?
if scores_AB != scores_BA:
    print("⚠️ Position bias detected!")

# Tarefa: Implementar mitigação
```

**Desafio**: Desenvolva estratégia para reduzir viés

---

## 🐛 Troubleshooting

### CUDA Out of Memory (01)

**Problema**: GPU sem memória suficiente

**Soluções:**
```bash
# 1. Reduzir batch size
per_device_train_batch_size=1

# 2. Usar gradient accumulation
gradient_accumulation_steps=4

# 3. Usar 8-bit quantization
load_in_8bit=True

# 4. Reduzir LoRA rank
r=8
```

### API Key Error (03)

**Problema**: ANTHROPIC_API_KEY não definida

**Soluções:**
```bash
# Temporário (sessão atual)
export ANTHROPIC_API_KEY="sk-ant-..."

# Permanente (adicionar ao ~/.bashrc ou ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

### LoRA Merge Failure (01)

**Problema**: Erro ao fazer merge de adapter

**Solução:**
```python
# Verificar compatibilidade de versões
# peft>=0.7.0
# transformers>=4.35.0

# Re-instalar se necessário
uv pip install --upgrade peft transformers
```

---

## 📚 Recursos Adicionais

### Papers

- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning](https://arxiv.org/abs/2305.14314)
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)

### Tutoriais

- [HuggingFace PEFT](https://huggingface.co/docs/peft/)
- [Fine-tuning Guide](https://huggingface.co/docs/transformers/training)
- [Anthropic API Docs](https://docs.anthropic.com/)

### Tools

- [Weight & Biases](https://wandb.ai/) - Experiment tracking
- [Aim](https://aimstack.io/) - Open-source alternative
- [TensorBoard](https://www.tensorflow.org/tensorboard) - Visualization

---

## 💡 Boas Práticas

### Fine-Tuning

1. **Start small**: Teste com GPT-2 antes de Llama-2-70B
2. **Quality over quantity**: 100 exemplos bons > 1000 ruins
3. **Validate early**: Avalie a cada epoch
4. **Save checkpoints**: Múltiplos pontos de salvamento

### Evaluation

1. **Multiple judges**: Use 2-3 LLMs diferentes
2. **Human validation**: Sample 10% para validação humana
3. **Blind evaluation**: Randomize order para evitar viés
4. **Rubrica clara**: Critérios objetivos e mensuráveis

### Cost Optimization

1. **Cache prompts**: Reutilize system messages
2. **Batch requests**: Agrupe quando possível
3. **Monitor usage**: Track spending em tempo real
4. **Set budgets**: Alerts quando atingir limites

---

**Próximo passo**: Após dominar fine-tuning e avaliação, prossiga para o Capítulo 4 (Dominando LLMs na Prática) onde você verá otimização avançada e deployment em produção.
