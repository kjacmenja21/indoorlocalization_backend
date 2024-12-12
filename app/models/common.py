import logging
from typing import Type

from pydantic import BaseModel
from sqlalchemy import ColumnElement, and_
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


def filters_from_model(
    user: BaseModel,
    class_name: Type[Base],
    include: list[str] | None = None,
    exclude: list[str] | None = None,
) -> ColumnElement[bool]:
    field_values = user.model_dump(include=include, exclude=exclude)
    filters = [
        getattr(class_name, field) == value for field, value in field_values.items()
    ]
    filter_query = and_(*filters)

    return filter_query
