from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.api.common import PaginationBase


class AssetBase(BaseModel):
    name: str
    active: bool
    floormap_id: int


class AssetCreate(AssetBase):
    model_config = ConfigDict(from_attributes=True)


class AssetModel(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    x: float
    y: float
    lastSync: datetime


class AssetPagination(PaginationBase):
    page: list[AssetModel]
