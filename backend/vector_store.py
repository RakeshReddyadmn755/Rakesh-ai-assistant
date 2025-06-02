import os
import chromadb
from chromadb.utils import embedding_functions
from document_loader import load_documents
import openai

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize embedding function with OpenAI
embed_fn = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key=openai.api_key
)

# Initialize Chroma in-memory client
client = chromadb.Client()

# Get or create a persistent collection for Confluence docs
collection = client.get_or_create_collection(
    name="confluence-docs",
    embedding_function=embed_fn
)

def ingest_documents():
    """
    Loads and indexes documents from the /docs directory into the vector DB.
    Skips loading if documents are already present.
    """
    try:
        existing_ids = collection.get()['ids']
        if not existing_ids:
            docs = load_documents()
            if docs:
                for idx, doc in enumerate(docs):
                    collection.add(documents=[doc], ids=[str(idx)])
                print(f"[INFO] Loaded {len(docs)} documents into vector store.")
            else:
                print("[WARN] No documents found. Ensure /docs has valid HTML files.")
    except Exception as e:
        print(f"[ERROR] Failed to ingest documents: {e}")

def search_similar_docs(query: str, top_k: int = 5) -> list[str]:
    """
    Performs semantic search over the vector store using the given query.
    Returns the top_k most similar document chunks.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results["documents"][0] if results and "documents" in results else []
    except Exception as e:
        print(f"[ERROR] Failed to search documents: {e}")
        return []
