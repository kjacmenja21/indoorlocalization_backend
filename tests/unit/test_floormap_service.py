from functools import lru_cache

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.services.floormap_service import FloormapService
from app.models.floor_map import FloorMap
from app.schemas.api.floormap import FloormapBase, FloormapCreate, FloormapModel


@pytest.fixture
def floormap_service(mock_session: Session) -> FloormapService:
    return FloormapService(session=mock_session)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    mock_session.query(FloorMap).delete()


@lru_cache(maxsize=32)
def get_test_image() -> bytes:
    with open("tests/unit/misc_files/floormap_example.png", "rb") as image_file:
        image_data = image_file.read()
    return image_data


def get_floormap(name: str):
    return FloorMap(
        name=name,
        image=get_test_image(),
        image_type="png",
        width=100.0,
        height=100.0,
        tx=10.0,
        ty=10.0,
        tw=50.0,
        th=50.0,
    )


def test_create_floormap(floormap_service: FloormapService, mock_session: Session):
    floormap_data = FloormapCreate(
        name="Test FloorMap",
        width=100.0,
        height=100.0,
        tx=10.0,
        ty=10.0,
        tw=50.0,
        th=50.0,
    )

    image_data = get_test_image()
    image_type = "png"

    result = floormap_service.create_floormap(floormap_data, image_data, image_type)
    expected = {
        "name_is_equal": True,
        "image_matches": True,
    }

    actual = {
        "name_is_equal": result.name == floormap_data.name,
        "image_matches": result.image
        == floormap_service.bytes_to_base64(image_data, image_type),
    }

    assert expected == actual


def test_create_floormap_conflict(
    floormap_service: FloormapService, mock_session: Session
):
    floormap_data = FloormapCreate(
        name="Test FloorMap",
        description="Test Description",
        width=100.0,
        height=100.0,
        tx=10.0,
        ty=10.0,
        tw=50.0,
        th=50.0,
    )
    image_data = get_test_image()
    image_type = "png"

    mock_session.add(
        FloorMap(
            **floormap_data.model_dump(),
            image=image_data,
            image_type=image_type,
        )
    )
    mock_session.commit()

    with pytest.raises(HTTPException):
        floormap_service.create_floormap(floormap_data, image_data, image_type)


def test_delete_floormap(floormap_service: FloormapService, mock_session: Session):
    floormap = get_floormap(name="Test FloorMap")
    mock_session.add(floormap)
    mock_session.commit()

    floormap_service.delete_floor_map_by_id(floormap.id)

    assert (
        mock_session.query(FloorMap).filter(FloorMap.id == floormap.id).first() is None
    )


def test_delete_floormap_not_found(floormap_service: FloormapService):
    import random

    with pytest.raises(HTTPException):
        floormap_service.delete_floor_map_by_id(random.randrange(1000, 9999))


def test_get_floormap_by_id(floormap_service: FloormapService, mock_session: Session):
    floormap = get_floormap(name="Test FloorMap")
    mock_session.add(floormap)
    mock_session.commit()

    result = floormap_service.get_floormap(floormap.id)

    expected = {
        "name_is_equal": True,
        "image_matches": True,
    }

    actual = {
        "name_is_equal": result.name == floormap.name,
        "image_matches": result.image
        == floormap_service.bytes_to_base64(floormap.image, floormap.image_type),
    }

    assert expected == actual


def test_get_floormap_by_name(floormap_service: FloormapService, mock_session: Session):
    test_floormap = get_floormap(name="Test FloorMap")
    mock_session.add(test_floormap)
    mock_session.commit()

    floormap_base = FloormapModel.model_validate(test_floormap)
    floormap_id = test_floormap.id
    result_with_object = floormap_service.get_floormap(floormap_base)
    result_with_id = floormap_service.get_floormap(floormap_id)

    expected = {
        "results_are_equal": True,
        "results_equal_test_floormap": True,
    }

    actual = {
        "results_are_equal": result_with_object == result_with_id,
        "results_equal_test_floormap": all(
            [
                result.name == test_floormap.name
                for result in [result_with_object, result_with_id]
            ]
        ),
    }

    assert expected == actual


def test_get_all_floormaps(floormap_service: FloormapService, mock_session: Session):
    floormap1 = get_floormap(name="FloorMap 1")
    floormap2 = get_floormap(name="Floormap 2")
    mock_session.add_all([floormap1, floormap2])
    mock_session.commit()

    result = floormap_service.get_all_floormap(page=0, limit=10)

    expected = {
        "total_floormaps": 2,
        "first_floormap_name": floormap1.name,
        "second_floormap_name": floormap2.name,
    }

    actual = {
        "total_floormaps": len(result),
        "first_floormap_name": result[0].name,
        "second_floormap_name": result[1].name,
    }

    assert expected == actual


def test_floormap_exists(floormap_service: FloormapService, mock_session: Session):
    floormap = get_floormap(name="Existing FloorMap")
    mock_session.add(floormap)
    mock_session.commit()

    floormap_base = FloormapBase.model_validate(floormap)
    expected = {
        "existing_floormap_base": True,
        "existing_floormap_id": True,
        "non_existing_floormap_base": False,
        "non_existing_floormap_id": False,
    }

    actual = {
        "existing_floormap_base": floormap_service.floormap_exists(floormap_base),
        "existing_floormap_id": floormap_service.floormap_exists(floormap.id),
        "non_existing_floormap_base": floormap_service.floormap_exists(
            get_floormap(name="Non-existing")
        ),
        "non_existing_floormap_id": floormap_service.floormap_exists(999),
    }

    assert expected == actual
