"""
Capítulo 6: Embeddings e Representação Semântica
Script 05: Hybrid Search (Semantic + BM25)

Combina busca semântica (embeddings) com keyword search (BM25).
Ver exercícios práticos no capítulo para detalhes.

Dependências:
    uv pip install faiss-cpu sentence-transformers rank-bm25 numpy
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss


class HybridSearchEngine:
    """Combina semantic search (FAISS) com keyword search (BM25)."""

    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.faiss_index = None
        self.bm25 = None
        self.chunks = []
        self.metadata = []

    def index_documents(self, documents):
        """Indexa documentos tanto para semantic search quanto BM25."""
        print(f"Indexando {len(documents)} documentos...")

        # Processar documentos
        for doc_id, doc in enumerate(documents):
            text = doc if isinstance(doc, str) else doc.get('text', '')
            self.chunks.append(text)
            self.metadata.append({'doc_id': doc_id, 'source': f'doc_{doc_id}'})

        print(f"Total de chunks: {len(self.chunks)}")

        # Indexação vetorial (FAISS)
        print("Indexação FAISS...")
        embeddings = self.model.encode(
            self.chunks,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )
        self.faiss_index = faiss.IndexHNSWFlat(self.dimension, 32)
        self.faiss_index.add(embeddings.astype('float32'))

        # Indexação BM25
        print("Indexação BM25...")
        tokenized_chunks = [chunk.lower().split() for chunk in self.chunks]
        self.bm25 = BM25Okapi(tokenized_chunks)

        print("✓ Indexação híbrida completa!")

    def semantic_search(self, query, top_k=10):
        """Busca semântica pura."""
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype('float32')

        distances, indices = self.faiss_index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                'chunk': self.chunks[idx],
                'score': float(dist),
                'metadata': self.metadata[idx],
                'idx': int(idx)
            })
        return results

    def bm25_search(self, query, top_k=10):
        """Busca BM25 pura."""
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        # Normalizar scores para [0, 1]
        if max(scores) > 0:
            scores = scores / max(scores)

        # Top-k indices
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'chunk': self.chunks[idx],
                'score': float(scores[idx]),
                'metadata': self.metadata[idx],
                'idx': int(idx)
            })
        return results

    def hybrid_search(self, query, top_k=10, alpha=0.7):
        """
        Busca híbrida: combina semantic + BM25.

        Args:
            alpha: peso para semantic (1.0 = só semantic, 0.0 = só BM25)
        """
        # Busca semântica (top-k * 2 para garantir overlap)
        semantic_results = self.semantic_search(query, top_k=top_k * 2)

        # Scores BM25 para todos os chunks
        query_tokens = query.lower().split()
        bm25_scores = self.bm25.get_scores(query_tokens)

        # Normalizar BM25
        if max(bm25_scores) > 0:
            bm25_scores = bm25_scores / max(bm25_scores)

        # Combinar scores
        combined_scores = {}
        for result in semantic_results:
            idx = result['idx']
            semantic_score = result['score']
            bm25_score = bm25_scores[idx]

            combined_scores[idx] = alpha * semantic_score + (1 - alpha) * bm25_score

        # Ordenar por score combinado
        ranked_indices = sorted(combined_scores.items(),
                                key=lambda x: x[1],
                                reverse=True)[:top_k]

        return [
            {
                'chunk': self.chunks[idx],
                'score': score,
                'metadata': self.metadata[idx],
                'semantic_score': next((r['score'] for r in semantic_results if r['idx'] == idx), 0),
                'bm25_score': float(bm25_scores[idx])
            }
            for idx, score in ranked_indices
        ]


def demo():
    """Demonstração de hybrid search."""
    print("=" * 80)
    print("Hybrid Search: Semantic + BM25")
    print("=" * 80)

    documents = [
        "FAISS é uma biblioteca desenvolvida pela Meta para busca vetorial eficiente.",
        "Machine learning permite que sistemas aprendam padrões a partir de dados.",
        "Python é uma linguagem de programação popular para ciência de dados.",
        "HNSW (Hierarchical Navigable Small World) é um algoritmo de approximate nearest neighbors.",
        "Vector databases como Pinecone e Weaviate são otimizados para embeddings.",
        "GPT-4 é um modelo de linguagem desenvolvido pela OpenAI com capacidades avançadas."
    ]

    engine = HybridSearchEngine(model_name='all-MiniLM-L6-v2')
    engine.index_documents(documents)

    # Query que beneficia de BM25 (nome específico)
    query = "Qual biblioteca da Meta para busca vetorial?"

    print(f"\nQuery: '{query}'")
    print("\n" + "=" * 80)

    # Comparar pure semantic vs hybrid
    print("1. Busca Puramente Semântica (alpha=1.0):")
    print("-" * 80)
    semantic_results = engine.hybrid_search(query, top_k=3, alpha=1.0)
    for i, r in enumerate(semantic_results, 1):
        print(f"{i}. [score={r['score']:.4f}] {r['chunk'][:80]}")

    print("\n2. Busca Híbrida (alpha=0.7):")
    print("-" * 80)
    hybrid_results = engine.hybrid_search(query, top_k=3, alpha=0.7)
    for i, r in enumerate(hybrid_results, 1):
        print(f"{i}. [score={r['score']:.4f}] {r['chunk'][:80]}")
        print(f"    semantic={r['semantic_score']:.3f}, bm25={r['bm25_score']:.3f}")

    print("\n3. Busca Puramente BM25 (alpha=0.0):")
    print("-" * 80)
    bm25_results = engine.hybrid_search(query, top_k=3, alpha=0.0)
    for i, r in enumerate(bm25_results, 1):
        print(f"{i}. [score={r['score']:.4f}] {r['chunk'][:80]}")

    print("\n" + "=" * 80)
    print("Análise:")
    print("=" * 80)
    print("Hybrid search combina:")
    print("  ✓ Semantic: captura significado ('biblioteca' ≈ 'sistema')")
    print("  ✓ BM25: captura termos exatos ('Meta', 'FAISS')")
    print("\nAlpha=0.7 (70% semantic, 30% BM25) funciona bem na maioria dos casos.")


if __name__ == "__main__":
    print("\n🚀 Capítulo 6: Hybrid Search\n")
    demo()
    print("\n✅ Demo concluída!")
    print("\nExperimente:")
    print("  - Diferentes valores de alpha")
    print("  - Queries com nomes próprios vs conceituais")
    print("  - Seus próprios documentos")
