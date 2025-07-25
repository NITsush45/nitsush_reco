import json
import faiss
import numpy as np
from backend.embeddings import get_embedding
from backend.utils import load_json_file

DATA_PATHS = {
    "movies": "backend/data/movies.json",
    "stories": "backend/data/stories.json",
    "youtube": "backend/data/youtube.json",
    "ecommerce": "backend/data/ecommerce.json",
}

def load_data(domain):
    if domain not in DATA_PATHS:
        raise ValueError(f"Invalid domain: {domain}")
    data = load_json_file(DATA_PATHS[domain])
    if not data:
        raise ValueError(f"No data found for domain '{domain}'")
    return data

def build_index(domain, model):
    data = load_data(domain)
    
    # Ensure 'description' key exists
    vectors = []
    filtered_data = []
    for item in data:
        if "description" in item:
            emb = get_embedding(item["description"], model)
            vectors.append(emb)
            filtered_data.append(item)

    if not vectors:
        raise ValueError(f"No valid items with 'description' in domain '{domain}'")

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))
    return index, filtered_data

def search_similar_items(query, domain, model, k=5):
    index, data = build_index(domain, model)
    query_vec = get_embedding(query, model)
    D, I = index.search(np.array([query_vec]).astype("float32"), k)
    return [data[i] for i in I[0]]
