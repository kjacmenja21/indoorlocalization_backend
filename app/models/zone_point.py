from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class ZonePoint(Base):
    zoneId: Mapped[int] = mapped_column(Integer, primary_key=True)
    ordinalNumber: Mapped[int] = mapped_column(Integer)
    x: Mapped[Float] = mapped_column(Float)
    y: Mapped[Float] = mapped_column(Float)
