import os
from openai import OpenAI

# Only set API key through environment variable or default config
client = OpenAI()

def ask_openai(question: str) -> str:
    """
    Sends a question to the OpenAI API and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert SRE assistant that answers questions from internal Confluence documentation."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] Could not generate answer: {e}"
