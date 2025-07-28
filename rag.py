import faiss
import pickle
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

# Retrieval Augmented Generation

# === Setup ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"
encoder = tiktoken.encoding_for_model("gpt-4")

# === Load FAISS index and chunks ===
index = faiss.read_index("course_index.faiss")

with open("chunks.pkl", "rb") as f:
    mapping = pickle.load(f)

chunks = mapping["chunks"]
sources = mapping["sources"]

# === Embed and search ===
def get_relevant_chunks(query, top_k=5):
    res = client.embeddings.create(
        input=[query],
        model=EMBEDDING_MODEL
    )
    query_vector = np.array (res.data[0].embedding).astype("float32").reshape(1, -1)

    D, I = index.search(query_vector, top_k)
    results = [chunks[i] for i in I[0]]
    return results
