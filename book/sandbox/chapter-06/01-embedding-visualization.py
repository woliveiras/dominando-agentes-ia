"""
Visualização de Embeddings com t-SNE

Este script demonstra como visualizar embeddings de frases em um espaço 2D usando t-SNE.
Frases semanticamente similares aparecem próximas no gráfico, formando clusters distintos.

Dependências:
    uv pip install sentence-transformers scikit-learn matplotlib numpy

Uso:
    python 01-embedding-visualization.py
"""

# uv pip install sentence-transformers scikit-learn matplotlib numpy

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 1. Frases de exemplo com clusters semânticos claros
frases = [
    # Cluster 1: Animais
    "O leão é o rei da selva.",
    "Gatos são animais de estimação populares.",
    "Cachorros são conhecidos por sua lealdade.",
    "Elefantes são os maiores mamíferos terrestres.",

    # Cluster 2: Frutas
    "Maçãs são frutas saudáveis.",
    "Bananas são ricas em potássio.",
    "Laranjas são uma ótima fonte de vitamina C.",
    "Morangos são deliciosos em sobremesas.",

    # Cluster 3: Tecnologia
    "Python é uma linguagem de programação versátil.",
    "Inteligência artificial está transformando o mundo.",
    "A computação em nuvem oferece escalabilidade.",
    "Blockchain é a tecnologia por trás do Bitcoin."
]

# Mapeamento de cores para os clusters
cores = ['r'] * 4 + ['g'] * 4 + ['b'] * 4
labels = ['Animal'] * 4 + ['Fruta'] * 4 + ['Tecnologia'] * 4

# 2. Gerar embeddings
print("Gerando embeddings...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(frases)
print(f"Shape dos embeddings: {embeddings.shape}")

# 3. Redução de dimensionalidade com t-SNE
print("Aplicando t-SNE para redução de dimensionalidade...")
tsne = TSNE(n_components=2, perplexity=5, random_state=42, init='random', learning_rate=200)
embeddings_2d = tsne.fit_transform(embeddings)
print(f"Shape após t-SNE: {embeddings_2d.shape}")

# 4. Plotar o resultado
print("Gerando visualização...")
plt.figure(figsize=(12, 8))
for i, (x, y) in enumerate(embeddings_2d):
    plt.scatter(x, y, c=cores[i], label=labels[i] if i % 4 == 0 else "")
    plt.annotate(frases[i].split()[0], (x, y), textcoords="offset points", xytext=(5,2), ha='right')

# Criar legenda única
handles, labels_legend = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels_legend, handles))
plt.legend(by_label.values(), by_label.keys(), title="Clusters Semânticos")

plt.title("Visualização 2D de Embeddings de Frases com t-SNE")
plt.xlabel("Dimensão 1 (t-SNE)")
plt.ylabel("Dimensão 2 (t-SNE)")
plt.grid(True)

# Salvar a imagem
output_path = 'embedding_visualization.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\nImagem salva em: {output_path}")

# Mostrar o gráfico
plt.show()

# 5. Análise dos resultados
print("\n=== Análise dos Clusters ===")
for cluster_name in ['Animal', 'Fruta', 'Tecnologia']:
    cluster_indices = [i for i, label in enumerate(labels) if label == cluster_name]
    cluster_embeddings = embeddings[cluster_indices]
    
    # Calcular centroide do cluster
    centroid = np.mean(cluster_embeddings, axis=0)
    
    # Calcular distâncias do centroide
    distances = [np.linalg.norm(emb - centroid) for emb in cluster_embeddings]
    avg_distance = np.mean(distances)
    
    print(f"\nCluster '{cluster_name}':")
    print(f"  - Distância média do centroide: {avg_distance:.4f}")
    print(f"  - Frases:")
    for idx in cluster_indices:
        print(f"    • {frases[idx]}")
