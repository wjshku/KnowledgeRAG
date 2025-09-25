# Query operations for Elastic Search

from elasticsearch import Elasticsearch

def submit_query(client: Elasticsearch, index_name: str, query: str, query_type: str):
    if query_type == "keyword":
        # [assumed] Simple multi_match over common text fields
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content", "text", "body"],
                    "type": "best_fields"
                }
            }
        }
        return client.search(index=index_name, body=body)
    elif query_type == "vector":
        # [assumed] Expect `query` to be a JSON-encoded list of floats (embedding)
        # If not JSON, try to parse comma-separated floats
        import json
        if isinstance(query, str):
            try:
                vector = json.loads(query)
            except Exception:
                vector = [float(x) for x in query.split(",") if x.strip()]
        else:
            vector = query  # [assumed] already a list

        # [assumed] Use kNN query on field "embedding"
        body = {
            "knn": {
                "field": "embedding",
                "query_vector": vector,
                "k": 10,
                "num_candidates": 100
            }
        }
        return client.search(index=index_name, body=body)
    else:
        raise ValueError(f"Invalid query type: {query_type}")