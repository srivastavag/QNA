# 🧠 Document-Based Q&A System (FastAPI + FAISS + LLaMA3)

This is a lightweight, retrieval-augmented question-answering (RAG) application that answers user questions based **only on the information present in uploaded documents** (PDF or text).

Built with:
- 🧪 FastAPI (backend server)
- 🔍 SentenceTransformer embeddings + FAISS for semantic search
- 🦙 LLaMA3 (via Ollama) for natural language reasoning and answers
- 📄 Document ingestion with paragraph chunking
- ☁️ Ready for Render.com deployment

---

## 🚀 Features

- **Strict fact-based answering**: No hallucinations
- **Chunk-based document search** using sentence embeddings
- **PDF and TXT document support**
- **Handles multiple documents and topics**
- **Switchable LLM backend** (local llama3 or cloud APIs)

---

## 📁 Folder Structure

├── app/
│ ├── main.py # FastAPI app
│ ├── qa_engine.py # Embedding, chunking, LLM prompt logic
│ └── utils.py # PDF/TXT reading, chunking
├── docs/ # Folder for your document files
├── requirements.txt
├── render.yaml # Render deployment config
└── README.md