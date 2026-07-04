from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from api.database import get_incidents

model = SentenceTransformer('/home/uzair/models/all-MiniLM-L6-v2')
def embed_text(text: str):
    embedding = model.encode(text)
    return embedding

def build_index():
    incidents = get_incidents()
    if not incidents:
        return None

    embeddings = [embed_text(incident['diagnosis']) for incident in incidents]
    embeddings_array = np.array(embeddings).astype('float32')
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)
    return index, incidents

def retrieve_similar(query_text: str, index, incidents, k=3):
    query_embedding = embed_text(query_text).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    similar_incidents = [incidents[i] for i in indices[0]]
    return similar_incidents
