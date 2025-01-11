from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.services.asset_service import AssetService
from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.schemas.api.asset import AssetCreate, AssetModel, AssetPut
from tests.unit.util import get_asset, get_floormap


@pytest.fixture
def asset_service(mock_session):
    return AssetService(session=mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    floormaps = []
    for _ in range(10):
        floormaps.append(get_floormap("Test FloorMap"))
    mock_session.add_all(floormaps)
    mock_session.commit()

    assets = []
    for _ in range(10):
        floormap = mock_session.query(FloorMap).first()
        asset_data = get_asset(floormap)
        assets.append(
            Asset(
                **asset_data.model_dump(),
                **{"x": 0, "y": 0, "last_sync": datetime.now()}
            )
        )
    mock_session.add_all(assets)
    mock_session.commit()
    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    mock_session.query(Asset).delete()
    mock_session.query(FloorMap).delete()
    mock_session.commit()


def test_create_asset(asset_service: AssetService, mock_session: Session):
    floormap = mock_session.query(FloorMap).first()
    asset_data = AssetCreate(name="Test Asset", active=True, floormap_id=floormap.id)

    result = asset_service.create_asset(asset_data)

    expected = {
        "is_asset_model": True,
        "name_matches": True,
    }
    actual = {
        "is_asset_model": isinstance(result, AssetModel),
        "name_matches": result.name == asset_data.name,
    }

    assert expected == actual


def test_create_asset_conflict(asset_service: AssetService, mock_session: Session):
    floormap = mock_session.query(FloorMap).first()
    asset_data = get_asset(floormap)

    asset_service.create_asset(asset_data)
    with pytest.raises(HTTPException):
        asset_service.create_asset(asset_data)


def test_update_asset(asset_service: AssetService, mock_session: Session):
    floormap = mock_session.query(FloorMap).first()
    asset_data_create = get_asset(floormap)

    asset_id = asset_service.create_asset(asset_data_create).id

    asset_data_put = AssetPut(
        id=asset_id, name="Updated Asset", active=True, floormap_id=floormap.id
    )
    result = asset_service.update_asset(asset_data_put)

    expected = {
        "is_asset_model": True,
        "name_matches": True,
    }
    actual = {
        "is_asset_model": isinstance(result, AssetModel),
        "name_matches": result.name == asset_data_put.name,
    }

    assert expected == actual


def test_update_asset_not_found(asset_service: AssetService, mock_session: Session):
    import random

    asset_data = AssetPut(
        id=random.randrange(1000, 9999),
        name="Updated Asset",
        active=True,
        floormap_id=1,
    )

    with pytest.raises(HTTPException):
        asset_service.update_asset(asset_data)


def test_get_all_assets(asset_service: AssetService, mock_session: Session):
    assets = mock_session.query(Asset).all()

    result = asset_service.get_all_assets(active=None, page=0, limit=len(assets))

    expected = {
        "is_list": True,
        "length_matches": True,
        "are_asset_models": True,
    }

    actual = {
        "is_list": True,
        "length_matches": len(assets) == len(result),
        "are_asset_models": all(isinstance(asset, AssetModel) for asset in result),
    }

    assert expected == actual


def test_get_all_assets_pagination(asset_service: AssetService, mock_session: Session):
    assets = mock_session.query(Asset).all()
    page_size = 5
    total_pages = (len(assets) + page_size - 1) // page_size

    tests = []
    for page in range(total_pages):
        result = asset_service.get_all_assets(active=None, page=page, limit=page_size)

        expected = {
            "is_list": True,
            "length_matches": True,
            "are_asset_models": True,
        }

        actual = {
            "is_list": isinstance(result, list),
            "length_matches": len(result)
            == min(page_size, len(assets) - page * page_size),
            "are_asset_models": all(isinstance(asset, AssetModel) for asset in result),
        }

        tests.append(expected == actual)

    assert all(tests)


def test_get_asset_by_id(asset_service: AssetService, mock_session: Session):

    asset = mock_session.query(Asset).first()

    result = asset_service.get_asset(asset.id)

    expected = {
        "is_asset_model": True,
        "id_matches": True,
        "name_matches": True,
    }

    actual = {
        "is_asset_model": isinstance(result, AssetModel),
        "id_matches": result.id == asset.id,
        "name_matches": result.name == asset.name,
    }

    assert expected == actual


def test_get_asset_by_name(asset_service: AssetService, mock_session: Session):
    asset = mock_session.query(Asset).first()
    result_object = asset_service.get_asset(AssetModel.model_validate(asset))
    result_id = asset_service.get_asset(asset.id)

    results = [result_object, result_id]

    expected = {
        "results_are_asset_models": True,
        "ids_match": True,
        "names_match": True,
    }

    actual = {
        "results_are_asset_models": all(
            isinstance(result, AssetModel) for result in results
        ),
        "ids_match": result_object.id == result_id.id,
        "names_match": result_object.name == result_id.name,
    }

    assert expected == actual


def test_asset_exists_by_id(asset_service: AssetService, mock_session: Session):
    asset_id = mock_session.query(Asset).first().id
    result = asset_service.asset_exists(1)

    assert result is True


def test_asset_exists_by_name(asset_service: AssetService, mock_session: Session):
    asset_name = mock_session.query(Asset).first()
    result = asset_service.asset_exists(AssetModel.model_validate(asset_name))

    assert result is True
