import os
from typing import List
from PyPDF2 import PdfReader

CHUNK_WORDS = 120   # 100–150 word chunks
CHUNK_OVERLAP = 30  # 20–30% overlap

def read_pdf_file(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_txt_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = CHUNK_WORDS, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Breaks text into overlapping chunks of N words each."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_documents_from_folder(folder_path: str, chunk_size: int = CHUNK_WORDS) -> List[str]:
    """Reads .txt and .pdf files and splits them into chunks."""
    all_chunks = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        raw_text = ""

        if filename.endswith(".txt"):
            raw_text = read_txt_file(filepath)

        elif filename.endswith(".pdf"):
            raw_text = read_pdf_file(filepath)

        if raw_text:
            chunks = chunk_text(raw_text, chunk_size=chunk_size)
            all_chunks.extend(chunks)

    return all_chunks
