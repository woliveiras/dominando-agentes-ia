# Capítulo 2: Treinamento de Tokenizer Customizado
# Exemplo prático com HuggingFace Tokenizers

from tokenizers import (
    Tokenizer,
    models,
    pre_tokenizers,
    trainers,
    processors
)

# 1. Configurar o modelo (BPE)
tokenizer = Tokenizer(models.BPE())

# 2. Pre-tokenização (como dividir texto antes de BPE)
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

# 3. Configurar trainer
trainer = trainers.BpeTrainer(
    vocab_size=50000,           # Tamanho do vocabulário
    min_frequency=2,             # Ignorar tokens que aparecem < 2 vezes
    special_tokens=[             # Tokens especiais
        "<s>",                   # Start of sequence
        "</s>",                  # End of sequence  
        "<unk>",                 # Unknown token
        "<pad>",                 # Padding
    ],
    show_progress=True
)

# 4. Criar dados de treinamento de exemplo
print("="*60)
print("Treinamento de Tokenizer Customizado")
print("="*60)

# Criar arquivo de exemplo se não existir
import os
os.makedirs("../../datasets", exist_ok=True)

example_texts = [
    "A inteligência artificial está revolucionando o mundo.",
    "Machine learning é uma área importante da IA.",
    "Transformers são a arquitetura dominante em NLP.",
    "Deep learning usa redes neurais profundas.",
    "Python é a linguagem preferida para ciência de dados."
] * 100  # Repetir para ter mais dados

with open("../../datasets/tokenizer_train.txt", "w", encoding="utf-8") as f:
    for text in example_texts:
        f.write(text + "\n")

print("\n📦 Dados de treinamento criados")

# 5. Treinar em arquivos
files = ["../../datasets/tokenizer_train.txt"]
print("\n🔄 Treinando tokenizer...")
tokenizer.train(files, trainer)

# 6. Post-processamento (adicionar tokens especiais)
tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)

# 7. Salvar
output_path = "./my_tokenizer.json"
tokenizer.save(output_path)
print(f"\n✅ Tokenizer salvo em {output_path}")

# Testar tokenizer treinado
print("\n" + "="*60)
print("Testando Tokenizer Treinado")
print("="*60)

test_texts = [
    "A inteligência artificial revolucionou tudo.",
    "Deep learning e machine learning são importantes.",
    "Python é usado em ciência de dados."
]

for text in test_texts:
    tokens = tokenizer.encode(text).tokens
    print(f"\nTexto: {text}")
    print(f"Tokens ({len(tokens)}): {tokens}")

# Calcular fertility rate
def fertility_rate(texts):
    total_words = sum(len(text.split()) for text in texts)
    total_tokens = sum(len(tokenizer.encode(text).tokens) for text in texts)
    return total_tokens / total_words

fertility = fertility_rate(test_texts)
print(f"\n📊 Fertility rate: {fertility:.2f}")

if fertility < 1.2:
    print("✅ EXCELENTE: Tokenização muito eficiente!")
elif fertility < 1.5:
    print("✅ BOM: Tokenização eficiente")
elif fertility < 2.0:
    print("⚠️  MODERADO: Tokenização aceitável mas pode melhorar")
else:
    print("❌ RUIM: Vocabulário muito pequeno, considere aumentar vocab_size")

print("\n" + "="*60)
print("💡 INSIGHTS")
print("="*60)
print("""
1. Tokenizer customizado aprende padrões do seu domínio
2. BPE cria tokens baseados em frequência estatística
3. Fertility rate mede eficiência da tokenização
4. Vocabulário de 50K oferece bom balanço
5. Pre-tokenização ByteLevel preserva informação de espaços
""")
