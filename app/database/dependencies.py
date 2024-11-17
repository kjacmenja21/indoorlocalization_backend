from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import create_async_session, create_sa_engine

DatabaseSessionAsync = Annotated[
    AsyncSession,
    Depends(lambda: create_async_session(create_sa_engine()), use_cache=True),
]
