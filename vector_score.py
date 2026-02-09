import faiss
import numpy as np

index = faiss.IndexFlatIP(512)
items = []

def normalize(v):
    return v / np.linalg.norm(v)

def add_item(embedding, metadata):
    embedding = normalize(embedding)
    index.add(embedding)
    items.append(metadata)

def search(query_embedding, k=5):
    query_embedding = normalize(query_embedding)
    D, I = index.search(query_embedding, k)
    return [(items[i], float(D[0][j])) for j, i in enumerate(I[0])]
