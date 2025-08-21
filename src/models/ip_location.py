from ipaddress import ip_address

from sqlalchemy import BigInteger, Column, Index, Integer, String

from src.models.database import Base


class IPLocation(Base):

    __tablename__ = "ip_locations"

    id = Column(Integer, primary_key=True)
    start_ip_int = Column(BigInteger, nullable=False, index=True)
    end_ip_int = Column(BigInteger, nullable=False, index=True)
    start_ip_str = Column(String(45), nullable=False)
    end_ip_str = Column(String(45), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    __table_args__ = (Index("idx_ip_range", "start_ip_int", "end_ip_int"),)

    @staticmethod
    def ip_to_int(ip_str: str) -> int:
        return int(ip_address(ip_str))

    def set_ip_range(self, start_ip: str, end_ip: str) -> None:
        self.start_ip_str = start_ip
        self.end_ip_str = end_ip
        self.start_ip_int = self.ip_to_int(start_ip)
        self.end_ip_int = self.ip_to_int(end_ip)

    def __repr__(self) -> str:
        return (
            f"<IPLocation({self.start_ip_str}-{self.end_ip_str}, "
            f"{self.city}, {self.country})>"
        )
