from elasticsearch import Elasticsearch
from .basic import index_exists, create_index, delete_index, write_data, list_indices
from .query import submit_query

class ElasticSearchClient:
    def __init__(self, elasticurl: str, username: str, password: str, index_name: str):
        self.client = Elasticsearch([elasticurl],
                            basic_auth=(username, password))
        self.index_name = index_name

    def list_indices(self):
        return list_indices(self.client)

    def index_exists(self, index_name: str):
        return index_exists(self.client, index_name)

    def create_index(self, index_name: str):
        return create_index(self.client, index_name)

    def delete_index(self, index_name: str):
        return delete_index(self.client, index_name)

    def write_data(self, index_name: str, data: dict):
        return write_data(self.client, index_name, data)

    def submit_query(self, query: str, query_type: str, index_name: str = None):
        if index_name is None:
            index_name = self.index_name
        return submit_query(self.client, index_name, query, query_type)