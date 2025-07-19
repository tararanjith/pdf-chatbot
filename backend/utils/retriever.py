import numpy as np
import faiss

def retrieve_answer(query, chunks, embeddings, embedder, k=3):
    # Build a FAISS index from the passed embeddings
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Embed the user query using the provided embedder model
    query_embedding = embedder.encode([query]).astype("float32")

    # Search top-k nearest neighbors in the index
    distances, indices = index.search(query_embedding, k)

    # Collect matched text chunks by index
    matched_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    return matched_chunks
