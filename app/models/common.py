from sqlalchemy.orm import DeclarativeBase

from app.database.db import engine


class Base(DeclarativeBase):
    pass


def init_orm() -> None:
    Base.metadata.create_all(engine)
