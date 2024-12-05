from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    contract: Mapped[str] = mapped_column(String(20), nullable=True)
    password: Mapped[LargeBinary] = mapped_column(LargeBinary)
    salt: Mapped[LargeBinary] = mapped_column(LargeBinary)
    roleId: Mapped[int] = mapped_column(ForeignKey("userRole.id"))


class UserRole(Base):
    __tablename__ = "userRole"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
