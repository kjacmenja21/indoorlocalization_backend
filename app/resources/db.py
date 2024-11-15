import logging
import typing

from sqlalchemy.ext import asyncio as sa

from app.settings import Settings

logger = logging.getLogger(__name__)


async def create_sa_engine() -> typing.AsyncIterator[sa.AsyncEngine]:
    logger.info("Initializing SQLAlchemy engine")
    engine = sa.create_async_engine(str(Settings()))
    logger.info("SQLAlchemy engine has been initialized")

    try:
        yield engine
    finally:
        await engine.dispose()
        logger.info("SQLAlchemy engine has been cleaned up")
