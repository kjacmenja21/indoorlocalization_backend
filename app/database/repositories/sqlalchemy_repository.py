from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.repositories.irepository import IRepository
from app.models.common import Base

TModel = TypeVar("TModel", bound=Base)
TPydantic = TypeVar("TPydantic", bound=BaseModel)


class SQLAlchemyRepository(IRepository[TModel], Generic[TModel, TPydantic]):
    def __init__(self, model: type[TModel], session: Session) -> None:
        self.model = model
        self.db_session = session

    def add(self, data: TPydantic) -> TModel:
        """Add a new entity to the database."""
        db_entity = self.model(**data.model_dump())
        self.db_session.add(db_entity)
        self.db_session.commit()
        self.db_session.refresh(db_entity)
        return db_entity

    def get(self, id: int) -> Optional[TModel]:
        """Retrieve an entity by its ID."""
        return self.db_session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[TModel]:
        """Retrieve all entities."""
        return self.db_session.query(self.model).all()

    def update(self, id: int, data: TPydantic) -> Optional[TModel]:
        """Update an entity by its ID."""
        db_entity = self.get(id)
        if not db_entity:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_entity, key, value)
        self.db_session.commit()
        self.db_session.refresh(db_entity)
        return db_entity

    def delete(self, id: int) -> None:
        """Delete an entity by its ID."""
        db_entity = self.get(id)
        if db_entity:
            self.db_session.delete(db_entity)
            self.db_session.commit()
