from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload

from app.functions.exceptions import not_found
from app.functions.jwt import verify_password
from app.models.user import User, UserRole
from app.schemas.api.user import UserCreate, UserModel, UserRoleModel


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def authenticate_user(self, username: str, password: str) -> None | User:
        user = self.session.query(User).where(User.username == username).first()

        if user is None:
            return None

        if verify_password(password, user.password):
            return user

    def create_user(self, user: UserCreate) -> UserModel:
        role = self.session.query(UserRole).where(UserRole.name == user.role).first()
        if not role:
            raise not_found("Role does not exist!")

        if self.user_exists(user):
            raise not_found("User already exists!")

        user_model = UserModel(**user.model_dump())
        user_model.roleId = role.id
        new_user = User(**user_model.model_dump())

        self.session.add(new_user)
        self.session.commit()

        return user_model

    def get_all_users(self) -> list[UserModel]:
        user_query = self.session.query(User).options(joinedload(User.role)).all()
        users = []

        for user in user_query:
            user_role = UserRoleModel.model_validate(user.role) if user.role else None

            user_model = UserModel.model_validate({**user.__dict__, "role": user_role})
            users.append(user_model)

        return users

    def user_exists(self, user: UserModel | UserCreate) -> bool:
        user_exists = self.session.query(
            exists().where(User.username == user.username, User.email == user.email)
        ).scalar()
        return bool(user_exists)
