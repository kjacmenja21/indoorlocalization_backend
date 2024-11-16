from pydantic_settings import BaseSettings
from uvicorn import Config


class FastAPISettings(BaseSettings):
    title: str = "Indoor Localization Backend"
    description: str = "# TODO write me down!"
    version: str = "0.0.0"


uvicorn_config = Config(
    app="main:app",
    host="0.0.0.0",
    reload=True,
    port=8000,
)
