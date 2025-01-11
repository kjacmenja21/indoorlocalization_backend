from datetime import datetime

import pytest
from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.database.services.zone_position_service import ZonePositionService
from app.models.history import AssetZoneHistory
from app.models.zone import Zone
from app.schemas.api.zone_position import AssetZoneHistoryCreate, AssetZonePositionQuery


@pytest.fixture
def zone_position_service(mock_session) -> ZonePositionService:
    return ZonePositionService(mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    yield


def test_get_asset_zone_position_history(
    zone_position_service: ZonePositionService, session: Session
):
    result = zone_position_service.get_asset_zone_position_history(query)

    assert len(result) == 1
    assert result[0].assetId == 1


def test_get_current_zone(zone_position_service: ZonePositionService, session: Session):
    mock_history = AssetZoneHistory(
        assetId=1, enterDateTime=datetime(2023, 6, 1), exitDateTime=None
    )
    session.query().filter().one_or_none.return_value = mock_history

    result = zone_position_service.get_current_zone(1)

    assert result is not None
    assert result.assetId == 1


def test_mark_zone_exit(zone_position_service: ZonePositionService, session: Session):
    mock_history = AssetZoneHistory(
        assetId=1, enterDateTime=datetime(2023, 6, 1), exitDateTime=None
    )
    session.query().filter().one_or_none.return_value = mock_history

    zone_position_service.mark_zone_exit(1)

    assert mock_history.exitDateTime is not None
    session.add.assert_called_once_with(mock_history)
    session.commit.assert_called_once()


def test_find_zone_containing_point(
    zone_position_service: ZonePositionService, session: Session
):
    mock_zone = Zone(
        id=1, floorMapId=1, points=[Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
    )
    session.query().filter().options().all.return_value = [mock_zone]

    test_point = Point(0.5, 0.5)
    result = zone_position_service.find_zone_containing_point(1, test_point)

    assert result is not None
    assert result.id == 1


def test_create_asset_zone_position_entry(
    zone_position_service: ZonePositionService, session: Session
):
    entry = AssetZoneHistoryCreate(
        assetId=1, zoneId=1, enterDateTime=datetime(2023, 6, 1), exitDateTime=None
    )
    mock_history = AssetZoneHistory(
        assetId=1, zoneId=1, enterDateTime=datetime(2023, 6, 1), exitDateTime=None
    )
    session.add.return_value = None
    session.commit.return_value = None
    session.query().filter().one_or_none.return_value = mock_history

    result = zone_position_service.create_asset_zone_position_entry(entry)

    assert result.assetId == 1
    assert result.zoneId == 1
    session.add.assert_called_once()
    session.commit.assert_called_once()
