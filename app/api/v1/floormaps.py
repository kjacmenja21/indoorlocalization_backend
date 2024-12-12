from fastapi import APIRouter

from app.api.dependencies import get_current_user_with_scope
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

floormap_router = APIRouter(prefix="/floor-maps", tags=["Floor Maps"])


@floormap_router.get("/")
def retrieve_floor_maps(
    _: UserBase = get_current_user_with_scope([Role.USER]),
):
    pass


@floormap_router.post("/")
def create_new_floor_map(
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass


@floormap_router.delete("/{id}")
def delete_floor_map_by_id(
    id: int,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass
