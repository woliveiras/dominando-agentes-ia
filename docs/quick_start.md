## 🚀 Quick Start

### Passo 1: Clone e Configure (2 minutos)

```bash
# Clone o repositório
git clone https://github.com/woliveiras/medscheduler-ai
cd medscheduler-ai

# Instale UV (gerenciador de pacotes Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure o ambiente
uv sync

# Configure suas API keys
cp .env.example .env
# Edite .env e adicione:
# - VERTEX_AI_PROJECT_ID=seu-projeto
# - VERTEX_AI_LOCATION=us-central1
```

### Passo 2: Inicie a Infraestrutura (30 segundos)

```bash
# Inicia API, Web UI, databases - tudo de uma vez!
./scripts/start.sh

# Aguarde a mensagem:
# ✓ Infrastructure ready!
# ✓ API running on http://localhost:8000
# ✓ Web UI running on http://localhost:5173
```

### Passo 3: Popule Dados Sintéticos (1 minuto)

```bash
uv run python scripts/seed_data.py

# Output:
# ✓ Created 10,000 patients
# ✓ Created 500 doctors
# ✓ Created 1,000 appointments
# ✓ Generated embeddings
```

### Passo 4: Teste o Sistema

**Via Web UI:**

```bash
# Acesse: http://localhost:5173
# Converse com o agente de triagem
```

**Via CLI (Recomendado para Desenvolvimento):**

```bash
medscheduler chat

# Ou teste um agente específico:
medscheduler test triage "Estou com febre há 3 dias"
```

### 🎯 Pronto! Agora você pode começar a construir seus agentes.

**Nota Importante:** A infraestrutura (API + Web) está rodando, mas você **não precisa** entender como funciona. O livro foca 100% em construir os agentes que fazem o sistema inteligente.

---

## 🖥️ CLI: Sua Ferramenta Principal de Desenvolvimento

O MedScheduler CLI é sua interface principal para desenvolver e testar agentes durante todo o livro.

### Comandos Principais

#### 1. Chat Interativo
```bash
medscheduler chat

# Inicia sessão de chat com o sistema completo
# Útil para: Testar fluxos end-to-end
```

#### 2. Testar Agentes Isolados
```bash
# Testa apenas o TriageAgent
medscheduler test triage "Estou com dor de cabeça"

# Output detalhado:
# ┌─────────────────────────────────────┐
# │ Testing: TriageAgent                │
# ├─────────────────────────────────────┤
# │ Input: "Estou com dor de cabeça"    │
# │ Urgency: ROUTINE                    │
# │ Specialty: Neurologista             │
# │ Confidence: 0.85                    │
# │ Reasoning: Dor de cabeça isolada... │
# │ Duration: 1.2s                      │
# │ Tokens: 450                         │
# │ Cost: $0.002                        │
# └─────────────────────────────────────┘

# Testa workflow completo
medscheduler test workflow "Preciso agendar consulta"
```

#### 3. Debug com Traces
```bash
# Mostra todos os passos do agente
medscheduler debug triage "febre há 3 dias" --trace

# Output:
# 📝 Step 1: Analyzing symptoms...
#    → LLM Call (model: gemini-1.5-pro, temp: 0.3)
#    → Prompt: [shows full prompt]
#    → Response: [shows response]
# 
# 📝 Step 2: Classifying urgency...
#    → Logic: fever > 2 days = URGENT
#    → Result: URGENT
#
# 📝 Step 3: Recommending specialty...
#    → Tool Call: search_specialty_by_symptoms
#    → Result: Clínico Geral
```

#### 4. Logs e Monitoring
```bash
# Últimos 10 logs do TriageAgent
medscheduler logs --agent=triage --last=10

# Logs em tempo real
medscheduler logs --follow

# Filtrar por erro
medscheduler logs --level=error
```

#### 5. Benchmarking
```bash
# Testa performance com dataset
medscheduler benchmark triage --dataset=data/test_cases.json

# Output:
# Running 100 test cases...
# ━━━━━━━━━━━━━━━━━━━━━━━━ 100/100 100% 0:00:45
#
# Results:
# ✓ Accuracy: 92%
# ✓ Avg Duration: 1.3s
# ✓ Avg Cost: $0.003
# ✗ Failed: 8 cases
```

#### 6. Ferramentas de Desenvolvimento
```bash
# Valida configuração de agente
medscheduler validate agents/triage/

# Gera template de novo agente
medscheduler generate agent --name=MyAgent

# Roda testes
medscheduler test run

# Formata código
medscheduler format
```

### Usando o CLI no Livro

**Padrão em Cada Capítulo:**

1. Você escreve código do agente
2. Testa via CLI: `medscheduler test agent-name`
3. Debug se necessário: `medscheduler debug agent-name --trace`
4. Vê funcionando na Web UI
5. Roda benchmarks: `medscheduler benchmark agent-name`
6. Comita e segue para próximo capítulo

### Vantagens do CLI

✅ Feedback instantâneo  
✅ Debugging detalhado  
✅ Isola agentes para testar  
✅ Não precisa recarregar browser  
✅ Logs estruturados  
✅ Métricas de performance  
✅ Scriptable (CI/CD)
