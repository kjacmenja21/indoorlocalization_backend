from sqlalchemy.orm import Session

from app.functions.exceptions import not_found
from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.models.history import AssetPositionHistory
from app.schemas.api.asset_position import (
    AssetPositionCreate,
    AssetPositionModel,
    AssetPositionQuery,
)


class AssetPositionService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_asset_position_history(
        self, data: AssetPositionQuery
    ) -> list[AssetPositionModel]:
        query = self.session.query(AssetPositionHistory).where(
            (AssetPositionHistory.assetId == data.id)
        )

        results = query.filter(
            (AssetPositionHistory.timestamp >= data.startDate)
            & (AssetPositionHistory.timestamp <= data.endDate)
        ).all()
        return [AssetPositionModel.model_validate(r) for r in results]

    def create_asset_position_history(self, data: AssetPositionCreate):
        floormap = (
            self.session.query(FloorMap).where(FloorMap.id == data.floorMapId).first()
        )
        asset = self.session.query(Asset).where(Asset.id == data.assetId).first()

        if not floormap:
            raise not_found(f"Floor map with id {data.floorMapId} does not exist.")
        if not asset:
            raise not_found(f"Asset with id {data.assetId} does not exist.")

        asset_position = AssetPositionHistory(**data.model_dump())

        self.session.add(asset_position)
        self.session.commit()
