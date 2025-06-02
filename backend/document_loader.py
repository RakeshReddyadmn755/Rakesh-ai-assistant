import os
from bs4 import BeautifulSoup

# Constants
DOCS_DIR = "docs"
CHUNK_SIZE = 800  # characters per chunk

def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def load_documents():
    chunks = []

    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".html"):
            file_path = os.path.join(DOCS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Extract all visible text
                text = soup.get_text(separator=" ", strip=True)
                # Skip blank pages
                if not text or len(text.strip()) < 50:
                    continue

                # Chunk the extracted text
                text_chunks = chunk_text(text)
                chunks.extend(text_chunks)

    print(f"[INFO] Loaded and chunked {len(chunks)} text blocks from HTML files.")
    return chunks

