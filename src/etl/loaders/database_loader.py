import logging
from typing import Dict, List

from src.models.database import get_db_session
from src.models.ip_location import IPLocation

logger = logging.getLogger(__name__)


class DatabaseLoader:

    @staticmethod
    def load(clean_data: List[Dict[str, str]]) -> bool:
        session = get_db_session()

        try:
            session.query(IPLocation).delete()
            logger.info("Cleared existing data")

            for record in clean_data:
                ip_location = IPLocation()
                ip_location.set_ip_range(record["start_ip"], record["end_ip"])
                ip_location.country = record["country"]
                ip_location.city = record["city"]

                session.add(ip_location)

            session.commit()
            logger.info("Loaded %d records into database", len(clean_data))
            return True

        except Exception as e:
            session.rollback()
            logger.error("Database error: %s", e)
            return False
        finally:
            session.close()
