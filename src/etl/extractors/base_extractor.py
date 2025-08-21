from abc import ABC, abstractmethod
from typing import Dict, List


class BaseExtractor(ABC):
    """
    Abstract base class for all data extractors

    Any new data source (CSV, JSON, API, Database) must implement this interface
    to work with the ETL pipeline.
    """

    @abstractmethod
    def extract(self) -> List[Dict[str, str]]:
        """
        Extract data from the source and return in standard format

        Returns:
            List of dictionaries with keys: start_ip, end_ip, country, city
            Example: [
                {'start_ip': '1.0.0.0', 'end_ip': '1.255.255.255',
                 'country': 'Australia', 'city': 'Sydney'},
                ...
            ]
        """
        pass

    @abstractmethod
    def get_source_info(self) -> str:
        """
        Return human-readable description of the data source

        Returns:
            String describing the source (for logging/debugging)
            Example: "CSV file: /path/to/data.csv"
        """
        pass
