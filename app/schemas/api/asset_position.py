from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetPositionCreate(BaseModel):
    x: float
    y: float
    timestamp: datetime = datetime.now()
    assetId: int
    floorMapId: int


class AssetPositionBase(BaseModel):
    id: int


class AssetPositionQuery(AssetPositionBase):
    startDate: datetime
    endDate: datetime


class AssetPositionModel(AssetPositionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
