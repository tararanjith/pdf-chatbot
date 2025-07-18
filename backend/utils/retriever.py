import os
import pickle
import numpy as np
import faiss

VECTORSTORE_PATH = "vectorstore/faiss_index.pkl"

def load_faiss_index(path=VECTORSTORE_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError("FAISS index and chunks file(s) not found. Please upload and embed a PDF first.")
    with open(path, "rb") as f:
        index, text_chunks = pickle.load(f)
    return index, text_chunks

def retrieve_answer(query, embedder, k=3):
    # Load the FAISS index and chunks
    index, text_chunks = load_faiss_index()

    # Embed the user query
    query_embedding = embedder.encode([query]).astype("float32")

    # Perform similarity search
    distances, indices = index.search(query_embedding, k)

    # Gather top-k matched text chunks
    matched_chunks = [text_chunks[i] for i in indices[0] if i < len(text_chunks)]

    return {"context": "\n\n".join(matched_chunks)}
