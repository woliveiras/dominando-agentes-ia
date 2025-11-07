"""
Exercício 1: Few-Shot Dynamic Classifier

Implementa classificador de sentimento usando few-shot learning com seleção
dinâmica de exemplos baseada em similaridade semântica.

Dependências:
    uv pip install sentence-transformers scikit-learn openai anthropic

Uso:
    python 01-few-shot-classifier.py
"""

import json
import random
from pathlib import Path
from typing import List, Dict
from collections import Counter

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class FewShotSelector:
    """
    Seletor dinâmico de exemplos few-shot baseado em similaridade semântica.
    """
    
    def __init__(self, example_bank: List[Dict[str, str]], k: int = 5):
        """
        Args:
            example_bank: Lista de dicts com 'text' e 'sentiment'
            k: Número de exemplos a selecionar
        """
        self.example_bank = example_bank
        self.k = k
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Pré-computar embeddings
        texts = [ex['text'] for ex in example_bank]
        print(f"Computando embeddings de {len(texts)} exemplos...")
        self.embeddings = self.encoder.encode(texts, show_progress_bar=True)
    
    def select_random(self, query: str) -> List[Dict[str, str]]:
        """
        Seleciona k exemplos aleatórios (baseline).
        
        Args:
            query: Texto a classificar
        
        Returns:
            Lista de k exemplos aleatórios
        """
        return random.sample(self.example_bank, self.k)
    
    def select_similar(self, query: str) -> List[Dict[str, str]]:
        """
        Seleciona k exemplos mais similares ao query.
        
        Args:
            query: Texto a classificar
        
        Returns:
            Lista de k exemplos mais relevantes
        """
        query_embedding = self.encoder.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Top-k índices
        top_k_indices = np.argsort(similarities)[-self.k:][::-1]
        
        return [self.example_bank[i] for i in top_k_indices]
    
    def build_prompt(
        self, 
        query: str, 
        examples: List[Dict[str, str]],
        method: str
    ) -> str:
        """
        Constrói prompt few-shot com exemplos.
        
        Args:
            query: Texto a classificar
            examples: Exemplos selecionados
            method: Método de seleção usado
        
        Returns:
            Prompt completo formatado
        """
        task_description = """Classifique o sentimento do texto como POSITIVO, NEGATIVO ou NEUTRO.

Exemplos:
"""
        
        prompt_parts = [task_description]
        
        for i, ex in enumerate(examples, 1):
            prompt_parts.append(f"{i}. Texto: \"{ex['text']}\"")
            prompt_parts.append(f"   Sentimento: {ex['sentiment']}\n")
        
        prompt_parts.append(f"Agora classifique:\nTexto: \"{query}\"")
        prompt_parts.append("Sentimento:")
        
        return "\n".join(prompt_parts)


def load_examples(dataset_path: str) -> List[Dict[str, str]]:
    """
    Carrega exemplos do dataset JSONL.
    
    Args:
        dataset_path: Caminho para arquivo JSONL
    
    Returns:
        Lista de dicionários com text e sentiment
    """
    examples = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))
    return examples


def simulate_llm_response(prompt: str, examples: List[Dict[str, str]]) -> str:
    """
    Simula resposta de LLM usando heurística simples.
    
    Em produção, substituir por chamada real:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    
    Args:
        prompt: Prompt construído
        examples: Exemplos usados no prompt
    
    Returns:
        Sentimento classificado (POSITIVO/NEGATIVO/NEUTRO)
    """
    # Heurística simples: conta sentimentos dos exemplos
    sentiments = [ex['sentiment'] for ex in examples]
    sentiment_counts = Counter(sentiments)
    
    # Retorna sentimento mais comum nos exemplos (simplificação)
    return sentiment_counts.most_common(1)[0][0]


def evaluate_method(
    selector: FewShotSelector,
    test_examples: List[Dict[str, str]],
    method: str = 'similar'
) -> Dict[str, float]:
    """
    Avalia acurácia de um método de seleção.
    
    Args:
        selector: Seletor de exemplos configurado
        test_examples: Exemplos para testar
        method: 'random' ou 'similar'
    
    Returns:
        Dict com métricas de avaliação
    """
    correct = 0
    total = len(test_examples)
    
    for test_ex in test_examples:
        # Selecionar exemplos
        if method == 'random':
            selected = selector.select_random(test_ex['text'])
        else:
            selected = selector.select_similar(test_ex['text'])
        
        # Construir prompt
        prompt = selector.build_prompt(test_ex['text'], selected, method)
        
        # Obter predição (simulada)
        predicted = simulate_llm_response(prompt, selected)
        
        # Verificar acurácia
        if predicted == test_ex['sentiment']:
            correct += 1
    
    accuracy = correct / total
    return {
        'method': method,
        'accuracy': accuracy,
        'correct': correct,
        'total': total
    }


def main():
    """
    Função principal que executa comparação de métodos.
    """
    # Configuração
    dataset_path = Path(__file__).parent.parent.parent / "datasets" / "sentiment_examples.jsonl"
    k_examples = 3  # Número de exemplos few-shot
    
    # Carregar dados
    print(f"Carregando exemplos de {dataset_path}...")
    all_examples = load_examples(str(dataset_path))
    
    # Split train/test (80/20)
    random.seed(42)
    random.shuffle(all_examples)
    split_idx = int(len(all_examples) * 0.8)
    train_examples = all_examples[:split_idx]
    test_examples = all_examples[split_idx:]
    
    print(f"Train: {len(train_examples)} exemplos")
    print(f"Test: {len(test_examples)} exemplos\n")
    
    # Criar seletor
    selector = FewShotSelector(train_examples, k=k_examples)
    
    # Avaliar método aleatório
    print("=" * 60)
    print("Avaliando seleção ALEATÓRIA de exemplos...")
    print("=" * 60)
    results_random = evaluate_method(selector, test_examples, method='random')
    print(f"Acurácia: {results_random['accuracy']:.2%}")
    print(f"Corretos: {results_random['correct']}/{results_random['total']}\n")
    
    # Avaliar método por similaridade
    print("=" * 60)
    print("Avaliando seleção por SIMILARIDADE SEMÂNTICA...")
    print("=" * 60)
    results_similar = evaluate_method(selector, test_examples, method='similar')
    print(f"Acurácia: {results_similar['accuracy']:.2%}")
    print(f"Corretos: {results_similar['correct']}/{results_similar['total']}\n")
    
    # Comparação
    improvement = results_similar['accuracy'] - results_random['accuracy']
    print("=" * 60)
    print("COMPARAÇÃO DE RESULTADOS")
    print("=" * 60)
    print(f"Método Aleatório: {results_random['accuracy']:.2%}")
    print(f"Método Semântico: {results_similar['accuracy']:.2%}")
    print(f"Melhoria: {improvement:+.2%}")
    
    # Exemplo prático
    print("\n" + "=" * 60)
    print("EXEMPLO PRÁTICO")
    print("=" * 60)
    test_text = "Este produto é fantástico, adorei!"
    
    # Exemplos aleatórios
    random_ex = selector.select_random(test_text)
    print("\nExemplos ALEATÓRIOS selecionados:")
    for i, ex in enumerate(random_ex, 1):
        print(f"{i}. \"{ex['text']}\" → {ex['sentiment']}")
    
    # Exemplos similares
    similar_ex = selector.select_similar(test_text)
    print("\nExemplos SIMILARES selecionados:")
    for i, ex in enumerate(similar_ex, 1):
        print(f"{i}. \"{ex['text']}\" → {ex['sentiment']}")
    
    print(f"\nTexto para classificar: \"{test_text}\"")
    print(f"Sentimento esperado: POSITIVO")


if __name__ == "__main__":
    main()
