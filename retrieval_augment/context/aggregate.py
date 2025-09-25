# Aggregate results after reranking

class Aggregate:
    def __init__(self):
        pass

    def aggregate(self, query: str, hits: list):
        # Aggregate the retrieved results after reranking. Create a new context for the query
        # Create the documents text with newlines
        documents_text = '\n'.join([hit['text'] + ' (Source: ' + hit['metadata']['source'] + ')' for hit in hits])
        
        prompt = f"""
        You are a helpful assistant to answer question
        The query is: {query}
        The most relevant documents are:
        {documents_text}
        Please answer the query based on the information retrieved and provide reference to the source documents.
        Very important: Always provide source information in the answer.
        """
        return prompt