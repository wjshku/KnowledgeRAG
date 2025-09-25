# Table Module for PDF

from utils.pdf_utils import _build_chapter_map
import fitz  # PyMuPDF
from typing import List, Dict, Any
from utils.client import OpenAIClient

def extract_tables_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    page_to_chapter = _build_chapter_map(pdf_path)
    results = []
    for page_num in range(doc.page_count):
        try:
            page = doc.load_page(page_num)
            metadata = dict(getattr(doc, "metadata", {}) or {})
            metadata.setdefault("source", pdf_path)
            metadata["page"] = page_num
            # get chapter number
            chapter_num = page_to_chapter.get(int(page_num)) if isinstance(page_num, int) or (isinstance(page_num, str) and page_num.isdigit()) else None
            metadata["chapter"] = chapter_num
            page_tables = page.find_tables()

            for table_index, table in enumerate(page_tables):
                try:
                    md = table.to_markdown()
                    metadata = metadata | {"table_index": table_index, "table_markdown": md}
                    metadata = metadata | {"page_text": page.get_text()}
                    results.append(metadata)
                except Exception:
                    pass
        except Exception:
            pass
    doc.close()
    return results

class TableProcessor:
    def __init__(self):
        pass

    def context_augment(self, table_md: str, context: str) -> str:
        prompt = f"""
        目标：请根据输入的表格和上下文信息以及来源文件信息，生成针对于该表格的一段简短的语言描述

        注意：
        在描述中尽可能包含以下内容：
        - 表格名称：根据上下文或表格内容推测表格的名称。
        - 表格内容简介：使用自然语言总结表格的内容，包括主要信息、数据点和结构。准确记录重要数据如时间，地点等。
        - 表格意图：分析表格的用途或目的，例如是否用于展示、比较、统计等。
        你生成的描述需要控制在三句话以内。

        输出案例：
        1. 该表格详细列出了 Apple Inc. 在 2023 年 12 月 31 日至 2024 年 3 月 30 日期间的股票回购情况，包括回购数量、平均价格、公开计划购买的股票数及剩余可购买股票的价值，以展示其资本回报策略。
        2. 该表格记录了用户对商品的评分、评论以及相关用户信息，包含字段如订单编号、评分值、评论文本和用户名等，作为协同过滤推荐系统的核心数据来源。其主要作用是通过用户的评分和评论信息，结合协同过滤算法，优化广告推荐的精准度和个性化效果，使系统能够基于用户历史行为和相似用户的偏好，提高广告投放的匹配度。此外，该表格与用户点击行为数据共同构成了智能广告推荐系统的数据基础，可能存储于 MySQL 数据库，并通过 Django 框架进行管理和操作。

        输入表格：
        {table_md}

        表格上下文：
        {context}
        """
        print('len(prompt):', len(prompt))
        client = OpenAIClient()
        result = client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能AI助手，根据表格的上下文对表格描述进行补充，补充后的描述要更加准确，更加详细，更加完整。"},
                {"role": "user", "content": prompt},
            ],
        )
        return result

    def get_metadata(self, dict_data: dict) -> dict:
        return {
            "source": dict_data.get("source", ""),
            "title": dict_data.get("title", ""),
            "author": dict_data.get("author", ""),
            "subject": dict_data.get("subject", ""),
            "keywords": dict_data.get("keywords", ""),
            "page": dict_data.get("page", None),
            "chapter": dict_data.get("chapter", None),
            "table_index": dict_data.get("table_index", None),
            "table_markdown": dict_data.get("table_markdown", ""),
        }

    def process(self, info_path: str) -> list[dict]:
        # Read table from PDF and output table chunks (context augmented), with metadata
        table_results = extract_tables_from_pdf(info_path)
        chunks: List[Dict[str, Any]] = []
        for table_result in table_results:
            context_aug_content = self.context_augment(table_result["table_markdown"], table_result["page_text"])
            print(f'Context Augmented Content: {context_aug_content}')
            metadata = self.get_metadata(table_result)
            chunks.append({
                "content": context_aug_content,
                "metadata": metadata,
            })
        return chunks