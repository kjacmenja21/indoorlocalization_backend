from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import not_found
from app.functions.jwt import verify_password
from app.models.user import User, UserRole
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
        role = self.session.query(UserRole).where(UserRole.name == user.role).first()
        if not role:
            raise not_found("Role does not exist!")

        user_exists = self.session.query(
            exists().where(User.username == user.username, User.email == user.email)
        ).scalar()
        if user_exists:
            raise not_found("User already exists!")

        user_model = UserModel(**user.model_dump())
        user_model.roleId = role.id
        new_user = User(**user_model.model_dump())

        self.session.add(new_user)
        self.session.commit()

        return new_user
