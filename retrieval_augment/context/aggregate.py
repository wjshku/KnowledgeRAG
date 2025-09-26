# Aggregate results after reranking

class Aggregate:
    def __init__(self):
        pass

    def aggregate(self, query: str, hits: list):
        # Aggregate the retrieved results after reranking. Create a new context for the query
        # Create the documents text with newlines
        documents_text = '\n'.join([hit['text'] + ' (Source: ' + hit['metadata']['source'] + 'Page: ' + str(hit['metadata']['page']) + ')' for hit in hits])
        
        prompt = f"""
        You are an AI assistant. Answer the query strictly based on the information provided below. 
        Do NOT use any outside knowledge.

        The query is: {query}

        The most relevant documents are:
        {documents_text}

        Instructions:
        1. Answer the query only using the content above.
        2. When you use information from a document, add an inline reference like [1], [2], etc. right after the sentence.
        3. At the end of your answer, provide a "References" section that lists each reference number and the corresponding source document and the text.
        4. If the answer cannot be found in the provided text, respond with: "The information is not available in the provided context."
        """
        return prompt