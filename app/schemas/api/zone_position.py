from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.api.common import round_up_to_hour


class AssetZonePositionQuery(BaseModel):
    assetId: int
    startDate: datetime = round_up_to_hour(datetime.now() - timedelta(days=1))
    endDate: datetime = round_up_to_hour(datetime.now())


class AssetZoneHistoryBase(BaseModel):
    assetId: int
    zoneId: int
    enterDateTime: datetime = Field(
        datetime.now(),
        example=round_up_to_hour(datetime.now()),
    )
    exitDateTime: Optional[datetime] = Field(
        default=None,
        example=round_up_to_hour(datetime.now() - timedelta(days=1)),
    )


class AssetZoneHistoryCreate(AssetZoneHistoryBase): ...


class AssetZoneHistoryModel(AssetZoneHistoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
