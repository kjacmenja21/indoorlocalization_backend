from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    contract: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(64))
    salt: Mapped[str] = mapped_column(String(64))
    roleId: Mapped[int] = mapped_column(ForeignKey("userRole.id"))


class UserRole(Base):
    __tablename__ = "userRole"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
