"""
Capítulo 4: Dominando LLMs na Prática
Exemplo 3: Rastreamento Distribuído com OpenTelemetry

Demonstra instrumentação de workflows LLM com traces distribuídos
para visualização de latência e dependências.

Instalação necessária:
uv pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp

Execução:
python 03-distributed-tracing.py

Nota: Para visualizar traces, você precisa de um OpenTelemetry Collector
ou Jaeger rodando. Este exemplo exporta traces para console para demonstração.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from typing import Dict, Any
import asyncio
import random
import time

# ============================================================================
# Configuração do OpenTelemetry
# ============================================================================

# Define resource (identifica o serviço)
resource = Resource.create({
    "service.name": "llm-agent-service",
    "service.version": "1.0.0",
    "deployment.environment": "development"
})

# Configura provider
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configura exportador para console (em produção, use OTLP para Jaeger/etc)
console_exporter = ConsoleSpanExporter()
span_processor = BatchSpanProcessor(console_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# ============================================================================
# Simuladores de Componentes
# ============================================================================

async def simulate_llm_call(model: str, prompt: str) -> Dict[str, Any]:
    """Simula chamada a LLM"""
    latency = random.uniform(0.5, 2.0)
    await asyncio.sleep(latency)
    
    return {
        "content": f"Resposta do {model}",
        "usage": {
            "prompt_tokens": len(prompt.split()) * 1.3,
            "completion_tokens": random.randint(100, 500)
        }
    }

async def simulate_embedding(text: str) -> list:
    """Simula geração de embedding"""
    await asyncio.sleep(random.uniform(0.1, 0.3))
    return [random.random() for _ in range(1536)]

async def simulate_vector_search(embedding: list, top_k: int = 3) -> list:
    """Simula busca vetorial"""
    await asyncio.sleep(random.uniform(0.3, 0.8))
    return [
        {"text": f"Documento {i+1}", "score": random.random()}
        for i in range(top_k)
    ]

# ============================================================================
# Workflow com Rastreamento Distribuído
# ============================================================================

class TracedLLMWorkflow:
    """
    Workflow de LLM com rastreamento distribuído completo.
    
    Cada etapa cria um span, permitindo visualizar:
    - Latência de cada componente
    - Dependências entre chamadas
    - Gargalos e falhas
    """
    
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    async def process_user_query(self, query: str) -> Dict[str, Any]:
        """
        Processa query do usuário em múltiplas etapas rastreadas.
        
        Args:
            query: Pergunta do usuário
            
        Returns:
            Resultado processado com metadados
        """
        # Span raiz do workflow completo
        with self.tracer.start_as_current_span(
            "process_user_query",
            attributes={
                "query.length": len(query),
                "workflow.version": "v2"
            }
        ) as root_span:
            
            print(f"\n{'='*70}")
            print(f"🔍 Processando: '{query}'")
            print(f"{'='*70}\n")
            
            # Etapa 1: Classificação de intenção
            intent = await self._classify_intent(query)
            root_span.set_attribute("query.intent", intent)
            print(f"  ✓ Intenção classificada: {intent}")
            
            # Etapa 2: Recuperação de contexto (se necessário)
            if intent in ["factual", "technical"]:
                context = await self._retrieve_context(query)
                root_span.set_attribute("context.retrieved", True)
                print(f"  ✓ Contexto recuperado: {len(context)} documentos")
            else:
                context = None
                root_span.set_attribute("context.retrieved", False)
                print(f"  ℹ️  Sem necessidade de contexto")
            
            # Etapa 3: Geração de resposta
            response = await self._generate_response(query, context, intent)
            print(f"  ✓ Resposta gerada: {len(response['content'])} caracteres")
            
            # Etapa 4: Pós-processamento
            final_response = await self._post_process(response["content"])
            print(f"  ✓ Pós-processamento concluído")
            
            root_span.set_attribute("response.length", len(final_response))
            
            result = {
                "response": final_response,
                "intent": intent,
                "used_context": context is not None,
                "tokens_used": response.get("usage", {})
            }
            
            print(f"\n{'='*70}")
            print(f"✅ Processamento concluído")
            print(f"{'='*70}\n")
            
            return result
    
    async def _classify_intent(self, query: str) -> str:
        """Classifica intenção da query"""
        with self.tracer.start_as_current_span(
            "classify_intent",
            attributes={"component": "classifier"}
        ) as span:
            
            # Simula chamada LLM para classificação
            response = await simulate_llm_call(
                "gpt-3.5-turbo",
                f"Classifique a intenção: {query}"
            )
            
            # Simula classificação
            intents = ["factual", "technical", "conversational", "creative"]
            intent = random.choice(intents)
            
            span.set_attribute("intent.classified", intent)
            span.set_attribute("tokens.used", response["usage"]["completion_tokens"])
            
            return intent
    
    async def _retrieve_context(self, query: str) -> list:
        """Recupera contexto relevante via RAG"""
        with self.tracer.start_as_current_span(
            "retrieve_context",
            attributes={"component": "rag"}
        ) as span:
            
            # Sub-span: Gera embedding da query
            with self.tracer.start_as_current_span(
                "generate_embedding",
                attributes={"text.length": len(query)}
            ):
                embedding = await simulate_embedding(query)
            
            # Sub-span: Busca vetorial
            with self.tracer.start_as_current_span(
                "vector_search",
                attributes={"top_k": 3}
            ) as search_span:
                results = await simulate_vector_search(embedding, top_k=3)
                search_span.set_attribute("results.count", len(results))
            
            span.set_attribute("context.documents", len(results))
            return results
    
    async def _generate_response(
        self,
        query: str,
        context: list,
        intent: str
    ) -> Dict[str, Any]:
        """Gera resposta final"""
        with self.tracer.start_as_current_span(
            "generate_response",
            attributes={
                "component": "generator",
                "intent": intent,
                "has_context": context is not None
            }
        ) as span:
            
            # Monta prompt
            if context:
                context_text = "\n".join([doc["text"] for doc in context])
                prompt = f"Contexto: {context_text}\n\nPergunta: {query}"
            else:
                prompt = query
            
            span.set_attribute("prompt.length", len(prompt))
            
            # Chamada principal
            response = await simulate_llm_call("gpt-4-turbo", prompt)
            
            span.set_attribute("response.tokens", response["usage"]["completion_tokens"])
            
            return response
    
    async def _post_process(self, response: str) -> str:
        """Pós-processa resposta"""
        with self.tracer.start_as_current_span(
            "post_process",
            attributes={"component": "post_processor"}
        ):
            # Simula validação, formatação, moderação
            await asyncio.sleep(0.05)
            return response.strip()

# ============================================================================
# Demonstração de Workflows Paralelos
# ============================================================================

async def demo_parallel_workflows():
    """
    Demonstra múltiplos workflows paralelos.
    Útil para ver como traces ajudam a entender concorrência.
    """
    print("\n" + "="*70)
    print("🔀 DEMONSTRAÇÃO: Workflows Paralelos")
    print("="*70)
    print("Processando múltiplas queries simultaneamente...\n")
    
    workflow = TracedLLMWorkflow()
    
    queries = [
        "O que é Kubernetes?",
        "Como funciona Docker?",
        "Explique microserviços",
    ]
    
    # Processa todas em paralelo
    tasks = [workflow.process_user_query(q) for q in queries]
    results = await asyncio.gather(*tasks)
    
    print("\n" + "="*70)
    print("📊 RESUMO DOS RESULTADOS")
    print("="*70)
    for i, (query, result) in enumerate(zip(queries, results), 1):
        print(f"\n{i}. Query: {query}")
        print(f"   Intent: {result['intent']}")
        print(f"   Usou contexto: {'Sim' if result['used_context'] else 'Não'}")
        print(f"   Tokens: {result['tokens_used'].get('completion_tokens', 0)}")

# ============================================================================
# Demonstração de Trace de Erro
# ============================================================================

async def demo_error_tracking():
    """
    Demonstra como traces capturam e propagam erros.
    """
    print("\n" + "="*70)
    print("❌ DEMONSTRAÇÃO: Rastreamento de Erros")
    print("="*70)
    print("Simulando falha no componente de RAG...\n")
    
    with tracer.start_as_current_span("process_with_error") as span:
        try:
            # Simula erro no componente de RAG
            with tracer.start_as_current_span("retrieve_context_failed") as rag_span:
                rag_span.set_attribute("error.simulated", True)
                await asyncio.sleep(0.5)
                raise Exception("Vector database connection timeout")
        
        except Exception as e:
            # Span captura o erro
            span.set_attribute("error.type", type(e).__name__)
            span.set_attribute("error.message", str(e))
            span.record_exception(e)
            
            print(f"  ✗ Erro capturado no span: {e}")
            print(f"  ℹ️  Trace permite identificar exatamente onde falhou")

# ============================================================================
# Exemplo Principal
# ============================================================================

async def main():
    """Executa demonstrações de tracing"""
    print("\n🎯 OpenTelemetry Distributed Tracing - Demonstração\n")
    
    # 1. Workflow single
    print("\n" + "="*70)
    print("📍 DEMONSTRAÇÃO: Workflow Single")
    print("="*70)
    
    workflow = TracedLLMWorkflow()
    result = await workflow.process_user_query("O que é machine learning?")
    
    await asyncio.sleep(1)  # Delay para visualização
    
    # 2. Workflows paralelos
    await demo_parallel_workflows()
    
    await asyncio.sleep(1)
    
    # 3. Tracking de erros
    await demo_error_tracking()
    
    # Force flush dos spans
    trace.get_tracer_provider().force_flush()
    
    print("\n" + "="*70)
    print("✅ Demonstração completa!")
    print("="*70)
    print("\n📝 Notas:")
    print("  - Spans foram exportados para console acima")
    print("  - Em produção, configure OTLP exporter para Jaeger/Zipkin")
    print("  - Traces permitem identificar gargalos e erros facilmente")
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
