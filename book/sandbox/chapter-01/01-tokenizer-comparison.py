"""
Capítulo 1: Fundamentos de Transformers
Exemplo 1: Comparação de Tokenizers

Este exemplo demonstra como diferentes tokenizers processam o mesmo texto,
comparando vocabulário, fertility rate e eficiência de compressão.

Instalação necessária:
uv pip install transformers torch

Execução:
python 01-tokenizer-comparison.py

Nota: Se não tiver GPU, o código funcionará (apenas mais lento).
Para CPU: uv pip install torch --index-url https://download.pytorch.org/whl/cpu

Ref.: https://huggingface.co/docs/transformers/en/installation
"""

from transformers import AutoTokenizer

# Texto de exemplo
texto = """
A inteligência artificial está revolucionando a forma como construímos 
sistemas de software. Os foundation models representam uma mudança 
fundamental no paradigma de machine learning.
"""

# Vamos testar com diferentes modelos

# 1. GPT-2 (usa BPE)
print("=" * 60)
print("GPT-2 Tokenization (BPE)")
print("=" * 60)
tokenizer_gpt2 = AutoTokenizer.from_pretrained("gpt2")
tokens_gpt2 = tokenizer_gpt2.tokenize(texto)
print(f"Número de tokens: {len(tokens_gpt2)}")
print(f"Primeiros 20 tokens: {tokens_gpt2[:20]}")
print(f"IDs dos tokens: {tokenizer_gpt2.encode(texto)[:20]}")

# 2. BERT (usa WordPiece)
print("\n" + "=" * 60)
print("BERT Tokenization (WordPiece)")
print("=" * 60)
tokenizer_bert = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
tokens_bert = tokenizer_bert.tokenize(texto)
print(f"Número de tokens: {len(tokens_bert)}")
print(f"Primeiros 20 tokens: {tokens_bert[:20]}")
print(f"IDs dos tokens: {tokenizer_bert.encode(texto)[:20]}")

# 3. XLM-RoBERTa (usa SentencePiece)
print("\n" + "=" * 60)
print("XLM-RoBERTa Tokenization (SentencePiece)")
print("=" * 60)
tokenizer_xlm = AutoTokenizer.from_pretrained("xlm-roberta-base")
tokens_xlm = tokenizer_xlm.tokenize(texto)
print(f"Número de tokens: {len(tokens_xlm)}")
print(f"Primeiros 20 tokens: {tokens_xlm[:20]}")
print(f"IDs dos tokens: {tokenizer_xlm.encode(texto)[:20]}")

# Exemplo detalhado: tokenizar palavra por palavra
print("\n" + "=" * 60)
print("Tokenização Palavra por Palavra (GPT-2)")
print("=" * 60)
palavras = ["inteligência", "artificial", "revolucionando", "software"]
for palavra in palavras:
    tokens = tokenizer_gpt2.tokenize(palavra)
    ids = tokenizer_gpt2.encode(palavra, add_special_tokens=False)
    print(f"\n'{palavra}':")
    print(f"  Tokens: {tokens}")
    print(f"  IDs: {ids}")
    print(f"  Número de tokens: {len(tokens)}")

# Demonstrar decodificação (tokens → texto)
# O processo inverso: converter IDs numéricos de volta para texto
print("\n" + "=" * 60)
print("Decodificação: Tokens → Texto")
print("=" * 60)
# Pega os primeiros 5 tokens de "inteligência artificial" e reconstrói o texto
texto_decodificado = tokenizer_gpt2.decode(
    tokenizer_gpt2.encode("inteligência artificial")[:5]
)
print(f"Texto original: 'inteligência artificial'")
print(f"Tokens: {tokenizer_gpt2.tokenize('inteligência artificial')[:5]}")
print(f"Texto decodificado: '{texto_decodificado}'")

# Comparação de eficiência entre idiomas
# Modelos treinados em inglês geralmente tokenizam português menos eficientemente
print("\n" + "=" * 60)
print("Comparação: Português vs Inglês")
print("=" * 60)
texto_pt = "A inteligência artificial está revolucionando o mundo."
texto_en = "Artificial intelligence is revolutionizing the world."

# Tokeniza a mesma frase em dois idiomas
tokens_pt = tokenizer_gpt2.tokenize(texto_pt)
tokens_en = tokenizer_gpt2.tokenize(texto_en)

print(f"Português: '{texto_pt}'")
print(f"  Tokens: {len(tokens_pt)} - {tokens_pt}")
print(f"\nInglês: '{texto_en}'")
print(f"  Tokens: {len(tokens_en)} - {tokens_en}")
# Note como português requer mais tokens (custo maior em APIs)
print(f"\nEficiência: Inglês usa ~{len(tokens_pt)/len(tokens_en):.2f}x menos tokens")
