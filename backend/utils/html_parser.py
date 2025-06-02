import os
from bs4 import BeautifulSoup

def extract_chunks_from_docs(doc_folder="./docs"):
    all_chunks = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".html"):
            with open(os.path.join(doc_folder, filename), "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                all_chunks.extend(chunks)
    return all_chunks

