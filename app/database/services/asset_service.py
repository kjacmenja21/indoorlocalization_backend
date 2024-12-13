from typing import Optional

from pydantic import Field, PositiveInt
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.api.asset import AssetModel


class AssetService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_assets(
        self,
        active: Optional[bool],
        page: PositiveInt = Field(0, gt=-1),
        limit: PositiveInt = Field(1, gt=0),
    ) -> list[AssetModel]:
        query = self.session.query(Asset)

        if isinstance(active, bool):
            query = query.where(Asset.active == active)

        offset = page * limit
        asset_query: list[Asset] = query.limit(limit).offset(offset).all()

        assets: list[AssetModel] = []
        for asset in asset_query:
            asset_model = AssetModel.model_validate(asset)
            assets.append(asset_model)

        return assets
