from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db_session
from app.database.repositories import UserRepository
from app.database.services import UserService


def get_user_service() -> UserService:
    return UserService(UserRepository(get_db_session()))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
