# Query Decomposition for Retrieval Augmentation

from utils.client import OpenAIClient
import json

class QueryDecomposition:
    def __init__(self):
        pass

    def decompose(self, query: str) -> list:
        prompt=f''' 
        目标：分析用户的问题，判断其是否需要拆分为子问题以提高信息检索的准确性。如果需要拆分，提供拆分后的子问题列表；如果不需要，直接返回原问题。

        说明：
        - 用户的问题可能含糊不清或包含多个概念，导致难以直接回答。
        - 为提高知识库查询的质量和相关性，需评估问题是否应分解为更具体的子问题。
        - 根据问题的复杂性和广泛性，判断是否需要拆分：
        - 如果问题涉及多个方面（如比较多个实体、包含多个独立步骤），需要拆分为子问题。
        - 如果问题已集中且明确，无需拆分。
        - 输出结果必须为 JSON 格式。请直接输出JSON，不需要做任何解释。

        输出格式：
        {{
        "query": ["子问题1", "子问题2"...] 
        }}  

        案例 1
        ---
        用户问题: "林冲、关羽、孙悟空的性格有什么不同？"
        推理过程: 该问题涉及多个实体的比较，需要分别了解每个实体的性格。
        输出:
        {{
        "query": ["林冲的性格是什么？", "关羽的性格是什么？", "孙悟空的性格是什么？"]
        }}

        案例 2
        ---
        用户问题: "Find environmentally friendly electric cars with over 300 miles of range under $40,000."
        推理过程: 问题包含多个条件要求，需要拆分为具体的子问题以提高检索准确性。
        输出:
        {{
        "query": ["Which cars are environmentally friendly electric vehicles?", "Which electric vehicles have a range of over 300 miles?", "What electric vehicles are priced under $40,000?"]
        }}

        案例 3
        ---
        用户问题: "如何设计一个智能家居系统并实时监控设备状态？"
        推理过程: 问题包含两个独立方面（设计系统和监控状态），需要拆分。
        输出:
        {{
        "query": ["如何设计一个智能家居系统？", "如何实时监控智能家居系统的设备状态？"]
        }}

        案例 4
        ---
        用户问题: "Covid对经济的影响是什么？"
        推理过程: 问题集中且明确，无需拆分。
        输出:
        {{
        "query": []
        }}

        案例 5
        ---
        用户问题: "LangChain和LangGraph的区别是什么？"
        推理过程: 该问题涉及比较，可拆分为各自定义再加比较，以提高检索准确性。
        输出:
        {{
        "query": ["LangChain是什么？", "LangGraph是什么？"]
        }}

        用户问题:
        "{query}"
        '''
        client = OpenAIClient()
        response = client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能AI助手，专注于做查询拆分，并以 JSON 格式输出"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        parsed_result = json.loads(response)
        return parsed_result.get("query")