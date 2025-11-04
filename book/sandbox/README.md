# README - Sandbox de Exemplos de Código

Este diretório contém todos os exemplos de código práticos dos capítulos 1, 2 e 3 do livro "Dominando Agentes de IA". Cada exemplo é projetado para ilustrar conceitos-chave discutidos no livro, permitindo que você experimente e aprofunde seu entendimento sobre foundation models, treinamento, fine-tuning e otimização.

## Instalação de Dependências

Para executar os exemplos, você precisará instalar as bibliotecas necessárias:

```bash
# Instalar todas as dependências
uv pip install transformers torch tiktoken peft datasets accelerate bitsandbytes datasketch tokenizers anthropic

# Ou instalar apenas o necessário para cada capítulo:

# Capítulo 1
uv pip install transformers torch

# Capítulo 2
uv pip install datasketch tokenizers

# Capítulo 3
uv pip install transformers torch tiktoken peft datasets anthropic
```

## Execução dos Exemplos

### Capítulo 1: Fundamentos dos Transformers

```bash
# Comparação de tokenizers
uv run chapter-01/01-tokenizer-comparison.py

# Exemplo de self-attention
uv run chapter-01/02-self-attention-example.py

# Máscara causal
uv run chapter-01/03-causal-mask-example.py

# KV-Cache
uv run chapter-01/04-kv-cache-example.py
```

### Capítulo 2: Treinamento de Foundation Models

```bash
# Métricas de qualidade
uv run chapter-02/01-quality-metrics.py

# Deduplicação com MinHash
uv run chapter-02/02-minhash-deduplication.py

# Treinar tokenizer customizado
uv run chapter-02/03-train-custom-tokenizer.py
```

### Capítulo 3: Fine-Tuning e Otimização

```bash
# Fine-tuning com LoRA (SIMPLIFICADO - veja notas no código)
uv run chapter-03/01-lora-fine-tuning.py

# Análise de tokenização e custos
uv run chapter-03/02-tokenization-analysis.py

# Avaliação com LLM-as-judge (requer API key)
export ANTHROPIC_API_KEY="sua-chave-aqui"
uv run chapter-03/03-llm-as-judge.py
```

## Notas Importantes

### GPU vs CPU

- A maioria dos exemplos funciona em CPU, mas será mais lento
- Para GPU CUDA, instale: `uv pip install torch --index-url https://download.pytorch.org/whl/cu118`
- Para CPU apenas: `uv pip install torch --index-url https://download.pytorch.org/whl/cpu`

### API Keys

Alguns exemplos requerem API keys:

- `chapter-03/03-llm-as-judge.py`: Requer `ANTHROPIC_API_KEY`
  - Obtenha em: https://console.anthropic.com/

### Datasets

Alguns exemplos criam datasets automaticamente em `../../datasets/`:
- `tech_terms_pt_en.jsonl`
- `evaluation_examples.jsonl`
- `tokenizer_train.txt`

## Troubleshooting

### Erro: "No module named 'transformers'"

```bash
uv pip install transformers
```

### Erro: "torch not compiled with CUDA enabled"

Seu PyTorch foi instalado sem suporte CUDA. Reinstale:

```bash
uv pip uninstall torch
uv pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Erro: "API key not found"

Defina a variável de ambiente:

```bash
export ANTHROPIC_API_KEY="sua-chave"
```

## Recursos Adicionais

- Documentação Transformers: https://huggingface.co/docs/transformers
- Documentação PEFT (LoRA): https://huggingface.co/docs/peft
- Documentação Tokenizers: https://huggingface.co/docs/tokenizers
- Anthropic API: https://docs.anthropic.com/

## Contribuindo

Encontrou um bug ou tem uma sugestão? Abra uma issue no repositório do livro.

## Licença

Estes exemplos são parte do livro "Dominando Agentes de IA" e seguem a mesma licença do livro.
