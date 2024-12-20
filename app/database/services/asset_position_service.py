from sqlalchemy.orm import Session

from app.models.history import AssetPositionHistory
from app.schemas.api.asset_position import AssetPositionModel, AssetPositionQuery


class AssetPositionService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_asset_position_history(
        self, data: AssetPositionQuery
    ) -> list[AssetPositionModel]:
        query = self.session.query(AssetPositionHistory).where(
            (AssetPositionHistory.assetId == data.id)
        )

        results = query.all()
        # results = query.filter(
        #     (AssetPositionHistory.dateTime >= data.startDate)
        #     & (AssetPositionHistory.dateTime <= data.endDate)
        # ).all()
        print(results)
        return [AssetPositionModel.model_validate(r) for r in results]
