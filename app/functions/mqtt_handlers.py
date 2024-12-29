import json
import logging

from fastapi import HTTPException
from pydantic import ValidationError
from shapely import Point
from sqlalchemy.orm import Session

from app.database.db import get_db_session_ctx
from app.database.services.asset_position_service import AssetPositionService
from app.database.services.floormap_service import FloormapService
from app.database.services.zone_position_service import ZonePositionService
from app.functions.exceptions import not_found
from app.schemas.api.asset_position import AssetPositionCreate
from app.schemas.api.zone_position import AssetZoneHistoryCreate
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


class MQTTAssetZoneMovementHandler(MQTTTopicHandler):
    def __init__(self) -> None:
        super().__init__()
        self.topic = "/test/topic"
        self.handler = self.handle

    async def handle(self, _topic: str, payload: bytes) -> None:
        try:
            data = json.loads(payload)
            message = MQTTAssetUpdateMessage.model_validate(data)

            position = AssetPositionCreate(
                assetId=message.id,
                floorMapId=message.floorMap,
                x=message.x,
                y=message.y,
            )

            with get_db_session_ctx() as session:
                self._validate_floormap(session, position)

                self._handle_position(session, position)

        except (ValidationError, HTTPException) as exception:
            logging.warning(
                "Error processing MQTT message: %s: %s",
                exception.__class__.__name__,
                exception,
            )

    def _validate_floormap(
        self, session: Session, position: AssetPositionCreate
    ) -> None:
        service = FloormapService(session)
        if service.floormap_exists(floormap=position.assetId):
            return
        raise not_found(f"Floormap with id {position.assetId} does not exist.")

    def _handle_position(self, session: Session, position: AssetPositionCreate) -> None:
        service = ZonePositionService(session)

        zone = service.find_zone_containing_point(
            floorMapId=position.floorMapId, test_point=Point(position.x, position.y)
        )

        current_zone = service.get_current_zone(asset_id=position.assetId)

        if zone and (not current_zone or current_zone.zoneId != zone.id):
            # The asset has entered a new zone
            if current_zone:
                # Mark the previous zone entry as exited
                service.mark_zone_exit(asset_id=position.assetId)
                # Create a new entry for the current zone
            service.create_asset_zone_position_entry(
                AssetZoneHistoryCreate(
                    assetId=position.assetId,
                    zoneId=zone.id,
                )
            )
        elif not zone and current_zone:
            # The asset has exited a zone and is no longer in any zone
            service.mark_zone_exit(asset_id=position.assetId)
