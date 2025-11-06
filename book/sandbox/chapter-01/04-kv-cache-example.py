"""
Capítulo 1: Fundamentos de Transformers
Exemplo 4: KV-Cache para Geração Autoregressiva Eficiente

Implementação de KV-Cache que reduz computação redundante durante geração
de texto, reutilizando keys e values já calculados.

Instalação necessária:
uv pip install torch

Execução:
python 04-kv-cache-example.py
"""

import torch
import torch.nn as nn

class KVCachedAttention(nn.Module):
    def __init__(self, d_model, d_k, d_v):
        super().__init__()
        # Matrizes de projeção (mesmas do SelfAttention)
        self.W_Q = nn.Linear(d_model, d_k)
        self.W_K = nn.Linear(d_model, d_k)
        self.W_V = nn.Linear(d_model, d_v)
        self.d_k = d_k

        # Cache para armazenar K e V de tokens já processados
        # Isso evita recomputar K e V toda vez que geramos um novo token
        self.k_cache = None  # Shape: (batch, seq_len, d_k)
        self.v_cache = None  # Shape: (batch, seq_len, d_v)

    def forward(self, x, use_cache=True):
        """
        Processa novo token usando cache de K e V anteriores.
        
        Args:
            x: (batch, 1 ou seq_len, d_model) - novo token ou sequência completa
            use_cache: se True, usa e atualiza o cache
        """
        batch_size = x.size(0)

        # Passo 1: Compute Q, K, V APENAS para o novo token
        # Economiza computação pois não recalcula tokens anteriores
        Q_new = self.W_Q(x)  # (batch, 1, d_k) - Query do novo token
        K_new = self.W_K(x)  # (batch, 1, d_k) - Key do novo token
        V_new = self.W_V(x)  # (batch, 1, d_v) - Value do novo token

        # Passo 2: Combinar novo K/V com cache existente
        if use_cache and self.k_cache is not None:
            # Concatena K e V novos com os já computados anteriormente
            K = torch.cat([self.k_cache, K_new], dim=1)  # (batch, seq_len+1, d_k)
            V = torch.cat([self.v_cache, V_new], dim=1)  # (batch, seq_len+1, d_v)
        else:
            # Primeira iteração ou cache desabilitado
            K = K_new
            V = V_new

        # Passo 3: Atualiza cache para a próxima iteração
        if use_cache:
            # Detach evita acumular gradientes desnecessários no cache
            self.k_cache = K.detach()
            self.v_cache = V.detach()

        # Passo 4: Compute attention usando K e V completos (incluindo cache)
        scores = (Q_new @ K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k))

        # Máscara causal não é necessária aqui pois Q_new é apenas o último token
        # que naturalmente só atende a tokens anteriores + ele mesmo

        attention_weights = torch.softmax(scores, dim=-1)
        output = attention_weights @ V  # (batch, 1, d_v)

        return output

    def clear_cache(self):
        """Limpa cache entre diferentes gerações (importante entre prompts)"""
        self.k_cache = None
        self.v_cache = None

# Exemplo de uso simulando geração autoregressiva
if __name__ == "__main__":
    # Configuração
    d_model = 512
    d_k = 64
    d_v = 64
    seq_len = 10  # Vamos gerar 10 tokens

    # Criar módulo com KV-Cache
    attention = KVCachedAttention(d_model, d_k, d_v)

    print("="*60)
    print("Simulação de Geração Autoregressiva com KV-Cache")
    print("="*60)

    # Simular geração token-por-token
    for i in range(seq_len):
        # Novo token (simulado como embedding aleatório)
        new_token = torch.randn(1, 1, d_model)

        # Processar com KV-Cache
        output = attention(new_token, use_cache=True)

        print(f"\nToken {i+1}:")
        print(f"  Cache size: {attention.k_cache.size(1) if attention.k_cache is not None else 0}")
        print(f"  Output shape: {output.shape}")

    print("\n" + "="*60)
    print("Estatísticas finais:")
    print("="*60)
    print(f"Tokens gerados: {seq_len}")
    print(f"Tamanho final do cache: {attention.k_cache.size(1)}")
    print(f"\nSem KV-Cache: {seq_len * (seq_len + 1) // 2} computações de K/V")
    print(f"Com KV-Cache: {seq_len} computações de K/V")
    print(f"Economia: {100 * (1 - seq_len / (seq_len * (seq_len + 1) // 2)):.1f}%")

    # Limpar cache
    attention.clear_cache()
    print("\n✅ Cache limpo - pronto para novo prompt")
