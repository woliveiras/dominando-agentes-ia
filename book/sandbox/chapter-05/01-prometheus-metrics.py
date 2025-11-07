"""
Capítulo 4: Dominando LLMs na Prática
Exemplo 1: Sistema de Métricas com Prometheus

Este exemplo demonstra como instrumentar chamadas LLM com métricas Prometheus
para monitoramento de produção.

Instalação necessária:
uv pip install prometheus-client openai anthropic

Execução:
python 01-prometheus-metrics.py

Acesse as métricas em: http://localhost:8000/metrics
"""

from prometheus_client import Counter, Histogram, Gauge, Info, start_http_server
from contextlib import contextmanager
from typing import Optional, Dict, Any
import time
import random

# ============================================================================
# Definição de Métricas
# ============================================================================

# Contador: incrementa sempre (nunca decrementa)
llm_requests_total = Counter(
    'llm_requests_total',
    'Total de requisições LLM',
    ['model', 'provider', 'status', 'cached']
)

# Histograma: distribui valores em buckets (ideal para latência)
llm_request_duration_seconds = Histogram(
    'llm_request_duration_seconds',
    'Duração de requisições LLM em segundos',
    ['model', 'provider'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]  # Buckets customizados
)

llm_tokens_total = Counter(
    'llm_tokens_total',
    'Total de tokens processados',
    ['model', 'provider', 'token_type']  # token_type: input, output
)

llm_cost_usd_total = Counter(
    'llm_cost_usd_total',
    'Custo total acumulado em USD',
    ['model', 'provider']
)

# Gauge: valor que pode subir ou descer (snapshot do estado atual)
llm_active_requests = Gauge(
    'llm_active_requests',
    'Requisições LLM ativas no momento',
    ['model', 'provider']
)

llm_cache_hit_rate = Gauge(
    'llm_cache_hit_rate',
    'Taxa de cache hit (0.0 - 1.0)',
    ['model']
)

# Info: metadados estáticos
llm_build_info = Info(
    'llm_build',
    'Informações de build da aplicação'
)
llm_build_info.info({
    'version': '1.0.0',
    'environment': 'production',
    'commit_sha': 'abc123def'
})

# ============================================================================
# Simulador de Chamadas LLM (para demonstração)
# ============================================================================

class MockLLMResponse:
    """Simula resposta de LLM para demonstração"""
    def __init__(self, input_tokens: int, output_tokens: int):
        self.usage = type('obj', (object,), {
            'prompt_tokens': input_tokens,
            'completion_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens
        })()
        self.choices = [type('obj', (object,), {
            'message': type('obj', (object,), {
                'content': "Resposta simulada do modelo"
            })(),
            'finish_reason': 'stop'
        })()]

def simulate_llm_call(model: str, delay: float = None) -> MockLLMResponse:
    """Simula chamada LLM com latência variável"""
    if delay is None:
        delay = random.uniform(0.5, 3.0)
    
    time.sleep(delay)
    
    # Simula tokens baseado no modelo
    if "gpt-4" in model:
        input_tokens = random.randint(100, 500)
        output_tokens = random.randint(200, 800)
    else:
        input_tokens = random.randint(50, 200)
        output_tokens = random.randint(100, 400)
    
    return MockLLMResponse(input_tokens, output_tokens)

# ============================================================================
# Instrumentação de Chamadas LLM
# ============================================================================

class LLMMetricsCollector:
    """
    Coletor de métricas para chamadas LLM com suporte a Prometheus.
    
    Rastreia latência, tokens, custos, erros e cache hits em tempo real.
    """
    
    PRICING = {
        # Preços em USD por 1K tokens (input, output)
        "gpt-3.5-turbo": (0.0015, 0.002),
        "gpt-4": (0.03, 0.06),
        "gpt-4-turbo": (0.01, 0.03),
        "claude-3-5-sonnet-20241022": (0.003, 0.015),
        "claude-3-haiku-20240307": (0.00025, 0.00125),
    }
    
    def __init__(self, cache_client=None):
        self.cache = cache_client
        self.cache_stats = {}
    
    def _calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calcula custo baseado em tokens e modelo"""
        if model not in self.PRICING:
            return 0.0
        
        input_price, output_price = self.PRICING[model]
        cost = (input_tokens / 1000) * input_price + (output_tokens / 1000) * output_price
        return cost
    
    @contextmanager
    def track_request(
        self,
        model: str,
        provider: str,
        prompt: str,
        config: Dict[str, Any]
    ):
        """
        Context manager para rastrear métricas de uma chamada LLM.
        
        Uso:
            with collector.track_request("gpt-4", "openai", prompt, config) as ctx:
                response = llm.generate(prompt)
                ctx["response"] = response
        """
        # Marca início da requisição
        start_time = time.time()
        llm_active_requests.labels(model=model, provider=provider).inc()
        
        # Contexto para armazenar dados da resposta
        context = {"cached": False, "error": None}
        
        try:
            # Verifica cache antes da chamada (simulado)
            if self.cache and random.random() > 0.6:  # 40% cache hit rate
                context["cached"] = True
                context["response"] = MockLLMResponse(0, 0)
            
            yield context
            
            # Após yield, registra sucesso
            status = "success"
            
        except Exception as e:
            # Registra erro
            status = "error"
            context["error"] = str(e)
            raise
        
        finally:
            # Sempre executa (sucesso ou erro)
            duration = time.time() - start_time
            
            # Decrementa requisições ativas
            llm_active_requests.labels(model=model, provider=provider).dec()
            
            # Registra latência
            llm_request_duration_seconds.labels(
                model=model,
                provider=provider
            ).observe(duration)
            
            # Registra contadores
            cached_label = "true" if context["cached"] else "false"
            llm_requests_total.labels(
                model=model,
                provider=provider,
                status=status,
                cached=cached_label
            ).inc()
            
            # Atualiza cache hit rate
            if model not in self.cache_stats:
                self.cache_stats[model] = {"hits": 0, "total": 0}
            
            self.cache_stats[model]["total"] += 1
            if context["cached"]:
                self.cache_stats[model]["hits"] += 1
            
            hit_rate = self.cache_stats[model]["hits"] / self.cache_stats[model]["total"]
            llm_cache_hit_rate.labels(model=model).set(hit_rate)
            
            # Registra tokens e custo (se disponível)
            if "response" in context and not context["cached"]:
                response = context["response"]
                if hasattr(response, "usage"):
                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens
                    
                    # Tokens
                    llm_tokens_total.labels(
                        model=model,
                        provider=provider,
                        token_type="input"
                    ).inc(input_tokens)
                    
                    llm_tokens_total.labels(
                        model=model,
                        provider=provider,
                        token_type="output"
                    ).inc(output_tokens)
                    
                    # Custo
                    cost = self._calculate_cost(model, input_tokens, output_tokens)
                    llm_cost_usd_total.labels(
                        model=model,
                        provider=provider
                    ).inc(cost)

# ============================================================================
# Exemplo de Uso
# ============================================================================

def example_instrumented_llm_calls():
    """Exemplo de chamadas LLM completamente instrumentadas"""
    collector = LLMMetricsCollector(cache_client=True)
    
    prompts = [
        "Explique o que é Kubernetes em 2 parágrafos",
        "Como funciona Docker?",
        "Diferença entre REST e GraphQL",
        "O que é CI/CD?",
        "Explique microserviços",
    ]
    
    models = [
        ("gpt-4-turbo", "openai"),
        ("gpt-3.5-turbo", "openai"),
        ("claude-3-5-sonnet-20241022", "anthropic"),
        ("claude-3-haiku-20240307", "anthropic"),
    ]
    
    print("🚀 Iniciando simulação de chamadas LLM...")
    print("📊 Métricas disponíveis em: http://localhost:8000/metrics\n")
    
    for i in range(20):
        model, provider = random.choice(models)
        prompt = random.choice(prompts)
        config = {"temperature": 0.7, "max_tokens": 300}
        
        print(f"[{i+1}/20] Chamando {model}...", end=" ")
        
        with collector.track_request(
            model=model,
            provider=provider,
            prompt=prompt,
            config=config
        ) as ctx:
            if not ctx["cached"]:
                # Simula chamada real
                response = simulate_llm_call(model)
                ctx["response"] = response
                print(f"✓ ({response.usage.total_tokens} tokens)")
            else:
                print("✓ (cache hit)")
        
        # Pequeno delay entre chamadas
        time.sleep(0.5)
    
    print("\n✅ Simulação concluída!")
    print("\n📈 Exemplos de queries PromQL úteis:")
    print("   - Taxa de requisições: rate(llm_requests_total[5m])")
    print("   - Latência P95: histogram_quantile(0.95, rate(llm_request_duration_seconds_bucket[5m]))")
    print("   - Custo/hora: rate(llm_cost_usd_total[1h]) * 3600")
    print("   - Taxa de erro: sum(rate(llm_requests_total{status='error'}[5m])) / sum(rate(llm_requests_total[5m]))")
    print("\n🔄 Servidor de métricas rodando... (Ctrl+C para parar)")

if __name__ == "__main__":
    # Inicia servidor HTTP para Prometheus scraping
    # Métricas expostas em http://localhost:8000/metrics
    start_http_server(8000)
    
    try:
        example_instrumented_llm_calls()
        
        # Mantém servidor rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando servidor de métricas...")
