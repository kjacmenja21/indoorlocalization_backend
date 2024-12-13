from datetime import datetime
from typing import Optional

from pydantic import Field, PositiveInt
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict, not_found
from app.models.asset import Asset
from app.schemas.api.asset import AssetBase, AssetCreate, AssetModel, AssetPut


class AssetService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_asset(self, asset: AssetCreate) -> AssetModel:
        if self.asset_exists(asset):
            raise conflict()
        new_asset = Asset(
            **asset.model_dump(), **{"x": 0, "y": 0, "last_sync": datetime.now()}
        )

        self.session.add(new_asset)
        self.session.commit()

        return AssetModel.model_validate(new_asset)

    def update_asset(self, asset: AssetPut):
        if not self.asset_exists(asset):
            raise not_found(f"Asset with id={asset.id} was not found.")

        updated_asset = self.session.query(Asset).where(Asset.id == asset.id).first()

        if not updated_asset:
            raise not_found()

        changed_fields = asset.model_dump(
            exclude_unset=True, exclude_none=True, exclude=[""]
        )

        for field, value in changed_fields.items():
            if value is not None:
                setattr(updated_asset, field, value)

        self.session.commit()

        return AssetModel.model_validate(updated_asset)

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

    def get_asset(self, asset: AssetBase | int) -> AssetModel:
        filter_query = None
        if isinstance(asset, AssetBase):
            filter_query = Asset.name == asset.name
        if isinstance(asset, int):
            filter_query = Asset.id == asset

        found_asset = self.session.query(Asset).filter(filter_query).first()

        return AssetModel.model_validate(found_asset)

    def asset_exists(self, asset: AssetBase) -> bool:
        query = exists().where((Asset.name == asset.name))
        asset_exists = self.session.query(query).scalar()
        return bool(asset_exists)
