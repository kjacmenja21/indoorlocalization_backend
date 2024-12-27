from pydantic import BaseModel, ConfigDict


class ZoneBase(BaseModel):
    name: str
    floorMapId: int
    color: int


class ZoneCreate(ZoneBase): ...


class ZoneModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
