import random
from datetime import datetime, timedelta

import pytest
from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.database.services.zone_position_service import ZonePositionService
from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.models.history import AssetZoneHistory
from app.models.zone import Zone, ZonePoint
from app.schemas.api.zone_position import AssetZoneHistoryCreate, AssetZonePositionQuery
from tests.unit.util import get_asset, get_floormap, get_zone


@pytest.fixture
def zone_position_service(mock_session) -> ZonePositionService:
    return ZonePositionService(mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    floormap = get_floormap("Test FloorMap")
    mock_session.add(floormap)
    mock_session.commit()

    assets: list[Asset] = []
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

    zones: list[Zone] = []
    for _ in range(3):
        zone_model = get_zone("Seeded Zone", floormap)[1]
        zone = Zone(**zone_model.model_dump(exclude=["points"]))
        zone.points = []
        for point in zone_model.points:
            zone.points.append(
                ZonePoint(ordinalNumber=point.ordinalNumber, x=point.x, y=point.y)
            )
        zones.append(zone)

    mock_session.add_all(zones)
    mock_session.commit()

    histories = []

    for asset in assets:
        for _ in range(20):
            zone = random.choice(zones)
            date = datetime(2023, 6, 1) + timedelta(days=random.randint(0, 10))
            exit_date = random.choice(
                [None, date + timedelta(days=random.randint(0, 2))]
            )
            histories.append(
                AssetZoneHistory(
                    assetId=asset.id,
                    zoneId=zone.id,
                    enterDateTime=date,
                    exitDateTime=exit_date,
                )
            )
    mock_session.add_all(histories)
    mock_session.commit()
    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    mock_session.query(FloorMap, Asset, Zone, AssetZoneHistory).delete()
    mock_session.commit()


def test_get_asset_zone_position_history(
    zone_position_service: ZonePositionService, mock_session: Session
):

    asset = mock_session.query(Asset).first()
    date = datetime(2023, 6, 1)
    query = AssetZonePositionQuery(
        assetId=asset.id,
        startDate=date,
        endDate=date + timedelta(days=20),
    )

    result = zone_position_service.get_asset_zone_position_history(query)

    expected = {
        "positions_exist": True,
        "is_list": True,
    }

    actual = {
        "positions_exist": any(result),
        "is_list": isinstance(result, list),
    }

    assert expected == actual


def test_get_current_zone(
    zone_position_service: ZonePositionService, mock_session: Session
):
    mock_session.query(Zone).delete()
    mock_session.commit()

    zone_model = get_zone("Test Zone", mock_session.query(FloorMap).first())[1]
    zone = Zone(**zone_model.model_dump(exclude=["points"]))

    points = []
    for point in zone_model.points:
        points.append(ZonePoint())
    mock_session.add(zone)
    mock_session.commit()

    asset = mock_session.query(Asset).first()
    entry = AssetZoneHistoryCreate(
        assetId=asset.id,
        zoneId=zone.id,
        enterDateTime=datetime(2023, 6, 1),
        exitDateTime=None,
    )
    zone_position_service.create_asset_zone_position_entry(entry)
    result = zone_position_service.get_current_zone(asset.id)

    assert True


def test_mark_zone_exit(
    zone_position_service: ZonePositionService, mock_session: Session
):

    asset = mock_session.query(Asset).first()
    zone_position_service.mark_zone_exit(asset.id)


def test_find_zone_containing_point(
    zone_position_service: ZonePositionService, mock_session: Session
):
    floormap = mock_session.query(FloorMap).first()
    zone = mock_session.query(Zone).first()
    test_point = Point(zone.points[0].x, zone.points[0].y)
    result = zone_position_service.find_zone_containing_point(floormap.id, test_point)

    assert False


def test_create_asset_zone_position_entry(
    zone_position_service: ZonePositionService, mock_session: Session
):
    asset = mock_session.query(Asset).first()
    zone = mock_session.query(Zone).first()
    entry = AssetZoneHistoryCreate(
        assetId=asset.id,
        zoneId=zone.id,
        enterDateTime=datetime(2023, 6, 1),
        exitDateTime=None,
    )

    result = zone_position_service.create_asset_zone_position_entry(entry)

    assert result.assetId == asset.id
