import logging
from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.settings import db_settings as settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.db_dsn,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    echo=settings.echo,
    pool_pre_ping=settings.pool_pre_ping,
)


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, Any, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session_ctx() -> Generator[Session, Any, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
