"""
Capítulo 2: Treinamento de Foundation Models
Exemplo 1: Métricas de Qualidade de Dataset

Implementa heurísticas para avaliar qualidade textual: entropia de Shannon,
type-token ratio, e detecção de padrões problemáticos.

Instalação necessária:
(Usa apenas bibliotecas padrão do Python)

Execução:
python 01-quality-metrics.py
"""

import math
from collections import Counter

def calculate_entropy(text):
    """Calcula entropia de Shannon dos tokens (diversidade vocabular)"""
    words = text.lower().split()
    if not words:
        return 0.0

    # Conta frequência de cada palavra
    word_counts = Counter(words)
    total_words = len(words)

    # Calcula entropia: H = -Σ(p(x) * log2(p(x)))
    entropy = 0.0
    for count in word_counts.values():
        probability = count / total_words
        entropy -= probability * math.log2(probability)

    return entropy

def count_stopwords(text):
    """Conta stopwords comuns (palavras funcionais)"""
    # Stopwords básicas em inglês
    stopwords = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their'
    }

    words = text.lower().split()
    stopword_count = sum(1 for word in words if word in stopwords)
    return stopword_count

def count_uppercase(text):
    """Conta caracteres maiúsculos"""
    return sum(1 for c in text if c.isupper())

def count_duplicates(lines):
    """Calcula proporção de linhas duplicadas"""
    if not lines:
        return 0.0
    line_counts = Counter(lines)
    duplicates = sum(count - 1 for count in line_counts.values() if count > 1)
    return duplicates / len(lines)

def is_high_quality(text):
    # Proporção de stopwords (palavras comuns)
    words = text.split()
    if len(words) == 0:
        return False

    stopword_ratio = count_stopwords(text) / len(words)
    if stopword_ratio < 0.2:  # Muito técnico ou spam
        return False

    # Entropia de tokens (diversidade vocabular)
    token_entropy = calculate_entropy(text)
    if token_entropy < 3.0:  # Muito repetitivo
        return False

    # Proporção de letras maiúsculas
    if len(text) > 0:
        upper_ratio = count_uppercase(text) / len(text)
        if upper_ratio > 0.3:  # MUITO SPAM ASSIM
            return False

    # Número de linhas duplicadas
    duplicate_lines = count_duplicates(text.split('\n'))
    if duplicate_lines > 0.5:  # Mais de 50% repetido
        return False

    return True


# Testes de exemplo
if __name__ == "__main__":
    print("="*60)
    print("Testando Métricas de Qualidade de Texto")
    print("="*60)

    # Texto de alta qualidade
    good_text = """
    The transformer architecture revolutionized natural language processing.
    It uses self-attention mechanisms to process sequences efficiently.
    This has led to breakthroughs in language understanding.
    """

    # Texto de baixa qualidade (spam)
    spam_text = """
    BUY NOW BUY NOW BUY NOW!!!
    CLICK HERE CLICK HERE!!!
    FREE FREE FREE!!!
    """

    # Texto repetitivo
    repetitive_text = "hello hello hello " * 100

    print("\n--- Texto de Alta Qualidade ---")
    print(f"Entropia: {calculate_entropy(good_text):.2f}")
    print(f"Stopword ratio: {count_stopwords(good_text) / len(good_text.split()):.2f}")
    print(f"Uppercase ratio: {count_uppercase(good_text) / len(good_text):.2f}")
    print(f"É alta qualidade? {is_high_quality(good_text)}")

    print("\n--- Texto de Spam ---")
    print(f"Entropia: {calculate_entropy(spam_text):.2f}")
    print(f"Stopword ratio: {count_stopwords(spam_text) / len(spam_text.split()):.2f}")
    print(f"Uppercase ratio: {count_uppercase(spam_text) / len(spam_text):.2f}")
    print(f"É alta qualidade? {is_high_quality(spam_text)}")

    print("\n--- Texto Repetitivo ---")
    print(f"Entropia: {calculate_entropy(repetitive_text):.2f}")
    print(f"É alta qualidade? {is_high_quality(repetitive_text)}")
