# uv pip install llama-cpp-python psutil

"""
Benchmark de Quantização de Modelos

Este script compara diferentes níveis de quantização (Q8, Q5, Q4) medindo:
- Uso de memória
- Latência de inferência
- Throughput (tokens/segundo)
- Qualidade subjetiva

Autor: Dominando Agentes IA
Capítulo 3: Fine-Tuning e Otimização
"""

import time
import psutil
import os
from typing import Dict, List

try:
    from llama_cpp import Llama
except ImportError:
    print("❌ llama-cpp-python não instalado.")
    print("   Instale com: uv pip install llama-cpp-python")
    raise


def get_memory_usage() -> float:
    """
    Retorna uso de memória do processo atual em MB.

    Returns:
        float: Memória utilizada em megabytes
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def format_memory(mb: float) -> str:
    """
    Formata memória em MB para string legível.

    Args:
        mb: Memória em megabytes

    Returns:
        str: String formatada (ex: "1,234 MB" ou "1.2 GB")
    """
    if mb >= 1024:
        return f"{mb/1024:.2f} GB"
    return f"{mb:.0f} MB"


def benchmark_model(model_path: str, test_prompt: str, max_tokens: int = 100) -> Dict:
    """
    Realiza benchmark completo de um modelo quantizado.

    Args:
        model_path: Caminho para arquivo GGUF do modelo
        test_prompt: Prompt de teste para inferência
        max_tokens: Número máximo de tokens a gerar

    Returns:
        Dict com métricas: load_time, memory_mb, gen_time, tokens_per_sec, output

    Raises:
        FileNotFoundError: Se modelo não existe
        RuntimeError: Se erro durante carregamento/inferência
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    # Medir memória antes
    mem_before = get_memory_usage()

    # Carregar modelo
    print(f"📦 Carregando modelo...")
    start_load = time.time()

    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=512,        # Context window
            n_threads=4,      # CPU threads
            verbose=False,    # Silenciar logs
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar modelo: {e}")

    load_time = time.time() - start_load
    mem_after = get_memory_usage()
    mem_used = mem_after - mem_before

    print(f"✅ Carregado em {load_time:.2f}s")
    print(f"💾 Memória utilizada: {format_memory(mem_used)}")

    # Medir latência de inferência
    print(f"🔄 Gerando resposta...")
    start_gen = time.time()

    try:
        output = llm(
            test_prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            echo=False,  # Não incluir prompt no output
        )
    except Exception as e:
        raise RuntimeError(f"Erro durante geração: {e}")

    gen_time = time.time() - start_gen
    generated_text = output['choices'][0]['text']
    tokens_generated = output['usage']['completion_tokens']
    tokens_per_sec = tokens_generated / gen_time if gen_time > 0 else 0

    print(f"✅ Geração completa em {gen_time:.2f}s")
    print(f"📊 Throughput: {tokens_per_sec:.1f} tokens/s")
    print(f"📝 Output: {generated_text[:100]}...")

    # Liberar memória
    del llm

    return {
        "load_time": load_time,
        "memory_mb": mem_used,
        "gen_time": gen_time,
        "tokens_per_sec": tokens_per_sec,
        "tokens_generated": tokens_generated,
        "output": generated_text
    }


def print_comparison_table(results: Dict[str, Dict], baseline_key: str = None):
    """
    Imprime tabela comparativa de resultados.

    Args:
        results: Dicionário {quantização: métricas}
        baseline_key: Chave do baseline para calcular percentuais (opcional)
    """
    if not results:
        print("Nenhum resultado para comparar.")
        return

    # Determinar baseline
    baseline = None
    if baseline_key and baseline_key in results:
        baseline = results[baseline_key]
    elif results:
        baseline = list(results.values())[0]

    # Cabeçalho
    print(f"\n{'='*80}")
    print("📊 COMPARAÇÃO DE PERFORMANCE")
    print(f"{'='*80}\n")

    headers = f"{'Quantização':<12} {'Memória':<15} {'Load (s)':<12} {'Gen (s)':<12} {'Tokens/s':<12}"
    print(headers)
    print("-" * 80)

    # Linhas de dados
    for quant, metrics in results.items():
        mem_pct = (metrics['memory_mb'] / baseline['memory_mb'] * 100) if baseline else 100
        speed_pct = (metrics['tokens_per_sec'] / baseline['tokens_per_sec'] * 100) if baseline else 100

        # Linha principal
        print(f"{quant:<12} {format_memory(metrics['memory_mb']):<15} "
              f"{metrics['load_time']:<12.2f} {metrics['gen_time']:<12.2f} "
              f"{metrics['tokens_per_sec']:<12.1f}")

        # Linha de percentuais (se não for baseline)
        if baseline and metrics != baseline:
            print(f"{'':>12} ({mem_pct:>5.1f}% mem)  {'':>8} "
                  f"({'':>6}) ({speed_pct:>5.1f}% speed)")

    print("-" * 80)


def print_quality_comparison(results: Dict[str, Dict]):
    """
    Imprime comparação de qualidade dos outputs.

    Args:
        results: Dicionário {quantização: métricas}
    """
    print(f"\n{'='*80}")
    print("🎯 COMPARAÇÃO DE QUALIDADE")
    print(f"{'='*80}\n")

    for quant, metrics in results.items():
        print(f"{quant}:")
        output_preview = metrics['output'][:200]
        # Quebrar linhas longas
        words = output_preview.split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= 75:
                line += word + " "
            else:
                print(f"  {line}")
                line = word + " "
        if line:
            print(f"  {line}")
        print()


def print_recommendations():
    """Imprime recomendações práticas baseadas nos resultados."""
    print(f"\n{'='*80}")
    print("🎯 RECOMENDAÇÕES PARA PRODUÇÃO")
    print(f"{'='*80}\n")

    recommendations = [
        ("API de produção (qualidade)", "Q8_0 ou Q5_K_M"),
        ("API de produção (custo)", "Q4_K_M"),
        ("Dispositivos edge/mobile", "Q4_0 ou Q3_K_M"),
        ("Pesquisa/desenvolvimento", "FP16 (baseline)"),
        ("Agentes com raciocínio complexo", "Q5_K_M ou superior"),
    ]

    print(f"{'Caso de Uso':<35} | {'Quantização Recomendada'}")
    print("-" * 80)
    for use_case, recommendation in recommendations:
        print(f"{use_case:<35} | {recommendation}")


def print_insights():
    """Imprime insights sobre quantização."""
    print(f"\n{'='*80}")
    print("💡 INSIGHTS")
    print(f"{'='*80}\n")

    insights = [
        "Q4_K_M: ~75% de redução de memória, qualidade excelente para maioria dos casos",
        "Q5_K_M: ~65% de redução, qualidade indistinguível de FP16 para tarefas comuns",
        "Q8_0: ~50% de redução, sem perda perceptível de qualidade",
        "Trade-off ideal: Q4_K_M ou Q5_K_M para produção balanceada",
        "Q4 permite rodar modelos 70B em GPUs consumidor (24GB)",
        "Quantização mais agressiva (Q3, Q2) só para casos extremos de memória",
    ]

    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")


def main():
    """
    Função principal que executa o benchmark completo.
    """
    print("="*80)
    print("🔬 BENCHMARK: Quantização de Modelos")
    print("="*80)
    print("\nEste benchmark compara diferentes níveis de quantização GGUF.")
    print("Você precisará baixar modelos previamente.\n")

    # Configuração
    model_paths = {
        "Q8_0": "./models/llama-2-7b.Q8_0.gguf",
        "Q5_K_M": "./models/llama-2-7b.Q5_K_M.gguf",
        "Q4_K_M": "./models/llama-2-7b.Q4_K_M.gguf",
    }

    test_prompt = "Explain quantum computing in simple terms:"
    results = {}

    # Verificar se modelos existem
    models_found = {k: v for k, v in model_paths.items() if os.path.exists(v)}

    if not models_found:
        print("⚠️  NENHUM modelo encontrado!")
        print("\n📥 Para executar este benchmark, baixe modelos GGUF:")
        print("   1. Instale: uv pip install huggingface-hub")
        print("   2. Baixe modelos:")
        print("      huggingface-cli download TheBloke/Llama-2-7B-GGUF \\")
        print("        llama-2-7b.Q4_K_M.gguf --local-dir ./models")
        print("      huggingface-cli download TheBloke/Llama-2-7B-GGUF \\")
        print("        llama-2-7b.Q5_K_M.gguf --local-dir ./models")
        print("      huggingface-cli download TheBloke/Llama-2-7B-GGUF \\")
        print("        llama-2-7b.Q8_0.gguf --local-dir ./models")
        print("\n   Ou use qualquer modelo GGUF de sua escolha.")
        print("\n💡 Para este benchmark, você pode:")
        print("   - Baixar apenas Q4_K_M (mais leve, ~4GB)")
        print("   - Comparar com Q8_0 para ver diferença de qualidade")
        return

    print(f"✅ {len(models_found)} modelo(s) encontrado(s)")
    print(f"   Modelos: {', '.join(models_found.keys())}\n")

    # Executar benchmarks
    for quant_level, model_path in models_found.items():
        print(f"\n{'='*80}")
        print(f"Testando: {quant_level}")
        print(f"{'='*80}\n")

        try:
            metrics = benchmark_model(model_path, test_prompt, max_tokens=100)
            results[quant_level] = metrics
        except Exception as e:
            print(f"❌ Erro ao testar {quant_level}: {e}")
            continue

        print(f"\n✅ {quant_level} benchmark completo\n")

    # Imprimir resultados
    if results:
        print_comparison_table(results, baseline_key="Q8_0")
        print_quality_comparison(results)
        print_insights()
        print_recommendations()
    else:
        print("\n❌ Nenhum benchmark foi executado com sucesso.")


if __name__ == "__main__":
    main()
