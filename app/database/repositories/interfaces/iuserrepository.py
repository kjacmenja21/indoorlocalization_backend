from app.database.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.schemas.db.user import UserModel


class IUserRepository(SQLAlchemyRepository[User, UserModel]):
    def get_user_by_username(self, username: str) -> None | User:
        raise NotImplementedError
