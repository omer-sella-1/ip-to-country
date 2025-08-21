import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    PORT = int(os.getenv("PORT", 8080))
    RATE_LIMIT_PER_SECOND = int(os.getenv("RATE_LIMIT_PER_SECOND", 10))
    IP_DATABASE_TYPE = os.getenv("IP_DATABASE_TYPE", "csv")
    IP_DATABASE_FILE = os.getenv("IP_DATABASE_FILE", "data/ip_database.csv")
