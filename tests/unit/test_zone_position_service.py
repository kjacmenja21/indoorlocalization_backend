import random
from datetime import datetime, timedelta

import pytest
from shapely.geometry import Point, Polygon
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
    for i in range(3):
        zone_model = get_zone(
            "Seeded Zone", floormap, center=Point(i * 1000, i * 1000)
        )[1]
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
            exit_date = date + timedelta(days=random.randint(0, 2))

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
    mock_session.query(FloorMap, Asset, Zone, AssetZoneHistory, ZonePoint).delete()
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
    asset = mock_session.query(Asset).first()
    zone = mock_session.query(Zone).first()

    mock_session.add(
        AssetZoneHistory(
            assetId=asset.id,
            zoneId=zone.id,
            enterDateTime=datetime(2023, 6, 19),
            exitDateTime=None,
        )
    )
    mock_session.commit()
    result = zone_position_service.get_current_zone(asset.id)

    expected = {
        "exit_date_is_none": True,
        "asset_id_is_correct": asset.id,
        "zone_id_is_correct": zone.id,
    }

    actual = {
        "exit_date_is_none": result.exitDateTime is None,
        "asset_id_is_correct": result.assetId,
        "zone_id_is_correct": result.zoneId,
    }
    assert expected == actual


def test_mark_zone_exit(
    zone_position_service: ZonePositionService, mock_session: Session
):
    asset = mock_session.query(Asset).first()
    zone = mock_session.query(Zone).first()
    mock_session.query(AssetZoneHistory).where(
        AssetZoneHistory.exitDateTime == None
    ).delete()
    mock_session.commit()
    history = AssetZoneHistory(
        assetId=asset.id,
        zoneId=zone.id,
        enterDateTime=datetime(2023, 6, 19),
        exitDateTime=None,
    )
    mock_session.add(history)
    mock_session.commit()
    zone_position_service.mark_zone_exit(asset.id)

    current_zone = zone_position_service.get_current_zone(asset.id)
    expected = {
        "current_zone_is_none": None,
        "history_is_updated": True,
    }

    actual = {
        "current_zone_is_none": current_zone,
        "history_is_updated": history.exitDateTime is not None,
    }
    assert expected == actual


def test_find_zone_containing_point(
    zone_position_service: ZonePositionService, mock_session: Session
):
    floormap = mock_session.query(FloorMap).first()
    zone = mock_session.query(Zone).first()
    zone_points = zone.points
    polygon = Polygon([(point.x, point.y) for point in zone_points])

    min_x = min(point.x for point in zone_points)
    max_x = max(point.x for point in zone_points)
    min_y = min(point.y for point in zone_points)
    max_y = max(point.y for point in zone_points)

    test_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
    while not polygon.contains(test_point):
        test_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))

    zone = zone_position_service.find_zone_containing_point(floormap.id, test_point)

    assert zone is not None


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
