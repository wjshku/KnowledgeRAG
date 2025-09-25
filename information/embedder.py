# Embedder for Text

from utils.embedding import get_embedding

class TextEmbedder:
    def __init__(self):
        self.embedder = get_embedding

    def embed(self, texts: list[str]) -> list[float]:
        return self.embedder(texts)