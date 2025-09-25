# Aggregate results after reranking

class Aggregate:
    def __init__(self):
        pass

    def aggregate(self, query: str, hits: list):
        # Aggregate the retrieved results after reranking. Create a new context for the query
        prompt = f"""
        You are a helpful assistant to answer the query based on the information retrieved and provide reference to the source documents.
        The query is: {query}
        The most relevant documents are:
        {'\n'.join([hit['text'] + ' (Source: ' + hit['source'] + ')' for hit in hits])}
        Please answer the query based on the information retrieved and provide reference to the source documents.
        """
        return prompt