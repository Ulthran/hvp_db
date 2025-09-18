from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_session(database_uri: str) -> sessionmaker:
    """Create a SQLAlchemy sessionmaker for the given database URI."""
    engine = create_engine(database_uri, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal
