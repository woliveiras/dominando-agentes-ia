# Exemplos do Capítulo 1: Fundamentos de Transformers

Exemplos práticos e executáveis demonstrando os componentes fundamentais da arquitetura Transformer.

## 📋 Visão Geral dos Exemplos

### 01-tokenizer-comparison.py

**Comparação de Tokenizers**

Compara como diferentes tokenizers (GPT-2, GPT-4, BERT, Llama) processam o mesmo texto.

**O que você vai aprender:**

- Diferenças entre tokenizers de diferentes modelos
- Cálculo de fertility rate (tokens/palavra)
- Impacto da tokenização em eficiência e custo

**Instalação:**

```bash
uv pip install transformers torch
```

**Execução:**

```bash
python 01-tokenizer-comparison.py
```

**Saída esperada:**

- Comparação de vocabulário entre modelos
- Fertility rate por tokenizer
- Análise de eficiência para texto em português

---

### 02-self-attention-example.py

**Mecanismo de Self-Attention**

Implementação simplificada do mecanismo de self-attention.

**O que você vai aprender:**

- Como tokens em uma sequência se relacionam
- Cálculo de Query, Key e Value
- Scores de atenção e normalização

**Instalação:**

```bash
uv pip install torch
```

**Execução:**

```bash
python 02-self-attention-example.py
```

**Conceitos demonstrados:**

- Projeções lineares (W_Q, W_K, W_V)
- Similarity scores (Q @ K^T)
- Softmax para probabilidades
- Weighted sum de valores

---

### 03-causal-mask-example.py

**Causal Mask para Modelos Decoder-Only**

Implementação da máscara causal que impede "olhar para o futuro".

**O que você vai aprender:**

- Por que modelos GPT-like precisam de causal mask
- Implementação de máscara triangular
- Aplicação em scores de atenção

**Instalação:**

```bash
uv pip install torch
```

**Execução:**

```bash
python 03-causal-mask-example.py
```

**Visualização:**

- Matriz de atenção sem máscara
- Matriz de atenção com máscara causal
- Comparação de outputs

---

### 04-kv-cache-example.py

**KV-Cache para Geração Eficiente**

Implementação de KV-Cache que reduz computação redundante.

**O que você vai aprender:**

- Por que recalcular keys/values é desperdício
- Como implementar cache de KV
- Ganho de performance em geração autoregressiva

**Instalação:**

```bash
uv pip install torch
```

**Execução:**

```bash
python 04-kv-cache-example.py
```

**Comparação demonstrada:**

- Geração sem KV-Cache (lento)
- Geração com KV-Cache (rápido)
- Medição de tempo economizado

---

## 🎯 Conceitos Aplicados

Estes exemplos cobrem os blocos fundamentais dos Transformers:

### Tokenização

- **Subword tokenization**: BPE, WordPiece
- **Fertility rate**: Eficiência de compressão
- **Vocabulário**: Tamanho e impacto em performance

### Self-Attention

- **Query, Key, Value**: Papel de cada projeção
- **Scaled Dot-Product**: Cálculo de similarity
- **Multi-Head**: Múltiplas representações paralelas

### Máscaras

- **Causal mask**: Autoregressive generation
- **Padding mask**: Ignorar tokens de padding
- **Combinação**: Múltiplas máscaras simultaneamente

### Otimizações

- **KV-Cache**: Redução de computação
- **Memory efficiency**: Gerenciamento de memória
- **Inference speed**: Aceleração de geração

---

## 🔧 Setup e Requisitos

### Dependências Principais

```bash
# Instalar todas as dependências de uma vez
uv pip install torch transformers
```

### Requisitos de Hardware

- **CPU**: Todos os exemplos funcionam em CPU
- **RAM**: Mínimo 4GB (8GB recomendado)
- **GPU**: Opcional (acelera execução mas não necessária)

### Verificar GPU (opcional)

```bash
# NVIDIA
nvidia-smi

# Apple Silicon
system_profiler SPDisplaysDataType | grep "Chipset Model"
```

---

## 📊 Ordem Recomendada de Estudo

1. **Comece com tokenização** (`01-tokenizer-comparison.py`)
   - Fundamento para tudo que vem depois
   - Entenda como texto vira números

2. **Self-attention** (`02-self-attention-example.py`)
   - Coração da arquitetura Transformer
   - Veja como tokens interagem

3. **Causal mask** (`03-causal-mask-example.py`)
   - Essencial para modelos generativos
   - Diferença entre encoder e decoder

4. **KV-Cache** (`04-kv-cache-example.py`)
   - Otimização crítica para produção
   - Ganho de performance real

---

## 🎓 Exercícios Sugeridos

### Após executar os exemplos:

1. **Tokenização**:
   - Teste com textos em diferentes idiomas
   - Compare fertility rate: português vs inglês vs código
   - Calcule custo de API baseado em tokens

2. **Self-Attention**:
   - Modifique dimensões (d_model, d_k)
   - Observe impacto nos scores de atenção
   - Implemente multi-head attention

3. **Causal Mask**:
   - Experimente remover a máscara
   - Compare outputs com/sem máscara
   - Teste com sequências de diferentes tamanhos

4. **KV-Cache**:
   - Meça tempo economizado em sequências longas
   - Calcule memória usada pelo cache
   - Implemente eviction policy para cache limitado

---

## 🐛 Troubleshooting

### Erro: "No module named 'transformers'"
```bash
uv pip install transformers
```

### Erro: "torch not found"
```bash
# CPU-only
uv pip install torch --index-url https://download.pytorch.org/whl/cpu

# Com CUDA (NVIDIA GPU)
uv pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### Lentidão em CPU
- Normal! Transformers são computacionalmente intensivos
- Reduza tamanho de sequência nos exemplos se necessário
- Considere usar Google Colab (GPU grátis) para experimentação

---

## 📚 Recursos Adicionais

- [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Transformers from Scratch](https://peterbloem.nl/blog/transformers)
- [HuggingFace Transformers Docs](https://huggingface.co/docs/transformers/)
- [Attention Is All You Need (Paper)](https://arxiv.org/abs/1706.03762)

---

**Próximo passo**: Após dominar estes fundamentos, prossiga para o Capítulo 2 (Treinamento de Foundation Models) onde você verá como estes componentes são treinados em larga escala.
