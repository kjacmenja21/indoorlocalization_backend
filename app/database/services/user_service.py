from sqlalchemy.orm import Session

from app.database.db import get_db_session
from app.functions.jwt import verify_password
from app.models.user import User
from app.schemas.api.user import UserCreate, UserModel


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def authenticate_user(self, username: str, password: str) -> None | User:
        user = self.session.query(User).where(User.username == username).first()

        if user is None:
            return None

        if verify_password(password, user.password):
            return user

    def create_user(self, user: UserCreate) -> User:
        create_dump = user.model_dump()
        create_dump.update()

        db_user = UserModel()
        created_user = self.repository.add(db_user)

        return created_user
