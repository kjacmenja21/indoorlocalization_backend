import logging

from sqlalchemy.orm import DeclarativeBase

from app.database.db import engine


class Base(DeclarativeBase):
    pass


def init_orm() -> None:
    logging.info("Creating ORM tables from metadata...")
    Base.metadata.create_all(engine)
    logging.info("Table creation done!")
