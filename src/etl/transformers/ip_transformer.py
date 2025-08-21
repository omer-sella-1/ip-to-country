import logging
from ipaddress import ip_address
from typing import Dict, List

logger = logging.getLogger(__name__)


class IPLocationTransformer:

    @staticmethod
    def transform(raw_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        clean_data = []

        for record in raw_data:
            try:
                start_ip = str(ip_address(record["start_ip"].strip()))
                end_ip = str(ip_address(record["end_ip"].strip()))

                if int(ip_address(start_ip)) > int(ip_address(end_ip)):
                    logger.warning("Skipping invalid range: %s > %s", start_ip, end_ip)
                    continue

                country = record["country"].strip()
                city = record["city"].strip()

                if not country or not city:
                    logger.warning("Skipping record with empty location: %s", record)
                    continue

                clean_data.append(
                    {
                        "start_ip": start_ip,
                        "end_ip": end_ip,
                        "country": country,
                        "city": city,
                    }
                )

            except Exception as e:
                logger.warning("Skipping invalid record: %s - Error: %s", record, e)
                continue

        logger.info("Transformed %d valid records", len(clean_data))
        return clean_data
