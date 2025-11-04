# Capítulo 1: Exemplo de Self-Attention
# Implementação simplificada do mecanismo de self-attention

import torch
import torch.nn as nn

class SelfAttention(nn.Module):
    def __init__(self, d_model, d_k):
        super().__init__()
        # Matrizes de projeção aprendidas durante treinamento
        # Essas matrizes transformam embeddings em queries, keys e values
        self.W_Q = nn.Linear(d_model, d_k)  # Projeta para "o que buscar"
        self.W_K = nn.Linear(d_model, d_k)  # Projeta para "o que oferecer"
        self.W_V = nn.Linear(d_model, d_k)  # Projeta para "a informação"
        self.d_k = d_k  # Dimensão das keys (usado para normalização)

    def forward(self, X):
        """
        Calcula self-attention sobre a sequência de entrada.
        
        Args:
            X: (batch, seq_len, d_model) - embeddings de entrada
        
        Returns:
            (batch, seq_len, d_k) - representações contextualizadas
        """
        # Passo 1: Projetar X em espaços Q, K, V
        # Cada token é transformado em 3 representações diferentes
        Q = self.W_Q(X)  # (batch, seq_len, d_k) - "Perguntas"
        K = self.W_K(X)  # (batch, seq_len, d_k) - "Chaves"
        V = self.W_V(X)  # (batch, seq_len, d_k) - "Valores"

        # Passo 2: Computar attention scores (similaridade entre Q e K)
        # @ é multiplicação matricial: cada query compara com todas as keys
        scores = (Q @ K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k))
        # scores: (batch, seq_len, seq_len) - matriz de similaridades
        # Dividimos por √d_k para evitar valores muito grandes

        # Passo 3: Aplicar softmax para obter pesos de atenção
        # Transforma scores em probabilidades que somam 1
        attention_weights = torch.softmax(scores, dim=-1)
        # attention_weights[i][j] = quanto o token i presta atenção no token j

        # Passo 4: Ponderar valores V pelos pesos de atenção
        # Cada token recebe uma combinação ponderada de todos os valores
        output = attention_weights @ V  # (batch, seq_len, d_k)

        return output

# Exemplo de uso
if __name__ == "__main__":
    # Configuração
    batch_size = 1
    seq_len = 5  # "The cat sat on mat"
    d_model = 512  # Dimensão dos embeddings
    d_k = 64  # Dimensão das queries/keys/values

    # Criar embeddings de exemplo (normalmente viriam do embedding layer)
    X = torch.randn(batch_size, seq_len, d_model)

    # Criar módulo de self-attention
    attention = SelfAttention(d_model, d_k)

    # Calcular atenção
    output = attention(X)

    print(f"Input shape: {X.shape}")
    print(f"Output shape: {output.shape}")
    print("\nSelf-attention processou a sequência e criou representações contextualizadas!")
