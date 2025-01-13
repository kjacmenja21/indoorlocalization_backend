import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db import engine_handler
from app.functions.alembic_jobs import create_config, prepare_database
from app.functions.logger import setup_logger
from app.functions.mqtt_client import MQTTClientHandler
from app.functions.mqtt_handlers import (
    MQTTAssetZoneMovementHandler,
    MQTTCoordinateHandler,
)
from app.functions.multicast_dns import MulticastDNS, init_mdns
from app.models.common import init_orm


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logging.info("Starting the application")
    engine = engine_handler.get_engine()
    multicast_dns: MulticastDNS | None = None

    logging.info("Checking if database is up to date...")
    prepare_database(engine, create_config())
    logging.info("Database is up to date with Alembic HEAD!")

    init_orm(engine)

    mqtt_client = MQTTClientHandler()
    await mqtt_client.start()
    mqtt_client.register_topic_handler(MQTTCoordinateHandler())
    mqtt_client.register_topic_handler(MQTTAssetZoneMovementHandler())

    multicast_dns = await init_mdns()

    yield

    await mqtt_client.stop()
    if multicast_dns:
        await multicast_dns.unregister_service()
    logging.warning("Shutting down the application")
