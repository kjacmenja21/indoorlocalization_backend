import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.functions.logger import setup_logger
from app.functions.multicast_dns import MulticastDNS
from app.models.common import init_orm


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    multicast_dns = MulticastDNS("indoor_localization", 8001)
    logging.info("Starting the application")
    init_orm()
    await multicast_dns.register_service()
    yield
    await multicast_dns.unregister_service()
    logging.warning("Shutting down the application")
