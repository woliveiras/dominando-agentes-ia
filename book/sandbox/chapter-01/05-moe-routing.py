"""
Capítulo 1: Fundamentos de Transformers
Exemplo 5: Mixture of Experts (MoE) Routing

Este exemplo demonstra como funciona o routing dinâmico em MoE,
onde diferentes experts processam diferentes tipos de tokens.

Instalação necessária:
uv pip install torch

Execução:
python 05-moe-routing.py

Conceito:
- Ao invés de uma única FFN processar todos os tokens, temos N experts
- Um router decide dinamicamente quais experts usar para cada token
- Apenas top-k experts são ativados por token (geralmente k=2)
- Resultado: Maior capacidade sem aumentar compute proporcionalmente

Exemplo real: Mixtral 8x7B
- 8 experts de 7B parâmetros cada
- Router seleciona top-2 experts por token
- Total: 47B parâmetros, mas apenas ~13B ativos por token
- Performance próxima a modelo denso de 47B, custo de inferência de 13B
"""

import torch
import torch.nn as nn


class FFN(nn.Module):
    """Feedforward Network - Expert individual."""

    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.w2(torch.relu(self.w1(x)))


class MoELayer(nn.Module):
    """
    Mixture of Experts Layer com routing dinâmico.

    Args:
        d_model: Dimensão do modelo (embeddings)
        d_ff: Dimensão interna das FFNs dos experts
        num_experts: Número de experts disponíveis
        top_k: Quantos experts ativar por token (geralmente 2)
    """

    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        super().__init__()

        # Cria múltiplos experts (cada um é uma FFN independente)
        # Cada expert pode se especializar em diferentes tipos de conteúdo
        self.experts = nn.ModuleList([
            FFN(d_model, d_ff) for _ in range(num_experts)
        ])

        # Router: rede neural que decide quais experts usar para cada token
        # Aprende automaticamente a rotear tokens para experts especializados
        self.router = nn.Linear(d_model, num_experts)
        self.top_k = top_k  # Quantos experts ativar por token (geralmente 2)
        self.num_experts = num_experts

    def forward(self, x):
        """
        Processa tokens através de experts selecionados dinamicamente.

        Args:
            x: (batch, seq_len, d_model) - tokens de entrada

        Returns:
            (batch, seq_len, d_model) - tokens processados por experts
            router_probs: (batch, seq_len, num_experts) - probabilidades de routing (para análise)
        """

        batch, seq_len, d_model = x.shape

        # Passo 1: Router computa scores para cada expert
        # Para cada token, determina quão relevante é cada expert
        router_logits = self.router(x)  # (batch, seq_len, num_experts)
        router_probs = torch.softmax(router_logits, dim=-1)

        # Passo 2: Seleciona top-k experts por token
        # Em vez de usar todos os 8 experts, usa apenas os 2 melhores
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k, dim=-1)

        # Normaliza probabilidades dos top-k para somarem 1
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        # Passo 3: Processa cada token pelos seus top-k experts
        output = torch.zeros_like(x)

        for i in range(self.top_k):
            # Índice do i-ésimo melhor expert para cada token
            expert_idx = top_k_indices[:, :, i]  # (batch, seq_len)
            # Peso (probabilidade) deste expert
            expert_prob = top_k_probs[:, :, i:i+1]  # (batch, seq_len, 1)

            # Roteamento dinâmico: diferentes tokens vão para diferentes experts
            # Um token sobre Python pode ir para Expert 1, sobre medicina para Expert 3
            for expert_id, expert in enumerate(self.experts):
                # Máscara: quais tokens devem usar este expert?
                mask = (expert_idx == expert_id)  # (batch, seq_len)

                if mask.any():
                    # Processa tokens pela FFN do expert
                    expert_output = expert(x)  # (batch, seq_len, d_model)
                    # Adiciona saída ponderada pela probabilidade do router
                    output += expert_output * expert_prob * mask.unsqueeze(-1).float()

        return output, router_probs


def demo():
    """Demonstração de MoE routing."""

    print("=" * 80)
    print("Mixture of Experts (MoE) - Routing Dinâmico")
    print("=" * 80)

    # Configuração similar a Mixtral 8x7B (escala reduzida)
    d_model = 128  # Dimensão dos embeddings (Mixtral usa 4096)
    d_ff = 512     # Dimensão interna FFN (Mixtral usa 14336)
    num_experts = 8
    top_k = 2

    # Criar camada MoE
    moe = MoELayer(d_model, d_ff, num_experts, top_k)

    # Simular batch de tokens
    batch_size = 2
    seq_len = 10
    x = torch.randn(batch_size, seq_len, d_model)

    print(f"\nConfiguração:")
    print(f"  Número de experts: {num_experts}")
    print(f"  Top-k experts ativos por token: {top_k}")
    print(f"  Batch size: {batch_size}")
    print(f"  Sequence length: {seq_len}")
    print(f"  Dimensão do modelo: {d_model}")

    # Forward pass
    output, router_probs = moe(x)

    print(f"\nFormas dos tensores:")
    print(f"  Input: {x.shape}")
    print(f"  Output: {output.shape}")
    print(f"  Router probs: {router_probs.shape}")

    # Analisar routing do primeiro batch, primeiro token
    print(f"\n{'-' * 80}")
    print("Análise de Routing (Batch 0, Token 0):")
    print(f"{'-' * 80}")

    first_token_probs = router_probs[0, 0, :]  # Probabilidades para cada expert
    top_k_values, top_k_experts = torch.topk(first_token_probs, top_k)

    print(f"\nProbabilidades de routing para todos os experts:")
    for expert_id in range(num_experts):
        prob = first_token_probs[expert_id].item()
        bar = "█" * int(prob * 50)  # Visualização em barra
        print(f"  Expert {expert_id}: {prob:.4f} {bar}")

    print(f"\nTop-{top_k} experts selecionados:")
    for i in range(top_k):
        expert_id = top_k_experts[i].item()
        prob = top_k_values[i].item()
        print(f"  #{i+1}: Expert {expert_id} (prob={prob:.4f})")

    # Calcular estatísticas de balanceamento
    print(f"\n{'-' * 80}")
    print("Estatísticas de Balanceamento de Carga:")
    print(f"{'-' * 80}")

    # Contar quantas vezes cada expert foi selecionado
    expert_counts = torch.zeros(num_experts)
    for b in range(batch_size):
        for s in range(seq_len):
            top_k_values, top_k_experts = torch.topk(router_probs[b, s, :], top_k)
            for expert_id in top_k_experts:
                expert_counts[expert_id] += 1

    total_selections = batch_size * seq_len * top_k
    print(f"\nTotal de seleções possíveis: {total_selections}")
    print(f"Distribuição das seleções:")
    for expert_id in range(num_experts):
        count = expert_counts[expert_id].item()
        percentage = (count / total_selections) * 100
        bar = "█" * int(percentage / 2)  # Visualização
        print(f"  Expert {expert_id}: {int(count):2d} seleções ({percentage:5.2f}%) {bar}")

    # Calcular load balance loss (usado durante treinamento)
    mean_probs = router_probs.mean(dim=[0, 1])  # Média através de batch e seq_len
    load_balance_loss = num_experts * (mean_probs ** 2).sum()

    print(f"\nLoad Balance Loss: {load_balance_loss:.4f}")
    print(f"  (Ideal seria {1/num_experts:.4f} para balanceamento perfeito)")

    # Comparação: MoE vs Modelo Denso
    print(f"\n{'-' * 80}")
    print("MoE vs Modelo Denso - Comparação:")
    print(f"{'-' * 80}")

    # Parâmetros
    moe_params_per_expert = d_model * d_ff * 2  # w1 + w2
    moe_total_params = moe_params_per_expert * num_experts
    moe_active_params = moe_params_per_expert * top_k

    dense_params = d_model * d_ff * 2

    print(f"\nMoE (Mixtral-style):")
    print(f"  Parâmetros totais: {moe_total_params:,}")
    print(f"  Parâmetros ativos por token: {moe_active_params:,}")
    print(f"  Eficiência: {(moe_active_params / moe_total_params) * 100:.1f}% dos parâmetros ativos")

    print(f"\nModelo Denso equivalente:")
    print(f"  Parâmetros: {dense_params:,}")

    print(f"\nVantagem do MoE:")
    print(f"  Capacidade {moe_total_params / dense_params:.1f}x maior")
    print(f"  Compute apenas {moe_active_params / dense_params:.1f}x maior")
    print(f"  Economia de compute: {(1 - moe_active_params / moe_total_params) * 100:.1f}%")

    print(f"\n{'-' * 80}")
    print("Desafios do MoE:")
    print(f"{'-' * 80}")
    print("""
1. Memória total alta: Todos experts precisam estar na memória
   - Mixtral 8x7B: Requer ~94GB VRAM (FP16)
   - Solução: Expert parallelism (distribuir experts entre GPUs)

2. Balanceamento de carga: Router pode favorecer alguns experts
   - Solução: Load balancing loss penalty
   - Formula: loss += weight * (num_experts * mean(router_probs)^2)

3. Complexidade de treinamento: All-to-all communication entre GPUs
   - Frameworks: Megatron-LM, DeepSpeed-MoE

4. Overfitting de routing: Router pode memorizar padrões
   - Solução: Dropout no router, noise no gating
    """)


if __name__ == "__main__":
    demo()

    print("\n" + "=" * 80)
    print("Modelos MoE em Produção:")
    print("=" * 80)
    print("""
- Mixtral 8x7B (Mistral AI): 47B params total, ~13B ativos
- GPT-4 (rumores): Suspeita-se que usa MoE com 8-16 experts
- Switch Transformers (Google): Até 1.6T params com sparse activation
- GShard (Google): MoE para tradução neural massiva

MoE é especialmente eficaz quando:
✓ Você tem diversidade de dados (múltiplos domínios/idiomas)
✓ Precisa de alta capacidade mas tem constraints de latência
✓ Pode pagar custo de memória total (todos experts carregados)
✓ Tem infraestrutura para treinamento distribuído
    """)
