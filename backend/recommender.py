from backend.embeddings import get_embedding_model
from backend.vector_db import search_similar_items
from backend.llm import generate_response

def get_recommendations(query, domain):
    embed_model = get_embedding_model()
    similar_items = search_similar_items(query, domain, embed_model)
    response = generate_response(query, similar_items, domain)
    return {"recommendations": response}
