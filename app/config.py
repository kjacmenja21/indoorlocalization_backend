from typing import Literal

from hypercorn import Config
from pydantic_settings import BaseSettings


class GeneralConfig(BaseSettings):
    log_level: Literal["INFO", "WARNING", "ERROR"] = "INFO"
    use_multicast_dns: bool = True


class mDNSConfig(BaseSettings):
    hostname: str = "adaptiq_indoor_localization"
    port: int = 8001


class JWTConfig(BaseSettings):
    secret_key: str = "supersecretkey"
    refresh_token_secret_key: str = "refreshtokensecret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7


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
