import os
from openai import OpenAI

# Initialize the OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(question: str) -> str:
    """
    Sends a prompt to the OpenAI chat completion API and returns the response.

    Args:
        question (str): The user question.

    Returns:
        str: The assistant's reply or error message.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Site Reliability Engineering (SRE) assistant that answers questions based on internal Confluence documentation and best practices."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] Could not generate answer: {e}"
