import logging
from pathlib import Path

from src.etl.etl_service import ETLService

logger = logging.getLogger(__name__)


def initialize_database() -> None:
    logger.info("Initializing IP geolocation database...")

    etl_service = ETLService()
    try:
        stats = etl_service.run_configured_pipeline()
        logger.info("ETL completed: %s", stats)
    except Exception as e:
        logger.error("ETL pipeline failed: %s", e)
        logger.warning("Application will continue but database may be empty")


def bootstrap_application() -> None:
    lock_file = Path("/tmp/db_initialized.lock")

    if not lock_file.exists():
        initialize_database()
        lock_file.touch()
        logger.info("Database initialization complete - created lock file")
    else:
        logger.info("Database already initialized - skipping ETL")
