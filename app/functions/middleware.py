import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.functions.logger import setup_logger
from app.models.common import init_orm


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logging.info("Starting the application")
    init_orm()
    yield
    logging.warning("Shutting down the application")
