# Test Elastic Search Client
import warnings
from elasticsearch import ElasticsearchWarning
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

from elastic_search.es_client import ElasticSearchClient
import os

# Connect to Elastic Search
elasticurl = os.getenv("ELASTIC_URL")
username = os.getenv("ELASTIC_USERNAME")
password = os.getenv("ELASTIC_PASSWORD")
es_client = ElasticSearchClient(elasticurl, username, password, "book_index")

# List indices, Create index, Delete index
print(es_client.list_indices())
es_client.create_index("book_index")
print(es_client.list_indices())
es_client.delete_index("book_index")
print(es_client.list_indices())

# Test Elastic Search Query
query = "刑事诉讼法"
hits = es_client.submit_query(query, "keyword")

print("=== Initial Retrieval Results ===")
for idx, doc in enumerate(hits, 1):
    print(f"Len ({len(doc['text'])})   Text: {doc['text'][:100]}{'...' if len(doc['text']) > 100 else ''}")
