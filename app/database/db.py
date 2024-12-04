import logging
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.settings import db_settings

logger = logging.getLogger(__name__)

engine = create_engine(db_settings.db_dsn)


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, Any, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
