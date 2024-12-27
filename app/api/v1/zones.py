from fastapi import APIRouter, Body, Query

from app.api.dependencies import get_current_user_with_scope
from app.schemas.api.user import UserBase
from app.schemas.api.zone import ZoneCreate
from app.schemas.auth.role_types import Role

zone_router = APIRouter(prefix="/zones", tags=["Zone"])


@zone_router.get("/")
def get_zones_for_floormap(
    floorMapId: int = Query(),
    _: UserBase = get_current_user_with_scope([Role.USER]),
):
    pass


@zone_router.post("/")
def create_zone(
    data: ZoneCreate = Body(...),
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass
