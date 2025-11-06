"""
Capítulo 3: Fine-Tuning e Otimização
Exemplo 3: Avaliação com LLM-as-Judge

Sistema de avaliação automática de respostas de LLM usando outro LLM
como juiz, incluindo rubrica estruturada e análise de viés.

Instalação necessária:
uv pip install anthropic

Execução:
export ANTHROPIC_API_KEY="sua-chave-aqui"
python 03-llm-as-judge.py

Nota: Requer chave de API da Anthropic.
"""

import anthropic
import json
import os
from typing import Dict

# Configurar cliente
# IMPORTANTE: Defina ANTHROPIC_API_KEY como variável de ambiente
# export ANTHROPIC_API_KEY="sua-chave-aqui"
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    print("="*60)
    print("⚠️  ANTHROPIC_API_KEY não definida!")
    print("="*60)
    print("""
Para usar este exemplo, você precisa:

1. Criar conta na Anthropic: https://console.anthropic.com/
2. Obter sua API key
3. Definir como variável de ambiente:
   
   export ANTHROPIC_API_KEY='sua-chave-aqui'

Ou defina no código (não recomendado para produção):
   
   api_key = "sua-chave-aqui"
""")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)
print("✅ Cliente Anthropic configurado")

def evaluate_with_judge(question: str, model_answer: str, correct_answer: str, task: str) -> Dict:
    """Usa Claude como judge para avaliar resposta"""

    judge_prompt = f"""Você é um avaliador imparcial de respostas de modelos de linguagem.

Tarefa: {task}
Pergunta: {question}
Resposta esperada: {correct_answer}
Resposta do modelo: {model_answer}

Avalie a resposta do modelo nos seguintes critérios (0-5):
1. Correção factual: A resposta está factualmente correta?
2. Completude: A resposta é completa e aborda toda a pergunta?
3. Clareza: A resposta é clara e bem articulada?

Forneça sua avaliação em formato JSON:
{{
    "factual_correctness": <score 0-5>,
    "completeness": <score 0-5>,
    "clarity": <score 0-5>,
    "overall": <score 0-5>,
    "justification": "<breve explicação>"
}}
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{"role": "user", "content": judge_prompt}]
    )

    # Parsear resposta JSON
    try:
        result = json.loads(response.content[0].text)
        return result
    except json.JSONDecodeError:
        return {"error": "Failed to parse judge response"}

# Dados de exemplo para avaliação
eval_data = [
    {
        "question": "Qual é a capital da França?",
        "correct_answer": "Paris",
        "task": "Resposta factual direta"
    },
    {
        "question": "Quem escreveu Dom Casmurro?",
        "correct_answer": "Machado de Assis",
        "task": "Conhecimento literário"
    },
    {
        "question": "Explique o que é uma função em Python",
        "correct_answer": "Uma função em Python é um bloco de código reutilizável definido com 'def' que pode receber parâmetros e retornar valores.",
        "task": "Explicação técnica"
    }
]

# Simular respostas de dois modelos
model_a_responses = {
    "Qual é a capital da França?": "Paris",
    "Quem escreveu Dom Casmurro?": "Machado de Assis",
    "Explique o que é uma função em Python": "Uma função é um bloco de código reutilizável definido com 'def'."
}

model_b_responses = {
    "Qual é a capital da França?": "A capital francesa é Paris, localizada no norte do país.",
    "Quem escreveu Dom Casmurro?": "Machado de Assis, um dos maiores escritores brasileiros.",
    "Explique o que é uma função em Python": "Em Python, uma função é um bloco de código que pode ser reutilizado. Você a define usando a palavra-chave 'def' seguida pelo nome da função e parâmetros opcionais."
}

# Avaliar alguns exemplos
print("="*60)
print("🧪 AVALIAÇÃO COM LLM-AS-JUDGE")
print("="*60 + "\n")

results_a = []
results_b = []

for example in eval_data[:3]:  # Avaliar apenas primeiros 3 para demonstração
    question = example['question']
    correct = example['correct_answer']
    task = example['task']

    # Avaliar Modelo A
    print(f"\nAvaliando: {question}")
    print(f"Task: {task}")

    if question in model_a_responses:
        print("\n⏳ Avaliando respostas...")

        eval_a = evaluate_with_judge(question, model_a_responses[question], correct, task)
        eval_b = evaluate_with_judge(question, model_b_responses[question], correct, task)

        results_a.append(eval_a)
        results_b.append(eval_b)

        print(f"\nModelo A: {model_a_responses[question]}")
        print(f"  Score: {eval_a.get('overall', 'N/A')}/5")
        print(f"  Razão: {eval_a.get('justification', 'N/A')}")

        print(f"\nModelo B: {model_b_responses[question]}")
        print(f"  Score: {eval_b.get('overall', 'N/A')}/5")
        print(f"  Razão: {eval_b.get('justification', 'N/A')}")

# Comparação final
print("\n" + "="*60)
print("📊 RESUMO COMPARATIVO")
print("="*60 + "\n")

avg_a = sum(r.get('overall', 0) for r in results_a) / len(results_a) if results_a else 0
avg_b = sum(r.get('overall', 0) for r in results_b) / len(results_b) if results_b else 0

print(f"Modelo A - Score médio: {avg_a:.2f}/5")
print(f"Modelo B - Score médio: {avg_b:.2f}/5")
print(f"\nVencedor: {'Modelo B' if avg_b > avg_a else 'Modelo A' if avg_a > avg_b else 'Empate'}")

print("\n" + "="*60)
print("💡 INSIGHTS")
print("="*60)
print("""
1. LLM-as-judge correlaciona bem com preferências humanas (~0.7-0.85)
2. Mais rápido e barato que avaliação humana
3. Útil para iteração rápida durante desenvolvimento
4. Cuidado com vieses (comprimento, estilo)
5. Sempre validar com avaliação humana para decisões críticas
""")
