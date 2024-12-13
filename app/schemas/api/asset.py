from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    name: str
    active: bool
    floormap_id: int
    x: float
    y: float
    lastSync: datetime


class AssetModel(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
