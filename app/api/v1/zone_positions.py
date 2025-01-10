from fastapi import APIRouter, Query

from app.api.dependencies import ZonePositionDep, get_current_user_with_scope
from app.schemas.api.user import UserBase
from app.schemas.api.zone_position import AssetZoneHistoryModel, AssetZonePositionQuery
from app.schemas.auth.role_types import Role

zone_position_router = APIRouter(
    prefix="/asset-zone-history", tags=["Asset Zone History"]
)


@zone_position_router.get("/")
def retrieve_asset_zone_history(
    zone_position_service: ZonePositionDep,
    query: AssetZonePositionQuery = Query(),
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> list[AssetZoneHistoryModel]:
    return zone_position_service.get_asset_zone_position_history(query)
