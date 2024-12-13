import logging

from sqlalchemy.orm import DeclarativeBase

from app.database.db import engine
from app.functions.exceptions import stop_application


class Base(DeclarativeBase):
    pass


def init_orm() -> None:
    logging.info("Creating ORM tables from metadata...")
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        message = (
            "\n\nPossibly misconfigured database .env file, check example file and if your database variables match!\nError:"
            + e.args[0]
        )
        raise stop_application(message) from e
    logging.info("Table creation done!")
