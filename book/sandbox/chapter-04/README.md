# Exemplos do Capítulo 4: Dominando LLMs na Prática

Exemplos práticos e executáveis demonstrando observabilidade e otimização de sistemas LLM em produção.

## 📋 Visão Geral dos Exemplos

### 01-prometheus-metrics.py

**Sistema de Métricas com Prometheus**

Demonstra instrumentação completa de chamadas LLM com métricas Prometheus para monitoramento de produção.

**O que você vai aprender:**
- Definir métricas essenciais (Counter, Histogram, Gauge)
- Rastrear latência, tokens, custos e cache hits
- Expor métricas para scraping do Prometheus
- Queries PromQL úteis para dashboards

**Instalação:**
```bash
uv pip install prometheus-client
```

**Execução:**
```bash
python 01-prometheus-metrics.py
```

**Acesse:** http://localhost:8000/metrics

**Métricas expostas:**

- `llm_requests_total` - Total de requisições por modelo/provider/status
- `llm_request_duration_seconds` - Histograma de latência
- `llm_tokens_total` - Tokens processados (input/output)
- `llm_cost_usd_total` - Custo acumulado em USD
- `llm_active_requests` - Requisições ativas
- `llm_cache_hit_rate` - Taxa de cache hit

---

### 02-load-balancer.py

**Load Balancer com Fallback Automático**

Implementação de load balancing entre múltiplos providers LLM com fallback automático e diferentes estratégias de roteamento.

**O que você vai aprender:**

- Implementar fallback automático entre providers
- Estratégias de balanceamento (PRIORITY, ROUND_ROBIN, FASTEST_FIRST)
- Rastrear estatísticas de performance por provider
- Garantir alta disponibilidade

**Instalação:**

```bash
uv pip install asyncio
```

**Execução:**

```bash
python 02-load-balancer.py
```

**Estratégias demonstradas:**

1. **PRIORITY**: Usa provider de maior prioridade, fallback se falhar
2. **ROUND_ROBIN**: Distribui carga uniformemente entre providers
3. **FASTEST_FIRST**: Adapta-se dinamicamente ao provider mais rápido

**Benefícios:**

- ✅ Resiliência: Sistema continua funcionando se um provider falha
- ✅ Otimização de custo: Roteamento inteligente
- ✅ Latência reduzida: Usa provider mais rápido
- ✅ SLA melhorado: Alta disponibilidade

---

### 03-distributed-tracing.py

**Rastreamento Distribuído com OpenTelemetry**

Demonstra instrumentação de workflows LLM com traces distribuídos para visualização de latência, dependências e gargalos.

**O que você vai aprender:**
- Instrumentar workflows multi-step com spans
- Rastrear chamadas através de múltiplos componentes
- Capturar e propagar erros em traces
- Identificar gargalos de performance

**Instalação:**

```bash
uv pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

**Execução:**

```bash
python 03-distributed-tracing.py
```

**Workflow rastreado:**

```
process_user_query (3.2s)
├── classify_intent (0.5s)
│   └── llm_call [gpt-3.5-turbo] (0.4s)
├── retrieve_context (0.8s)
│   ├── generate_embedding (0.2s)
│   └── vector_search (0.6s)
├── generate_response (1.7s)
│   └── llm_call [gpt-4-turbo] (1.6s)
└── post_process (0.05s)
```

**Casos de uso:**

- 🔍 Debugging de latência em workflows complexos
- 🎯 Identificação de gargalos
- ❌ Rastreamento de propagação de erros
- 📊 Análise de dependências entre componentes

---

## 🎯 Conceitos Aplicados

Estes exemplos demonstram práticas de produção reais:

### Observabilidade Completa

- **Métricas**: Agregações numéricas (latência P95, custo/hora)
- **Traces**: Rastreamento distribuído de chamadas
- **Logs**: Eventos estruturados (não incluído nos exemplos, veja capítulo)

### Otimização de Performance

- Cache hit tracking (reduz custos em 40%+)
- Load balancing inteligente
- Fallback automático (zero downtime)

### Métricas Críticas para LLMs

| Categoria | Métrica | SLO Típico |
|-----------|---------|------------|
| Performance | Latency P95 | < 3s |
| Performance | TTFT (Time to First Token) | < 800ms |
| Custo | Cost per Request | < $0.05 |
| Qualidade | Cache Hit Rate | > 40% |
| Resiliência | Error Rate | < 0.1% |

---

## 🔧 Setup de Ambiente de Produção

Para usar estes exemplos em produção real, você precisará:

### Prometheus + Grafana
```bash
# Docker Compose
version: '3'
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

**prometheus.yml:**

```yaml
scrape_configs:
  - job_name: 'llm-service'
    static_configs:
      - targets: ['host.docker.internal:8000']
    scrape_interval: 15s
```

### OpenTelemetry Collector + Jaeger

```bash
# Docker Compose
version: '3'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC
  
  otel-collector:
    image: otel/opentelemetry-collector
    volumes:
      - ./otel-config.yml:/etc/otel/config.yml
    ports:
      - "4318:4318"
```

---

## 📊 Queries Úteis

### PromQL (Prometheus)

```promql
# Taxa de requisições por segundo
rate(llm_requests_total[5m])

# Latência P95 por modelo
histogram_quantile(0.95, rate(llm_request_duration_seconds_bucket[5m]))

# Custo acumulado na última hora
increase(llm_cost_usd_total[1h])

# Taxa de erro
sum(rate(llm_requests_total{status="error"}[5m])) 
/ sum(rate(llm_requests_total[5m]))

# Tokens/segundo
rate(llm_tokens_total{token_type="output"}[5m])
```

---

## 🎓 Próximos Passos

Depois de experimentar estes exemplos:

1. **Integre com seus LLMs reais**:
   - Substitua `simulate_llm_call()` por chamadas reais (OpenAI, Anthropic, etc.)
   - Adicione suas métricas específicas de negócio

2. **Configure alertas**:
   - Use Alertmanager do Prometheus
   - Defina SLOs apropriados para seu caso de uso

3. **Expanda observabilidade**:
   - Adicione logs estruturados (structlog)
   - Implemente custom exporters se necessário

4. **Otimize para produção**:
   - Implemente caching real (Redis)
   - Configure rate limiting
   - Adicione circuit breakers

---

## 📚 Recursos Adicionais

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [Grafana Dashboard Templates](https://grafana.com/grafana/dashboards/)

---

**Nota**: Estes exemplos são simulações para fins didáticos. Em produção, substitua as simulações por integrações reais com providers de LLM e infraestrutura de observabilidade.
