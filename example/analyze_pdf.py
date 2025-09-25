# Example to analyze pdf file with RAG: index text, image, table
from retrieval_augment.rag_client import RAGClient
from elastic_search.es_client import ElasticSearchClient
from information.processor import InformationProcessor
import os
from dotenv import load_dotenv
load_dotenv()

def analyze_pdf(pdf_path: str):
    # Create Elastic Search Client
    username = os.getenv("ELASTIC_USERNAME")
    password = os.getenv("ELASTIC_PASSWORD")
    es_client = ElasticSearchClient(host="localhost", port=9200, username=username, password=password)

    # Create Elastic Search Index
    index_name = "book_index"
    if not es_client.index_exists(index_name):
        es_client.create_index(index_name)

    # Create Information Processing Client
    info_client = InformationProcessor()

    # Create RAG Client
    rag_client = RAGClient()
    
    # Load PDF File
    info_client.load_pdf(pdf_path)

    # Process PDF File
    info_client.process_pdf()

    for info_type, info_chunk in info_client.get_info_chunks():
        # Index Information
        es_client.write_data(index_name, info_chunk)

    # RAG Query Exmaple: Text
    query = "What is the main topic of the document?"
    response = rag_client.query(query)
    print(response)

    # RAG Query Exmaple: Image
    query = "" # Refer to some image in the document
    response = rag_client.query(query)
    print(response)

    # RAG Query Exmaple: Table
    query = "How did stock perform in 2024?"
    response = rag_client.query(query)
    print(response)

if __name__ == "__main__":
    analyze_pdf("example.pdf")