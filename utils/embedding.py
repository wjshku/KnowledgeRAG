# Embedding text

import os
import time
import traceback
import requests
from dotenv import load_dotenv
load_dotenv()
EMBEDDING_URL = os.getenv("EMBEDDING_URL")

def get_embedding(inputs):
    """Get embeddings from the embedding service"""
    
    headers = {"Content-Type": "application/json"}
    data = {"texts": inputs}
    try:    
        response = requests.post(EMBEDDING_URL, headers=headers, json=data)
        
        result = response.json()
        return result['data']['text_vectors']
    except Exception as e:
        print(e)
        vector = [0.0] * 10
        return [vector] * len(inputs)