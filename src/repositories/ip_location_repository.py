from ipaddress import ip_address
from typing import Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from src.models.database import get_db_session
from src.models.ip_location import IPLocation


class IPLocationRepository:
    """Simple repository for IP location queries"""

    def __init__(self):
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = get_db_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def find_location_by_ip(self, ip_str: str) -> Tuple[Dict[str, str], int]:
        try:
            ip_int = int(ip_address(ip_str))

            if self.session is None:
                return {"error": "Database session not initialized"}, 500

            location = (
                self.session.query(IPLocation)
                .filter(IPLocation.start_ip_int <= ip_int)
                .filter(IPLocation.end_ip_int >= ip_int)
                .first()
            )

            if location:
                return {
                    "country": location.country or "Unknown",
                    "city": location.city or "Unknown",
                }, 200
            else:
                return {"error": "No location found for the provided IP address"}, 404

        except Exception:
            return {"error": "Invalid IP address format"}, 400

    def get_stats(self) -> Dict[str, Union[str, List[str]]]:
        """Get database statistics"""
        try:
            if self.session is None:
                return {"total_records": "0", "sample_countries": [], "status": "error"}

            total = self.session.query(IPLocation).count()
            countries = [
                c[0] for c in self.session.query(IPLocation.country).distinct().all()
            ]

            return {
                "total_records": str(total),
                "countries": countries,
                "status": "active",
            }
        except Exception:
            return {"total_records": "0", "sample_countries": [], "status": "error"}
