# Test RAG
import warnings
from elasticsearch import ElasticsearchWarning
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

import os
from dotenv import load_dotenv
load_dotenv(".env.development")

from elastic_search.es_client import ElasticSearchClient
from information.processor import InformationProcessor
from utils.text import display_hits


# Connect to Elastic Search
elasticurl = os.getenv("ELASTIC_URL")
username = os.getenv("ELASTIC_USERNAME")
password = os.getenv("ELASTIC_PASSWORD")
es_client = ElasticSearchClient(elasticurl, username, password, "book_index")

def test_elastic():
    es_client.delete_index("book_index")
    print(es_client.list_indices())
    es_client.create_index("book_index")
    print(es_client.list_indices())

def test_processor():
    info_client = InformationProcessor()
    info_paths = [
                # "data/pdf/table_extraction_example.pdf", 
                # "data/pdf/image_extraction_example.pdf", 
                # "data/pdf/刑事诉讼法.pdf",
                "data/pdf/In The Plex (Google).pdf"
                ]
    info_type = info_client.which_info_type(info_paths[0])
    print('info_type:', info_type)
    info_client.load_info(info_paths)
    info_client.process_info()

    # Test Text Embedder
    from elastic_search.es_client import ElasticSearchClient
    from information.embedder import TextEmbedder
    text_embedder = TextEmbedder()

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

def test_search(query = "Image of Moses, Michelangelo"):
    # hits = es_client.submit_query(query, "keyword")
    # display_hits(hits)
    hits = es_client.submit_query(query, "vector")
    display_hits(hits)

def test_image_processor():
    from information.module.image import ImageProcessor
    info_path = "data/pdf/image_extraction_example.pdf"
    image_processor = ImageProcessor()
    _ = image_processor.process(info_path)

def test_table_processor():
    from information.module.table import TableProcessor
    info_path = "data/pdf/table_extraction_example.pdf"
    table_processor = TableProcessor()
    _ = table_processor.process(info_path)

def test_rag_rewrite():
    from retrieval_augment.rag_client import RAGClient
    query = "米开朗琪罗和对话系统"
    rag_client = RAGClient(es_client)
    print(rag_client.rewrite(query, ""))

def test_rag_query():
    # Test RAG Search
    from retrieval_augment.rag_client import RAGClient
    query = "米开朗琪罗和对话系统"
    rag_client = RAGClient(es_client)

    # Test RAG Query
    hits = rag_client.query(query)
    display_hits(hits[:3])

    # Test RAG Rerank
    hits = rag_client.rerank(query, hits)
    display_hits(hits[:3])

def test_rag_context_augment():
    from retrieval_augment.rag_client import RAGClient
    query = "米开朗琪罗和对话系统"
    rag_client = RAGClient(es_client)
    print(rag_client.context_augment(query))

def test_rag_answer():
    from retrieval_augment.rag_client import RAGClient
    query = "米开朗琪罗和对话系统"
    rag_client = RAGClient(es_client)
    print(rag_client.answer(query))

def test_chat():
    from retrieval_augment.answer.chat import Chat
    chat = Chat()
    _ = (chat.chat("米开朗琪罗和对话系统"))
    print(chat.get_chat_history())

def test_rag_chat():
    from retrieval_augment.rag_client import RAGClient
    rag_client = RAGClient(es_client)
    rag_client.rag_chat()

def main():
    # test_elastic() # Restart the index (Need to start docker first)
    # test_image_processor() # Test image processor
    # test_table_processor() # Test table processor
    # test_processor() # Test processor and write to Elastic Search
    # test_search('Table of stock performance in 2024') # Test vector search
    # test_rag_rewrite() # Test RAG (Rewrite)
    # test_rag_query() # Test RAG (Query, Rerank)
    # test_rag_context_augment() # Test RAG (Context Augment)
    # test_rag_answer() # Test RAG ChatBot (with memory)
    # test_chat() # Test ChatBot (with memory)
    test_rag_chat() # Test RAG ChatBot (with memory)

if __name__ == "__main__":
    main()