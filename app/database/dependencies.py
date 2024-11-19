from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.db import get_session

AsyncSession = Annotated[async_sessionmaker, Depends(get_session())]
