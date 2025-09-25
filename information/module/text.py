# Text Module for PDF

from __future__ import annotations

from typing import List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
import fitz  # PyMuPDF
from utils.pdf_utils import _build_chapter_map

def num_tokens_from_string(string: str) -> int:
    import tiktoken
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

class TextProcessor:
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_metadata(self, dict_data: dict) -> dict:
        return {
            "source": dict_data.get("source", ""),
            "title": dict_data.get("title", ""),
            "author": dict_data.get("author", ""),
            "subject": dict_data.get("subject", ""),
            "keywords": dict_data.get("keywords", ""),
            "page": dict_data.get("page", None),
            "chapter": dict_data.get("chapter", None),
        }

    def process(self, info_path: str) -> list[dict]:
        # Read text from PDF and output text chunks, with metadata
        loader = PyMuPDFLoader(info_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap, 
            separators=["\n\n", "\n", " ", ""],
            length_function=num_tokens_from_string
        )

        split_docs = splitter.split_documents(documents)

        page_to_chapter = _build_chapter_map(info_path)

        chunks: List[Dict[str, Any]] = []
        for idx, doc in enumerate(split_docs):
            metadata: Dict[str, Any] = dict(getattr(doc, "metadata", {}) or {})
            metadata.setdefault("source", info_path)
            page_num = metadata.get("page")
            chapter_num = page_to_chapter.get(int(page_num)) if isinstance(page_num, int) or (isinstance(page_num, str) and page_num.isdigit()) else None
            metadata["chapter"] = chapter_num
            content: str = getattr(doc, "page_content", "")

            metadata = self.get_metadata(metadata)
            chunks.append({
                "content": content,
                "metadata": metadata,
            })

        return chunks