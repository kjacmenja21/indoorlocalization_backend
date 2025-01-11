from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class AssetPositionHistory(Base):
    __tablename__ = "assetPositionHistory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assetId: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    floorMapId: Mapped[int] = mapped_column(ForeignKey("floorMap.id"))


class AssetZoneHistory(Base):
    __tablename__ = "assetZoneHistory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assetId: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    zoneId: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    enterDateTime: Mapped[datetime] = mapped_column(DateTime)
    exitDateTime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
