# Client for Answer Generation with OpenAI
from openai import OpenAI
import os
import re
from dotenv import load_dotenv
load_dotenv()

USE_MOCK_FALLBACK = os.getenv("USE_MOCK_FALLBACK", "false").lower() == "true"

def strip_think_blocks(s: str) -> str:
    # Remove <think>...</think> including newlines inside
    s = re.sub(r"<think>.*?</think>", "", s, flags=re.DOTALL)
    return s.strip()

class OpenAIClient:
    def __init__(self, 
                model: str = os.getenv("OPENAI_MODEL"), 
                api_key: str = os.getenv("OPENAI_API_KEY"), 
                base_url: str = os.getenv("OPENAI_BASE_URL")):
        # Auth with OpenAI
        print(f'Model: {model}')
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def chat(self, messages: list, **kwargs):
        if USE_MOCK_FALLBACK:
            return messages[-1]['content']
        else:
            # Chat with the client
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return strip_think_blocks(response.choices[0].message.content)