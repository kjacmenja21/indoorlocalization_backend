import logging
from datetime import datetime

from shapely import Point, Polygon
from sqlalchemy.orm import Session, joinedload

from app.models.history import AssetZoneHistory
from app.models.zone import Zone
from app.schemas.api.zone_position import (
    AssetZoneHistoryCreate,
    AssetZoneHistoryModel,
    AssetZonePositionQuery,
)


class ZonePositionService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_asset_zone_position_history(
        self, query: AssetZonePositionQuery
    ) -> list[AssetZoneHistoryModel]:

        for_asset = AssetZoneHistory.assetId == query.assetId

        entered_during_period = (AssetZoneHistory.enterDateTime >= query.startDate) & (
            AssetZoneHistory.enterDateTime <= query.endDate
        )

        results = (
            self.session.query(AssetZoneHistory)
            .filter(for_asset & entered_during_period)
            .all()
        )
        return [AssetZoneHistoryModel.model_validate(r) for r in results]

    def get_current_zone(self, asset_id: int) -> AssetZoneHistory | None:
        """
        Get the current active zone for the given asset.
        """
        active_zones = (
            self.session.query(AssetZoneHistory)
            .filter(
                AssetZoneHistory.assetId == asset_id,
                AssetZoneHistory.exitDateTime == None,
            )
            .all()
        )

        if len(active_zones) > 1:
            logging.error("Multiple active zones found for asset %d", asset_id)
            raise Exception("Multiple active zones found for asset")

        return active_zones[0] if active_zones else None

    def mark_zone_exit(self, asset_id: int):
        """
        Mark the current zone entry for the given asset as exited.
        """
        current_zone = self.get_current_zone(asset_id)
        if current_zone:
            current_zone.exitDateTime = datetime.now()
            self.session.add(current_zone)
            self.session.commit()

    def find_zone_containing_point(
        self, floorMapId: int, test_point: Point
    ) -> Zone | None:
        """
        Find the zone in a specific floor map that contains the given point.

        :param floor_map_id: The ID of the floor map.
        :param x: X-coordinate of the point.
        :param y: Y-coordinate of the point.
        :return: The Zone object that contains the point, or None if no zone matches.
        """
        zones = (
            self.session.query(Zone)
            .filter(Zone.floorMapId == floorMapId)
            .options(joinedload(Zone.points))  # Load points to minimize queries
            .all()
        )

        for zone in zones:
            polygon_points = [(point.x, point.y) for point in zone.points]
            if not polygon_points:
                logging.warning("Zone %d has no points defined.", zone.id)
                continue

            polygon = Polygon(polygon_points)
            if polygon.contains(test_point):
                return zone

        return None

    def create_asset_zone_position_entry(
        self, entry: AssetZoneHistoryCreate
    ) -> AssetZoneHistoryModel:
        new_entry = AssetZoneHistory(**entry.model_dump())

        self.session.add(new_entry)
        self.session.commit()

        return AssetZoneHistoryModel.model_validate(new_entry)
