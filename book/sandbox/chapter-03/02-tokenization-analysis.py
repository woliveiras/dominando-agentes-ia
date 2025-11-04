# Capítulo 3: Análise de Tokenização e Custos de API
# Exercício 1 do capítulo - análise prática de eficiência

# Instalação necessária: pip install tiktoken transformers

import tiktoken

# Carregar tokenizer GPT-4
try:
    enc = tiktoken.encoding_for_model("gpt-4")
except KeyError:
    enc = tiktoken.get_encoding("cl100k_base")

def analyze_tokenization(text, language):
    """Analisa eficiência de tokenização para um texto"""
    tokens = enc.encode(text)
    token_count = len(tokens)

    print(f"\n{'='*60}")
    print(f"Idioma: {language}")
    print(f"{'='*60}")
    print(f"Texto original: {text}")
    print(f"Número de tokens: {token_count}")
    print(f"Caracteres: {len(text)}")
    print(f"Razão caracteres/token: {len(text)/token_count:.2f}")

    # Visualizar tokens
    print("\nTokens decodificados:")
    for i, token in enumerate(tokens[:10]):  # Mostrar apenas primeiros 10
        decoded = enc.decode([token])
        print(f"  Token {i}: '{decoded}' (ID: {token})")

    if len(tokens) > 10:
        print(f"  ... e mais {len(tokens) - 10} tokens")

    return token_count

# Teste 1: Comparar eficiência entre idiomas
print("\n🔍 TESTE 1: Eficiência Multilíngue\n")

texts = {
    "Inglês": "The quick brown fox jumps over the lazy dog. Machine learning models require large datasets.",
    "Português": "A rápida raposa marrom pula sobre o cachorro preguiçoso. Modelos de aprendizado de máquina requerem grandes conjuntos de dados.",
    "Japonês": "素早い茶色の狐が怠け者の犬を飛び越える。機械学習モデルは大規模なデータセットを必要とする。",
    "Espanhol": "El rápido zorro marrón salta sobre el perro perezoso. Los modelos de aprendizaje automático requieren grandes conjuntos de datos."
}

results = {}
for lang, text in texts.items():
    results[lang] = analyze_tokenization(text, lang)

# Comparação
print(f"\n{'='*60}")
print("📊 COMPARAÇÃO DE EFICIÊNCIA")
print(f"{'='*60}")
baseline = results["Inglês"]
for lang, count in results.items():
    efficiency = (count / baseline) * 100
    print(f"{lang:12} {count:4} tokens ({efficiency:6.1f}% vs Inglês)")

# Teste 2: Estimar custos de API
print("\n\n💰 TESTE 2: Estimativa de Custos de API\n")

# Preços típicos (valores aproximados em USD por 1K tokens)
pricing = {
    "GPT-4 Turbo": {"input": 0.01, "output": 0.03},
    "GPT-3.5 Turbo": {"input": 0.0005, "output": 0.0015},
    "Claude 3 Opus": {"input": 0.015, "output": 0.075},
    "Claude 3 Haiku": {"input": 0.00025, "output": 0.00125}
}

# Simular prompt típico
prompt = texts["Português"]
expected_output_tokens = 200  # Resposta esperada
input_tokens = results["Português"]

print(f"Prompt: '{prompt[:50]}...'")
print(f"Tokens de input: {input_tokens}")
print(f"Tokens de output estimados: {expected_output_tokens}")
print(f"\nCustos estimados por requisição:\n")

for model, prices in pricing.items():
    input_cost = (input_tokens / 1000) * prices["input"]
    output_cost = (expected_output_tokens / 1000) * prices["output"]
    total_cost = input_cost + output_cost
    print(f"{model:20} ${total_cost:.6f} (input: ${input_cost:.6f} + output: ${output_cost:.6f})")

# Teste 3: Otimização de Prompt
print("\n\n✂️ TESTE 3: Otimização de Prompt para Reduzir Tokens\n")

verbose_prompt = """
Por favor, você poderia me ajudar a analisar o seguinte texto e me fornecer uma análise
completa e detalhada sobre o sentimento expresso no texto, incluindo se é positivo,
negativo ou neutro? Aqui está o texto que eu gostaria que você analisasse:

"Este produto é excelente! Recomendo fortemente."

Muito obrigado pela sua ajuda!
"""

optimized_prompt = """
Classifique o sentimento (positivo/negativo/neutro):

"Este produto é excelente! Recomendo fortemente."
"""

verbose_tokens = len(enc.encode(verbose_prompt))
optimized_tokens = len(enc.encode(optimized_prompt))
reduction = ((verbose_tokens - optimized_tokens) / verbose_tokens) * 100

print(f"Prompt verboso: {verbose_tokens} tokens")
print(f"Prompt otimizado: {optimized_tokens} tokens")
print(f"Redução: {reduction:.1f}%")
print(f"\nEconomia em 1000 requisições (GPT-4):")
saved_tokens = (verbose_tokens - optimized_tokens) * 1000
saved_cost = (saved_tokens / 1000) * pricing["GPT-4 Turbo"]["input"]
print(f"  Tokens economizados: {saved_tokens:,}")
print(f"  Custo economizado: ${saved_cost:.2f}")

print("\n" + "="*60)
print("💡 INSIGHTS")
print("="*60)
print("""
1. Inglês é ~40-50% mais eficiente que português em tokenização
2. Otimizar prompts pode reduzir custos em 50-70%
3. Para alto volume, considere modelos mais baratos ou self-hosted
4. Tokenização eficiente = menor latência + menor custo
5. Monitore custos de API de perto em produção
""")
