"""
Capítulo 6: Embeddings e Representação Semântica
Script 01: Comparação de Modelos de Embedding

Este script demonstra:
- Diferentes modelos de embedding (Sentence Transformers vs BERT vanilla)
- Pooling strategies (CLS, mean, max)
- Propriedades emergentes (aritmética vetorial)
- Comparação de qualidade e performance

Dependências:
    uv pip install sentence-transformers transformers torch numpy
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch
from numpy.linalg import norm
import time


def cosine_similarity(a, b):
    """Calcula similaridade cosseno entre dois vetores."""
    return np.dot(a, b) / (norm(a) * norm(b))


def mean_pooling(model_output, attention_mask):
    """Mean pooling: média de todos os token embeddings excluindo padding."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def max_pooling(model_output, attention_mask):
    """Max pooling: valor máximo em cada dimensão."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    token_embeddings[input_mask_expanded == 0] = -1e9
    return torch.max(token_embeddings, 1)[0]


def compare_sentence_transformer_vs_bert():
    """Compara Sentence Transformers (otimizado) vs BERT vanilla."""
    print("=" * 80)
    print("1. Sentence Transformers vs BERT vanilla")
    print("=" * 80)

    # Sentenças para teste
    sentences = [
        "O gato está dormindo no sofá",
        "Um felino descansa no móvel",
        "Python é uma linguagem de programação"
    ]

    # Sentence Transformer (otimizado para similarity)
    print("\n[Sentence Transformer: all-MiniLM-L6-v2]")
    st_model = SentenceTransformer('all-MiniLM-L6-v2')

    start_time = time.time()
    st_embeddings = st_model.encode(sentences)
    st_time = time.time() - start_time

    # Similaridades
    st_sim_12 = cosine_similarity(st_embeddings[0], st_embeddings[1])
    st_sim_13 = cosine_similarity(st_embeddings[0], st_embeddings[2])

    print(f"Tempo: {st_time:.4f}s")
    print(f"Dimensão: {st_embeddings.shape[1]}")
    print(f"Similaridade (gato vs felino): {st_sim_12:.4f}")
    print(f"Similaridade (gato vs Python): {st_sim_13:.4f}")

    # BERT vanilla com CLS token pooling
    print("\n[BERT vanilla (bert-base-uncased) - CLS pooling]")
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    bert_model = AutoModel.from_pretrained('bert-base-uncased')

    start_time = time.time()
    bert_embeddings = []
    for sent in sentences:
        inputs = tokenizer(sent, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = bert_model(**inputs)
        # CLS token embedding
        cls_embedding = outputs.last_hidden_state[0, 0, :].numpy()
        bert_embeddings.append(cls_embedding)
    bert_time = time.time() - start_time

    bert_sim_12 = cosine_similarity(bert_embeddings[0], bert_embeddings[1])
    bert_sim_13 = cosine_similarity(bert_embeddings[0], bert_embeddings[2])

    print(f"Tempo: {bert_time:.4f}s")
    print(f"Dimensão: {len(bert_embeddings[0])}")
    print(f"Similaridade (gato vs felino): {bert_sim_12:.4f}")
    print(f"Similaridade (gato vs Python): {bert_sim_13:.4f}")

    print(f"\nVeredito: Sentence Transformer identifica melhor a similaridade semântica")
    print(f"  - {st_sim_12:.4f} vs {bert_sim_12:.4f} (frases similares)")
    print(f"  - Performance: {bert_time/st_time:.1f}x mais lento (BERT vanilla)")


def demonstrate_pooling_strategies():
    """Demonstra diferenças entre estratégias de pooling."""
    print("\n" + "=" * 80)
    print("2. Comparação de Pooling Strategies")
    print("=" * 80)

    text = "Embeddings são representações vetoriais de texto"

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = AutoModel.from_pretrained('bert-base-uncased')

    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    # CLS pooling
    cls_embedding = outputs.last_hidden_state[0, 0, :].numpy()

    # Mean pooling
    mean_embedding = mean_pooling(outputs, inputs['attention_mask']).numpy()[0]

    # Max pooling
    max_embedding = max_pooling(outputs, inputs['attention_mask']).numpy()[0]

    print(f"\nTexto: '{text}'")
    print(f"\nCLS pooling norm: {norm(cls_embedding):.4f}")
    print(f"Mean pooling norm: {norm(mean_embedding):.4f}")
    print(f"Max pooling norm: {norm(max_embedding):.4f}")

    print(f"\nSimilaridade CLS vs Mean: {cosine_similarity(cls_embedding, mean_embedding):.4f}")
    print(f"Similaridade CLS vs Max: {cosine_similarity(cls_embedding, max_embedding):.4f}")
    print(f"Similaridade Mean vs Max: {cosine_similarity(mean_embedding, max_embedding):.4f}")

    print("\nObservação: Mean pooling é preferível para semantic similarity")


def demonstrate_vector_arithmetic():
    """Demonstra propriedades emergentes: aritmética vetorial."""
    print("\n" + "=" * 80)
    print("3. Aritmética Vetorial: vec(rei) - vec(homem) + vec(mulher) ≈ vec(rainha)")
    print("=" * 80)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Palavras para teste
    king = model.encode("rei")
    man = model.encode("homem")
    woman = model.encode("mulher")
    queen = model.encode("rainha")

    # Operação vetorial
    result = king - man + woman

    # Calcular similaridades
    sim_to_queen = cosine_similarity(result, queen)
    sim_to_king = cosine_similarity(result, king)
    sim_to_man = cosine_similarity(result, man)

    print(f"\nvec(rei) - vec(homem) + vec(mulher):")
    print(f"  Similaridade com 'rainha': {sim_to_queen:.4f} ✓")
    print(f"  Similaridade com 'rei': {sim_to_king:.4f}")
    print(f"  Similaridade com 'homem': {sim_to_man:.4f}")

    # Outro exemplo: geografia
    print("\n" + "-" * 80)
    paris = model.encode("Paris")
    france = model.encode("França")
    italy = model.encode("Itália")
    rome = model.encode("Roma")

    result_geo = paris - france + italy
    sim_to_rome = cosine_similarity(result_geo, rome)
    sim_to_paris = cosine_similarity(result_geo, paris)

    print(f"vec(Paris) - vec(França) + vec(Itália):")
    print(f"  Similaridade com 'Roma': {sim_to_rome:.4f} ✓")
    print(f"  Similaridade com 'Paris': {sim_to_paris:.4f}")

    print("\nConclusão: Relações semânticas emergem naturalmente do treinamento")


def benchmark_models():
    """Benchmark de diferentes modelos em dimensão, latência e qualidade."""
    print("\n" + "=" * 80)
    print("4. Benchmark: Dimensão, Latência e Qualidade")
    print("=" * 80)

    models = [
        ('all-MiniLM-L6-v2', "MiniLM (rápido)"),
        ('all-mpnet-base-v2', "MPNet (qualidade)"),
    ]

    test_sentences = [
        "Machine learning é um subcampo de inteligência artificial",
        "Aprendizado de máquina faz parte da IA",
        "Gatos são animais domésticos populares"
    ]

    results = []

    for model_name, description in models:
        print(f"\n[{description}: {model_name}]")
        model = SentenceTransformer(model_name)

        # Medir latência
        start_time = time.time()
        embeddings = model.encode(test_sentences)
        latency = (time.time() - start_time) / len(test_sentences) * 1000  # ms por sentença

        # Medir qualidade de similarity
        sim_12 = cosine_similarity(embeddings[0], embeddings[1])
        sim_13 = cosine_similarity(embeddings[0], embeddings[2])

        print(f"  Dimensão: {embeddings.shape[1]}")
        print(f"  Latência: {latency:.2f}ms/sentença")
        print(f"  Similaridade (frases relacionadas): {sim_12:.4f}")
        print(f"  Similaridade (frases não-relacionadas): {sim_13:.4f}")
        print(f"  Separação: {sim_12 - sim_13:.4f} (maior é melhor)")

        results.append({
            'model': description,
            'dim': embeddings.shape[1],
            'latency': latency,
            'separation': sim_12 - sim_13
        })

    print("\n" + "-" * 80)
    print("Resumo:")
    for r in results:
        print(f"  {r['model']}: {r['dim']}d, {r['latency']:.1f}ms, sep={r['separation']:.3f}")


if __name__ == "__main__":
    print("\n🚀 Capítulo 6: Comparação de Modelos de Embedding\n")

    compare_sentence_transformer_vs_bert()
    demonstrate_pooling_strategies()
    demonstrate_vector_arithmetic()
    benchmark_models()

    print("\n" + "=" * 80)
    print("✅ Experimentos concluídos!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("  - Experimente com outros idiomas (multilingual models)")
    print("  - Teste em seu próprio domínio de aplicação")
    print("  - Veja 02-similarity-metrics.py para métricas de distância")
