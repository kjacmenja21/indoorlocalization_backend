from sqlalchemy import Column, Integer, Serial, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Serial, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    contract = Column(String(20))
    password = Column(String(64))
    salt = Column(String(64))
    roleId = Column(Integer)
