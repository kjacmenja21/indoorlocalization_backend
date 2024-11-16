import logging
from typing import AsyncIterator

from sqlalchemy.ext import asyncio as sa

from app.database.settings import DBSettings

logger = logging.getLogger(__name__)


async def create_sa_engine() -> AsyncIterator[sa.AsyncEngine]:
    logger.info("Initializing SQLAlchemy engine")
    engine = sa.create_async_engine(str(DBSettings()))
    logger.info("SQLAlchemy engine has been initialized")

    try:
        yield engine
    finally:
        await engine.dispose()
        logger.info("SQLAlchemy engine has been cleaned up")


class CustomAsyncSession(sa.AsyncSession):
    async def close(self) -> None:
        if isinstance(self.bind, sa.AsyncConnection):
            return self.expunge_all()

        return await super().close()


async def create_session(
    engine: sa.AsyncEngine,
) -> AsyncIterator[sa.AsyncSession]:
    async with CustomAsyncSession(
        engine, expire_on_commit=False, autoflush=False
    ) as session:
        logger.info("session created")
        yield session
        logger.info("session closed")
