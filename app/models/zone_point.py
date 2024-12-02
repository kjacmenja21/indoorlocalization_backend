from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class Zone(Base):
    __tablename__ = "zone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    floorMapId: Mapped[int] = mapped_column(ForeignKey("floorMap.id"))


class ZonePoint(Base):
    __tablename__ = "zonePoint"
    zoneId: Mapped[int] = mapped_column(Integer, primary_key=True)
    ordinalNumber: Mapped[int] = mapped_column(Integer)
    x: Mapped[Float] = mapped_column(Float)
    y: Mapped[Float] = mapped_column(Float)
