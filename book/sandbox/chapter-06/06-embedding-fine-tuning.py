"""
Capítulo 6: Embeddings e Representação Semântica
Script 06: Fine-Tuning de Embeddings

Demonstra fine-tuning de Sentence Transformers usando contrastive learning.
Ver exercícios práticos no capítulo para instruções detalhadas.

Dependências:
    uv pip install sentence-transformers torch numpy
"""

from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader
import numpy as np


def create_training_data_from_pairs(query_doc_pairs):
    """
    Cria InputExamples para MultipleNegativesRankingLoss.

    Args:
        query_doc_pairs: lista de tuplas (query, documento_relevante)
    """
    train_examples = []
    for query, doc in query_doc_pairs:
        train_examples.append(InputExample(texts=[query, doc]))
    return train_examples


def create_training_data_from_triplets(triplets):
    """
    Cria InputExamples para TripletLoss.

    Args:
        triplets: lista de tuplas (anchor, positive, negative)
    """
    train_examples = []
    for anchor, positive, negative in triplets:
        train_examples.append(InputExample(texts=[anchor, positive, negative]))
    return train_examples


def fine_tune_with_mnr_loss(model_name='all-MiniLM-L6-v2', epochs=3):
    """
    Fine-tune usando MultipleNegativesRankingLoss (implementa InfoNCE).
    Método recomendado - mais eficiente que TripletLoss.
    """
    print("=" * 80)
    print("Fine-Tuning com MultipleNegativesRankingLoss")
    print("=" * 80)

    # Dados de exemplo: queries e documentos relevantes
    # Em produção, use milhares de pares
    training_pairs = [
        ("Como instalar Python?", "Python pode ser instalado através de python.org ou usando pyenv."),
        ("O que é machine learning?", "Machine learning é um subcampo de IA que permite sistemas aprenderem padrões de dados."),
        ("Como usar FAISS?", "FAISS é uma biblioteca para busca vetorial eficiente desenvolvida pela Meta."),
        ("Explique embeddings", "Embeddings são representações vetoriais densas que capturam significado semântico."),
        ("Tutorial de PyTorch", "PyTorch é um framework de deep learning com autograd dinâmico e suporte a GPU."),
    ]

    print(f"\nDados de treino: {len(training_pairs)} pares (query, documento)")

    # Criar training examples
    train_examples = create_training_data_from_pairs(training_pairs)

    # Carregar modelo base
    print(f"\nCarregando modelo base: {model_name}")
    model = SentenceTransformer(model_name)

    # DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

    # Loss function: MultipleNegativesRankingLoss
    # Cada exemplo no batch serve como negative para os outros
    train_loss = losses.MultipleNegativesRankingLoss(model=model)

    print(f"\nIniciando fine-tuning por {epochs} epochs...")
    print("(Em produção, use 1000+ exemplos e monitore validation loss)\n")

    # Fine-tune
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=int(len(train_dataloader) * 0.1),
        output_path='./models/finetuned-embeddings',
        show_progress_bar=True
    )

    print("\n✓ Fine-tuning concluído!")
    print(f"Modelo salvo em: ./models/finetuned-embeddings")

    return model


def fine_tune_with_triplet_loss(model_name='all-MiniLM-L6-v2', epochs=3):
    """Fine-tune usando TripletLoss (método clássico)."""
    print("\n" + "=" * 80)
    print("Fine-Tuning com TripletLoss")
    print("=" * 80)

    # Triplets: (anchor, positive, negative)
    triplets = [
        ("Como instalar Python?",
         "Python pode ser instalado via python.org",
         "JavaScript é uma linguagem para web"),

        ("O que é machine learning?",
         "Machine learning permite sistemas aprenderem de dados",
         "Receita de bolo de chocolate"),
    ]

    print(f"\nDados de treino: {len(triplets)} triplets")

    train_examples = create_training_data_from_triplets(triplets)

    model = SentenceTransformer(model_name)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=4)

    # TripletLoss com margin=1.0
    train_loss = losses.TripletLoss(
        model=model,
        distance_metric=losses.TripletDistanceMetric.COSINE,
        triplet_margin=1.0
    )

    print("\nIniciando fine-tuning...\n")

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=10,
        show_progress_bar=True
    )

    print("\n✓ Fine-tuning concluído!")
    return model


def compare_baseline_vs_finetuned(baseline_model, finetuned_model, test_cases):
    """Compara performance baseline vs fine-tuned."""
    print("\n" + "=" * 80)
    print("Comparação: Baseline vs Fine-Tuned")
    print("=" * 80)

    for query, positive_doc, negative_doc in test_cases:
        print(f"\nQuery: '{query}'")
        print(f"Positivo: '{positive_doc}'")
        print(f"Negativo: '{negative_doc}'")

        # Baseline
        query_emb_base = baseline_model.encode([query])[0]
        pos_emb_base = baseline_model.encode([positive_doc])[0]
        neg_emb_base = baseline_model.encode([negative_doc])[0]

        sim_pos_base = np.dot(query_emb_base, pos_emb_base)
        sim_neg_base = np.dot(query_emb_base, neg_emb_base)

        # Fine-tuned
        query_emb_ft = finetuned_model.encode([query])[0]
        pos_emb_ft = finetuned_model.encode([positive_doc])[0]
        neg_emb_ft = finetuned_model.encode([negative_doc])[0]

        sim_pos_ft = np.dot(query_emb_ft, pos_emb_ft)
        sim_neg_ft = np.dot(query_emb_ft, neg_emb_ft)

        print(f"\nBaseline:")
        print(f"  Similaridade (query, positivo): {sim_pos_base:.4f}")
        print(f"  Similaridade (query, negativo): {sim_neg_base:.4f}")
        print(f"  Separação: {sim_pos_base - sim_neg_base:.4f}")

        print(f"\nFine-tuned:")
        print(f"  Similaridade (query, positivo): {sim_pos_ft:.4f}")
        print(f"  Similaridade (query, negativo): {sim_neg_ft:.4f}")
        print(f"  Separação: {sim_pos_ft - sim_neg_ft:.4f}")

        improvement = ((sim_pos_ft - sim_neg_ft) - (sim_pos_base - sim_neg_base))
        if improvement > 0:
            print(f"\n  ✓ Melhoria na separação: +{improvement:.4f}")
        else:
            print(f"\n  ⚠ Piora na separação: {improvement:.4f}")


def demo():
    """Demonstração completa de fine-tuning."""
    print("\n🚀 Capítulo 6: Fine-Tuning de Embeddings\n")

    # Fine-tune modelo
    baseline_model = SentenceTransformer('all-MiniLM-L6-v2')
    finetuned_model = fine_tune_with_mnr_loss(epochs=1)  # Apenas 1 epoch para demo

    # Casos de teste
    test_cases = [
        ("Como usar Python para IA?",
         "Python é popular para machine learning com bibliotecas como PyTorch e TensorFlow",
         "Gatos são animais domésticos populares"),

        ("Tutorial de vector search",
         "FAISS oferece busca vetorial eficiente para embeddings de alta dimensão",
         "Receitas de culinária italiana"),
    ]

    compare_baseline_vs_finetuned(baseline_model, finetuned_model, test_cases)

    print("\n" + "=" * 80)
    print("Recomendações para Fine-Tuning em Produção:")
    print("=" * 80)
    print("""
1. Dataset: Mínimo 5K-10K pares (query, documento)
2. Validação: Separe 10-20% para validation set
3. Métricas: Monitore Precision@k e NDCG no validation set
4. Early stopping: Pare se validation loss não melhorar por N epochs
5. Synthetic data: Use LLMs para gerar queries a partir de documentos
6. Batch size: 32-64 para MultipleNegativesRankingLoss
7. Epochs: 3-5 epochs geralmente suficiente
8. Meta: >10% melhoria relativa em Precision@5 para justificar deploy
    """)

    print("\n✅ Demo concluída!")


if __name__ == "__main__":
    demo()
    print("\nPróximos passos:")
    print("  - Colete/gere 1000+ pares de treino para seu domínio")
    print("  - Implemente validation set e early stopping")
    print("  - Compare com baseline em test set realista")
    print("  - Veja documentação de Sentence Transformers para técnicas avançadas")
