from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict


def round_up_to_hour(dt: datetime) -> datetime:
    """Helper function to truncate seconds and microseconds, and round up to the next hour."""
    # Truncate seconds and microseconds
    dt = dt.replace(second=0, microsecond=0)
    # If minutes are non-zero, round up to the next hour
    if dt.minute > 0:
        dt += timedelta(hours=1)
    # Reset minutes to 0
    dt = dt.replace(minute=0)
    return dt


class AssetPositionCreate(BaseModel):
    x: float
    y: float
    timestamp: datetime = datetime.now()
    assetId: int
    floorMapId: int


class AssetPositionBase(BaseModel):
    id: int


class AssetPositionQuery(AssetPositionBase):
    startDate: datetime = round_up_to_hour(datetime.now() - timedelta(days=1))
    endDate: datetime = round_up_to_hour(datetime.now())


class AssetPositionModel(AssetPositionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
