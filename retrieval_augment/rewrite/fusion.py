# Query Fusion for Retrieval Augmentation

from utils.client import OpenAIClient
import json

class QueryFusion:
    def __init__(self):
        pass

    def fuse(self, query: str) -> list:
        # RAG Fusion is an advanced retrieval technique that generates 
        # multiple query variations from a single user question, retrieves 
        # documents for each variation, and then fuses the results to provide 
        # more comprehensive and accurate information.
        # - **Better Coverage:** Addresses different ways the same information might be expressed
        # - **Reduced Bias:** Less dependent on specific query phrasing
        prompt = f'''请根据用户的查询，将其重新改写为 2 个不同的查询。
        这些改写后的查询应当尽可能覆盖原始查询中的不同方面或角度，以便更全面地获取相关信息。
        请确保每个改写后的查询仍然与原始查询相关，并且在内容上有所不同。

        用JSON的格式输出：
        {{
            "rag_fusion":["query1","query2"]
        }}

        原始查询：{query}
        '''
            # Call OpenAI ChatGPT 4o nano to generate query variations
            
        client = OpenAIClient()
        response = client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能AI助手，专注于改写用户查询，并以 JSON 格式输出"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        parsed_result = json.loads(response)
        return parsed_result.get("rag_fusion", [])