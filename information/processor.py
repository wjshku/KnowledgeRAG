# Source Based Multimodal Information Processor

from .source import pdf

class InformationProcessor:
    def __init__(self):
        self.prosessors = {
            "pdf": pdf.PDFProcessor()
        }
        self.info_paths = {
            "pdf": []
        }
        self.valid_info_types = {
            "pdf": "pdf"
        }

    def which_info_type(self, info_path: str) -> str:
        lower_path = info_path.lower()
        source = lower_path.split(".")[-1]
        return source

    def load_info(self, info_paths: list[str], source: str = None) -> None:
        for info_path in info_paths:
            if source is None:
                source = self.which_info_type(info_path)
            if source not in self.valid_info_types:
                raise ValueError(f"Invalid source: {source}")
            self.info_paths[source].append(info_path)

    def process_info(self) -> None:
        for source in self.info_paths:
            self.prosessors[source].process(self.info_paths[source])

    def get_info_chunks(self) -> list[dict]:
        for name, processor in self.prosessors.items():
            for info_chunk in processor.get_info_chunks():
                yield name, info_chunk
