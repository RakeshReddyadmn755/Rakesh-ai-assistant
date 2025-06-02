import os
from openai import OpenAI

# Initialize the OpenAI client using the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(question: str) -> str:
    """
    Sends a question to the OpenAI API and returns the response.

    Args:
        question (str): The user input question.

    Returns:
        str: The AI-generated response or an error message.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert SRE assistant that answers questions from internal Confluence documentation."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].messa
