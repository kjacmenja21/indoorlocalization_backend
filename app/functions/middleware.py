import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import GeneralConfig
from app.functions.logger import setup_logger
from app.functions.multicast_dns import MulticastDNS
from app.models.common import init_orm


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logging.info("Starting the application")

    config = GeneralConfig()
    multicast_dns: MulticastDNS | None = None

    init_orm()

    if config.use_multicast_dns:
        multicast_dns = MulticastDNS("indoor_localization", 8001)
        await multicast_dns.register_service()
    yield

    if multicast_dns:
        await multicast_dns.unregister_service()
    logging.warning("Shutting down the application")
