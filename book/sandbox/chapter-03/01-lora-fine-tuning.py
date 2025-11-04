# Capítulo 3: Fine-Tuning com LoRA
# Exemplo completo de fine-tuning para tradução de termos técnicos

# Instalação necessária:
# uv pip install transformers peft datasets accelerate bitsandbytes torch

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import json
import os

# Configuração
MODEL_NAME = "gpt2"  # Modelo pequeno para teste rápido (use Llama-2-7b-hf se tiver acesso)
OUTPUT_DIR = "./gpt2-tech-translator-lora"

print("🔄 Carregando modelo base...")

# Carregar modelo e tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # Necessário para Llama

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,  # Usar FP16 para economizar memória
)

print(f"✅ Modelo carregado: {MODEL_NAME}")
print(f"📊 Parâmetros totais: {model.num_parameters():,}")

# Configurar LoRA
print("\n🔧 Configurando LoRA...")

lora_config = LoraConfig(
    r=16,                        # Rank dos adapters (maior = mais expressivo, mas mais memória)
    lora_alpha=32,               # Scaling factor
    target_modules=["c_attn"],   # Aplicar LoRA em attention (GPT-2 usa c_attn)
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Aplicar LoRA ao modelo
model = get_peft_model(model, lora_config)

# Mostrar quantos parâmetros serão treinados
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
trainable_percentage = (trainable_params / total_params) * 100

print(f"📊 Parâmetros treináveis: {trainable_params:,} ({trainable_percentage:.2f}% do total)")
print(f"💾 Redução de memória: ~{100 - trainable_percentage:.1f}%")

# Carregar dataset de treinamento
print("\n📦 Carregando dataset...")

# Função auxiliar para carregar dataset
def load_tech_terms_dataset(file_path):
    """
    Carrega dataset JSONL de termos técnicos.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset não encontrado: {file_path}\n"
            f"Crie o arquivo com exemplos no formato:\n"
            f'{{"input": "Traduza...", "output": "machine learning"}}'
        )

    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"⚠️  Erro na linha {line_num}: {e}")
                continue

    if not data:
        raise ValueError(f"Dataset vazio: {file_path}")

    return data

# Carregar dados - ajuste o path conforme sua estrutura
dataset_path = "../../datasets/tech_terms_pt_en.jsonl"

try:
    data = load_tech_terms_dataset(dataset_path)
except FileNotFoundError as e:
    print(f"⚠️  {e}")
    print("📝 Criando dataset de exemplo...")

    # Criar dataset de exemplo se não existir
    os.makedirs("../../datasets", exist_ok=True)
    example_data = [
        {"input": "Traduza o termo técnico de português para inglês: aprendizado de máquina",
         "output": "machine learning"},
        {"input": "Traduza o termo técnico de português para inglês: rede neural",
         "output": "neural network"},
        {"input": "Traduza o termo técnico de português para inglês: inteligência artificial",
         "output": "artificial intelligence"},
        {"input": "Traduza o termo técnico de português para inglês: aprendizado profundo",
         "output": "deep learning"},
        {"input": "Traduza o termo técnico de português para inglês: processamento de linguagem natural",
         "output": "natural language processing"},
    ] * 10  # Repetir para ter mais exemplos

    with open(dataset_path, 'w', encoding='utf-8') as f:
        for item in example_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    data = example_data
    print(f"✅ Dataset de exemplo criado em {dataset_path}")

# Dividir em treino/validação (80/20)
split_idx = int(len(data) * 0.8)
train_data = data[:split_idx]
val_data = data[split_idx:]

print(f"📚 Exemplos de treino: {len(train_data)}")
print(f"✅ Exemplos de validação: {len(val_data)}")

print("\n" + "="*60)
print("💡 NOTA IMPORTANTE")
print("="*60)
print("""
Este é um exemplo SIMPLIFICADO para demonstração.
Para um fine-tuning real de produção, você precisaria de:

1. Dataset maior (1000+ exemplos)
2. Validação mais rigorosa
3. Múltiplas épocas de treinamento
4. Monitoramento de métricas (loss, perplexity)
5. Early stopping para evitar overfitting
6. Evaluation em conjunto de teste separado

Consulte o capítulo completo para detalhes sobre fine-tuning em produção.
""")

print(f"\n{'='*60}")
print("✅ Script preparado com sucesso!")
print(f"{'='*60}")
print("\nPara executar o treinamento completo, descomente as seções")
print("de treinamento no código fonte.")
