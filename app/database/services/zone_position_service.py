from shapely import Point, Polygon
from sqlalchemy.orm import Session, joinedload

from app.models.history import AssetZoneHistory
from app.models.zone import Zone
from app.schemas.api.asset_position import AssetPositionModel
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

        after_start_date = (AssetZoneHistory.enterDateTime >= query.startDate) | (
            AssetZoneHistory.exitDateTime >= query.startDate
        )

        before_end_date = (AssetZoneHistory.enterDateTime <= query.endDate) | (
            AssetZoneHistory.exitDateTime <= query.endDate
        )

        results = (
            self.session.query(AssetZoneHistory)
            .filter(for_asset & (after_start_date | before_end_date))
            .all()
        )

        return [AssetZoneHistoryModel.model_validate(r) for r in results]

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
                continue

            polygon = Polygon(polygon_points)
            if polygon.contains(test_point):
                return zone

        return None

    def create_asset_zone_position_entry(
        self, entry: AssetZoneHistoryCreate
    ) -> AssetPositionModel:
        new_entry = AssetZoneHistory(**entry.model_dump())

        self.session.add(new_entry)
        self.session.commit()

        return AssetPositionModel.model_validate(new_entry)
