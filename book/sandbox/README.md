# Sandbox - Exemplos Práticos do Livro

Este diretório contém todos os exemplos de código executáveis dos capítulos do livro **"Dominando Agentes de IA"**. Cada exemplo é projetado para ilustrar conceitos-chave, permitindo experimentação prática e aprofundamento dos tópicos discutidos.

## 📁 Estrutura

```
sandbox/
├── chapter-01/          # Fundamentos de Transformers
│   ├── 01-tokenizer-comparison.py
│   ├── 02-self-attention-example.py
│   ├── 03-causal-mask-example.py
│   ├── 04-kv-cache-example.py
│   └── README.md
├── chapter-02/          # Treinamento de Foundation Models
│   ├── 01-quality-metrics.py
│   ├── 02-minhash-deduplication.py
│   ├── 03-train-custom-tokenizer.py
│   └── README.md
├── chapter-03/          # Fine-Tuning e Otimização
│   ├── 01-lora-fine-tuning.py
│   ├── 02-tokenization-analysis.py
│   ├── 03-llm-as-judge.py
│   └── README.md
└── chapter-04/          # Dominando LLMs na Prática
    ├── 01-prometheus-metrics.py
    ├── 02-load-balancer.py
    ├── 03-distributed-tracing.py
    └── README.md
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes recomendado)

### Instalação do UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verificar instalação
uv --version
```

### Instalação de Dependências

```bash
# Instalar todas as dependências de uma vez
uv pip install transformers torch tiktoken peft datasets accelerate \
               bitsandbytes datasketch tokenizers anthropic openai \
               prometheus-client opentelemetry-api opentelemetry-sdk

# OU instalar por capítulo (recomendado)
# Veja seções abaixo
```

## 📚 Exemplos por Capítulo

### Capítulo 1: Fundamentos de Transformers

**Tópicos**: Tokenização, Self-Attention, Causal Mask, KV-Cache

**Instalação:**
```bash
uv pip install transformers torch
```

**Execução:**
```bash
cd chapter-01

# Comparação de tokenizers
python 01-tokenizer-comparison.py

# Mecanismo de self-attention
python 02-self-attention-example.py

# Máscara causal para modelos decoder-only
python 03-causal-mask-example.py

# KV-Cache para geração eficiente
python 04-kv-cache-example.py
```

**📖 README detalhado**: [chapter-01/README.md](chapter-01/README.md)

---

### Capítulo 2: Treinamento de Foundation Models

**Tópicos**: Curadoria de dados, Deduplicação, Tokenizer customizado

**Instalação:**
```bash
uv pip install datasketch tokenizers
```

**Execução:**
```bash
cd chapter-02

# Métricas de qualidade de dataset
python 01-quality-metrics.py

# Deduplicação com MinHash e LSH
python 02-minhash-deduplication.py

# Treinamento de tokenizer customizado
python 03-train-custom-tokenizer.py
```

**📖 README detalhado**: [chapter-02/README.md](chapter-02/README.md)

---

### Capítulo 3: Fine-Tuning e Otimização

**Tópicos**: LoRA, Análise de tokenização, LLM-as-Judge

**Instalação:**
```bash
uv pip install transformers peft datasets accelerate bitsandbytes \
               tiktoken anthropic torch
```

**Execução:**
```bash
cd chapter-03

# Fine-tuning com LoRA
python 01-lora-fine-tuning.py

# Análise de tokenização e custos
python 02-tokenization-analysis.py

# Avaliação com LLM-as-Judge
export ANTHROPIC_API_KEY="sua-chave-aqui"
python 03-llm-as-judge.py
```

**📖 README detalhado**: [chapter-03/README.md](chapter-03/README.md)

---

### Capítulo 4: Dominando LLMs na Prática

**Tópicos**: Observabilidade, Load Balancing, Distributed Tracing

**Instalação:**
```bash
uv pip install prometheus-client openai anthropic opentelemetry-api \
               opentelemetry-sdk opentelemetry-exporter-otlp
```

**Execução:**
```bash
cd chapter-04

# Sistema de métricas com Prometheus
python 01-prometheus-metrics.py
# Acesse: http://localhost:8000/metrics

# Load balancer com fallback automático
python 02-load-balancer.py

# Rastreamento distribuído com OpenTelemetry
python 03-distributed-tracing.py
```

**📖 README detalhado**: [chapter-04/README.md](chapter-04/README.md)

---

## 🎯 Progressão Recomendada

Os exemplos foram projetados para serem executados em ordem:

1. **Capítulo 1**: Fundamentos (arquitetura Transformer)
2. **Capítulo 2**: Treinamento (curadoria de dados, tokenizers)
3. **Capítulo 3**: Fine-Tuning (adaptação de modelos)
4. **Capítulo 4**: Produção (observabilidade, otimização)

Cada capítulo constrói sobre o conhecimento do anterior.

---

## 🔧 Requisitos de Sistema

### Hardware Mínimo

- **CPU**: 4 cores
- **RAM**: 8GB (16GB recomendado)
- **Disco**: 10GB espaço livre
- **GPU**: Opcional (acelera execução, mas não obrigatória)

### Software

- **Python**: 3.10 ou superior
- **UV**: Latest version
- **SO**: macOS, Linux, ou Windows (WSL2 recomendado)

### GPU (Opcional)

Para exemplos com modelos grandes (Capítulo 3):

- **NVIDIA**: CUDA 11.8+ (Drivers atualizados)
- **Apple Silicon**: Metal support (automático)
- **AMD**: ROCm (suporte limitado)

**Verificar GPU:**

```bash
# NVIDIA
nvidia-smi

# Apple Silicon
system_profiler SPDisplaysDataType | grep "Chipset Model"
```

---

## 🐛 Troubleshooting Comum

### Erro: "uv: command not found"

**Solução**: Instalar UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Erro: "No module named 'transformers'"

**Solução**: Instalar dependências

```bash
uv pip install transformers torch
```

### Erro: "CUDA out of memory"

**Soluções**:
```bash
# 1. Usar CPU (mais lento)
export CUDA_VISIBLE_DEVICES=""

# 2. Reduzir batch size nos scripts
# Edite per_device_train_batch_size=1

# 3. Usar quantização
# Veja exemplos no Capítulo 3
```

### Erro: "API key not found"

**Solução**: Configurar variáveis de ambiente
```bash
# Anthropic (Capítulo 3)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (Capítulo 4)
export OPENAI_API_KEY="sk-..."

# Verificar
echo $ANTHROPIC_API_KEY
```

### Performance Lenta em CPU

**Normal!** LLMs são computacionalmente intensivos.

**Alternativas**:
- Use Google Colab (GPU grátis)
- Teste com modelos menores (GPT-2 vs Llama-2-70B)
- Execute em horários de menor uso

---

## 📊 Datasets Necessários

Alguns exemplos requerem datasets específicos:

### Capítulo 2

**Tokenizer Training** (`03-train-custom-tokenizer.py`):
- Arquivo: `../datasets/tokenizer_train.txt`
- Tamanho mínimo: 1MB
- Formato: Texto simples

### Capítulo 3

**LoRA Fine-Tuning** (`01-lora-fine-tuning.py`):
- Arquivo: `../datasets/tech_terms_pt_en.jsonl`
- Formato: JSON Lines
- Exemplo:
  ```json
  {"input": "traduza: API", "output": "Application Programming Interface"}
  ```

**Criar datasets de exemplo:**
```bash
# Navegar para diretório de datasets
cd ../datasets

# Criar dataset para tokenizer
echo "Texto de exemplo para treinar tokenizer..." > tokenizer_train.txt

# Criar dataset para fine-tuning
cat > tech_terms_pt_en.jsonl << EOF
{"input": "traduza: API", "output": "Application Programming Interface"}
{"input": "traduza: container", "output": "contêiner"}
EOF
```

---

## 🎓 Recursos Adicionais

### Documentação

- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch](https://pytorch.org/docs/)
- [PEFT (Parameter-Efficient Fine-Tuning)](https://huggingface.co/docs/peft/)
- [Anthropic API](https://docs.anthropic.com/)
- [OpenTelemetry](https://opentelemetry.io/docs/)

### Tutoriais

- [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Fine-tuning Guide](https://huggingface.co/docs/transformers/training)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

### Comunidade

- [HuggingFace Forum](https://discuss.huggingface.co/)
- [PyTorch Forum](https://discuss.pytorch.org/)

---

## 💡 Dicas de Uso

### Para Iniciantes

1. **Comece pelo Capítulo 1**: Fundamentos são essenciais
2. **Execute linha por linha**: Use debugger para entender fluxo
3. **Modifique parâmetros**: Experimente valores diferentes
4. **Leia os READMEs**: Cada capítulo tem guia detalhado

### Para Usuários Avançados

1. **Combine exemplos**: Integre componentes de diferentes capítulos
2. **Experimente modelos**: Troque GPT-2 por Llama, Claude, etc.
3. **Profile performance**: Use `cProfile` para otimizar
4. **Contribua**: Abra PRs com melhorias

### Melhores Práticas

1. **Virtual environments**: Sempre use ambientes isolados
2. **Version control**: Commit experimentos bem-sucedidos
3. **Documente mudanças**: Anote o que funcionou/falhou
4. **Backup de modelos**: Salve checkpoints importantes

---

## 🤝 Contribuindo

Encontrou um bug? Tem sugestão de melhoria?

1. **Issues**: Abra issue no repositório
2. **Pull Requests**: Contribuições são bem-vindas
3. **Discussões**: Use GitHub Discussions para dúvidas

**Guidelines**:
- Mantenha código limpo e documentado
- Siga estilo PEP 8 para Python
- Teste antes de submeter PR
- Atualize READMEs se necessário

---

## 📝 Licença

Veja arquivo LICENSE no repositório principal.

---

## ✨ Créditos

Exemplos criados para o livro **"Dominando Agentes de IA"**.

**Autor**: William Oliveira de Souza  
**Repositório**: github.com/woliveiras/dominando-agentes-ia

---

**Última atualização**: 2025-01-06  
**Versão**: 1.0.0

