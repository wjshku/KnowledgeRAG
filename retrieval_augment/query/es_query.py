# Search by keyword and vector
from elastic_search.es_client import ElasticSearchClient
import re

class ESQuery:
    def __init__(self):
        pass

    def keyword_search(self, query: str, es_client: ElasticSearchClient):
        # Search by keyword
        return es_client.submit_query(query, "keyword")

    def vector_search(self, query: str, es_client: ElasticSearchClient):
        # Search by vector (not implemented yet)
        return es_client.submit_query(query, "vector")

    def rrf(self, hits1: list, hits2: list, k: int = 60):
         # RRF is a technique that reranks the results of a query based on the relevance of the documents
        # Combine keyword and vector search results, and rerank the results based on the relevance of the documents
        
        # RRF formula:
        # RRF = (1 / (1 + r1)) * (1 / (1 + r2))
        # where r1 is the rank of the keyword result and r2 is the rank of the vector result
        # RRF is the reciprocal of the sum of the reciprocal of the rank of the keyword and vector results

        # Initialize score dictionary
        scores = {}
        
        # Process keyword hits
        for hit in hits1:
            doc_id = hit['id']
            if doc_id not in scores:
                scores[doc_id] = {'score': 0, 'id': doc_id, 'text': hit['text'], 'metadata':hit['metadata']}
            scores[doc_id]['score'] += 1 / (k + hit['rank'])
        
        # Process vector hits
        for hit in hits2:
            doc_id = hit['id']
            if doc_id not in scores:
                scores[doc_id] = {'score': 0, 'id': doc_id, 'text': hit['text'], 'metadata':hit['metadata']}
            scores[doc_id]['score'] += 1 / (k + hit['rank'])
        
        # Sort documents by their RRF score and assign ranks
        ranked_docs = sorted(scores.values(), key=lambda x: x['score'], reverse=True)

        # Removing the timestamps
        for _, doc in enumerate(ranked_docs):
            timestamp_pattern = re.compile(r'\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}')
            doc['text'] = re.sub(timestamp_pattern, '', doc['text'])    

        # Format the final list of results                  
        final_results = [{'id': doc['id'], 'text': doc['text'], 'metadata':doc['metadata'],'rank': idx + 1} for idx, doc in enumerate(ranked_docs)]
        # print(final_results)
        return final_results

    def search(self, query: str, es_client: ElasticSearchClient):
        # Search by keyword and vector
        print(f'Search for query in database: {query}')
        keyword_hits = self.keyword_search(query, es_client)
        vector_hits = self.vector_search(query, es_client)
        return self.rrf(keyword_hits, vector_hits)



