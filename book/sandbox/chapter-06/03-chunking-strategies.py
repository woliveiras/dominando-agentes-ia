"""
Capítulo 6: Embeddings e Representação Semântica
Script 03: Estratégias de Chunking

Este script demonstra:
- Fixed-size chunking
- Sentence-based chunking
- Paragraph-based chunking
- Semantic chunking (usando embeddings)
- Comparação de qualidade e trade-offs

Dependências:
    uv pip install nltk sentence-transformers numpy
"""

import nltk
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

# Download necessário
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


# Texto de exemplo: documentação técnica
SAMPLE_TEXT = """
Embeddings são representações vetoriais densas de texto que capturam significado semântico.
Diferente de one-hot encoding, embeddings posicionam palavras semanticamente relacionadas próximas no espaço vetorial.

A arquitetura Transformer revolucionou o processamento de linguagem natural. Através do mecanismo de self-attention,
Transformers podem modelar dependências de longo alcance de forma eficiente. Modelos como BERT e GPT são baseados nessa arquitetura.

Vector databases são sistemas especializados para busca em alta dimensionalidade. FAISS, desenvolvido pela Meta,
oferece implementações eficientes de approximate nearest neighbor search. Outras opções incluem Pinecone, Weaviate e Qdrant.

Fine-tuning permite adaptar modelos pré-treinados para domínios específicos. Técnicas como LoRA reduzem requisitos computacionais.
O processo requer dados rotulados e cuidado para evitar overfitting em datasets pequenos.
"""


def fixed_size_chunking(text, tokenizer, chunk_size=50, overlap=10):
    """Fixed-size chunking: divide em blocos de tamanho fixo."""
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks


def sentence_based_chunking(text, target_size=100, max_size=150):
    """Sentence-based: agrupa sentenças até atingir tamanho-alvo."""
    sentences = nltk.sent_tokenize(text)
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    chunks = []
    current_chunk = []
    current_length = 0

    for sent in sentences:
        sent_length = len(tokenizer.encode(sent))

        if current_length + sent_length > max_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

        current_chunk.append(sent)
        current_length += sent_length

        if current_length >= target_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def paragraph_based_chunking(text, target_size=150):
    """Paragraph-based: divide em parágrafos, agrupa se necessário."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(tokenizer.encode(para))

        # Parágrafo muito grande: split em sentenças
        if para_length > target_size * 1.5:
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_length = 0
            chunks.extend(sentence_based_chunking(para, target_size))
            continue

        if current_length + para_length > target_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0

        current_chunk.append(para)
        current_length += para_length

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


def semantic_chunking(text, model, similarity_threshold=0.7, min_chunk_size=2):
    """Semantic: divide quando similaridade entre sentenças cai."""
    sentences = nltk.sent_tokenize(text)

    if len(sentences) < 2:
        return [text]

    # Gerar embeddings
    embeddings = model.encode(sentences, normalize_embeddings=True)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        # Similaridade entre sentença atual e anterior
        similarity = np.dot(embeddings[i], embeddings[i-1])

        if similarity >= similarity_threshold:
            # Ainda no mesmo conceito
            current_chunk.append(sentences[i])
        else:
            # Mudança de conceito detectada
            if len(current_chunk) >= min_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
            else:
                # Chunk muito pequeno, forçar continuar
                current_chunk.append(sentences[i])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def add_contextual_overlap(chunks, num_context_sentences=1):
    """Adiciona overlap contextual entre chunks."""
    if not chunks or len(chunks) < 2:
        return chunks

    overlapped_chunks = [chunks[0]]

    for i in range(1, len(chunks)):
        prev_sentences = nltk.sent_tokenize(chunks[i-1])
        context = " ".join(prev_sentences[-num_context_sentences:])
        overlapped_chunks.append(f"[Contexto: {context}]\n\n{chunks[i]}")

    return overlapped_chunks


def compare_strategies():
    """Compara todas as estratégias de chunking."""
    print("=" * 80)
    print("Comparação de Estratégias de Chunking")
    print("=" * 80)

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print(f"\nTexto original: {len(SAMPLE_TEXT)} caracteres")
    print(f"Tokens: {len(tokenizer.encode(SAMPLE_TEXT))}")

    strategies = {
        "Fixed-size (50 tokens, overlap=10)": lambda: fixed_size_chunking(SAMPLE_TEXT, tokenizer, 50, 10),
        "Sentence-based (target=100)": lambda: sentence_based_chunking(SAMPLE_TEXT, 100),
        "Paragraph-based (target=150)": lambda: paragraph_based_chunking(SAMPLE_TEXT, 150),
        "Semantic (threshold=0.7)": lambda: semantic_chunking(SAMPLE_TEXT, model, 0.7)
    }

    for strategy_name, strategy_func in strategies.items():
        print("\n" + "-" * 80)
        print(f"Estratégia: {strategy_name}")
        chunks = strategy_func()

        print(f"  Número de chunks: {len(chunks)}")
        chunk_sizes = [len(tokenizer.encode(chunk)) for chunk in chunks]
        print(f"  Tamanho médio: {np.mean(chunk_sizes):.1f} tokens")
        print(f"  Tamanho min/max: {min(chunk_sizes)}/{max(chunk_sizes)} tokens")

        print(f"\n  Preview do primeiro chunk:")
        preview = chunks[0][:150] + "..." if len(chunks[0]) > 150 else chunks[0]
        print(f"  '{preview}'")


def demonstrate_overlap():
    """Demonstra estratégia de overlap contextual."""
    print("\n" + "=" * 80)
    print("Overlap Contextual")
    print("=" * 80)

    chunks = sentence_based_chunking(SAMPLE_TEXT, target_size=100)

    print(f"\nChunks sem overlap: {len(chunks)} chunks")
    print(f"Primeiro chunk: '{chunks[0][:100]}...'")
    if len(chunks) > 1:
        print(f"Segundo chunk: '{chunks[1][:100]}...'")

    overlapped = add_contextual_overlap(chunks, num_context_sentences=1)

    print(f"\nChunks com overlap contextual: {len(overlapped)} chunks")
    if len(overlapped) > 1:
        print(f"\nSegundo chunk (com contexto):")
        print(f"'{overlapped[1][:200]}...'")

    print("\n💡 Overlap preserva contexto entre boundaries de chunks")


def domain_recommendations():
    """Recomendações de chunking por domínio."""
    print("\n" + "=" * 80)
    print("Recomendações por Domínio")
    print("=" * 80)

    recommendations = {
        "Código-fonte": "100-200 tokens, paragraph (função/classe completa)",
        "Documentação técnica": "400-600 tokens, paragraph + sentence",
        "Artigos científicos": "500-800 tokens, semantic chunking",
        "FAQs/Q&A": "200-400 tokens, sentence-based (1-3 sentenças)",
        "Transcrições/Chat": "300-500 tokens, semantic (detecta mudanças de tópico)",
        "Documentação legal": "600-1000 tokens, paragraph (cláusula completa)"
    }

    print("\nTamanho e estratégia recomendados:")
    for domain, recommendation in recommendations.items():
        print(f"  • {domain}: {recommendation}")

    print("\n💡 Sempre adicione 10-20% de overlap entre chunks!")


if __name__ == "__main__":
    print("\n🚀 Capítulo 6: Estratégias de Chunking\n")

    compare_strategies()
    demonstrate_overlap()
    domain_recommendations()

    print("\n" + "=" * 80)
    print("✅ Experimentos concluídos!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("  - Experimente com seus próprios documentos")
    print("  - Veja 04-faiss-search-engine.py para semantic search completo")
    print("  - Ajuste thresholds e tamanhos para seu caso de uso")
