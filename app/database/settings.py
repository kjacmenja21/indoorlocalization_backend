from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


class DBSettings(BaseSettings):
    service_name: str = "FastAPI template"
    debug: bool = False

    db_driver: str = "postgresql"
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_user: str = "dev"
    db_password: str = "dev_password"
    db_database: str = "indoor_dev"

    db_pool_size: int = 5
    db_max_overflow: int = 0
    db_echo: bool = False
    db_pool_pre_ping: bool = True

    app_port: int = 8000

    @property
    def db_dsn(self) -> URL:
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            host=self.db_host,
            port=self.db_port,
            database=self.db_database,
            password=self.db_password,
        )


db_settings = DBSettings()
