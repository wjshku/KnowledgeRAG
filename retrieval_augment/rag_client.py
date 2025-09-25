# RAG Client for Retrieval Augmentation

from elastic_search.basic import truncate_text
from retrieval_augment.rewrite.coref_resolve import CoreferenceResolution
from retrieval_augment.rewrite.decomp import QueryDecomposition
from retrieval_augment.rewrite.fusion import QueryFusion
from retrieval_augment.query.es_query import ESQuery
from retrieval_augment.query.web_query import WebQuery
from retrieval_augment.rerank.neural import NeuralReranker
from retrieval_augment.context.aggregate import Aggregate
from retrieval_augment.answer.chat import Chat
from elastic_search.es_client import ElasticSearchClient
import logging

class RAGClient:
    def __init__(self, es_client: ElasticSearchClient):
        self.coreference_resolution = CoreferenceResolution()
        self.query_decomposition = QueryDecomposition()
        self.query_fusion = QueryFusion()
        self.es_query = ESQuery()
        self.web_query = WebQuery()
        self.neural_reranker = NeuralReranker()
        self.aggregate = Aggregate()
        self.es_client = es_client
        self.chat = Chat()
        
    def rewrite(self, query: str, chat_history: str = None) -> str:
        # Rewrite the query: Coreference Resolution -> Fusion -> Decomposition
        if chat_history is None:
            chat_history = self.chat.get_chat_history()
        print(f'Chat History: {truncate_text(chat_history, 100)}')
        query = self.coreference_resolution.coreference_resolution(query, chat_history)
        print(f'Coreference Resolution: {query}')
        rag_fusion = self.query_fusion.fuse(query)
        logging.info(f'Query Fusion: {rag_fusion}')
        queries = []
        for q in rag_fusion:
            qs = self.query_decomposition.decompose(q)
            queries.extend(qs)
            logging.info(f'Query Decomposition: {q} -> {qs}')
        return queries

    def query(self, query: str) -> list:
        # Query the ES and Web
        es_query = self.es_query.search(query, self.es_client)
        web_query = self.web_query.query(query)
        return es_query + web_query
    
    def rerank(self, query: str, hits: list) -> list:
        # Rerank the hits
        return self.neural_reranker.rerank(query,hits)
    
    def context_augment(self, query: str) -> str:
        # Aggregate queries and hits
        print(f'Original Query: {query}')
        rewritten_queries = self.rewrite(query)
        print(f'Rewritten Queries: {rewritten_queries}')
        aggregated_hits = []
        for rewritten_query in rewritten_queries:
            hits = self.query(rewritten_query)
            hits = self.rerank(rewritten_query, hits)
            logging.info(f'Reranked Hits: {hits[:3]}')
            aggregated_hits.extend(hits[:3])
        return self.aggregate.aggregate(query, aggregated_hits[:5])
    
    def answer(self, query: str) -> str:
        # Context Augment
        context_augment = self.context_augment(query)
        print(f'Context Augmented: {context_augment}')
        # Answer the query
        return self.chat.chat(query)

    def rag_chat(self):
        query = ""
        # Input from command line
        while query != "exit":
            query = input("User: ")
            if query == "exit":
                break
            print('RAG Assistant: ', self.answer(query))