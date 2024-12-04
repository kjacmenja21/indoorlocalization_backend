from app.database.repositories import SQLAlchemyRepository
from app.models.user import User
from app.schemas.db.user import UserModel


class UserRepository(SQLAlchemyRepository[User, UserModel]): ...
