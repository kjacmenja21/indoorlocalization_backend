from datetime import datetime

from pydantic import BaseModel


class AssetZonePositionQuery(BaseModel):
    assetId: int
    startDate: datetime
    endDate: datetime
