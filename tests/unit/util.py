import uuid
from functools import lru_cache

from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.models.floor_map import FloorMap
from app.models.user import UserRole
from app.schemas.api.asset import AssetCreate
from app.schemas.api.zone import ZoneCreate, ZonePointBase
from app.schemas.auth.role_types import Role


@lru_cache(maxsize=32)
def get_test_image() -> bytes:
    with open("tests/unit/misc_files/floormap_example.png", "rb") as image_file:
        image_data = image_file.read()
    return image_data


def create_user_roles(session: Session):
    # Define the function to create user roles
    admin_role = UserRole(name=Role.ADMIN)
    user_role = UserRole(name=Role.USER)
    session.add_all([admin_role, user_role])
    session.commit()


def create_users(session: Session):
    from app.models.user import User
    from app.schemas.api.user import UserCreate

    users_data = [
        UserCreate(
            username="admin",
            email="admin@example.com",
            plain_password="adminpass",
            role=Role.ADMIN,
        ),
        UserCreate(
            username="user",
            email="user@example.com",
            plain_password="userpass",
            role=Role.USER,
        ),
        UserCreate(
            username="testuser",
            email="testuser@example.com",
            plain_password="testpass",
            role=Role.USER,
        ),
        UserCreate(
            username="delete_user",
            email="delete_user@example.com",
            plain_password="deletepass",
            role=Role.USER,
        ),
    ]

    roles = session.query(UserRole).all()
    commit_users = []
    for user in users_data:
        commit_user = User(
            **user.model_dump(exclude_none=True, exclude=["plain_password", "role"])
        )
        commit_user.role = next(role for role in roles if role.name == user.role)
        commit_users.append(commit_user)

    session.add_all(commit_users)
    session.commit()


def create_floormaps(session: Session):
    floormaps = [
        get_floormap("First Floor 1"),
        get_floormap("Second Floor 1"),
        get_floormap("Third Floor 1"),
    ]
    session.add_all(floormaps)
    session.commit()


def get_floormap(name: str):
    return FloorMap(
        name=name + uuid.uuid4().hex,
        image=get_test_image(),
        image_type="png",
        width=100.0,
        height=100.0,
        tx=10.0,
        ty=10.0,
        tw=50.0,
        th=50.0,
    )


def get_asset(floormap: FloorMap) -> AssetCreate:
    return AssetCreate(
        name="Test Asset" + uuid.uuid4().hex, active=True, floormap_id=floormap.id
    )


def get_zone(
    name: str,
    floormap: FloorMap,
    center: Point = Point(50, 50),
    radius: int = 25,
    sides: int = 3,
) -> tuple[int, ZoneCreate]:
    import math

    from shapely.geometry.polygon import Polygon

    polygon = Polygon(
        [
            (
                center.x + radius * math.cos(2 * math.pi * i / sides),
                center.y + radius * math.sin(2 * math.pi * i / sides),
            )
            for i in range(sides)
        ]
    ).exterior.coords

    points = [
        ZonePointBase(
            ordinalNumber=i,
            x=point[0],
            y=point[1],
        )
        for i, point in enumerate(polygon)
    ]
    color = int("0x0000FF", 16)
    zone_create = ZoneCreate(
        name=name + uuid.uuid4().hex,
        floorMapId=floormap.id,
        color=color,
        points=points,
    )
    return color, zone_create
