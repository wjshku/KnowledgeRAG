# Processor for PDF, Information type: Text, Image, Table
from ..module.text import TextProcessor
from ..module.image import ImageProcessor
from ..module.table import TableProcessor

class PDFProcessor:
    def __init__(self):
        self.processors = {
            "text": TextProcessor(),
            "image": ImageProcessor(),
            "table": TableProcessor()
        }

        self.info_chunks = {
            "text": [],
            "image": [],
            "table": []
        }

    def process(self, info_paths: list[str]) -> None:
        for info_path in info_paths:
            self.process_single_pdf(info_path)

    def process_single_pdf(self, info_path: str) -> None:
        for name, processor in self.processors.items():
            info_chunks = processor.process(info_path)
            self.info_chunks[name].extend(info_chunks)

    def get_info_chunks(self) -> list[dict]:
        for name, info_chunks in self.info_chunks.items():
            for info_chunk in info_chunks:
                yield name, info_chunk
    
    def clear_info_chunks(self) -> None:
        self.info_chunks = {
            "text": [],
            "image": [],
            "table": []
        }
    
    def get_info_chunks_count(self) -> dict:
        return {
            "text": len(self.info_chunks["text"]),
            "image": len(self.info_chunks["image"]),
            "table": len(self.info_chunks["table"])
        }