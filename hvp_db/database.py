from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _sqlite_read_only_uri(database_uri: str) -> str:
    parsed = urlparse(database_uri)
    query = dict(parse_qsl(parsed.query))
    query.setdefault("mode", "ro")
    updated = parsed._replace(query=urlencode(query))
    return urlunparse(updated)


def db_session(database_uri: str, read_only: bool = False) -> sessionmaker:
    """Create a SQLAlchemy sessionmaker for the given database URI."""
    connect_args = None
    engine_uri = database_uri
    if read_only:
        if database_uri.startswith("sqlite:"):
            engine_uri = _sqlite_read_only_uri(database_uri)
            connect_args = {"uri": True}
        else:
            raise ValueError("Read-only mode is only supported for SQLite databases.")
    engine = create_engine(engine_uri, echo=False, connect_args=connect_args or {})
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal
