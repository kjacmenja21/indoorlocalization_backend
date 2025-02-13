from datetime import datetime
from typing import Optional

from pydantic import Field, PositiveInt
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict, not_found
from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.schemas.api.asset import AssetBase, AssetCreate, AssetModel, AssetPut


class AssetService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_asset(self, asset: AssetCreate) -> AssetModel:
        floormap = (
            self.session.query(FloorMap).where(FloorMap.id == asset.floormap_id).first()
        )
        if floormap is None:
            raise not_found()
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

    def get_asset_pages(self, page_size: int):
        total_items = self.session.query(Asset).count()
        return (total_items + page_size - 1) // page_size

    def get_asset(self, asset: AssetBase | int) -> AssetModel:
        filter_query = None
        if isinstance(asset, AssetBase):
            filter_query = Asset.name == asset.name
        if isinstance(asset, int):
            filter_query = Asset.id == asset

        found_asset = self.session.query(Asset).filter(filter_query).first()

        return AssetModel.model_validate(found_asset)

    def asset_exists(self, asset: AssetBase | int) -> bool:
        query = exists()
        if isinstance(asset, int):
            query = query.where(Asset.id == asset)
        elif hasattr(asset, "id"):
            query = query.where(Asset.id == asset.id)
        else:
            query = query.where(Asset.name == asset.name)

        asset_exists = self.session.query(query).scalar()
        return bool(asset_exists)

    def asset_exists_bulk(self, asset_ids: list[int]) -> list[bool]:
        """Bulk check if assets exist."""
        if not asset_ids:
            return []

        # Query the database to check if the assets exist
        existing_assets = (
            self.session.query(Asset.id).filter(Asset.id.in_(asset_ids)).all()
        )

        existing_asset_ids = {asset.id for asset in existing_assets}
        return [asset_id in existing_asset_ids for asset_id in asset_ids]
