from typing import TypeVar

from sqlalchemy.orm import Session

from app.database.repositories.irepository import IRepository, T
from app.models.common import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(IRepository[T]):
    def __init__(self, model: type[Model], session: Session) -> None:
        self.model = model
        self.session = session
