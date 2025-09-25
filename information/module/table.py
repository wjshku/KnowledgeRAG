# Table Module for PDF

from ..utils.pdf_utils import _build_chapter_map
import fitz  # PyMuPDF
from typing import List, Dict, Any

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

    def context_augment(self, table_markdown: str, page_text: str) -> str:
        return table_markdown + "\n\n" + page_text

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
            metadata = self.get_metadata(table_result)
            chunks.append({
                "content": context_aug_content,
                "metadata": metadata,
            })
        return chunks