from typing import Annotated

from fastapi import Depends

from app.database.db import get_db_session
from app.database.services import UserService


def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
