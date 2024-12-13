from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class Asset(Base):
    __tablename__ = "asset"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    last_sync: Mapped[DateTime] = mapped_column(DateTime)
    floormap_id: Mapped[int] = mapped_column(ForeignKey("floorMap.id"))
    active: Mapped[bool] = mapped_column(BIT)
