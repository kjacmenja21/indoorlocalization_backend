from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    contract: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(64))
    salt: Mapped[str] = mapped_column(String(64))
    roleId: Mapped[int] = mapped_column(Integer)
