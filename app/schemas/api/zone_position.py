from datetime import datetime, timedelta

from pydantic import BaseModel

from app.schemas.api.common import round_up_to_hour


class AssetZonePositionQuery(BaseModel):
    assetId: int
    startDate: datetime = round_up_to_hour(datetime.now() - timedelta(days=1))
    endDate: datetime = round_up_to_hour(datetime.now())
