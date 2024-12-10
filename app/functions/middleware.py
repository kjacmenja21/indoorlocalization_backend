import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db import engine
from app.functions.alembic_jobs import prepare_database
from app.functions.logger import setup_logger
from app.functions.multicast_dns import MulticastDNS, init_mdns
from app.models.common import init_orm
from migrations.env import config


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logging.info("Starting the application")

    multicast_dns: MulticastDNS | None = None

    logging.info("Checking if database is up to date...")
    prepare_database(engine, config)
    logging.info("Database is up to date with Alembic HEAD!")

    init_orm()

    multicast_dns = await init_mdns()

    yield

    if multicast_dns:
        await multicast_dns.unregister_service()
    logging.warning("Shutting down the application")
