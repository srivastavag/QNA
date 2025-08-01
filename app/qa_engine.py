import os
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from app.utils import load_documents_from_folder

DOCS_FOLDER = "docs"
CHUNK_WORDS = 120   # 100–150 word chunks
CHUNK_OVERLAP = 30  # 20–30% overlap
TOP_K = 10
SIMILARITY_THRESHOLD = 1.0
L2_THRESHOLD = 1.2
RELEVANCE_RATIO = 0.85
MAX_CONTEXT_CHUNKS = 5

# Load & embed
DOCUMENTS = load_documents_from_folder(DOCS_FOLDER)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
doc_embeddings = model.encode(DOCUMENTS, convert_to_numpy=True, normalize_embeddings=True)

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
faiss.normalize_L2(doc_embeddings)
index.add(np.array(doc_embeddings))

def call_local_llm(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    data = response.json()
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"].strip()
    elif "response" in data:
        return data["response"].strip()
    return "Error: LLM response invalid."

def answer_question(question: str, threshold: float = SIMILARITY_THRESHOLD, top_k: int = TOP_K) -> str:
    q_embedding = model.encode([question], normalize_embeddings=True)[0]
    D, I = index.search(np.array([q_embedding]), k=top_k)

    best_score = D[0][0]
    filtered_chunks, filtered_scores = [], []

    for idx, score in zip(I[0], D[0]):
        if 0 <= score < 1000 and score >= best_score * RELEVANCE_RATIO:
            filtered_chunks.append(DOCUMENTS[idx])
            filtered_scores.append(score)
			
    if not filtered_chunks or all(score > L2_THRESHOLD for score in filtered_scores):
        return "I don't know based on the provided information."

    context = "\n\n".join(filtered_chunks[:MAX_CONTEXT_CHUNKS])

    prompt = f"""
You are a helpful assistant.

Use only the information provided in the <context> below to answer the question. You may paraphrase and briefly explain your answer, but do not add information that is not in the document.

<context>
{context}
</context>

Question:
{question}

Instructions:
- If the document provides a clear answer, give the answer along with a brief explanation based on the context.
- If the question contradicts the document, say "No," and correct the misinformation using the document.
- If the document does not contain enough information to answer, respond only with:
"I don't know based on the provided information."

Do not guess or provide extra details beyond the context.

Answer:
"""
    return call_local_llm(prompt)
