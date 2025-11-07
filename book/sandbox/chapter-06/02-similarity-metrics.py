"""
Capítulo 6: Embeddings e Representação Semântica
Script 02: Métricas de Similaridade

Este script demonstra:
- Similaridade cosseno vs distância euclidiana vs Manhattan
- Impacto da normalização
- Quando usar cada métrica
- Dot product otimizado para vetores normalizados

Dependências:
    uv pip install numpy sentence-transformers
"""

import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import time


def cosine_similarity(a, b):
    """Similaridade cosseno: mede ângulo entre vetores."""
    return np.dot(a, b) / (norm(a) * norm(b))


def euclidean_distance(a, b):
    """Distância euclidiana: comprimento direto entre pontos."""
    return norm(a - b)


def manhattan_distance(a, b):
    """Distância Manhattan (L1): soma de diferenças absolutas."""
    return np.sum(np.abs(a - b))


def l2_normalize(v):
    """L2 normalization: força ||v|| = 1."""
    return v / norm(v)


def demonstrate_metrics():
    """Demonstra diferentes métricas de similaridade."""
    print("=" * 80)
    print("1. Comparação de Métricas de Similaridade")
    print("=" * 80)

    # Vetores de exemplo
    doc1 = np.array([0.5, 0.8, 0.2, 0.1])
    doc2 = np.array([0.6, 0.7, 0.3, 0.2])  # Similar em direção
    doc3 = np.array([-0.5, -0.8, -0.2, -0.1])  # Oposto
    doc4 = np.array([0.1, 0.1, 0.9, 0.8])  # Diferente direção

    print("\nVetores:")
    print(f"  doc1: {doc1}")
    print(f"  doc2: {doc2} (direção similar)")
    print(f"  doc3: {doc3} (direção oposta)")
    print(f"  doc4: {doc4} (direção diferente)")

    print("\n" + "-" * 80)
    print("Similaridade Cosseno (range: [-1, 1], 1 = idêntico):")
    print(f"  cos_sim(doc1, doc2) = {cosine_similarity(doc1, doc2):.4f} - Similar ✓")
    print(f"  cos_sim(doc1, doc3) = {cosine_similarity(doc1, doc3):.4f} - Oposto")
    print(f"  cos_sim(doc1, doc4) = {cosine_similarity(doc1, doc4):.4f} - Diferente")

    print("\n" + "-" * 80)
    print("Distância Euclidiana (range: [0, ∞), 0 = idêntico):")
    print(f"  euclidean(doc1, doc2) = {euclidean_distance(doc1, doc2):.4f} - Próximo ✓")
    print(f"  euclidean(doc1, doc3) = {euclidean_distance(doc1, doc3):.4f} - Distante")
    print(f"  euclidean(doc1, doc4) = {euclidean_distance(doc1, doc4):.4f} - Distante")

    print("\n" + "-" * 80)
    print("Distância Manhattan:")
    print(f"  manhattan(doc1, doc2) = {manhattan_distance(doc1, doc2):.4f}")
    print(f"  manhattan(doc1, doc3) = {manhattan_distance(doc1, doc3):.4f}")
    print(f"  manhattan(doc1, doc4) = {manhattan_distance(doc1, doc4):.4f}")


def demonstrate_normalization_impact():
    """Mostra o impacto da normalização nas métricas."""
    print("\n" + "=" * 80)
    print("2. Impacto da Normalização")
    print("=" * 80)

    # Dois vetores na mesma direção, mas magnitudes diferentes
    vec_small = np.array([1.0, 2.0, 3.0])
    vec_large = np.array([10.0, 20.0, 30.0])  # 10x maior, mesma direção

    print(f"\nvec_small: {vec_small} (norm={norm(vec_small):.2f})")
    print(f"vec_large: {vec_large} (norm={norm(vec_large):.2f})")
    print(f"Direção idêntica, magnitude 10x diferente")

    print("\n" + "-" * 80)
    print("SEM normalização:")
    print(f"  Similaridade cosseno: {cosine_similarity(vec_small, vec_large):.4f} - Identifica como idênticos ✓")
    print(f"  Distância euclidiana: {euclidean_distance(vec_small, vec_large):.2f} - Considera muito diferentes")
    print(f"  Dot product: {np.dot(vec_small, vec_large):.2f} - Influenciado pela magnitude")

    print("\n" + "-" * 80)
    print("COM normalização (L2):")
    vec_small_norm = l2_normalize(vec_small)
    vec_large_norm = l2_normalize(vec_large)

    print(f"  vec_small_norm: {vec_small_norm} (norm={norm(vec_small_norm):.2f})")
    print(f"  vec_large_norm: {vec_large_norm} (norm={norm(vec_large_norm):.2f})")

    print(f"\n  Similaridade cosseno: {cosine_similarity(vec_small_norm, vec_large_norm):.4f} - Idêntico")
    print(f"  Distância euclidiana: {euclidean_distance(vec_small_norm, vec_large_norm):.6f} - Praticamente 0 ✓")
    print(f"  Dot product: {np.dot(vec_small_norm, vec_large_norm):.4f} - Idêntico")

    print("\n💡 Conclusão: Após normalização, dot product = cosine similarity")


def demonstrate_dot_product_optimization():
    """Mostra otimização de dot product vs cosine para vetores normalizados."""
    print("\n" + "=" * 80)
    print("3. Otimização: Dot Product vs Cosine Similarity")
    print("=" * 80)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Gerar muitos embeddings para benchmark
    sentences = [f"Sentença de teste número {i}" for i in range(1000)]
    print(f"\nGerando {len(sentences)} embeddings...")

    embeddings = model.encode(sentences, normalize_embeddings=True)
    print(f"Embeddings normalizados: shape={embeddings.shape}")

    query_embedding = embeddings[0]

    # Benchmark: cosine similarity
    print("\n" + "-" * 80)
    print("Método 1: Cosine Similarity (com cálculo de normas)")
    start_time = time.time()
    cosine_scores = []
    for emb in embeddings:
        score = np.dot(query_embedding, emb) / (norm(query_embedding) * norm(emb))
        cosine_scores.append(score)
    cosine_time = time.time() - start_time
    print(f"  Tempo: {cosine_time:.4f}s")

    # Benchmark: dot product (vetores já normalizados)
    print("\nMétodo 2: Dot Product (vetores já normalizados)")
    start_time = time.time()
    dot_scores = []
    for emb in embeddings:
        score = np.dot(query_embedding, emb)
        dot_scores.append(score)
    dot_time = time.time() - start_time
    print(f"  Tempo: {dot_time:.4f}s")

    # Verificar equivalência
    max_diff = max(abs(c - d) for c, d in zip(cosine_scores, dot_scores))
    print(f"\n  Diferença máxima entre métodos: {max_diff:.10f}")
    print(f"  Speedup: {cosine_time/dot_time:.2f}x mais rápido")

    print("\n💡 Conclusão: Para vetores normalizados, use dot product - é equivalente e mais rápido!")


def decision_guide():
    """Guia de decisão: qual métrica usar."""
    print("\n" + "=" * 80)
    print("4. Guia de Decisão: Qual Métrica Usar?")
    print("=" * 80)

    guide = {
        "Similaridade Cosseno (ou Dot Product normalizado)": [
            "✓ Embeddings de modelos de linguagem (BERT, Sentence Transformers)",
            "✓ Documentos de comprimentos variados",
            "✓ Quando direção > magnitude",
            "✓ Padrão seguro para 90% dos casos"
        ],
        "Distância Euclidiana": [
            "✓ Quando magnitude carrega informação (ex: intensidade)",
            "✓ Embeddings não-normalizados onde escala importa",
            "✓ Clustering espacial",
            "⚠ Menos comum em NLP moderno"
        ],
        "Distância Manhattan": [
            "✓ Features esparsas ou one-hot",
            "✓ Quando máxima eficiência é crítica",
            "⚠ Menos interpretável em alta dimensão"
        ]
    }

    for metric, use_cases in guide.items():
        print(f"\n{metric}:")
        for case in use_cases:
            print(f"  {case}")


def practical_example():
    """Exemplo prático: busca semântica com diferentes métricas."""
    print("\n" + "=" * 80)
    print("5. Exemplo Prático: Busca Semântica")
    print("=" * 80)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    documents = [
        "Python é uma linguagem de programação interpretada",
        "Machine learning é um subcampo de IA",
        "Gatos são animais domésticos populares",
        "JavaScript é usada para desenvolvimento web",
        "Deep learning usa redes neurais artificiais"
    ]

    query = "Qual a melhor linguagem para aprendizado de máquina?"

    print(f"\nQuery: '{query}'")
    print(f"\nDocumentos indexados: {len(documents)}")

    # Gerar embeddings (normalizados)
    doc_embeddings = model.encode(documents, normalize_embeddings=True)
    query_embedding = model.encode([query], normalize_embeddings=True)[0]

    print("\n" + "-" * 80)
    print("Ranking por Cosine Similarity (dot product):")
    scores = [(i, np.dot(query_embedding, emb)) for i, emb in enumerate(doc_embeddings)]
    scores.sort(key=lambda x: x[1], reverse=True)

    for rank, (doc_idx, score) in enumerate(scores[:3], 1):
        print(f"  {rank}. [{score:.4f}] {documents[doc_idx]}")

    print("\n" + "-" * 80)
    print("Ranking por Distância Euclidiana:")
    distances = [(i, euclidean_distance(query_embedding, emb)) for i, emb in enumerate(doc_embeddings)]
    distances.sort(key=lambda x: x[1])

    for rank, (doc_idx, dist) in enumerate(distances[:3], 1):
        print(f"  {rank}. [dist={dist:.4f}] {documents[doc_idx]}")

    print("\n💡 Ambos métodos retornam mesmo ranking (vetores normalizados)")


if __name__ == "__main__":
    print("\n🚀 Capítulo 6: Métricas de Similaridade\n")

    demonstrate_metrics()
    demonstrate_normalization_impact()
    demonstrate_dot_product_optimization()
    decision_guide()
    practical_example()

    print("\n" + "=" * 80)
    print("✅ Experimentos concluídos!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("  - Veja 03-chunking-strategies.py para estratégias de segmentação")
    print("  - Experimente com seus próprios dados")
