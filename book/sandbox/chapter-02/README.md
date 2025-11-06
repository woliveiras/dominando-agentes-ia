# Exemplos do Capítulo 2: Treinamento de Foundation Models

Exemplos práticos demonstrando curadoria de dados, deduplicação e treinamento de tokenizers customizados.

## 📋 Visão Geral dos Exemplos

### 01-quality-metrics.py

**Métricas de Qualidade de Dataset**

Implementa heurísticas para avaliar qualidade textual de datasets de treinamento.

**O que você vai aprender:**

- Cálculo de entropia de Shannon (diversidade vocabular)
- Type-Token Ratio (riqueza linguística)
- Detecção de padrões problemáticos (repetição excessiva, boilerplate)
- Métricas de complexidade sintática

**Instalação:**

```bash
# Usa apenas bibliotecas padrão do Python
# Nenhuma instalação necessária
```

**Execução:**

```bash
python 01-quality-metrics.py
```

**Métricas calculadas:**

- **Entropia**: H = -Σ(p(x) * log₂(p(x)))
- **Type-Token Ratio**: Unique words / Total words
- **Sentence complexity**: Palavras por sentença
- **Repetition rate**: Porcentagem de n-grams repetidos

---

### 02-minhash-deduplication.py

**Deduplicação com MinHash e LSH**

Detecta documentos near-duplicates usando MinHash e Locality-Sensitive Hashing.

**O que você vai aprender:**

- MinHash para similarity estimation eficiente
- LSH (Locality-Sensitive Hashing) para busca rápida
- Trade-off entre threshold e recall
- Deduplicação em datasets massivos

**Instalação:**

```bash
uv pip install datasketch
```

**Execução:**

```bash
python 02-minhash-deduplication.py
```

**Configuração:**

- `threshold=0.8`: Detecta docs com Jaccard similarity ≥ 80%
- `num_perm=128`: Número de permutações para MinHash
- Complexidade: O(n) vs O(n²) da comparação direta

**Casos de uso:**

- Remover duplicatas de web scraping
- Deduplicate training corpora
- Detectar plagiarism em larga escala

---

### 03-train-custom-tokenizer.py

**Treinamento de Tokenizer Customizado**

Treina tokenizer BPE do zero para domínio específico.

**O que você vai aprender:**

- Configuração de tokenizer BPE
- Definição de vocabulário e tokens especiais
- Pre-tokenização (ByteLevel, Whitespace)
- Post-processamento (Template, Truncation)

**Instalação:**

```bash
uv pip install tokenizers
```

**Execução:**

```bash
python 03-train-custom-tokenizer.py
```

**Requisitos:**

- Arquivo de treinamento: `../../datasets/tokenizer_train.txt`
- Mínimo 1MB de texto recomendado
- Maior corpus = melhor vocabulário

**Parâmetros importantes:**

- `vocab_size`: Tamanho do vocabulário (ex: 50000)
- `min_frequency`: Frequência mínima para inclusão (ex: 2)
- `special_tokens`: `[PAD]`, `[UNK]`, `[BOS]`, `[EOS]`

---

## 🎯 Conceitos Aplicados

### Curadoria de Dados

| Etapa | Objetivo | Ferramenta |
|-------|----------|------------|
| **Filtragem de qualidade** | Remover conteúdo ruim | Heurísticas (01) |
| **Deduplicação** | Remover duplicatas | MinHash/LSH (02) |
| **Tokenização** | Vocabulário eficiente | BPE (03) |

### Pipeline Completo

```
Raw Data (100GB)
    ↓
Quality Filtering (01-quality-metrics.py)
    ↓ (70GB - 30% descartado)
Deduplication (02-minhash-deduplication.py)
    ↓ (50GB - 29% duplicatas)
Tokenizer Training (03-train-custom-tokenizer.py)
    ↓
Clean Training Corpus (50GB)
```

---

## 🔧 Setup e Uso

### Instalação Completa

```bash
# Instalar todas as dependências de uma vez
uv pip install datasketch tokenizers
```

### Preparar Dados

```bash
# Criar diretório de datasets se não existir
mkdir -p ../../datasets

# Baixar dataset de exemplo (ou usar seu próprio)
# Para tokenizer training, você precisa de texto suficiente:
cat > ../../datasets/tokenizer_train.txt << EOF
[Seu corpus de texto aqui]
Mínimo 1MB recomendado para vocabulário razoável
EOF
```

---

## 📊 Benchmarks e Resultados Esperados

### Quality Metrics (01)

**Texto de boa qualidade:**
- Entropia: > 8.0 bits
- Type-Token Ratio: 0.3 - 0.7
- Repetition rate: < 15%

**Texto de baixa qualidade:**
- Entropia: < 5.0 bits
- Type-Token Ratio: < 0.2
- Repetition rate: > 30%

### Deduplication (02)

**Dataset típico de web scraping:**
- Near-duplicates: 20-40% do corpus
- Exact duplicates: 5-15%
- Tempo de processamento: ~1M docs/hora (single machine)

### Tokenizer Training (03)

**Corpus de 10MB:**
- Tempo de treinamento: ~1-2 minutos
- Vocabulário resultante: 30K-50K tokens
- Fertility rate (PT-BR): ~1.3-1.5

---

## 🎓 Exercícios Práticos

### 1. Quality Metrics

**Objetivo**: Filtrar dataset por qualidade

```python
# Tarefa: Implementar filtro automático
def should_keep_document(text):
    metrics = calculate_all_metrics(text)
    return (
        metrics['entropy'] > 7.0 and
        metrics['type_token_ratio'] > 0.25 and
        metrics['repetition_rate'] < 0.2
    )
```

**Desafio**: Ajuste thresholds para seu domínio específico

### 2. Deduplication

**Objetivo**: Deduplicate corpus real

```python
# Tarefa: Processar 10K documentos
corpus = load_documents("your_corpus.jsonl")
deduped = deduplicate_with_minhash(corpus, threshold=0.85)
print(f"Removed {len(corpus) - len(deduped)} duplicates")
```

**Desafio**: Experimente diferentes thresholds (0.7, 0.8, 0.9)

### 3. Custom Tokenizer

**Objetivo**: Treinar tokenizer para código Python

```python
# Tarefa: Collect Python code from GitHub
# Train tokenizer optimizado para código
# Compare fertility rate vs GPT-4 tokenizer
```

**Desafio**: Compare vocabulários: código vs texto natural

---

## 🐛 Troubleshooting

### Erro: "datasketch not found"
```bash
uv pip install datasketch
```

### Erro: "tokenizers module not found"
```bash
uv pip install tokenizers
```

### Deduplication muito lento
- **Problema**: Dataset muito grande
- **Solução**: Processar em batches
- **Alternativa**: Use Apache Spark para distribuir processamento

### Tokenizer com vocabulário ruim
- **Problema**: Corpus de treinamento muito pequeno
- **Solução**: Colete mais dados (mínimo 10MB)
- **Dica**: Diversifique fontes de dados

---

## 📚 Recursos Adicionais

- [The Pile: Data Quality for LLMs](https://arxiv.org/abs/2101.00027)
- [Deduplicating Training Data](https://arxiv.org/abs/2107.06499)
- [MinHash Tutorial](https://ekzhu.com/datasketch/minhash.html)
- [HuggingFace Tokenizers](https://huggingface.co/docs/tokenizers/)
- [C4 Dataset Paper](https://arxiv.org/abs/1910.10683)

---

## 🔗 Datasets Públicos de Qualidade

Para treinar seus próprios tokenizers:

- **The Pile**: 825GB de texto de alta qualidade
- **C4 (Colossal Clean Crawled Corpus)**: 750GB web text
- **RedPajama**: 1.2TB open-source corpus
- **Wikipedia dumps**: Texto limpo e estruturado
- **GitHub Code**: Para tokenizers de código

---

**Próximo passo**: Após curar seus dados, prossiga para o Capítulo 3 (Fine-Tuning e Otimização) onde você verá como adaptar modelos para tarefas específicas.
