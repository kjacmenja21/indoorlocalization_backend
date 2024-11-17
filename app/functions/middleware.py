import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.warning(f"Starting the application: ENV= # TODO ADD ENV LOADING")
    yield
    logging.warning("Shutting down the application")
