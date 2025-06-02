import os
import openai
from vector_store import search_similar_docs

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(query: str) -> str:
    """
    Combines semantic search with GPT-4 to answer a user's question.
    """
    try:
        # Step 1: Semantic search
        context_chunks = search_similar_docs(query)
        context_text = "\n\n".join(context_chunks) if context_chunks else "No relevant documents found."

        # Step 2: Generate answer with GPT-4
        messages = [
            {
                "role": "system",
                "content": "You are a helpful internal SRE assistant. Answer based on the Confluence documentation provided."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion:\n{query}"
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[ERROR] Could not generate answer: {str(e)}"
