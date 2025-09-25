# Search by keyword and vector
from elastic_search.es_client import ElasticsearchClient

class ESQuery:
    def __init__(self):
        pass

    def keyword_search(self, query: str, es_client: ElasticsearchClient):
        # Search by keyword
        pass

    def vector_search(self, query: str, es_client: ElasticsearchClient):
        # Search by vector
        pass

    def rrf(self, hits1: list, hits2: list, k: int = 60):
         # RRF is a technique that reranks the results of a query based on the relevance of the documents
        # Combine keyword and vector search results, and rerank the results based on the relevance of the documents
        
        # RRF formula:
        # RRF = (1 / (1 + r1)) * (1 / (1 + r2))
        # where r1 is the rank of the keyword result and r2 is the rank of the vector result
        # RRF is the reciprocal of the sum of the reciprocal of the rank of the keyword and vector results
        pass

    def search(self, query: str, es_client: ElasticsearchClient):
        # Search by keyword and vector
        keyword_hits = self.keyword_search(query, es_client)
        vector_hits = self.vector_search(query, es_client)
        return self.rrf(keyword_hits, vector_hits)



