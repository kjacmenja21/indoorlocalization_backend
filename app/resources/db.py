import logging
import typing

from sqlalchemy.ext import asyncio as sa

logger = logging.getLogger(__name__)


async def create_sa_engine():
    logger.info("Initializing SQLAlchemy engine")
    engine = sa.create_async_engine()
    logger.info("SQLAlchemy engine has been initialized")

    try:
        yield engine
    finally:
        await engine.dispose()
        logger.info("SQLAlchemy engine has been cleaned up")
