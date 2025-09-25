# Test Information Processor

from information.processor import InformationProcessor

# Text Processor
from information.module.text import TextProcessor
info_path = "data/pdf/刑事诉讼法.pdf"
text_processor = TextProcessor()
print(text_processor.process(info_path)[:1])

# Image Processor
from information.module.image import ImageProcessor
info_path = "data/pdf/image_extraction_example.pdf"
image_processor = ImageProcessor()
print(image_processor.process(info_path)[:1])

# Table Processor
from information.module.table import TableProcessor
info_path = "data/pdf/table_extraction_example.pdf"
table_processor = TableProcessor()
print(table_processor.process(info_path)[:1])

# PDF Processor
from information.source.pdf import PDFProcessor
info_paths = ["data/pdf/table_extraction_example.pdf", 
            "data/pdf/image_extraction_example.pdf", 
            "data/pdf/刑事诉讼法.pdf"]
pdf_processor = PDFProcessor()
pdf_processor.process(info_paths)

# Get info chunks count
info_chunks_count = pdf_processor.get_info_chunks_count()
print(info_chunks_count)

# Get info chunks
for info_type, info_chunk in pdf_processor.get_info_chunks():
    print("-"*20, info_type, "-"*20)
    if info_type == "text":
        print(info_chunk["content"][:100])
        print('page:',info_chunk["metadata"]['page'])
    elif info_type == "image":
        print(info_chunk["content"][:100])
        print('page:',info_chunk["metadata"]['page'])
        print('image_path:',info_chunk["metadata"]['image_path'])
    elif info_type == "table":
        print(info_chunk["content"][:100])
        print('page:',info_chunk["metadata"]['page'])
        print('table_markdown:',info_chunk["metadata"]['table_markdown'][:100])

# Test Information Processor

info_client = InformationProcessor()
info_paths = [
            "data/pdf/table_extraction_example.pdf", 
            "data/pdf/image_extraction_example.pdf", 
            "data/pdf/刑事诉讼法.pdf"
            ]
info_type = info_client.which_info_type(info_paths[0])
print('info_type:', info_type)
info_client.load_info(info_paths)
info_client.process_info()

# Test Text Embedder
from elastic_search.es_client import ElasticSearchClient
from information.embedder import TextEmbedder
text_embedder = TextEmbedder()

import os

# Connect to Elastic Search
elasticurl = os.getenv("ELASTIC_URL")
username = os.getenv("ELASTIC_USERNAME")
password = os.getenv("ELASTIC_PASSWORD")
es_client = ElasticSearchClient(elasticurl, username, password, "book_index")


# Embedding by batch and index to Elastic Search
for batch in info_client.get_info_chunks_by_batch(batch_size=100):
    embeddings = text_embedder.embed([info_chunk['content'] for name, info_chunk in batch])
    for j, (name, info_chunk) in enumerate(batch):
        body = {
            'text': info_chunk['content'],
            'vector': embeddings[j],
            'metadata': info_chunk['metadata'],
        }
        es_client.write_data("book_index", body)
print('Saved to Elastic Search:', es_client.list_indices())
