from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.api.common import round_up_to_hour


class AssetPositionCreate(BaseModel):
    x: float
    y: float
    timestamp: datetime = Field(default_factory=datetime.now)
    assetId: int
    floorMapId: int


class AssetPositionBase(BaseModel):
    id: int


class AssetPositionQuery(AssetPositionBase):
    startDate: datetime = Field(
        default_factory=lambda: round_up_to_hour(datetime.now() - timedelta(days=1))
    )
    endDate: datetime = Field(
        default_factory=lambda: round_up_to_hour(datetime.now()),
    )


class AssetPositionModel(AssetPositionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AssetPositionEntitiesExist(BaseModel):
    position: AssetPositionCreate
    floormap_exists: bool
    asset_exists: bool
