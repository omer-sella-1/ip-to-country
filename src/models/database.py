from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import Config

# generates engine that connects to the database file specified in the config
engine = create_engine(
    f"sqlite:///{Config.IP_DATABASE_FILE.replace('.csv', '.db')}",
    echo=False,  # Set to True for SQL debugging
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative class definitions
Base = declarative_base()


# This method provides a session to interact with the database
# establish an actual connection to the DB and return a session object
def get_db_session():
    # create a new session
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise


# this function initializes the database by creating all tables defined in the models
def init_database():
    Base.metadata.create_all(bind=engine)
