# Client for Answer Generation with OpenAI
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class OpenAIClient:
    def __init__(self):
        # Auth with OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, query: str, context: str):
        # Chat with the client
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
                {"role": "assistant", "content": context},
            ]
        )
        return response.choices[0].message.content