from app.database.repositories.interfaces.iuserrepository import IUserRepository
from app.functions.jwt import verify_password
from app.models.user import User
from app.schemas.api.user import UserCreate, UserModel


class UserService:
    def __init__(self, repository: IUserRepository) -> None:
        self.repository: IUserRepository = repository

    def authenticate_user(self, username: str, password: str) -> None | User:
        user = self.repository.get_user_by_username(username)

        if user is None:
            return None

        if verify_password(password, user.salt):
            return self.repository.get(user.id)

    def create_user(self, user: UserCreate) -> User:
        user = UserModel(**user.model_dump())
        created_user = self.repository.add(user)

        return created_user
