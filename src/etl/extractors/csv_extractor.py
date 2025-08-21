import csv
import logging
from typing import Dict, List

from src.etl.extractors.base_extractor import BaseExtractor

logger = logging.getLogger(__name__)


class CSVExtractor(BaseExtractor):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[Dict[str, str]]:
        data = []

        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)

            required = {"start_ip", "end_ip", "country", "city"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError(
                    f"CSV missing headers: {required - set(reader.fieldnames or [])}"
                )

            for row in reader:
                clean_row = {k: v.strip() for k, v in row.items()}
                if all(clean_row.get(field) for field in required):
                    data.append(clean_row)

        logger.info("Extracted %d records from CSV", len(data))
        return data

    def get_source_info(self) -> str:
        """Return CSV file information"""
        return f"CSV file: {self.file_path}"
