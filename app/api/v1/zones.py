from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse

from app.api.dependencies import ZoneServiceDep, get_current_user_with_scope
from app.schemas.api.user import UserBase
from app.schemas.api.zone import ZoneCreate, ZoneModel
from app.schemas.auth.role_types import Role

zone_router = APIRouter(prefix="/zones", tags=["Zone"])


@zone_router.get("/")
def get_zones_for_floormap(
    zone_service: ZoneServiceDep,
    floorMapId: int = Query(),
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> list[ZoneModel]:
    return zone_service.get_zones_in_floormap(floorMapId)


@zone_router.post("/")
def create_zone(
    zone_service: ZoneServiceDep,
    data: ZoneCreate = Body(...),
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> JSONResponse:
    new_zone = zone_service.create_zone(data)
    return JSONResponse(
        {
            "message": "Zone successfully created.",
            "floormap": new_zone.model_dump(),
        }
    )


@zone_router.delete("/{zone_id}")
def delete_zone(
    zone_id: int,
    zone_service: ZoneServiceDep,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> JSONResponse:
    zone_service.delete_zone_by_id(zone_id)
    return JSONResponse({"message": f"Successfully deleted zone with id {zone_id}"})
