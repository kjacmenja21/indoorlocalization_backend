import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.settings import db_settings

logger = logging.getLogger(__name__)

engine = create_engine(db_settings.db_dsn)


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
