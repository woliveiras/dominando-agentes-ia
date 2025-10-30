## 🏥 Projeto Guia: MedScheduler

*Sistema Multi-Agente de Agendamento Inteligente para Hospitais*

### Visão Geral

Plataforma que otimiza agendamento de consultas, exames e procedimentos usando múltiplos agentes de IA especializados, considerando:

- Disponibilidade de médicos e equipamentos
- Urgência e triagem de casos
- Otimização de recursos
- Compliance com regulamentações (LGPD, CFM)
- Experiência do paciente

### Por Que Este Projeto?

✅ **Problema Real**: Hospitais perdem 30-40% de eficiência com agendamentos mal otimizados  
✅ **Complexidade Natural**: Múltiplos agentes, workflows, decisões, conflitos  
✅ **Impacto Social**: Open source que pode ajudar sistema de saúde  
✅ **Segurança Crítica**: Dados sensíveis, compliance, auditoria  
✅ **Multi-Stakeholder**: Pacientes, médicos, hospitais, planos de saúde

---

## 🏗️ Arquitetura Técnica

### Estrutura do Projeto Revisada

O projeto está organizado para **maximizar o foco nos agentes**:

```
medscheduler/
├── infrastructure/          # 🔒 FORNECIDO PRONTO (black box)
│   ├── api/                 # FastAPI (não ensinado no livro)
│   ├── web/                 # React (não ensinado no livro)
│   └── docker/              # Configs Docker
│
├── agents/                  # 🎯 FOCO DO LIVRO (white box)
│   ├── core/                # Classes base
│   ├── triage/              # Triage agent
│   ├── scheduling/          # Scheduling agent
│   ├── matching/            # Matching agent
│   ├── notification/        # Notification agent
│   ├── optimization/        # Optimization agent
│   └── orchestrator/        # Multi-agent orchestration
│
├── packages/                # 🎯 FERRAMENTAS PARA AGENTES
│   ├── tools/               # Tool definitions
│   ├── prompts/             # Prompt templates
│   ├── memory/              # Memory management
│   └── evaluators/          # Evaluation tools
│
├── cli/                     # 🎯 CLI PARA DESENVOLVIMENTO
│   ├── chat.py              # Chat interativo
│   ├── test_agent.py        # Testar agentes
│   └── debug.py             # Debug tools
│
├── shared/                  # Código compartilhado
│   ├── database/            # DB models (usado por agentes)
│   ├── schemas/             # Pydantic schemas
│   └── config/              # Configurações
│
├── data/                    # Dados sintéticos
├── tests/                   # Testes
├── docs/                    # Documentação
└── examples/                # Notebooks por capítulo
```

**🔒 Infraestrutura (Fornecida Pronta - Black Box):**
- `infrastructure/api/` - Backend FastAPI completo
- `infrastructure/web/` - Frontend React completo
- `infrastructure/docker/` - Containers e orquestração

**🎯 Agentes (Foco do Livro - White Box):**
- `agents/` - Todos os agentes que você vai construir
- `packages/` - Ferramentas para construir agentes
- `cli/` - Interface para testar agentes durante desenvolvimento

**📚 No Livro:**
- 95% do conteúdo é sobre construir agentes
- 5% é setup inicial (rodar infra pronta)
- Zero linhas de React ou FastAPI são ensinadas

---

### Tech Stack

**Backend (Fornecido Pronto):**
- **FastAPI** - API REST
- **SQLAlchemy** + **Alembic** - ORM e migrations
- **PostgreSQL** - Database principal
- **Redis** - Cache e message broker
- **ChromaDB** - Vector database

**Frontend (Fornecido Pronto):**
- **React 19** + **TypeScript**
- **Vite** - Build tool
- **TanStack Query** - Data fetching
- **shadcn/ui** - Components
- **Zustand** - State management

**CLI (Foco de Desenvolvimento):**
- **Click** - Framework CLI
- **Rich** - Output formatado e colorido
- **Typer** - Type-safe CLI commands
- **pytest** - Testing framework

**AI/Agents (Foco do Livro):**
- **LangGraph** - Agent orchestration
- **LangChain** - Tool chains
- **Vertex AI** - LLM provider (Gemini)
- **Sentence Transformers** - Embeddings

**DevOps:**
- **Docker** + **Docker Compose**
- **GitHub Actions** - CI/CD
- **Prometheus** + **Grafana** - Monitoring
- **Sentry** - Error tracking
- **Google Cloud** - Provedor de Nuvem

---

## 📈 Evolução do Projeto por MVPs

### MVP 1 - Fundamentos (Capítulos 1-4)
**"Agente de Triagem Básico"**

#### 🎯 O Que Você Vai Construir:
- `TriageAgent`: Agente que analisa sintomas
- Prompts especializados em triagem médica
- Lógica de classificação de urgência
- Sistema de recomendação de especialidade

#### 🔒 O Que Já Vem Pronto:
- Interface web de chat
- API endpoints para comunicação
- Banco de dados configurado
- Autenticação básica

#### 📚 Features:
- Paciente descreve sintomas em linguagem natural
- Agente classifica urgência (emergência, urgente, rotina)
- Sugere especialidade médica apropriada
- Interface web simples

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler test triage "Estou com febre há 3 dias"

# Output:
# ✓ Urgency: URGENT
# ✓ Specialty: Clínico Geral
# ✓ Reasoning: Febre persistente requer avaliação...
```

**Via Web UI:**
```
Acesse http://localhost:5173 e converse com o agente
```

#### 🎓 Estrutura de Arquivos:
```
agents/triage/
├── __init__.py
├── triage_agent.py      # 🎯 Você cria
├── prompts.py           # 🎯 Você cria
└── tests/
    └── test_triage.py   # 🎯 Você cria
```

---

### MVP 2 - Embeddings e RAG (Capítulo 5)
**"Sistema de Recomendação de Médicos"**

#### 🎯 O Que Você Vai Construir:
- `MatchingAgent`: Encontra melhor médico baseado em contexto
- Pipeline RAG completo
- Sistema de embeddings para conhecimento médico
- Query rewriting para melhor retrieval

#### 🔒 O Que Já Vem Pronto:
- ChromaDB configurado
- Interface de visualização de recomendações
- Sistema de cache de embeddings

#### 📚 Features:
- Base de conhecimento médico (especialidades, doenças, tratamentos)
- RAG para encontrar melhor médico/especialista
- Histórico do paciente pode ser considerado
- Recomendações personalizadas por paciente + histórico

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler test matching "Preciso de cardiologista com experiência em arritmia"

# Output:
# ✓ Top 3 Doctors:
# 1. Dr. João Silva (Cardio, 15y exp, 4.8★)
# 2. Dr. Maria Santos (Cardio, 12y exp, 4.7★)
# 3. Dr. Pedro Costa (Cardio, 10y exp, 4.6★)
```

#### 📊 Dados:
- CID-10 embeddings
- Perfis de médicos e especialidades
- Guidelines médicos

---

### MVP 3 - Tools e Multi-Agente (Capítulos 6-8)
**"Agendamento Inteligente Completo"**

#### 🎯 O Que Você Vai Construir:
1. `TriageAgent`: Classifica caso
2. `MatchingAgent`: Encontra melhor médico
3. `SchedulingAgent`: Agenda considerando restrições
4. `OptimizationAgent`: Otimiza distribuição de consultas
5. `NotificationAgent`: Gerencia comunicação

**Tools que você vai criar:**
```python
# packages/tools/
├── calendar_tools.py
│   ├── check_availability()
│   ├── create_appointment()
│   └── update_appointment()
├── notification_tools.py
│   ├── send_whatsapp()
│   ├── send_email()
│   └── send_sms()
├── database_tools.py
│   ├── get_patient_history()
│   ├── get_doctor_schedule()
│   └── check_insurance()
└── optimization_tools.py
    ├── calculate_priority_score()
    └── optimize_slot_allocation()
```

#### 🔒 O Que Já Vem Pronto:
- Integrações com serviços de notificação
- Sistema de calendário
- Dashboard administrativo

#### 📚 Features:
- Verificação de disponibilidade em tempo real
- Otimização de slots considerando múltiplos fatores
- Notificações automáticas (WhatsApp, SMS, Email)
- Reagendamento inteligente

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler test workflow "Agendar consulta com cardiologista"

# Output mostra cada passo:
# 📝 Step 1: Triage → ROUTINE, Cardiologia
# 📝 Step 2: Matching → Dr. João Silva
# 📝 Step 3: Scheduling → 2025-02-15 14:00
# 📝 Step 4: Notification → WhatsApp sent
# ✓ Appointment confirmed
```

#### 🔄 Comunicação Multi-Agente:
- MCP para context sharing
- Message queue (Redis) para coordenação
- Consensus para conflitos de horário
- Load balancing de requests

---

### MVP 4 - Workflows Avançados (Capítulo 7)
**"Automação de Processos Complexos"**

#### 🎯 O Que Você Vai Construir:
- Workflow de exames pré-operatórios com ToT
- Sistema de reagendamento em cascata com ReAct
- Follow-up automático com Self-Refine
- Gestão inteligente de lista de espera

#### 📚 Workflows Implementados:

**1. Workflow: Cirurgia Eletiva**
```
TriageAgent → classifica caso
     ↓
SchedulingAgent → agenda consulta pré-op
     ↓
CoordinationAgent → agenda exames necessários
     → ToT para otimizar ordem dos exames
     ↓
ApprovalAgent → valida com plano de saúde
     ↓
SchedulingAgent → agenda cirurgia
     ↓
NotificationAgent → notifica paciente + equipe
```

**2. Workflow: Cancelamento em Cascata**
```
EventAgent → detecta cancelamento
     ↓
ImpactAgent → identifica pacientes afetados
     → ReAct para replanejar
     ↓
ReschedulingAgent → propõe novos horários
     → Consensus para resolver conflitos
     ↓
NotificationAgent → comunica mudanças
```

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler test workflow surgery "Paciente precisa de cirurgia de catarata"

# Mostra cada decisão do ToT:
# 🌳 Exploring paths...
# Path 1: Exames cardio → oftalmológico → anestesia
# Path 2: Oftalmológico → cardio → anestesia
# Path 3: Anestesia → cardio → oftalmológico
# ✓ Best path: Path 2 (menos tempo, menos custo)
```

---

### MVP 5 - Arquitetura Otimizada (Capítulo 9)
**"Sistema de Alta Performance"**

#### 🎯 O Que Você Vai Construir:
- Cascade architecture com routing inteligente
- Sistema de caching multi-camada
- Batch processing de agendamentos
- Multi-tenancy para múltiplos hospitais

#### 📊 Arquitetura:

```
┌──────────────────────────────────────────────┐
│           API Gateway (FastAPI)              │
│     (Rate Limit, Auth, Request Router)       │
└───────────────────┬──────────────────────────┘
                    │
        ┌───────────▼────────────┐
        │   Manager Agent        │
        │   (LLM Router)         │
        │   - Simple → Small LLM │
        │   - Complex → Large LLM│
        └───────────┬────────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
│  Triage  │  │Scheduling│  │   Notif  │
│  Agent   │  │  Agent   │  │  Agent   │
│(Gemini   │  │(Gemini   │  │ (Local)  │
│ Pro)     │  │ Flash)   │  │          │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │              │
     └─────────────┼──────────────┘
                   │
     ┌─────────────▼──────────────┐
     │    Shared Services         │
     ├────────────────────────────┤
     │ Vector DB │ PostgreSQL     │
     │ Redis     │ Message Queue  │
     └────────────────────────────┘
```

#### 🔒 O Que Já Vem Pronto:
- Load balancer configurado
- Sistema de monitoring
- Auto-scaling infrastructure

#### ⚡ Otimizações:
- Small LLM (Flash) para queries simples
- Large LLM (Pro) para casos complexos
- Caching de embeddings
- Precomputed availability grids

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler benchmark system --concurrent=100

# Output:
# Testing with 100 concurrent users...
# ✓ Avg Response Time: 850ms
# ✓ P95 Response Time: 1.2s
# ✓ Success Rate: 99.2%
# ✓ Cost per request: $0.004
```

---

### MVP 6 - Segurança e Compliance (Capítulos 10-11)
**"Sistema Enterprise-Grade"**

#### 🎯 O Que Você Vai Construir:

```python
# packages/security/
├── guardrails/
│   ├── input_validator.py    # Sanitiza inputs
│   ├── output_validator.py   # Valida decisões
│   ├── pii_detector.py       # Detecta dados sensíveis
│   └── hallucination_check.py
├── audit/
│   ├── audit_logger.py       # Log todas ações
│   ├── compliance_checker.py
│   └── report_generator.py
└── encryption/
    ├── data_encryption.py
    └── key_management.py
```

#### 🔒 O Que Já Vem Pronto:
- HTTPS configurado
- Backup automático
- Sistema de recovery

#### 📚 Features:
- Conformidade LGPD/HIPAA
- Auditoria completa de ações
- Anonimização de dados
- Guardrails para decisões médicas
- Human-in-the-loop para casos críticos

#### 🛡️ Guardrails Específicos:
- Não agenda emergências (direciona para emergência)
- Valida especialidade médica vs. sintomas
- Detecta tentativas de prompt injection
- Redacta dados pessoais em logs
- Human approval para cirurgias

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler test security --attack=prompt-injection

# Output:
# Testing 50 attack vectors...
# ✓ Prompt injection: Blocked (100%)
# ✓ PII leakage: None detected
# ✓ Data validation: Passed
# ✗ Found 2 potential issues (flagged for review)
```

---

### MVP 7 - Produção (Capítulo 12)
**"Deploy e Operação"**

#### 🎯 O Que Você Vai Construir:
- CI/CD pipeline completo
- Monitoring e alerting
- Blue-green deployment
- Incident response playbooks

#### 📦 Infrastructure:

```yaml
# infrastructure/docker-compose.yml
services:
  api:
    build: ./infrastructure/api
    replicas: 3
    
  agents:
    build: ./agents
    
  postgres:
    image: postgres:16
    
  redis:
    image: redis:7
    
  chromadb:
    image: chromadb/chroma
    
  prometheus:
    image: prometheus
    
  grafana:
    image: grafana
```

#### 📊 Monitoring:
- Latência por agente
- Custo por query (LLM)
- Taxa de sucesso de agendamentos
- Satisfaction score
- Error rates

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler deploy staging

# Output:
# ✓ Running tests...
# ✓ Building containers...
# ✓ Deploying to staging...
# ✓ Health check passed
# ✓ Staging URL: https://staging.medscheduler.ai
```

---

### MVP 8 - Melhoria Contínua (Capítulo 13)
**"Sistema Auto-Evolutivo"**

#### 🎯 O Que Você Vai Construir:
- A/B testing framework para agentes
- Sistema de feedback contínuo
- Red team automation
- Fine-tuning pipeline

#### 📊 Métricas de Sucesso:
```python
# Métricas que você vai implementar
metrics = {
    "tempo_medio_agendamento": "< 2 minutos",
    "no_show_rate": "< 10%",
    "nps_paciente": "> 8.5",
    "ocupacao_agenda": "> 85%",
    "reagendamentos": "< 5%",
    "precisao_triagem": "> 95%"
}
```

#### 🧪 Como Testar:

**Via CLI:**
```bash
medscheduler experiment run "Test new triage prompt"

# Output:
# Running A/B test...
# Variant A (current): 92% accuracy
# Variant B (new): 95% accuracy
# ✓ Variant B is 3% better (p < 0.05)
# Recommendation: Deploy Variant B
```

---

## 📊 Datasets e Setup Inicial

### Dados Sintéticos (fornecidos no repo)

```
data/
├── synthetic/
│   ├── patients.json           # 10k pacientes fictícios
│   ├── doctors.json            # 500 médicos com especialidades
│   ├── symptoms_database.json  # Base de sintomas → especialidades
│   ├── medical_guidelines.txt  # Guidelines médicos
│   └── schedules.json          # Calendários simulados
├── embeddings/
│   ├── cid10_embeddings.pkl
│   └── specialty_embeddings.pkl
└── examples/
    └── triage_examples.json    # 1000 exemplos de triagem
```

### Compliance

- ✅ Dados 100% sintéticos
- ✅ Gerados com Faker + domain knowledge
- ✅ Não usa dados reais de pacientes
- ✅ Open source completo

---

## 🔄 User Flows Principais

### 1. Paciente Agenda Consulta

```
Paciente → Descreve sintomas
    ↓
TriageAgent → Classifica urgência + especialidade
    ↓
MatchingAgent → Recomenda médicos
    ↓
SchedulingAgent → Mostra disponibilidade
    ↓
Paciente → Escolhe horário
    ↓
SchedulingAgent → Confirma agendamento
    ↓
NotificationAgent → Envia confirmação (WhatsApp/Email)
```

### 2. Médico Cancela Horário

```
Médico → Cancela slot na agenda
    ↓
EventAgent → Detecta cancelamento
    ↓
ImpactAgent → Lista pacientes afetados
    ↓
ReschedulingAgent → Para cada paciente:
    - Encontra novo slot
    - Considera prioridade
    - Resolve conflitos
    ↓
NotificationAgent → Notifica pacientes + oferece alternativas
```

### 3. Hospital Otimiza Agenda

```
OptimizationAgent → Analisa semana
    - Identifica lacunas
    - Detecta over/under booking
    - Calcula metrics
    ↓
RecommendationAgent → Sugere ajustes
    ↓
ManagerAgent → Notifica administração
```

---

## 🎨 UI/UX Preview

### Fluxos Principais:

**Todas as "telas" serão fluxos de conversação com o chat.**

1. **"Dashboard" do Paciente**
   - Próximas consultas
   - Histórico
   - Agendar nova consulta (chatbot interface)

2. **"Dashboard" do Médico**
   - Agenda do dia
   - Perfil de pacientes
   - Analytics

3. **"Dashboard" Administrativo**
   - Occupancy rates
   - Wait times
   - Patient satisfaction
   - Revenue metrics

> **Nota:** As informações estão entre aspas (") porque não são realmente dashboards tradicionais. São conversações com o chat onde o agente traz essas informações para o usuário (paciente, médico, admin).

---

## 📚 Conteúdo Adicional no Repo

```
medscheduler/
├── examples/          # Notebooks Jupyter por capítulo
│   ├── cap01_foundation_models.ipynb
│   ├── cap03_prompting.ipynb
│   ├── cap05_rag.ipynb
│   └── ...
├── tutorials/         # Step-by-step guides
├── docs/              # Documentação completa
└── benchmarks/        # Performance comparisons
```

