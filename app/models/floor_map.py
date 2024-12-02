from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import Base


class FloorMap(Base):
    __tablename__ = "floorMap"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    image: Mapped[OID] = mapped_column(OID)
    offsetX: Mapped[float] = mapped_column(Float)
    offsetY: Mapped[float] = mapped_column(Float)
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
