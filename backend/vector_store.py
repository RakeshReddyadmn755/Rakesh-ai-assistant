import chromadb
from chromadb.utils import embedding_functions
from document_loader import load_documents
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_collection():
    # Define embedding function
    embed_fn = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key=openai.api_key
    )

    # Use Chroma's in-memory default client
    client = chromadb.Client()  # No arguments, no proxies

    # Create or get collection
    collection = client.get_or_create_collection("confluence-docs", embedding_function=embed_fn)

    # Load docs if collection is empty
    if len(collection.get()['ids']) == 0:
        docs = load_documents()
        for idx, doc in enumerate(docs):
            collection.add(documents=[doc], ids=[str(idx)])

    return collection
