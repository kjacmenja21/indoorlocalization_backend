from typing import Literal

from hypercorn import Config
from pydantic_settings import BaseSettings


class GeneralConfig(BaseSettings):
    LOG_LEVEL: Literal["INFO", "WARNING", "ERROR"] = "INFO"


class FastAPISettings(BaseSettings):
    title: str = "Indoor Localization Backend"
    description: str = "# TODO write me down!"
    version: str = "0.0.0"
    debug: bool = True


class ASGIConfig(BaseSettings):
    app: str = "app:app"
    host: str = "127.0.0.1"
    port: int = 8000


class HypercornConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        config = ASGIConfig()
        self.bind = f"{config.host}:{config.port}"
        self.loglevel = "INFO"
