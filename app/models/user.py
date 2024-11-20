from sqlalchemy import Column, Integer, String

from app.models.common import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    contract = Column(String(20))
    password = Column(String(64))
    salt = Column(String(64))
    roleId = Column(Integer)
