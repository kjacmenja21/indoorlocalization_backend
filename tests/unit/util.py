from functools import lru_cache

from app.models.floor_map import FloorMap


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
