from typing import Annotated

from fastapi import Depends

from app.database.db import get_db_session
from app.database.repositories import UserRepository
from app.database.services import UserService
from app.models.user import User


def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(UserRepository(model=User, session=session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
