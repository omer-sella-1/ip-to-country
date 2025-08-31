import json
import logging
from typing import Dict, List

from src.etl.extractors.base_extractor import BaseExtractor

logger = logging.getLogger(__name__)


class JSONExtractor(BaseExtractor):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[Dict[str, str]]:
        data = []
        try:
            with open(self.file_path, "r") as file:
                raw_data = json.load(file)

            if not isinstance(raw_data, list):
                raise ValueError("JSON root should be a list of records")

            for record in raw_data:
                try:
                    clean_record = {
                        "start_ip": record["start"].strip(),
                        "end_ip": record["end"].strip(),
                        "country": record["loc"]["country_name"].strip(),
                        "city": record["loc"]["city_name"].strip(),
                    }
                    data.append(clean_record)
                except KeyError as e:
                    logger.warning(f"skipping record due to missing key: {e}")
                    continue
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return data
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from file: {self.file_path}")
            return data

        logger.info("Extracted %d records from JSON", len(data))
        return data

    def get_source_info(self) -> str:
        """Return JSON file information"""
        return f"JSON file: {self.file_path}"
