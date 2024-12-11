from typing import Annotated, Literal

from hypercorn import Config
from pydantic import AfterValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def check_secret_set(value: str):
    if len(value) <= 0:
        raise ValueError(
            "Secret value has not been set! Consider using `openssl rand -hex <value>`"
        )
    return value


StringCheck = Annotated[str, AfterValidator(check_secret_set)]


class GeneralConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="", env_file="", env_ignore_unset=False
    )
    log_level: Literal["INFO", "WARNING", "ERROR"] = "INFO"
    refresh_token_cookie_name: StringCheck = "refresh-token"

    mdns_enable: bool = False
    mdns_hostname: str = "mdns_dev"
    mdns_port: int = 8001

    jwt_access_token_secret_key: StringCheck
    jwt_refresh_token_secret_key: StringCheck
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_minutes: int = 10080


class FastAPISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file=".env.app",
        env_ignore_empty=True,
    )
    title: str = "Indoor Localization Back-end"
    description: str = (
        "Indoor Localization project aims to make the process of tracking asset movement (pallet with goods, mobile equipment like forklifts, trucks and others) by utilizing MQTT to collect data from token devices attached to the assets. It displays real-time locations and generates reports based on historic data that can be used to improve business processes in which the assets is utilized"
    )
    version: str = "0.0.0"
    debug: bool = False


class HypercornConfig(Config):
    app: str = "app:app"
    host: str = "[::]"
    port: int = 8000

    def __init__(self) -> None:
        super().__init__()
        self.bind = [f"{self.host}:{self.port}"]
        self.loglevel = "INFO"
