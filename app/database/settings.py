import logging

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import make_url
from sqlalchemy.engine.url import URL

from app.functions.exceptions import stop_application

logger = logging.getLogger(__name__)


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="db_",
        env_file="db.env",
        env_ignore_empty=True,
    )
    postgres_url: PostgresDsn = "postgresql://postgres:example@localhost:5432/postgres"
    debug: bool = False

    driver: str = "postgresql"
    host: str = "127.0.0.1"
    port: int = 5432
    user: str = "dev"
    password: str = "dev_password"
    database: str = "indoor_dev"

    pool_size: int = 5
    max_overflow: int = 0
    echo: bool = False
    pool_pre_ping: bool = True

    @property
    def db_dsn(self) -> URL:
        """Creates DSN object for SQLAlchemy `create_engine` function

        Returns:
            URL: The URL object passed to the function
        """
        try:
            url = make_url(str(self.postgres_url))
            default_url = make_url(
                DBSettings.model_fields.get("postgres_url").default,
            )

            if url == default_url:

                url = URL.create(
                    drivername=self.driver,
                    username=self.user,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    password=self.password,
                )
        except TypeError as e:
            logger.exception("Error while creating DB URL:\n%s", str(e))
            stop_application()

        return url


db_settings = DBSettings()
