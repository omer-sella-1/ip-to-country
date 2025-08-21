from src.etl.extractors.base_extractor import BaseExtractor
from src.etl.extractors.csv_extractor import CSVExtractor


class ExtractorFactory:
    @staticmethod
    def create(extractor_type: str, file_path: str) -> BaseExtractor:
        extractors = {
            "csv": CSVExtractor,
        }

        extractor_class = extractors.get(extractor_type.lower())
        if not extractor_class:
            raise ValueError(f"Unsupported extractor type: {extractor_type}")

        return extractor_class(file_path)
