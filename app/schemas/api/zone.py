from pydantic import BaseModel, ConfigDict


class ZonePointBase(BaseModel):
    ordinalNumber: int
    x: float
    y: float


class ZonePointCreate(ZonePointBase): ...


class ZonePointModel(ZonePointBase):
    zoneId: int


class ZoneBase(BaseModel):
    name: str
    floorMapId: int
    color: int
    points: list[ZonePointCreate]


class ZoneCreate(ZoneBase): ...


class ZoneModel(ZoneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
