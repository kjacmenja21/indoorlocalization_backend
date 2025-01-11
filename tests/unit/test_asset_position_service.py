from datetime import datetime
from random import randint

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.services.asset_position_service import AssetPositionService
from app.functions.exceptions import not_found
from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.models.history import AssetPositionHistory
from app.schemas.api.asset_position import AssetPositionCreate, AssetPositionQuery
from tests.unit.util import create_assets, create_floormaps


@pytest.fixture
def asset_position_service(mock_session: Session) -> AssetPositionService:
    return AssetPositionService(mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    floormaps = []
    create_floormaps(floormaps, 1)
    mock_session.add_all(floormaps)
    mock_session.commit()

    assets = []
    create_assets(mock_session, assets)
    mock_session.add_all(assets)
    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    mock_session.query(FloorMap, Asset, AssetPositionHistory).delete()


def test_get_asset_position_history(
    asset_position_service: AssetPositionService, mock_session: Session
):
    asset = mock_session.query(Asset).first()
    data = AssetPositionQuery(
        id=asset.id, startDate=datetime(2023, 1, 1), endDate=datetime(2023, 1, 31)
    )
    mock_history = [
        AssetPositionHistory(
            assetId=asset.id,
            timestamp=datetime(2023, 1, 10),
            x=1.0,
            y=1.0,
            floorMapId=asset.floormap_id,
        ),
        AssetPositionHistory(
            assetId=asset.id,
            timestamp=datetime(2023, 1, 20),
            x=2.0,
            y=2.0,
            floorMapId=asset.floormap_id,
        ),
    ]
    mock_session.add_all(mock_history)
    mock_session.commit()

    result = asset_position_service.get_asset_position_history(data)

    assert True


def test_create_asset_position_history(
    asset_position_service: AssetPositionService, mock_session: Session
):
    asset = mock_session.query(Asset).first()
    data = AssetPositionCreate(
        assetId=asset.id,
        floorMapId=asset.floormap_id,
        timestamp=datetime(2023, 1, 10),
        x=1.0,
        y=1.0,
    )

    asset_position_service.create_asset_position_history(data)

    position = mock_session.query(AssetPositionHistory).first()

    assert position.assetId == data.assetId


def test_create_asset_position_history_floormap_not_found(
    asset_position_service: AssetPositionService, mock_session: Session
):
    asset = mock_session.query(Asset).first()
    wrong_floormap_data = AssetPositionCreate(
        assetId=asset.id,
        floorMapId=randint(1000, 9999),
        timestamp=datetime(2023, 1, 10),
        x=1.0,
        y=1.0,
    )

    with pytest.raises(HTTPException):
        asset_position_service.create_asset_position_history(wrong_floormap_data)


def test_create_asset_position_history_asset_not_found(
    asset_position_service: AssetPositionService, mock_session: Session
):
    floormap = mock_session.query(FloorMap).first()
    wrong_asset_data = AssetPositionCreate(
        assetId=randint(1000, 9999),
        floorMapId=floormap.id,
        timestamp=datetime(2023, 1, 10),
        x=1.0,
        y=1.0,
    )

    with pytest.raises(HTTPException):
        asset_position_service.create_asset_position_history(wrong_asset_data)
