# Aggregate results after reranking

class Aggregate:
    def __init__(self):
        pass

    def aggregate(self, query: str, hits: list):
        # Aggregate the retrieved results after reranking. Create a new context for the query
        # Create the documents text with newlines
        documents_text = '\n'.join([hit['text'] + ' (Source: ' + hit['metadata']['source'] + ')' for hit in hits])
        
        prompt = f"""
        You are a helpful assistant to answer question
        The query is: {query}
        The most relevant documents are:
        {documents_text}
        Please answer the query based on the information retrieved and provide reference to the source documents.
        Examples:
        ```
        The query is: 孙悟空和猪八戒的关系
        The most relevant documents are:
        孙悟空和猪八戒是师兄弟关系，是西游记中的两个角色。（Source: http://www.baidu.com/西游记/）
        ```
        The answer is: 孙悟空和猪八戒是师兄弟关系。(Source: http://www.baidu.com/西游记/)
        ```
        The query is: 中国有哪些主要城市
        The most relevant documents are:
        中国主要城市有上海，北京，广州，深圳。（Source: data/中国城市.md）
        美国主要城市有纽约，洛杉矶，芝加哥。（Source: http://www.baidu.com/美国城市/）
        ```
        The answer is: 中国主要城市有上海，北京，广州，深圳。(Source: data/中国城市.md)
        ```
        You are an AI assistant. Answer the question strictly based on the information provided below. 
        Do NOT use any knowledge not included in these sources. 
        If the answer cannot be found in the provided text, respond with: "The information is not available in the provided context."
        Very important: Always provide source information in the answer.
        """
        return prompt