from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import Config

engine = create_engine(
    f"sqlite:///{Config.IP_DATABASE_FILE.replace('.csv', '.db')}",
    echo=False,  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session():
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise


def init_database():
    Base.metadata.create_all(bind=engine)
