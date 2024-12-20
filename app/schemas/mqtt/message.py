from pydantic import BaseModel


class MQTTAssetUpdateMessage(BaseModel):
    id: int
    x: float
    y: float
    floorMap: int
