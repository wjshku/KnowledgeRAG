import jieba
import logging

# Suppress DEBUG messages
logger = logging.getLogger("jieba")
logger.setLevel(logging.WARNING)

def get_keyword(query):
    # 确保输入是字符串类型
    if not isinstance(query, str):
        print(f'[Get Keyword] Received non-string query: {query} (type: {type(query)}), converting to string')
        query = str(query) if query is not None else ''
    
    # 确保查询不为空
    if not query.strip():
        print('[Get Keyword] Empty query string, returning empty list')
        return []
    
    try:
        # 使用搜索引擎模式进行分词
        seg_list = jieba.cut_for_search(query)
        # Filter out stop words
        filtered_keywords = [word for word in seg_list if word not in stop_words]
        # logging.info('[Jieba Keywords Extraction] ' + ','.join(filtered_keywords))
        return filtered_keywords
    except Exception as e:
        print(f'[Get Keyword] Error processing query "{query}": {e}')
        return []
    
stop_words = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "与", "如何",
    "为", "得", "里", "后", "自己", "之", "过", "给", "然后", "那", "下", "能", "而", "来", "个", "这", "之间", "应该", "可以", "到", "由", "及", "对", "中", "会",
    "但", "年", "还", "并", "如果", "我们", "为了", "而且", "或者", "因为", "所以", "对于", "而言", "与否", "只是", "已经", "可能", "同时", "比如", "这样", "当然",
    "并且", "大家", "之后", "那么", "越", "虽然", "比", "还是", "只有", "现在", "应该", "由于", "尽管", "除了", "以外", "然而", "哪些", "这些", "所有", "并非",
    "例如", "尤其", "哪里", "那里", "何时", "多少", "以至", "以至于", "几乎", "已经", "仍然", "甚至", "更加", "无论", "不过", "不是", "从来", "何处", "到底", 
    "尽管", "何况", "不会", "何以", "怎样", "为何", "此外", "其中","怎么","什么","为什么","是否",'。', '？', '！', '.', '?', '!','，',','
])


def display_hits(hits):
    print("=== Retrieval Results ===")
    for idx, doc in enumerate(hits, 1):
        print(f"Len ({len(doc['text'])})   Text: {doc['text'][:100]}{'...' if len(doc['text']) > 100 else ''}")
