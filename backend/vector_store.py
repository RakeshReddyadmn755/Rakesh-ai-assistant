import chromadb
from chromadb.config import Settings
from chromadb.api.types import EmbeddingFunction
from document_loader import load_documents
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Embedding function with correct parameter name
class OpenAIEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: list[str]) -> list[list[float]]:
        response = openai.Embedding.create(
            model="text-embedding-3-small",
            input=input
        )
        return [d["embedding"] for d in response["data"]]

# ✅ Instantiate Chroma client
client = chromadb.Client(Settings(anonymized_telemetry=False))
embed_fn = OpenAIEmbeddingFunction()

# ✅ Get or create collection
collection = client.get_or_create_collection(
    name="confluence-docs",
    embedding_function=embed_fn
)

# ✅ Load docs if not already present
def ingest_documents():
    existing_ids = collection.get()['ids']
    if not existing_ids:
        docs = load_documents()
        if docs:
            for idx, doc in enumerate(docs):
                collection.add(documents=[doc], ids=[str(idx)])
            print(f"[INFO] Loaded {len(docs)} documents into vector DB.")
        else:
            print("[WARN] No documents loaded. Check /docs folder.")

# ✅ Vector similarity search
def search_similar_docs(query: str, top_k: int = 5) -> list[str]:
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        print(f"[ERROR] Failed to search documents: {e}")
        return []
