"""
Exercício 2: Chain-of-Thought Math Solver

Implementa solver de problemas matemáticos usando Chain-of-Thought com
self-consistency para maximizar acurácia.

Dependências:
    uv pip install openai anthropic

Uso:
    python 02-cot-math-solver.py
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter


def load_problems(dataset_path: str) -> List[Dict]:
    """
    Carrega problemas matemáticos do dataset JSONL.
    
    Args:
        dataset_path: Caminho para arquivo JSONL
    
    Returns:
        Lista de dicionários com problem, answer e steps
    """
    problems = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems


def zero_shot_cot_prompt(problem: str) -> str:
    """
    Cria prompt zero-shot CoT.
    
    Args:
        problem: Problema matemático
    
    Returns:
        Prompt formatado
    """
    return f"""{problem}

Vamos pensar passo a passo:"""


def few_shot_cot_prompt(problem: str, examples: List[Dict]) -> str:
    """
    Cria prompt few-shot CoT com exemplos de raciocínio.
    
    Args:
        problem: Problema matemático
        examples: Lista de problemas com steps de solução
    
    Returns:
        Prompt formatado com exemplos
    """
    prompt_parts = ["Resolva problemas matemáticos mostrando todo o raciocínio:\n"]
    
    for ex in examples:
        prompt_parts.append(f"Problema: {ex['problem']}")
        prompt_parts.append("Solução:")
        for step in ex['steps']:
            prompt_parts.append(f"  - {step}")
        prompt_parts.append(f"Resposta: {ex['answer']}\n")
    
    prompt_parts.append(f"Problema: {problem}")
    prompt_parts.append("Solução:")
    
    return "\n".join(prompt_parts)


def extract_answer(response: str) -> Optional[str]:
    """
    Extrai resposta numérica do raciocínio.
    
    Args:
        response: Texto de resposta do modelo
    
    Returns:
        Resposta extraída ou None
    """
    # Procurar padrão "Resposta: X" ou "= X"
    patterns = [
        r"Resposta:\s*([0-9]+(?:[.,][0-9]+)?)",
        r"=\s*([0-9]+(?:[.,][0-9]+)?)",
        r"([0-9]+(?:[.,][0-9]+)?)\s*(?:km|litros|reais|R\$|cm|%)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response)
        if match:
            # Normalizar formato numérico
            answer = match.group(1).replace(',', '.')
            return answer.split('.')[0]  # Retornar apenas parte inteira
    
    return None


def simulate_cot_response(problem: str, method: str, examples: List[Dict] = None) -> str:
    """
    Simula resposta de LLM com raciocínio CoT.
    
    Em produção, substituir por chamada real à API do LLM.
    
    Args:
        problem: Problema matemático
        method: 'zero-shot' ou 'few-shot'
        examples: Exemplos para few-shot (opcional)
    
    Returns:
        Resposta simulada com raciocínio
    """
    # Heurística simples: buscar resposta em problem bank
    # Em produção, seria chamada real ao LLM
    
    if "trem" in problem.lower() and "80 km/h" in problem:
        return """Vamos resolver passo a passo:
1. Velocidade = 80 km/h
2. Tempo = 2.5 horas
3. Distância = Velocidade × Tempo
4. Distância = 80 × 2.5 = 200 km
Resposta: 200 km"""
    
    elif "desconto" in problem.lower() and "150" in problem:
        return """Vamos resolver passo a passo:
1. Preço original = R$ 150
2. Desconto = 20% = 0.20
3. Valor do desconto = 150 × 0.20 = R$ 30
4. Preço final = 150 - 30 = R$ 120
Resposta: R$ 120"""
    
    else:
        # Fallback genérico
        return f"""Vamos pensar sobre este problema.
Após análise, a resposta é: 42"""


def self_consistency_solve(
    problem: str, 
    n_samples: int = 5,
    method: str = 'zero-shot'
) -> Dict:
    """
    Resolve problema usando self-consistency.
    
    Args:
        problem: Problema matemático
        n_samples: Número de amostras a gerar
        method: 'zero-shot' ou 'few-shot'
    
    Returns:
        Dict com resposta votada e estatísticas
    """
    answers = []
    reasonings = []
    
    for i in range(n_samples):
        response = simulate_cot_response(problem, method)
        reasonings.append(response)
        
        answer = extract_answer(response)
        if answer:
            answers.append(answer)
    
    # Voting majoritário
    if answers:
        vote_counts = Counter(answers)
        most_common = vote_counts.most_common(1)[0]
        consensus_answer = most_common[0]
        confidence = most_common[1] / len(answers)
    else:
        consensus_answer = None
        confidence = 0.0
    
    return {
        'answer': consensus_answer,
        'confidence': confidence,
        'vote_distribution': dict(Counter(answers)),
        'n_samples': n_samples,
        'all_answers': answers
    }


def evaluate_solver(
    problems: List[Dict],
    method: str = 'zero-shot',
    use_self_consistency: bool = False,
    n_samples: int = 5
) -> Dict[str, float]:
    """
    Avalia acurácia do solver.
    
    Args:
        problems: Lista de problemas para avaliar
        method: 'zero-shot' ou 'few-shot'
        use_self_consistency: Se True, usa self-consistency
        n_samples: Número de amostras para self-consistency
    
    Returns:
        Dict com métricas de avaliação
    """
    correct = 0
    total = len(problems)
    total_cost = 0.0
    
    for prob in problems:
        if use_self_consistency:
            result = self_consistency_solve(prob['problem'], n_samples, method)
            predicted = result['answer']
            # Custo proporcional a n_samples
            total_cost += n_samples * 0.001  # Exemplo: $0.001 por chamada
        else:
            response = simulate_cot_response(prob['problem'], method)
            predicted = extract_answer(response)
            total_cost += 0.001
        
        # Normalizar para comparação
        expected = prob['answer'].split('.')[0]  # Apenas parte inteira
        
        if predicted and predicted == expected:
            correct += 1
    
    accuracy = correct / total if total > 0 else 0.0
    
    return {
        'method': method,
        'use_self_consistency': use_self_consistency,
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'estimated_cost': total_cost
    }


def main():
    """
    Função principal que compara diferentes abordagens CoT.
    """
    # Configuração
    dataset_path = Path(__file__).parent.parent.parent / "datasets" / "math_problems.jsonl"
    
    # Carregar problemas
    print("Carregando problemas matemáticos...")
    problems = load_problems(str(dataset_path))
    print(f"Total de problemas: {len(problems)}\n")
    
    # Avaliar Zero-Shot CoT
    print("=" * 60)
    print("Avaliando ZERO-SHOT CoT")
    print("=" * 60)
    results_zero = evaluate_solver(problems, method='zero-shot', use_self_consistency=False)
    print(f"Acurácia: {results_zero['accuracy']:.2%}")
    print(f"Corretos: {results_zero['correct']}/{results_zero['total']}")
    print(f"Custo estimado: ${results_zero['estimated_cost']:.3f}\n")
    
    # Avaliar Few-Shot CoT
    print("=" * 60)
    print("Avaliando FEW-SHOT CoT")
    print("=" * 60)
    results_few = evaluate_solver(problems, method='few-shot', use_self_consistency=False)
    print(f"Acurácia: {results_few['accuracy']:.2%}")
    print(f"Corretos: {results_few['correct']}/{results_few['total']}")
    print(f"Custo estimado: ${results_few['estimated_cost']:.3f}\n")
    
    # Avaliar Self-Consistency
    print("=" * 60)
    print("Avaliando SELF-CONSISTENCY (5 amostras)")
    print("=" * 60)
    results_sc = evaluate_solver(problems, method='zero-shot', use_self_consistency=True, n_samples=5)
    print(f"Acurácia: {results_sc['accuracy']:.2%}")
    print(f"Corretos: {results_sc['correct']}/{results_sc['total']}")
    print(f"Custo estimado: ${results_sc['estimated_cost']:.3f}\n")
    
    # Comparação final
    print("=" * 60)
    print("COMPARAÇÃO DE RESULTADOS")
    print("=" * 60)
    print(f"{'Método':<30} {'Acurácia':<15} {'Custo':<15}")
    print("-" * 60)
    print(f"{'Zero-Shot CoT':<30} {results_zero['accuracy']:>6.2%}        ${results_zero['estimated_cost']:>6.3f}")
    print(f"{'Few-Shot CoT':<30} {results_few['accuracy']:>6.2%}        ${results_few['estimated_cost']:>6.3f}")
    print(f"{'Self-Consistency (5x)':<30} {results_sc['accuracy']:>6.2%}        ${results_sc['estimated_cost']:>6.3f}")
    
    # Exemplo prático
    print("\n" + "=" * 60)
    print("EXEMPLO PRÁTICO: Self-Consistency")
    print("=" * 60)
    example_problem = problems[0]
    print(f"Problema: {example_problem['problem']}")
    print(f"Resposta esperada: {example_problem['answer']}\n")
    
    result = self_consistency_solve(example_problem['problem'], n_samples=5)
    print(f"Resposta por voting: {result['answer']}")
    print(f"Confiança: {result['confidence']:.2%}")
    print(f"Distribuição de votos: {result['vote_distribution']}")
    print(f"Todas as respostas: {result['all_answers']}")


if __name__ == "__main__":
    main()
