import json
import logging

from fastapi import HTTPException
from pydantic import ValidationError

from app.database.db import get_db_session_ctx
from app.database.services.asset_position_service import AssetPositionService
from app.schemas.api.asset_position import AssetPositionCreate
from app.schemas.mqtt.handler import MQTTAssetUpdateMessage, MQTTTopicHandler


class MQTTCoordinateHandler(MQTTTopicHandler):
    def __init__(self) -> None:
        super().__init__()
        self.topic = "/test/topic"
        self.handler = self.handle

    async def handle(self, _topic: str, payload: bytes) -> None:
        try:
            data = json.loads(payload)
            message = MQTTAssetUpdateMessage.model_validate(data)

            entry = AssetPositionCreate(
                assetId=message.id,
                floorMapId=message.floorMap,
                x=message.x,
                y=message.y,
            )

            with get_db_session_ctx() as session:
                service = AssetPositionService(session)
                service.create_asset_position_history(data=entry)
        except (ValidationError, HTTPException) as exception:
            logging.warning(
                "Error processing MQTT message: %s: %s",
                exception.__class__.__name__,
                exception,
            )
