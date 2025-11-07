"""
Capítulo 6: Embeddings e Representação Semântica
Script 04: Semantic Search com FAISS

Implementação completa de semantic search engine usando FAISS.
Ver exercícios práticos no capítulo para instruções completas.

Dependências:
    uv pip install faiss-cpu sentence-transformers numpy nltk scikit-learn
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import nltk
from sklearn.metrics import ndcg_score

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class SemanticSearchEngine:
    """Pipeline completo de semantic search com FAISS."""

    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = []
        self.metadata = []

    def chunk_document(self, doc, strategy='paragraph', chunk_size=400):
        """Chunk um documento usando estratégia especificada."""
        text = doc if isinstance(doc, str) else doc.get('text', '')

        if strategy == 'paragraph':
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            return paragraphs
        elif strategy == 'sentence':
            return nltk.sent_tokenize(text)
        else:
            # Fixed size não implementado aqui por brevidade
            return [text]

    def index_documents(self, documents, chunk_strategy='paragraph'):
        """
        Indexa documentos:
        1. Chunking
        2. Gerar embeddings
        3. Construir índice FAISS
        """
        print(f"Indexando {len(documents)} documentos...")

        for doc_id, doc in enumerate(documents):
            if isinstance(doc, str):
                doc = {'text': doc, 'source': f'doc_{doc_id}'}

            chunks = self.chunk_document(doc, strategy=chunk_strategy)

            for chunk_id, chunk in enumerate(chunks):
                self.chunks.append(chunk)
                self.metadata.append({
                    'doc_id': doc_id,
                    'chunk_id': chunk_id,
                    'source': doc.get('source', 'unknown')
                })

        print(f"Total de chunks: {len(self.chunks)}")

        # Gerar embeddings
        print("Gerando embeddings...")
        embeddings = self.model.encode(
            self.chunks,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        # Construir índice HNSW
        print("Construindo índice FAISS HNSW...")
        self.index = faiss.IndexHNSWFlat(self.dimension, 32)
        self.index.hnsw.efConstruction = 40
        self.index.add(embeddings.astype('float32'))

        print(f"✓ Indexação completa! {len(self.chunks)} chunks indexados.")

    def search(self, query, top_k=5):
        """Busca por chunks mais relevantes."""
        if self.index is None:
            raise ValueError("Índice não foi construído. Execute index_documents primeiro.")

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype('float32')

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                'chunk': self.chunks[idx],
                'score': float(dist),
                'metadata': self.metadata[idx]
            })

        return results


def evaluate_search_system(search_engine, test_queries, ground_truth):
    """
    Avalia sistema de busca com métricas padrão.

    Args:
        test_queries: lista de queries de teste
        ground_truth: dict {query_id: [list of relevant chunk_ids]}
    """
    all_precision_at_5 = []
    all_ndcg = []

    for query_id, query in enumerate(test_queries):
        results = search_engine.search(query, top_k=10)
        retrieved_chunk_ids = [r['metadata']['chunk_id'] for r in results]
        relevant_chunk_ids = ground_truth.get(query_id, [])

        if not relevant_chunk_ids:
            continue

        # Precision@5
        relevant_in_top5 = len(set(retrieved_chunk_ids[:5]) & set(relevant_chunk_ids))
        all_precision_at_5.append(relevant_in_top5 / 5.0)

        # NDCG
        true_relevance = [1 if chunk_id in relevant_chunk_ids else 0
                          for chunk_id in retrieved_chunk_ids]
        # Scores decrescentes por posição
        predicted_relevance = list(range(len(true_relevance), 0, -1))

        if sum(true_relevance) > 0:
            ndcg = ndcg_score([true_relevance], [predicted_relevance])
            all_ndcg.append(ndcg)

    return {
        'mean_precision_at_5': np.mean(all_precision_at_5) if all_precision_at_5 else 0.0,
        'mean_ndcg': np.mean(all_ndcg) if all_ndcg else 0.0,
        'num_queries': len(all_precision_at_5)
    }


def demo():
    """Demonstração do semantic search engine."""
    print("=" * 80)
    print("Semantic Search Engine com FAISS")
    print("=" * 80)

    # Documentos de exemplo
    documents = [
        {
            'text': """
            Embeddings são representações vetoriais densas que capturam significado semântico de texto.
            Modelos como BERT e Sentence Transformers geram embeddings contextualizados de alta qualidade.
            A dimensionalidade típica varia de 384 a 1536 dimensões dependendo do modelo.
            """,
            'source': 'doc_embeddings.md'
        },
        {
            'text': """
            FAISS é uma biblioteca desenvolvida pela Meta para busca eficiente em espaços vetoriais de alta dimensão.
            Oferece múltiplos tipos de índices: Flat para busca exata, IVF para busca aproximada rápida, e HNSW
            para máxima qualidade. HNSW constrói grafos hierárquicos que permitem busca sub-milissegundo.
            """,
            'source': 'doc_faiss.md'
        },
        {
            'text': """
            Chunking é a técnica de dividir documentos longos em segmentos processáveis.
            Estratégias incluem fixed-size, sentence-based, paragraph-based, e semantic chunking.
            Overlap de 10-20% entre chunks é recomendado para preservar contexto nas boundaries.
            """,
            'source': 'doc_chunking.md'
        },
        {
            'text': """
            Machine learning é um subcampo de inteligência artificial que permite que sistemas aprendam
            padrões a partir de dados. Deep learning, usando redes neurais profundas, revolucionou
            processamento de linguagem natural, visão computacional, e outras áreas.
            """,
            'source': 'doc_ml.md'
        }
    ]

    # Criar e indexar
    engine = SemanticSearchEngine(model_name='all-MiniLM-L6-v2')
    engine.index_documents(documents, chunk_strategy='paragraph')

    # Queries de teste
    test_queries = [
        "Como funciona FAISS?",
        "O que são embeddings vetoriais?",
        "Qual a melhor estratégia de chunking?",
        "Explique deep learning"
    ]

    print("\n" + "=" * 80)
    print("Executando buscas de teste")
    print("=" * 80)

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 80)

        results = engine.search(query, top_k=2)

        for i, result in enumerate(results, 1):
            chunk_preview = result['chunk'][:120] + "..." if len(result['chunk']) > 120 else result['chunk']
            print(f"{i}. [score={result['score']:.4f}] {chunk_preview.strip()}")
            print(f"   Fonte: {result['metadata']['source']}")

    # Avaliação simplificada
    print("\n" + "=" * 80)
    print("Avaliação de Qualidade")
    print("=" * 80)

    # Ground truth simplificado (chunk_ids relevantes por query)
    ground_truth = {
        0: [1],  # FAISS query
        1: [0],  # Embeddings query
        2: [2],  # Chunking query
        3: [3]   # Deep learning query
    }

    metrics = evaluate_search_system(engine, test_queries, ground_truth)

    print(f"\nMétricas de Performance:")
    print(f"  Precision@5: {metrics['mean_precision_at_5']:.3f}")
    print(f"  NDCG: {metrics['mean_ndcg']:.3f}")
    print(f"  Queries testadas: {metrics['num_queries']}")

    target_precision = 0.70
    if metrics['mean_precision_at_5'] >= target_precision:
        print(f"\n✅ Meta atingida! (Precision@5 >= {target_precision})")
    else:
        print(f"\n⚠️  Abaixo da meta. Considere:")
        print(f"    - Usar modelo maior (all-mpnet-base-v2)")
        print(f"    - Ajustar estratégia de chunking")
        print(f"    - Implementar hybrid search (BM25 + embeddings)")


if __name__ == "__main__":
    print("\n🚀 Capítulo 6: Semantic Search Engine\n")
    demo()
    print("\n" + "=" * 80)
    print("✅ Demo concluída!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("  - Implemente com seus próprios documentos")
    print("  - Experimente diferentes modelos e estratégias")
    print("  - Veja 05-hybrid-search.py para combinar com BM25")
