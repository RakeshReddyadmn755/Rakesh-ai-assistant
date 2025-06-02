from vector_store import get_collection
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(question):
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])

    prompt = f"""You are a helpful assistant. Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
