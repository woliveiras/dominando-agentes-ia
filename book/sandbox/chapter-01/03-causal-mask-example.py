# Capítulo 1: Exemplo de Causal Mask
# Implementação da máscara causal para modelos decoder-only

import torch

def create_causal_mask(seq_len):
    """
    Cria máscara causal para impedir atenção em tokens futuros.
    Essencial para modelos decoder-only (GPT-like) que não podem "trapacear"
    olhando para o futuro durante o treinamento.
    
    Args:
        seq_len: comprimento da sequência
    
    Returns:
        mask: matriz (seq_len, seq_len) com 0s onde permitido, -inf onde bloqueado
    """
    # Matriz triangular inferior: 1s abaixo e na diagonal, 0s acima
    # Cada linha representa um token, cada coluna um token que pode ser visto
    mask = torch.tril(torch.ones(seq_len, seq_len))

    # Na prática, usamos -inf para posições bloqueadas antes do softmax
    # Quando somamos -inf ao attention score, softmax transforma em ~0
    # Isso garante que softmax(score + mask) ≈ 0 para posições futuras
    mask = mask.masked_fill(mask == 0, float('-inf'))  # Posições bloqueadas = -inf
    mask = mask.masked_fill(mask == 1, 0.0)            # Posições permitidas = 0

    return mask

def masked_attention(Q, K, V, mask):
    """
    Calcula atenção com máscara causal aplicada.
    
    Args:
        Q, K, V: queries, keys, values
        mask: máscara causal criada por create_causal_mask()
    
    Returns:
        output com atenção causal aplicada
    """
    d_k = Q.size(-1)
    # Calcula scores de atenção normalizados
    scores = (Q @ K.transpose(-2, -1)) / torch.sqrt(torch.tensor(d_k))

    # Adiciona máscara antes do softmax
    # scores + mask onde mask=-inf para posições bloqueadas
    # Isso faz com que essas posições tenham probabilidade ~0 após softmax
    scores = scores + mask

    # Softmax transforma -inf em ~0, efetivamente bloqueando atenção futura
    attention_weights = torch.softmax(scores, dim=-1)

    return attention_weights @ V

# Exemplo de uso
if __name__ == "__main__":
    seq_len = 5
    d_k = 64

    # Criar máscara causal
    mask = create_causal_mask(seq_len)

    print("Máscara Causal (seq_len=5):")
    print("Posições com 0.0 = permitido, -inf = bloqueado\n")
    print(mask)

    print("\n\nVisualização:")
    print("[[0, -inf, -inf, -inf, -inf],  # Token 0 só vê ele mesmo")
    print(" [0,   0,   -inf, -inf, -inf],  # Token 1 vê tokens 0-1")
    print(" [0,   0,     0,  -inf, -inf],  # Token 2 vê tokens 0-2")
    print(" [0,   0,     0,    0,  -inf],  # Token 3 vê tokens 0-3")
    print(" [0,   0,     0,    0,    0]]   # Token 4 vê todos tokens 0-4")

    # Simular Q, K, V
    Q = torch.randn(1, seq_len, d_k)
    K = torch.randn(1, seq_len, d_k)
    V = torch.randn(1, seq_len, d_k)

    # Aplicar atenção com máscara
    output = masked_attention(Q, K, V, mask)

    print(f"\n\nInput shapes:")
    print(f"  Q: {Q.shape}")
    print(f"  K: {K.shape}")
    print(f"  V: {V.shape}")
    print(f"\nOutput shape: {output.shape}")
    print("\nAtenção causal aplicada com sucesso!")
    print("Cada token agora só atende a tokens anteriores, não futuros.")
