from vector_store import get_collection
import openai
import os

# Set your OpenAI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(question):
    try:
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set.")

        # Retrieve vector collection
        collection = get_collection()
        results = collection.query(query_texts=[question], n_results=3)

        # Build context from top results
        context = "\n".join(results['documents'][0]) if results and results.get('documents') else "No context found."

        prompt = f"""
        You are a helpful AI assistant for SRE documentation. Answer the question below using the provided context.

        Context:
        {context}

        Question:
        {question}
        """

        # Call OpenAI's GPT model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
