from sqlalchemy.orm import Session

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
        user_model = UserModel(**user.model_dump())
        role = self.session.query(UserRole).where(UserRole.name == user.role).first()

        if not role:
            pass
        user_model.roleId = role.id
        new_user = User(**user_model.model_dump())
        self.session.add(new_user)
        self.session.commit()

        return user_model
