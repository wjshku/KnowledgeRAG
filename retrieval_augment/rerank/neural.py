# Neural Reranker

import os
import requests
from dotenv import load_dotenv
load_dotenv()
RERANK_URL = os.getenv("RERANK_URL")

class NeuralReranker:
    def __init__(self):
        pass

    def rerank(self, query: str, hits: list):
        # Neural Reranker is a technique that reranks the results of a query 
        # based on the relevance of the documents
        res = requests.post(RERANK_URL, json={"query": query, "documents": [doc['text'] for doc in hits]}).json()
        if res and 'scores' in res and len(res['scores']) == len(hits):
            for idx, doc in enumerate(hits):
                hits[idx]['score'] = res['scores'][idx]
            
            # Sort documents by rerank score in descending order (highest scores first)
            hits.sort(key=lambda x: x['score'], reverse=True)
                
        return hits