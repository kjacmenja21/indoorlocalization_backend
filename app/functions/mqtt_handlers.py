import asyncio
import json
import logging

from fastapi import HTTPException, WebSocket
from pydantic import ValidationError
from shapely import Point
from sqlalchemy.orm import Session

from app.database.db import engine_handler
from app.database.services.asset_position_service import AssetPositionService
from app.database.services.asset_service import AssetService
from app.database.services.floormap_service import FloormapService
from app.database.services.zone_position_service import ZonePositionService
from app.schemas.api.asset_position import (
    AssetPositionCreate,
    AssetPositionEntitiesExist,
)
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

            with engine_handler.get_db_session_ctx() as session:
                service = AssetPositionService(session)
                service.create_asset_position_history(data=entry)
        except (ValidationError, HTTPException) as exception:
            logging.warning(
                "Error processing MQTT message: %s",
                exception,
            )


class MQTTAssetZoneMovementHandler(MQTTTopicHandler):
    def __init__(self, buffer_size: int = 10, flush_interval: float = 1.0) -> None:
        super().__init__()
        self.topic = "/test/topic"
        self.handler = self.handle

        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.buffer: list[AssetPositionCreate] = []
        self.buffer_lock = asyncio.Lock()

        self.__exists_cache: list[AssetPositionEntitiesExist] = []

        # Start the periodic flush task
        asyncio.create_task(self._periodic_flush())

    async def handle(self, _topic: str, payload: bytes) -> None:
        """Handle incoming messages and add them to the buffer."""
        try:
            data = json.loads(payload)
            message = MQTTAssetUpdateMessage.model_validate(data)

            position = AssetPositionCreate(
                assetId=message.id,
                floorMapId=message.floorMap,
                x=message.x,
                y=message.y,
            )

            async with self.buffer_lock:
                self.buffer.append(position)
                if len(self.buffer) >= self.buffer_size:
                    await self._flush_buffer()

        except Exception as e:
            logging.warning("Error processing MQTT message: %s", e)

    async def _periodic_flush(self):
        """Flush the buffer periodically based on the flush interval."""
        while True:
            await asyncio.sleep(self.flush_interval)
            async with self.buffer_lock:
                if self.buffer:
                    await self._flush_buffer()

    async def _flush_buffer(self):
        """Process all messages in the buffer."""
        buffer_copy = self.buffer[:]
        self.buffer.clear()

        if not buffer_copy:
            return

        try:
            with engine_handler.get_db_session_ctx() as session:
                # Validate and process each position in bulk
                positions = self._validate_and_prepare_positions(session, buffer_copy)
                self._process_positions(session, positions)
                session.commit()

        except Exception as e:
            logging.warning("Error during bulk processing: %s", e)

    def _validate_and_prepare_positions(
        self, session: Session, positions: list[AssetPositionCreate]
    ):
        """Validate floormaps and assets for all positions using bulk checks."""
        valid_positions = []
        floormap_service = FloormapService(session)
        asset_service = AssetService(session)

        floormap_ids = [position.floorMapId for position in positions]
        asset_ids = [position.assetId for position in positions]

        # Perform bulk checks for all floormaps and assets
        floormap_validity = floormap_service.floormap_exists_bulk(floormap_ids)
        asset_validity = asset_service.asset_exists_bulk(asset_ids)

        for position, floormap_exists, asset_exists in zip(
            positions, floormap_validity, asset_validity
        ):
            if not floormap_exists:
                logging.warning("Invalid floormap ID: %s", position.floorMapId)
                continue
            if not asset_exists:
                logging.warning("Invalid asset ID: %s", position.assetId)
                continue
            valid_positions.append(position)

        return valid_positions

    def _process_positions(self, session: Session, positions):
        """Process all validated positions in bulk."""
        zone_service = ZonePositionService(session)

        for position in positions:
            zone = zone_service.find_zone_containing_point(
                floorMapId=position.floorMapId, test_point=Point(position.x, position.y)
            )
            current_zone = zone_service.get_current_zone(asset_id=position.assetId)

            if zone and (not current_zone or current_zone.zoneId != zone.id):
                # Handle zone entry
                if current_zone:
                    zone_service.mark_zone_exit(asset_id=position.assetId)

                zone_service.create_asset_zone_position_entry(
                    AssetZoneHistoryCreate(
                        assetId=position.assetId,
                        zoneId=zone.id,
                    )
                )
            elif not zone and current_zone:
                # Handle zone exit
                zone_service.mark_zone_exit(asset_id=position.assetId)


class ConnectionManagerHandler(MQTTTopicHandler):
    def __init__(self) -> None:
        super().__init__()
        self.topic = "/test/topic"  # Subscribe to all topics using a wildcard
        self.handler = self.broadcast_message
        self.active_connections: list[WebSocket] = []

    async def add_connection(self, websocket: WebSocket):
        """Add a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(
            "WebSocket connection added. Total connections: %d",
            len(self.active_connections),
        )

    def remove_connection(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)
        logging.info(
            "WebSocket connection removed. Total connections: %d",
            len(self.active_connections),
        )

    async def broadcast_message(self, _topic: str, payload: bytes):
        """Broadcast an MQTT message to all connected WebSocket clients."""
        try:
            data = json.loads(payload)
            message = MQTTAssetUpdateMessage.model_validate(data)
        except (TypeError, ValidationError) as e:
            logging.warning("Error parsing payload: %s", e)
            return

        for connection in self.active_connections:
            try:
                await connection.send_text(message.model_dump_json())
            except Exception as e:
                logging.warning("Error sending message to WebSocket: %s", e)
                # Optionally remove the connection on error
                self.remove_connection(connection)


connection_manager = ConnectionManagerHandler()
