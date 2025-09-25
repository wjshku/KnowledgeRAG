# Query operations for Elastic Search

from elasticsearch import Elasticsearch
from utils.embedding import get_embedding
from utils.text import get_keyword

def submit_query(client: Elasticsearch, index_name: str, query: str, query_type: str):
    if query_type == "keyword":
        # [assumed] Simple multi_match over common text fields
        keywords = get_keyword(query)
        keyword_query = {
            "bool": {
                "should": [
                    {"match": {"text": {"query": keyword, "fuzziness": "AUTO"}}} for keyword in keywords
                ],
                "minimum_should_match": 1
            }
        }
        
        result = client.search(index=index_name, query=keyword_query)
        
    elif query_type == "vector":
        embedding = get_embedding([query])
        vector_query = {
            "bool": {
                "must": [{"match_all": {}}],
                "should": [
                    {"script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.queryVector, 'vector') + 1.0",
                            "params": {"queryVector": embedding[0]}
                        }
                    }}
                ]
            }
        }
        result = client.search(index=index_name, query=vector_query)

    else:
        raise ValueError(f"Invalid query type: {query_type}")
    
    hits = [{
            'id': hit['_id'], 'text': hit['_source'].get('text'), 
            'metadata':hit['_source'].get('metadata'),
            'rank': idx + 1} 
            for idx, hit in enumerate(result['hits']['hits'])]
    
    return hits