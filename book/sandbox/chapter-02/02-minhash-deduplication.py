# Capítulo 2: Deduplicação com MinHash e LSH
# Exemplo de detecção de documentos near-duplicates

from datasketch import MinHash, MinHashLSH

# Configuração LSH
# threshold=0.8 significa detectar docs com Jaccard similarity >= 80%
lsh = MinHashLSH(threshold=0.8, num_perm=128)

def get_minhash(text, num_perm=128):
    """Cria MinHash signature de um documento"""
    m = MinHash(num_perm=num_perm)
    # Tokeniza em palavras (ou use n-gramas para mais robustez)
    words = text.lower().split()
    for word in words:
        m.update(word.encode('utf8'))
    return m

# Indexar documentos
docs = {
    "doc1": "A capital da França é Paris",
    "doc2": "Paris é a capital da França",
    "doc3": "Berlin é a capital da Alemanha",
    "doc4": "A França tem Paris como sua capital",
    "doc5": "Machine learning é uma área da inteligência artificial"
}

print("="*60)
print("Deduplicação com MinHash e LSH")
print("="*60)

print("\nIndexando documentos...")
for doc_id, text in docs.items():
    m = get_minhash(text)
    lsh.insert(doc_id, m)
    print(f"  {doc_id}: {text}")

# Buscar near-duplicates de um novo documento
print("\n" + "="*60)
print("Buscando duplicatas...")
print("="*60)

queries = [
    "A França tem Paris como capital",
    "Berlin é capital da Alemanha",
    "Deep learning usa redes neurais"
]

for query_text in queries:
    print(f"\n Query: '{query_text}'")
    query_minhash = get_minhash(query_text)
    duplicates = lsh.query(query_minhash)

    if duplicates:
        print(f"  Duplicatas encontradas: {duplicates}")
        for doc_id in duplicates:
            print(f"    - {doc_id}: {docs[doc_id]}")
    else:
        print("  Nenhuma duplicata encontrada")

print("\n" + "="*60)
print("Estatísticas:")
print("="*60)
print(f"Threshold de similaridade: 80%")
print(f"Número de permutações: 128")
print(f"Total de documentos indexados: {len(docs)}")
print("\n💡 LSH permite buscar duplicatas em O(1) em média!")
