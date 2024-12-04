from app.database.repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserService:
    def __init__(self, repository: SQLAlchemyRepository) -> None:
        self.repository = repository
