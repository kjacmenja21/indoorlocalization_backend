import logging
from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.settings import db_settings as settings

logger = logging.getLogger(__name__)


class DBEngineHandler:
    def __init__(
        self,
        url: str | URL,
        pool_size: int,
        max_overflow: int,
        echo: bool,
        pool_pre_ping: bool,
    ) -> None:
        self.engine = create_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
        )

    def get_engine(self) -> Engine:
        return self.engine

    def get_sessionmaker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db_session(self) -> Generator[Session, Any, None]:
        session_local = self.get_sessionmaker()
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def get_db_session_ctx(self) -> Generator[Session, Any, None]:
        session_local = self.get_sessionmaker()
        db = session_local()
        try:
            yield db
        finally:
            db.close()


engine_handler = DBEngineHandler(
    url=settings.db_dsn,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    echo=settings.echo,
    pool_pre_ping=settings.pool_pre_ping,
)
