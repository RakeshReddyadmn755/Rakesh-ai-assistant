from bs4 import BeautifulSoup
import os

def html_to_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()

def load_documents(directory='docs'):
    docs = []
    for file in os.listdir(directory):
        if file.endswith('.html'):
            text = html_to_text(os.path.join(directory, file))
            docs.append(text)
    return docs
