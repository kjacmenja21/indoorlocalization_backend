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

    multicast_dns: MulticastDNS | None = None

    init_orm()

    multicast_dns = await init_mdns()

    yield

    if multicast_dns:
        await multicast_dns.unregister_service()
    logging.warning("Shutting down the application")


async def init_mdns() -> MulticastDNS | None:
    multicast_dns = None
    config = GeneralConfig()
    if config.mdns_enable:
        multicast_dns = MulticastDNS(config.mdns_hostname, config.mdns_port)
        await multicast_dns.register_service()
    return multicast_dns
