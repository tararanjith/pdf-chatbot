import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text_chunks(text_chunks):
    embeddings = model.encode(text_chunks)
    return np.array(embeddings, dtype="float32")

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_faiss_index(index, text_chunks, path="vectorstore/faiss_index.pkl"):
    with open(path, "wb") as f:
        pickle.dump((index, text_chunks), f)

def embed_and_save(text_chunks, path="vectorstore/faiss_index.pkl"):
    embeddings = embed_text_chunks(text_chunks)
    index = build_faiss_index(embeddings)
    save_faiss_index(index, text_chunks, path)
