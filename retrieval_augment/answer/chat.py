# Chat for Answer Generation with OpenAI, With a chat history
from client import OpenAIClient

class Chat:
    def __init__(self):
        self.client = OpenAIClient()

    def chat(self, query: str, context: str, chat_history: list):
        # Chat with the client
        return self.client.chat(query, context, chat_history)