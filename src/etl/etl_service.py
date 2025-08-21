import logging

from src.config import Config
from src.etl.extractors.base_extractor import BaseExtractor
from src.etl.extractors.extractor_factory import ExtractorFactory
from src.etl.loaders.database_loader import DatabaseLoader
from src.etl.transformers.ip_transformer import IPLocationTransformer
from src.models.database import init_database

logger = logging.getLogger(__name__)


class ETLService:

    def create_extractor_from_config(self) -> BaseExtractor:
        return ExtractorFactory.create(Config.IP_DATABASE_TYPE, Config.IP_DATABASE_FILE)

    def run_pipeline(self, extractor: BaseExtractor) -> dict:
        logger.info("Starting ETL pipeline for: %s", extractor.get_source_info())

        init_database()

        raw_data = extractor.extract()

        transformer = IPLocationTransformer()
        clean_data = transformer.transform(raw_data)

        loader = DatabaseLoader()
        success = loader.load(clean_data)

        if success:
            logger.info("ETL pipeline completed successfully!")
            return {
                "extracted": len(raw_data),
                "transformed": len(clean_data),
                "loaded": len(clean_data),
                "errors": [],
            }
        else:
            raise RuntimeError("ETL pipeline failed")

    def run_configured_pipeline(self):
        extractor = self.create_extractor_from_config()
        return self.run_pipeline(extractor)
