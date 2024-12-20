from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload

from app.functions.exceptions import not_found
from app.functions.jwt import verify_password
from app.models.user import User, UserRole
from app.schemas.api.user import (
    UserBase,
    UserCreate,
    UserModel,
    UserModelCredentials,
    UserModelIndentified,
    UserRoleModel,
)


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def authenticate_user(
        self, username: str, password: str
    ) -> None | UserModelIndentified:
        user = self.session.query(User).where(User.username == username).first()

        if user is None:
            return None

        if verify_password(password, user.password):
            return UserModelIndentified.model_validate(user)

    def create_user(self, user: UserCreate) -> UserModelIndentified:
        role = self.session.query(UserRole).where(UserRole.name == user.role).first()
        if not role:
            raise not_found("Role does not exist!")

        if self.user_exists(user):
            raise not_found("User already exists!")

        user_model = UserModelCredentials(**user.model_dump(exclude="role"))

        new_user = User(**user_model.model_dump(exclude_none=True))
        new_user.role = role
        self.session.add(new_user)
        self.session.commit()

        return UserModelIndentified.model_validate(new_user)

    def delete_user(self, user: UserBase | int):
        user = self.find_user(user)
        try:
            self.session.delete(user)
            self.session.commit()
        except Exception:
            return False
        return True

    def get_all_users(self) -> list[UserModel]:
        user_query: list[User] = (
            self.session.query(User).options(joinedload(User.role)).all()
        )

        users = []
        for user in user_query:
            user_model = self.user_from_orm(user)
            users.append(user_model)

        return users

    def get_user(self, user: UserBase | int) -> UserModelIndentified:
        found_user = self.find_user(user)

        return UserModelIndentified.model_validate(found_user)

    def find_user(self, user: UserBase | int) -> User | None:
        filter_query = None
        if isinstance(user, UserBase):
            filter_query = (User.username == user.username) & (User.email == user.email)

        if isinstance(user, int):
            filter_query = User.id == user

        found_user = self.session.query(User).filter(filter_query).first()
        return found_user

    def user_from_orm(self, user: User) -> UserModel:
        user_role = UserRoleModel.model_validate(user.role) if user.role else None
        user_model = UserModel.model_validate({**user.__dict__, "role": user_role})
        return user_model

    def user_exists(self, user: UserBase | int) -> bool:
        query = exists()
        if isinstance(user, int):
            query = query.where(User.id == user)
        if isinstance(user, UserBase):
            query = query.where(
                (User.username == user.username) | (User.email == user.email)
            )
        user_exists = self.session.query(query).scalar()
        return bool(user_exists)
