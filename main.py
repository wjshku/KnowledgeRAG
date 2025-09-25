# Test RAG
import os
from dotenv import load_dotenv
load_dotenv(".env.development")

import warnings
from elasticsearch import ElasticsearchWarning
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

# Test Elastic Search Client

# from elastic_search.es_client import ElasticSearchClient

# elasticurl = os.getenv("ELASTIC_URL")
# username = os.getenv("ELASTIC_USERNAME")
# password = os.getenv("ELASTIC_PASSWORD")
# es_client = ElasticSearchClient(elasticurl, username, password)

# print(es_client.list_indices())
# es_client.create_index("book_index")
# print(es_client.list_indices())
# es_client.delete_index("book_index")
# print(es_client.list_indices())

# Test Information Processor

from information.processor import InformationProcessor

# from information.module.text import TextProcessor
# info_path = "data/pdf/刑事诉讼法.pdf"
# text_processor = TextProcessor()
# print(text_processor.process(info_path)[:1])

# from information.module.image import ImageProcessor
# info_path = "data/pdf/image_extraction_example.pdf"
# image_processor = ImageProcessor()
# print(image_processor.process(info_path)[:1])

from information.module.table import TableProcessor
info_path = "data/pdf/table_extraction_example.pdf"
table_processor = TableProcessor()
print(table_processor.process(info_path)[:1])


# from information.source.pdf import PDFProcessor
# pdf_processor = PDFProcessor()
# print(pdf_processor.process([info_path])[:1])

# info_client = InformationProcessor()
# info_type = info_client.which_info_type(info_path)
# print('info_type:', info_type)
# info_client.load_info([info_path])
# info_client.process_info()
# print(info_client.get_info_chunks()[:10])