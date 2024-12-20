from fastapi import APIRouter, Query

from app.api.dependencies import AssetPositionDep, get_current_user_with_scope
from app.schemas.api.asset_position import AssetPositionQuery
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

asset_position_router = APIRouter(prefix="asset-position", tags=["Asset Position"])


@asset_position_router.get("/")
def retrieve_asset_position(
    asset_position_service: AssetPositionDep,
    data: AssetPositionQuery = Query(),
    _: UserBase = get_current_user_with_scope([Role.USER]),
):
    pass


@asset_position_router.post("/")
def record_new_asset_position(
    asset_position_service: AssetPositionDep,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass
