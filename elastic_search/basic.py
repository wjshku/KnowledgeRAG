# Basic operations for Elastic Search
from elasticsearch import Elasticsearch

def list_indices(client: Elasticsearch):
    try:
        # Get all indices
        indices = client.indices.get_alias().keys()
        # Filter out system indices that start with . and known internal indices
        filtered_indices = [
            idx for idx in indices 
            if not idx.startswith('.') 
            and not idx.startswith('kibana')
            and not idx.startswith('elastic')
        ]
        return filtered_indices
    except Exception as exc:
        raise

def index_exists(client: Elasticsearch, index_name: str):
    try:
        # [assumed] Use indices.exists API
        return client.indices.exists(index=index_name)
    except Exception as exc:
        raise

def create_index(client: Elasticsearch, index_name: str):
    try:
        if not index_exists(client, index_name):
            # [assumed] Create with default settings/mappings
            return client.indices.create(index=index_name)
        return {"acknowledged": True, "index": index_name, "message": "already_exists"}
    except Exception as exc:
        raise

def delete_index(client: Elasticsearch, index_name: str):
    try:
        if index_exists(client, index_name):
            return client.indices.delete(index=index_name)
        return {"acknowledged": True, "index": index_name, "message": "not_found"}
    except Exception as exc:
        raise

def write_data(client: Elasticsearch, index_name: str, data: dict):
    try:
        if not index_exists(client, index_name):
            create_index(client, index_name)
        # [assumed] Let ES auto-generate _id
        return client.index(index=index_name, document=data)
    except Exception as exc:
        raise