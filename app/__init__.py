from fastapi import FastAPI

from app.api import add_api_routers
from app.config import FastAPISettings, GeneralConfig
from app.functions.middleware import lifespan


def create_server() -> FastAPI:
    prefix = "app_"
    config = GeneralConfig()
    settings = FastAPISettings.parse_settings(config, prefix)

    app = FastAPI(lifespan=lifespan, **settings.model_dump())
    add_api_routers(app)
    return app


app = create_server()
