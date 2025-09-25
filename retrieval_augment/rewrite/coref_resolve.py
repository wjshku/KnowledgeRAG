# Coreference Resolution for Retrieval Augmentation
import json
from utils.client import OpenAIClient

class CoreferenceResolution:
    def __init__(self):
        pass

    def coreference_resolution(self, query: str, chat_history: str) -> str:
        prompt = f'''目标：根据提供的用户与知识库助手的历史记录，做指代消解，将用户最新问题中出现的代词或指代内容替换为历史记录中的明确对象，生成一条完整的独立问题。

        说明：
        - 将用户问题中的指代词替换为历史记录中的具体内容，生成一条独立问题。

        以JSON的格式输出
        {{"query":["替换指代后的完整问题"]}}

        以下是一些案例

        ----------
        历史记录：
        ['user': Milvus是什么?
        'assistant': Milvus 是一个向量数据库]
        用户问题：怎么使用它？

        输出JSON：{{"query":["怎么使用Milvus?"]}}
        ----------
        历史记录：
        ['user': PyTorch是什么?
        'assistant': PyTorch是一个开源的机器学习库，用于Python。它提供了一个灵活且高效的框架，用于构建和训练深度神经网络。
        'user': TensorFlow是什么?
        'assistant': TensorFlow是一个开源的机器学习框架。它提供了一套全面的工具、库和资源，用于构建和部署机器学习模型。]
        用户问题: 它们的区别是什么？

        输出JSON：{{"query":["PyTorch和TensorFlow的区别是什么？"]}}
        ----------
        历史记录：
        ['user': 四川有哪些城市
        'assistant': 1. 成都。 2. 绵阳。 3. 资阳。]
        用户问题: 介绍一下第二个

        输出JSON：{{"query":["介绍一下绵阳"]}}
        ----------
        历史记录：
        {chat_history}
        用户问题：{query}

        输出JSON：
        ''' 
        # Call OpenAI ChatGPT 4o nano to generate query variations
        client = OpenAIClient()
        response = client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能AI助手，专注于做指代消解，并以 JSON 格式输出"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        parsed_result = json.loads(response)
        return parsed_result.get("query")
