from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class AssetPositionHistory(Base):
    __tablename__ = "assetPositionHistory"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    assetId: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    dateTime: Mapped[datetime] = mapped_column(DateTime)
    floorMapId: Mapped[int] = mapped_column(ForeignKey("floorMap.id"))
