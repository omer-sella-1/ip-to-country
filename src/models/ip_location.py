from ipaddress import ip_address

from sqlalchemy import BigInteger, Column, Index, Integer, String

from src.models.database import Base


class IPLocation(Base):
    # __tablename__ is a reserve word in SQLAlchemy to define the table name
    __tablename__ = "ip_locations"

    # columns definitions. nullable=False means the column cannot be null
    # index=True creates an index on the column to speed up queries
    # BigInteger is used for large integers (like IP addresses in integer form)
    # String(length) defines a string column with a maximum length
    # Index is used to create a composite index on multiple columns
    id = Column(Integer, primary_key=True)
    start_ip_int = Column(BigInteger, nullable=False, index=True)
    end_ip_int = Column(BigInteger, nullable=False, index=True)
    start_ip_str = Column(String(45), nullable=False)
    end_ip_str = Column(String(45), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    # __table_args__ allows for additional table arguments, like indexes
    # and other constraints
    __table_args__ = (Index("idx_ip_range", "start_ip_int", "end_ip_int"),)

    # static method to convert an IP address string to its integer representation
    # used for searching and storing IP addresses efficiently
    @staticmethod
    def ip_to_int(ip_str: str) -> int:
        return int(ip_address(ip_str))

    # method to set the IP range and automatically compute their integer representations
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
