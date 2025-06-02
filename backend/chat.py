from vector_store import get_collection
import openai
import os

# Load API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(question):
    try:
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set.")

        # Get relevant docs using embeddings
        collection = get_collection()
        results = collection.query(query_texts=[question], n_results=3)

        # Handle empty or missing results
        if not results or not results.get('documents'):
            context = "No relevant documents found."
        else:
            context = "\n".join(results['documents'][0])

        # Construct the prompt for GPT
        prompt = f"""
        You are a helpful AI assistant for SRE Confluence documentation.
        Use the following context to answer the question.

        Context:
        {context}

        Question:
        {question}
        """

        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERROR] Failed to generate response: {e}")
        return f"[ERROR] Could not generate answer: {str(e)}"
