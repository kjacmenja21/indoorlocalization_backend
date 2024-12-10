from typing import Literal

from hypercorn import Config
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="",
        env_file="",
        env_ignore_empty=True,
    )
    log_level: Literal["INFO", "WARNING", "ERROR"] = "INFO"
    refresh_token_cookie_name: str = "refresh-token"

    mdns_enable: bool = False
    mdns_hostname: str = "mdns_dev"
    mdns_port: int = 8001

    jwt_access_token_secret_key: str = "supersecretkey"
    jwt_refresh_token_secret_key: str = "refreshtokensecret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_minutes: int = 60 * 24 * 7

    app_title: str = "Indoor Localization Backend"
    app_description: str = "# TODO write me down!"
    app_version: str = "0.0.0"
    app_debug: bool = False


class FastAPISettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    app_title: str = "Indoor Localization Backend"
    app_description: str = "# TODO write me down!"
    app_version: str = "0.0.0"
    app_debug: bool = False

    @staticmethod
    def parse_settings(config: BaseSettings, prefix: str) -> "FastAPISettings":
        transformed_data = {
            key[len(prefix) :]: value
            for key, value in config.model_dump().items()
            if key.startswith(prefix)
        }
        settings = FastAPISettings.model_validate(**transformed_data)
        return settings


class HypercornConfig(Config):
    app: str = "app:app"
    host: str = "127.0.0.1"
    port: int = 8000

    def __init__(self) -> None:
        super().__init__()
        self.bind = f"{self.host}:{self.port}"
        self.loglevel = "INFO"
