from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.common import Base


class Zone(Base):
    __tablename__ = "zone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    floorMapId: Mapped[int] = mapped_column(ForeignKey("floorMap.id"))
    color: Mapped[int] = mapped_column(Integer)

    # Relationship to ZonePoint with cascade delete
    points: Mapped[list["ZonePoint"]] = relationship(
        "ZonePoint",
        back_populates="zone",  # Optional back-reference
        cascade="all, delete-orphan",  # Ensure deletion cascades to points
    )


class ZonePoint(Base):
    __tablename__ = "zonePoint"
    zoneId: Mapped[int] = mapped_column(ForeignKey("zone.id"), primary_key=True)
    ordinalNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)

    # Back-reference to Zone
    zone: Mapped["Zone"] = relationship("Zone", back_populates="points")
