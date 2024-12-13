from typing import Optional

from pydantic import Field, PositiveInt
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict
from app.models.asset import Asset
from app.schemas.api.asset import AssetBase, AssetCreate, AssetModel


class AssetService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_asset(self, asset: AssetCreate) -> AssetModel:
        if self.asset_exists(asset):
            raise conflict()
        new_asset = Asset(**asset.model_dump())

        self.session.add(new_asset)
        self.session.commit()

        return AssetModel.model_validate(new_asset)

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

    def asset_exists(self, asset: AssetBase) -> bool:
        query = exists().where((Asset.name == asset.name))
        asset_exists = self.session.query(query).scalar()
        return bool(asset_exists)
