"""
Capítulo 4: Dominando LLMs na Prática
Exemplo 2: Load Balancer com Fallback Automático

Demonstra implementação de load balancing entre múltiplos providers LLM
com fallback automático e estratégias de roteamento.

Instalação necessária:
uv pip install anthropic openai

Execução:
python 02-load-balancer.py
"""

import asyncio
from typing import List, Optional, Protocol, Dict, Any
from dataclasses import dataclass
from enum import Enum
import random
import time

# ============================================================================
# Interfaces e Configurações
# ============================================================================

class LLMProvider(Protocol):
    """Interface para providers de LLM"""
    async def generate(self, prompt: str, timeout: float) -> str: ...
    
    @property
    def name(self) -> str: ...

@dataclass
class ProviderConfig:
    """Configuração de um provider"""
    provider: 'MockLLMProvider'
    priority: int  # 0 = mais prioritário
    max_retries: int = 2
    timeout_seconds: float = 10.0

class LoadBalancingStrategy(Enum):
    """Estratégias de balanceamento"""
    ROUND_ROBIN = "round_robin"        # Alterna entre providers
    PRIORITY = "priority"               # Usa provider de maior prioridade primeiro
    FASTEST_FIRST = "fastest_first"     # Usa provider mais rápido historicamente

# ============================================================================
# Mock Providers (para demonstração)
# ============================================================================

class MockLLMProvider:
    """Provider simulado de LLM para demonstração"""
    
    def __init__(
        self,
        name: str,
        failure_rate: float = 0.0,
        avg_latency: float = 1.0
    ):
        self._name = name
        self.failure_rate = failure_rate
        self.avg_latency = avg_latency
    
    @property
    def name(self) -> str:
        return self._name
    
    async def generate(self, prompt: str, timeout: float) -> str:
        """Simula geração de resposta"""
        # Simula latência variável
        latency = random.gauss(self.avg_latency, self.avg_latency * 0.2)
        latency = max(0.1, latency)  # Mínimo 100ms
        
        await asyncio.sleep(latency)
        
        # Simula falhas aleatórias
        if random.random() < self.failure_rate:
            raise Exception(f"Provider {self.name} falhou (simulação)")
        
        return f"Resposta do {self.name} (latência: {latency:.2f}s)"

# ============================================================================
# Load Balancer
# ============================================================================

class LLMLoadBalancer:
    """
    Load balancer inteligente para múltiplos providers de LLM.
    Fornece fallback automático e distribuição de carga.
    """

    def __init__(
        self,
        providers: List[ProviderConfig],
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.PRIORITY
    ):
        self.providers = sorted(providers, key=lambda p: p.priority)
        self.strategy = strategy
        self.current_index = 0
        self.provider_stats = {
            p.provider.name: {
                "calls": 0,
                "failures": 0,
                "total_latency": 0.0
            } for p in providers
        }

    async def generate(
        self,
        prompt: str,
        max_attempts: Optional[int] = None
    ) -> dict:
        """
        Gera resposta com fallback automático entre providers.

        Args:
            prompt: Texto do prompt
            max_attempts: Máximo de tentativas (default: tenta todos os providers)

        Returns:
            Dict com 'response', 'provider_used', 'attempt_count', 'latency'

        Raises:
            Exception: Se todos os providers falharem
        """
        max_attempts = max_attempts or len(self.providers) * 2
        attempts = 0
        last_error = None
        start_time = time.time()

        for attempt in range(max_attempts):
            attempts += 1

            # Seleciona provider baseado na estratégia
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                provider_config = self.providers[self.current_index % len(self.providers)]
                self.current_index += 1
            elif self.strategy == LoadBalancingStrategy.FASTEST_FIRST:
                # Ordena por latência média
                provider_config = self._get_fastest_provider()
            else:  # PRIORITY
                provider_config = self.providers[attempt % len(self.providers)]

            provider = provider_config.provider
            self.provider_stats[provider.name]["calls"] += 1

            try:
                print(f"  ⏳ Tentativa {attempts}: usando {provider.name}")

                response = await asyncio.wait_for(
                    provider.generate(prompt, timeout=provider_config.timeout_seconds),
                    timeout=provider_config.timeout_seconds + 1.0  # +1s de buffer
                )
                
                latency = time.time() - start_time
                self.provider_stats[provider.name]["total_latency"] += latency

                print(f"  ✓ Sucesso com {provider.name} ({latency:.2f}s)")

                return {
                    "response": response,
                    "provider_used": provider.name,
                    "attempt_count": attempts,
                    "latency": latency
                }

            except asyncio.TimeoutError:
                last_error = f"Timeout com {provider.name}"
                print(f"  ✗ {last_error}")
                self.provider_stats[provider.name]["failures"] += 1

            except Exception as e:
                last_error = f"Erro com {provider.name}: {str(e)}"
                print(f"  ✗ {last_error}")
                self.provider_stats[provider.name]["failures"] += 1

            # Pequeno delay antes de tentar próximo provider
            await asyncio.sleep(0.1)

        # Todos os providers falharam
        raise Exception(
            f"Todos os providers falharam após {attempts} tentativas. "
            f"Último erro: {last_error}"
        )
    
    def _get_fastest_provider(self) -> ProviderConfig:
        """Retorna provider com menor latência média"""
        avg_latencies = {}
        for provider_config in self.providers:
            stats = self.provider_stats[provider_config.provider.name]
            if stats["calls"] > 0:
                avg_latencies[provider_config.provider.name] = (
                    stats["total_latency"] / (stats["calls"] - stats["failures"])
                    if stats["calls"] > stats["failures"] else float('inf')
                )
            else:
                avg_latencies[provider_config.provider.name] = 0.0
        
        # Se nenhum provider teve sucesso ainda, usa prioridade
        if all(lat == float('inf') or lat == 0.0 for lat in avg_latencies.values()):
            return self.providers[0]
        
        fastest = min(avg_latencies, key=avg_latencies.get)
        return next(p for p in self.providers if p.provider.name == fastest)

    def get_stats(self) -> dict:
        """Retorna estatísticas de uso dos providers"""
        return {
            name: {
                **stats,
                "success_rate": (
                    (stats["calls"] - stats["failures"]) / stats["calls"]
                    if stats["calls"] > 0 else 0
                ),
                "avg_latency": (
                    stats["total_latency"] / (stats["calls"] - stats["failures"])
                    if stats["calls"] > stats["failures"] else 0
                )
            }
            for name, stats in self.provider_stats.items()
        }

# ============================================================================
# Exemplos de Uso
# ============================================================================

async def demo_priority_strategy():
    """Demonstra estratégia PRIORITY"""
    print("\n" + "="*70)
    print("📋 ESTRATÉGIA: PRIORITY")
    print("="*70)
    print("Tenta providers na ordem de prioridade, faz fallback se falhar\n")
    
    providers = [
        ProviderConfig(
            provider=MockLLMProvider("OpenAI-GPT4", failure_rate=0.3, avg_latency=1.5),
            priority=0,  # Prioridade alta
            timeout_seconds=3.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("Anthropic-Claude", failure_rate=0.1, avg_latency=1.0),
            priority=1,  # Prioridade média
            timeout_seconds=3.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("Google-Gemini", failure_rate=0.0, avg_latency=2.0),
            priority=2,  # Backup
            timeout_seconds=3.0
        ),
    ]

    balancer = LLMLoadBalancer(providers, strategy=LoadBalancingStrategy.PRIORITY)

    # Faz múltiplas chamadas
    for i in range(5):
        print(f"\n🔹 Chamada {i+1}:")
        try:
            result = await balancer.generate("Explique machine learning")
            print(f"  📝 Resultado: {result['response'][:50]}...")
        except Exception as e:
            print(f"  ❌ Falha: {e}")
    
    # Estatísticas
    print("\n📊 Estatísticas dos providers:")
    stats = balancer.get_stats()
    for name, data in stats.items():
        print(f"  {name}:")
        print(f"    - Chamadas: {data['calls']}")
        print(f"    - Success rate: {data['success_rate']:.1%}")
        print(f"    - Latência média: {data['avg_latency']:.2f}s")

async def demo_round_robin_strategy():
    """Demonstra estratégia ROUND_ROBIN"""
    print("\n" + "="*70)
    print("🔄 ESTRATÉGIA: ROUND_ROBIN")
    print("="*70)
    print("Alterna entre providers para distribuir carga\n")
    
    providers = [
        ProviderConfig(
            provider=MockLLMProvider("OpenAI-1", failure_rate=0.0, avg_latency=1.0),
            priority=0,
            timeout_seconds=3.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("OpenAI-2", failure_rate=0.0, avg_latency=1.0),
            priority=0,
            timeout_seconds=3.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("OpenAI-3", failure_rate=0.0, avg_latency=1.0),
            priority=0,
            timeout_seconds=3.0
        ),
    ]

    balancer = LLMLoadBalancer(providers, strategy=LoadBalancingStrategy.ROUND_ROBIN)

    for i in range(6):
        print(f"\n🔹 Chamada {i+1}:")
        result = await balancer.generate("Explique Kubernetes")
        print(f"  📝 Provider usado: {result['provider_used']}")
    
    print("\n📊 Distribuição de carga:")
    stats = balancer.get_stats()
    for name, data in stats.items():
        print(f"  {name}: {data['calls']} chamadas")

async def demo_fastest_first_strategy():
    """Demonstra estratégia FASTEST_FIRST"""
    print("\n" + "="*70)
    print("⚡ ESTRATÉGIA: FASTEST_FIRST")
    print("="*70)
    print("Prefere provider mais rápido baseado em histórico\n")
    
    providers = [
        ProviderConfig(
            provider=MockLLMProvider("Slow-Provider", failure_rate=0.0, avg_latency=3.0),
            priority=0,
            timeout_seconds=5.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("Fast-Provider", failure_rate=0.0, avg_latency=0.5),
            priority=1,
            timeout_seconds=5.0
        ),
        ProviderConfig(
            provider=MockLLMProvider("Medium-Provider", failure_rate=0.0, avg_latency=1.5),
            priority=2,
            timeout_seconds=5.0
        ),
    ]

    balancer = LLMLoadBalancer(providers, strategy=LoadBalancingStrategy.FASTEST_FIRST)

    # Primeiras chamadas usam prioridade (ainda não há histórico)
    print("📍 Fase 1: Construindo histórico de latência...")
    for i in range(3):
        result = await balancer.generate(f"Chamada {i+1}")
        print(f"  Chamada {i+1}: {result['provider_used']} ({result['latency']:.2f}s)")
    
    # Próximas chamadas usam o mais rápido
    print("\n📍 Fase 2: Usando provider mais rápido...")
    for i in range(5):
        result = await balancer.generate(f"Chamada {i+4}")
        print(f"  Chamada {i+4}: {result['provider_used']} ({result['latency']:.2f}s)")
    
    print("\n📊 Latência média por provider:")
    stats = balancer.get_stats()
    for name, data in stats.items():
        print(f"  {name}: {data['avg_latency']:.2f}s")

async def main():
    """Executa todas as demonstrações"""
    print("\n🚀 Load Balancer para LLMs - Demonstração\n")
    
    await demo_priority_strategy()
    await asyncio.sleep(1)
    
    await demo_round_robin_strategy()
    await asyncio.sleep(1)
    
    await demo_fastest_first_strategy()
    
    print("\n" + "="*70)
    print("✅ Demonstração completa!")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
