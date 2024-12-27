from pydantic import BaseModel


class ZoneBase(BaseModel):
    name: str
    floorMapId: int
    color: int


class ZoneCreate(ZoneBase): ...


class ZoneModel(BaseModel):
    id: int
