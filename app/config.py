from pydantic_settings import BaseSettings


class FastAPISettings(BaseSettings):
    title: str = "Indoor Localization Backend"
    description: str = "# TODO write me down!"
    version: str = "0.0.0"


class UvicornConfig(BaseSettings):
    app: str = "main:app"
    host: str = "localhost"
    reload: bool = True
    port: int = 8000
