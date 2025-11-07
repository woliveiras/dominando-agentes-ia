# Capítulo 6: Embeddings e Representação Semântica

Este diretório contém exemplos práticos do **Capítulo 6** do livro "Dominando Agentes de IA", focando em embeddings, semantic search, vector databases e chunking strategies.

## 📚 Tópicos Abordados

- **Fundamentos de Embeddings**:
  - De texto para vetores densos
  - Embeddings contextualizados vs. estáticos
  - Propriedades emergentes (analogias, relações matemáticas)

- **Modelos de Embedding Modernos**:
  - Sentence Transformers (SBERT)
  - OpenAI text-embedding-3-small/large
  - Modelos multilíngues (mBERT, XLM-RoBERTa)
  - Code embeddings

- **Similaridade Semântica**:
  - Similaridade cosseno
  - Distância euclidiana e Manhattan
  - Quando usar cada métrica

- **Chunking Strategies**:
  - Fixed-size, sentence-based, paragraph-based
  - Chunking semântico
  - Overlap strategies

- **Vector Databases**:
  - FAISS (Facebook AI Similarity Search)
  - Pinecone, Weaviate, Chroma, Qdrant
  - Approximate Nearest Neighbors (ANN)
  - HNSW indexing

- **Semantic Search**:
  - Pipeline completo: texto → embedding → search → ranking
  - Re-ranking híbrido (BM25 + embeddings)
  - Avaliação: precision, recall, MRR, NDCG

- **Fine-tuning de Embeddings**:
  - Contrastive learning
  - Domain adaptation
  - Few-shot fine-tuning

## 🚀 Pré-requisitos

### Instalação de Dependências

```bash
uv pip install sentence-transformers \
               faiss-cpu \
               openai \
               tiktoken \
               numpy \
               scikit-learn
```

### Variáveis de Ambiente

```bash
# API Keys (opcional - só para OpenAI embeddings)
export OPENAI_API_KEY="sk-..."

# Verificar
echo $OPENAI_API_KEY
```

## 📝 Exemplos Práticos

### 01-embedding-comparison.py ✅
**Status**: Implementado

Compara diferentes modelos de embedding e pooling strategies:
- Sentence Transformers vs BERT vanilla
- CLS pooling vs Mean pooling vs Max pooling
- Aritmética vetorial (vec(rei) - vec(homem) + vec(mulher) ≈ vec(rainha))
- Benchmark de modelos (dimensão, latência, qualidade)

**Como executar**:
```bash
uv pip install sentence-transformers transformers torch numpy
python 01-embedding-comparison.py
```

### 02-similarity-metrics.py ✅
**Status**: Implementado

Demonstra métricas de similaridade:
- Similaridade cosseno vs distância euclidiana vs Manhattan
- Impacto da normalização L2
- Otimização: dot product para vetores normalizados
- Guia de decisão: qual métrica usar
- Exemplo prático de semantic search

**Como executar**:
```bash
uv pip install sentence-transformers numpy
python 02-similarity-metrics.py
```

### 03-chunking-strategies.py ✅
**Status**: Implementado

Implementa e compara estratégias de chunking:
- Fixed-size chunking (com overlap)
- Sentence-based chunking
- Paragraph-based chunking
- Semantic chunking (usando embeddings)
- Contextual overlap entre chunks
- Recomendações por domínio

**Como executar**:
```bash
uv pip install nltk sentence-transformers transformers numpy
python 03-chunking-strategies.py
```

### 04-faiss-search-engine.py ✅
**Status**: Implementado

Pipeline completo de semantic search com FAISS:
- Classe `SemanticSearchEngine` com indexação e busca
- Indexação HNSW para baixa latência
- Chunking configurável
- Avaliação com métricas (Precision@5, NDCG)
- Demonstração com documentos técnicos

**Como executar**:
```bash
uv pip install faiss-cpu sentence-transformers nltk scikit-learn numpy
python 04-faiss-search-engine.py
```

### 05-hybrid-search.py ✅
**Status**: Implementado

Hybrid search combinando semantic + keyword search:
- Classe `HybridSearchEngine`
- Busca semântica (FAISS) + BM25
- Parâmetro alpha para balancear semantic vs keyword
- Comparação de métodos puros vs híbrido
- Demonstração com queries específicas

**Como executar**:
```bash
uv pip install faiss-cpu sentence-transformers rank-bm25 numpy
python 05-hybrid-search.py
```

### 06-embedding-fine-tuning.py ✅
**Status**: Implementado

Fine-tuning de embeddings com contrastive learning:
- MultipleNegativesRankingLoss (InfoNCE) - recomendado
- TripletLoss (método clássico)
- Comparação baseline vs fine-tuned
- Recomendações para produção
- Exemplo com synthetic data

**Como executar**:
```bash
uv pip install sentence-transformers torch numpy
python 06-embedding-fine-tuning.py
```

## 📊 Datasets Necessários

Os seguintes datasets devem ser criados em `book/datasets/` para os exercícios práticos:

### documents_for_search.jsonl
**Formato**: Uma linha por documento em JSON
```jsonl
{"text": "Embeddings são representações vetoriais...", "source": "doc_embeddings.md", "metadata": {"category": "fundamentos"}}
{"text": "FAISS é uma biblioteca...", "source": "doc_faiss.md", "metadata": {"category": "tools"}}
```

**Conteúdo sugerido**: 100-200 documentos sobre tópicos de IA/ML:
- Fundamentos de embeddings
- Vector databases (FAISS, Pinecone, etc.)
- Chunking strategies
- Machine learning concepts
- LLMs e agentes

### query_relevance_pairs.jsonl
**Formato**: Pares de query e documentos relevantes
```jsonl
{"query": "Como funciona FAISS?", "relevant_doc_ids": [1, 5], "difficulty": "medium"}
{"query": "O que são embeddings?", "relevant_doc_ids": [0], "difficulty": "easy"}
```

**Conteúdo sugerido**: 50+ pares de query-relevance para avaliação:
- Queries factuais ("O que é X?")
- Queries conceituais ("Como funciona Y?")
- Queries comparativas ("Diferença entre X e Y?")

### embedding_training_triplets.jsonl
**Formato**: Triplets para fine-tuning (anchor, positive, negative)
```jsonl
{"anchor": "Como usar embeddings?", "positive": "Embeddings são representações vetoriais de texto...", "negative": "Receitas de culinária italiana"}
{"anchor": "Tutorial FAISS", "positive": "FAISS oferece busca vetorial eficiente...", "negative": "Gatos são animais domésticos"}
```

**Conteúdo sugerido**: 1000+ triplets para fine-tuning:
- Pares positivos: queries semanticamente relacionadas
- Negatives: documentos completamente não-relacionados
- Balancear dificuldade (easy, medium, hard negatives)

## 🎯 Conceitos-Chave

### Embeddings Básicos

Transformar texto em vetores densos que capturam significado semântico:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

textos = [
    "Gatos são animais domésticos",
    "Cães são pets populares",
    "Python é uma linguagem de programação"
]

embeddings = model.encode(textos)
# Shape: (3, 384) - 3 textos, 384 dimensões cada
```

### Similaridade Semântica

Medir quão próximos semanticamente dois textos estão:

```python
from sklearn.metrics.pairwise import cosine_similarity

# Embeddings dos textos
emb1 = model.encode(["Gatos são animais"])
emb2 = model.encode(["Cães são pets"])
emb3 = model.encode(["Python é código"])

# Similaridade cosseno
sim_1_2 = cosine_similarity(emb1, emb2)[0][0]  # ~0.75 (alta)
sim_1_3 = cosine_similarity(emb1, emb3)[0][0]  # ~0.20 (baixa)
```

### Chunking Inteligente

Dividir documentos longos preservando contexto:

```python
def chunk_by_sentences(text, chunk_size=3, overlap=1):
    """Divide texto em chunks de N sentenças com overlap"""
    sentences = text.split('. ')
    chunks = []

    for i in range(0, len(sentences), chunk_size - overlap):
        chunk = '. '.join(sentences[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

# Exemplo
doc = "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5."
chunks = chunk_by_sentences(doc, chunk_size=3, overlap=1)
# ['Sentence 1. Sentence 2. Sentence 3',
#  'Sentence 3. Sentence 4. Sentence 5']
```

### Semantic Search com FAISS

Busca eficiente em milhões de vetores:

```python
import faiss
import numpy as np

# Criar índice FAISS
dimension = 384  # Dimensionalidade dos embeddings
index = faiss.IndexFlatL2(dimension)

# Adicionar embeddings ao índice
embeddings_matrix = np.array(embeddings).astype('float32')
index.add(embeddings_matrix)

# Buscar top-k mais similares
query = "animais de estimação"
query_embedding = model.encode([query]).astype('float32')

k = 2  # Top-2 resultados
distances, indices = index.search(query_embedding, k)

# indices[0] = [0, 1]  # "Gatos..." e "Cães..." são mais similares
```

### Hybrid Search (BM25 + Embeddings)

Combinar keyword search com semantic search:

```python
from rank_bm25 import BM25Okapi

# BM25 (keyword search)
tokenized_docs = [doc.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)
bm25_scores = bm25.get_scores(query.split())

# Semantic search scores
semantic_scores = cosine_similarity(
    query_embedding,
    document_embeddings
)[0]

# Combinar (weighted average)
alpha = 0.7  # Peso para semantic search
final_scores = alpha * semantic_scores + (1-alpha) * bm25_scores

# Ranking final
top_indices = final_scores.argsort()[::-1][:k]
```

## 🔬 Experimentos Sugeridos

1. **Comparar Modelos de Embedding**:
   - Sentence Transformers (all-MiniLM-L6-v2 vs paraphrase-multilingual)
   - OpenAI (text-embedding-3-small vs text-embedding-3-large)
   - Modelos especializados (code-search-ada-code-001 para código)

2. **Otimizar Chunking**:
   - Testar diferentes tamanhos de chunk (100, 300, 500 tokens)
   - Comparar overlap strategies (0%, 10%, 20%)
   - Avaliar chunking semântico vs. fixed-size

3. **Benchmark Vector Databases**:
   - FAISS (flat vs IVF vs HNSW)
   - Pinecone, Weaviate, Chroma
   - Medir: latência, recall@k, memory usage

4. **Fine-tune para Domínio**:
   - Coletar pares positivos/negativos do domínio
   - Fine-tune com contrastive loss
   - Comparar vs. modelo base

## 📊 Métricas de Avaliação

### Precision@k e Recall@k

```python
def precision_at_k(retrieved, relevant, k):
    """Precisão nos top-k resultados"""
    retrieved_k = retrieved[:k]
    return len(set(retrieved_k) & set(relevant)) / k

def recall_at_k(retrieved, relevant, k):
    """Recall nos top-k resultados"""
    retrieved_k = retrieved[:k]
    return len(set(retrieved_k) & set(relevant)) / len(relevant)
```

### Mean Reciprocal Rank (MRR)

```python
def mrr(retrieved_lists, relevant_lists):
    """Mean Reciprocal Rank"""
    reciprocal_ranks = []
    for retrieved, relevant in zip(retrieved_lists, relevant_lists):
        for i, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                reciprocal_ranks.append(1.0 / i)
                break
        else:
            reciprocal_ranks.append(0.0)
    return np.mean(reciprocal_ranks)
```

### NDCG (Normalized Discounted Cumulative Gain)

```python
from sklearn.metrics import ndcg_score

# relevance_scores: matriz de relevância (queries x documentos)
# predicted_scores: scores preditos pelo sistema
ndcg = ndcg_score(relevance_scores, predicted_scores, k=10)
```

## 💡 Dicas Práticas

### Escolha de Modelo de Embedding

- **Velocidade > Qualidade**: all-MiniLM-L6-v2 (384 dim, rápido)
- **Qualidade > Velocidade**: all-mpnet-base-v2 (768 dim, preciso)
- **Multilíngue**: paraphrase-multilingual-mpnet-base-v2
- **Código**: code-search-ada-code-001 (OpenAI)
- **Alta dimensionalidade**: text-embedding-3-large (OpenAI, 3072 dim)

### Tamanho Ótimo de Chunks

- **Respostas factuais**: 100-300 tokens
- **Contexto geral**: 300-500 tokens
- **Documentos longos**: 500-1000 tokens
- **Overlap**: 10-20% do tamanho do chunk

### Quando usar cada Vector DB

- **FAISS**: Prototipagem, batch inference, self-hosted
- **Pinecone**: Produção cloud, escalabilidade automática
- **Weaviate**: Schema complexo, GraphQL, multi-tenancy
- **Chroma**: Embedding store simples, local development
- **Qdrant**: Alta performance, filtros avançados, self-hosted

## 🐛 Troubleshooting

### Erro: "No module named 'faiss'"
```bash
# CPU-only (mais rápido para instalar)
uv pip install faiss-cpu

# GPU (requer CUDA)
uv pip install faiss-gpu
```

### Embeddings muito lentos
- Use batch encoding: `model.encode(texts, batch_size=32)`
- Considere GPU: `model = SentenceTransformer('...', device='cuda')`
- Cache embeddings pré-computados

### Recall baixo em semantic search
- Aumente k (top-k results)
- Use hybrid search (BM25 + embeddings)
- Fine-tune embeddings para seu domínio
- Verifique qualidade dos chunks

### Memory error com FAISS
- Use IndexIVFFlat ao invés de IndexFlatL2
- Reduza dimensionalidade com PCA
- Processe em batches menores

## 📖 Referências

### Papers Fundamentais

1. **Sentence-BERT (Reimers & Gurevych, 2019)**
   - [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)

2. **FAISS (Johnson et al., 2019)**
   - [Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734)

3. **ColBERT (Khattab & Zaharia, 2020)**: Late interaction
   - [ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832)

4. **Dense Passage Retrieval (Karpukhin et al., 2020)**
   - [Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)

### Documentação

- [Sentence Transformers Docs](https://www.sbert.net/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)

### Recursos Adicionais

- [Massive Text Embedding Benchmark (MTEB)](https://huggingface.co/spaces/mteb/leaderboard)
- [Vector Database Comparison](https://vdbs.superlinked.com/)

## 🤝 Contribuindo

Testou diferentes estratégias de chunking? Comparou vector databases?

1. Documente setup e configuração
2. Benchmark com métricas (precision@k, recall@k, latência)
3. Compare com baseline
4. Abra PR com resultados

---

**Status**: ✅ Implementado (6 scripts Python, aguardando criação de datasets)
**Última atualização**: 2025-11-07
