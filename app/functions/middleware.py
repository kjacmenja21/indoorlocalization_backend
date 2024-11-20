import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models.common import init_orm


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info(f"Starting the application: ENV= # TODO ADD ENV LOADING")
    init_orm()
    yield
    logging.warning("Shutting down the application")
