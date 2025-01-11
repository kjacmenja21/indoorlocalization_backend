import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.services.zone_service import ZoneService
from app.models.floor_map import FloorMap
from app.models.zone import Zone
from app.schemas.api.zone import ZoneModel
from tests.unit.util import create_floormaps, get_floormap, get_zone


@pytest.fixture
def zone_service(mock_session: Session) -> ZoneService:
    return ZoneService(mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    floormaps = []
    create_floormaps(floormaps, 10)
    mock_session.add_all(floormaps)
    mock_session.commit()

    zones = []
    for floormap in floormaps:
        zones.append(
            Zone(**get_zone("Seeded Zone", floormap)[1].model_dump(exclude=["points"]))
        )
    mock_session.add_all(zones)
    mock_session.commit()

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want

    mock_session.query(Zone, FloorMap).delete()
    mock_session.commit()


def test_get_zones_in_floormap(zone_service: ZoneService, mock_session: Session):
    floormap = mock_session.query(FloorMap).first()
    zone = get_zone("Existing Zone", floormap)[1]
    zone_service.create_zone(zone)

    # Execute
    result = zone_service.get_zones_in_floormap(floormap.id)

    # Verify
    expected = {
        "is_not_empty": True,
        # "is_zone_model": True,
        "name_matches": True,
        "is_list": True,
    }

    actual = {
        "is_not_empty": bool(result),
        "is_list": isinstance(result, list),
        # "is_zone_model": isinstance(result[0], ZoneModel),
        "name_matches": result.pop().name == zone.name,
    }

    assert expected == actual


def test_create_zone(zone_service: ZoneService, mock_session: Session):
    # Setup
    floormap = mock_session.query(FloorMap).first()
    color, zone_create = get_zone("New Zone", floormap)

    # Execute
    result = zone_service.create_zone(zone_create)

    # Verify
    expected = {
        "is_zone_model": True,
        "name_matches": True,
        "color_matches": True,
    }
    actual = {
        "is_zone_model": isinstance(result, ZoneModel),
        "name_matches": result.name == zone_create.name,
        "color_matches": result.color == color,
    }

    assert expected == actual


def test_create_zone_conflict(zone_service: ZoneService, mock_session: Session):
    mock_session.add(get_floormap("Test FloorMap"))
    floormap = mock_session.query(FloorMap).first()
    zone_create = get_zone("Confict Zone", floormap)[1]
    zone_service.create_zone(zone_create)
    # Execute & Verify
    with pytest.raises(HTTPException):
        zone_service.create_zone(zone_create)


def test_delete_zone_by_id(zone_service: ZoneService, mock_session: Session):
    # Setup
    mock_session.add(get_floormap("Test FloorMap"))
    floormap = mock_session.query(FloorMap).first()
    zone = zone_service.create_zone(get_zone("Delete Zone", floormap)[1])

    # Execute
    zone_service.delete_zone_by_id(zone.id)

    # Verify
    deleted_zone = mock_session.query(Zone).filter_by(id=zone.id).first()
    assert deleted_zone is None


def test_zone_exists(zone_service: ZoneService, mock_session: Session):
    # Setup
    zone = get_zone("Existing Zone", mock_session.query(FloorMap).first())[1]
    exsiting_zone = zone_service.create_zone(zone)
    # Execute
    exists = zone_service.zone_exists(exsiting_zone.id)

    # Verify
    assert exists is True


def test_zone_not_exists(zone_service: ZoneService, mock_session: Session):
    # Execute
    exists = zone_service.zone_exists(999)

    # Verify
    assert exists is False
