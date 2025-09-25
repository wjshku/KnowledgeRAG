# Chat for Answer Generation with OpenAI, With a chat history
from utils.client import OpenAIClient

class Chat:
    def __init__(self):
        self.client = OpenAIClient()
        self.chat_history = []

    def get_chat_history(self) -> str:
        # Get the chat history from client
        return '\n'.join([f"{item['role']}: {item['content']}" for item in self.chat_history])

    def chat(self, query: str):
        # Create a chatbot with the client
        response = self.client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能助手，用户已提供关于问题的信息，请根据这些信息回答用户问题。并提供信息来源。"},
                # Add the chat history
                *self.chat_history,
                {"role": "user", "content": query},
            ]
        )

        self.chat_history.append({"role": "user", "content": query})
        self.chat_history.append({"role": "assistant", "content": response})

        print(f'Chat History Length: {len(self.chat_history)}')
        
        return response