# Basic operations for Elastic Search
from ctypes import sizeof
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
    mappings = {
            "properties": {
                "text": {
                    "type": "text"
                }, 
                "vector": {
                    "type": "dense_vector",
                    "dims": 1024,
                    "index": True,
                    "similarity": "cosine"
                },
                #metadata filtering
                "source": {
                    "type": "text"
                },
                "title": {
                    "type": "text"
                },
                "author": {
                    "type": "text"
                },
                "subject": {
                    "type": "text"
                },
                "keywords": {
                    "type": "text"
                },
                "page": {
                    "type": "integer"
                },
                "chapter": {
                    "type": "text"
                },
                "image_path": {
                    "type": "text"
                },
                "image_description": {
                    "type": "text"
                },
                "img_index": {
                    "type": "integer"
                },
                "table_markdown": {
                    "type": "text"
                },
                "table_index": {
                    "type": "integer"
                },
            }
    }
    #创建elastic
    try:
        client.indices.create(index=index_name, mappings=mappings)
        print('[Create Vector DB]' + index_name + ' created')
    except Exception as e:
        print(f'Create Vector DB Exception: {e}')
            

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
        print(f'Writing data to Elastic Search {index_name}')
        print('*'*50)
        print(f'Text: {truncate_text(data["text"], 100)}')
        print(f'Vector: Dimension {len(data["vector"])}')
        print(f'Source: {data["metadata"].get("source")}')
        print(f'Page: {data["metadata"].get("page")}')
        if 'image_path' in data["metadata"]:    
            print(f'Image Path: {data["metadata"].get("image_path")}')
            print(f'Image Description: {truncate_text(data["metadata"].get("image_description"), 100)}')
            print(f'Image Description: {data["metadata"].get("image_description")}')
            print(f'Image Index: {data["metadata"].get("img_index")}')
        if 'table_markdown' in data["metadata"]:
            print(f'Table Markdown: {truncate_text(data["metadata"].get("table_markdown"), 100)}')
            print(f'Table Index: {data["metadata"].get("table_index")}')
        return client.index(index=index_name, body=data)
    except Exception as exc:
        raise exc

def truncate_text(text: str, max_length: int):
    return text[:max_length] + "..." if len(text) > max_length else text