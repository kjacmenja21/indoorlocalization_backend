from sqlalchemy.orm import Session

from app.models.history import AssetZoneHistory
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

    def create_asset_zone_position_entry(
        self, entry: AssetZoneHistoryCreate
    ) -> AssetPositionModel:
        new_entry = AssetZoneHistory(**entry.model_dump())

        self.session.add(new_entry)
        self.session.commit()

        return AssetPositionModel.model_validate(new_entry)
