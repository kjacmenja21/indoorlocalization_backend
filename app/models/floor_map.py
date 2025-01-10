from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class FloorMap(Base):
    __tablename__ = "floorMap"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    image: Mapped[bytes] = mapped_column(BYTEA)
    image_type: Mapped[str] = mapped_column(String(10), default="png")
    tx: Mapped[float] = mapped_column(Float)
    ty: Mapped[float] = mapped_column(Float)
    tw: Mapped[float] = mapped_column(Float)
    th: Mapped[float] = mapped_column(Float)
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
