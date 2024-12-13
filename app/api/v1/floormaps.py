from fastapi import APIRouter, Body, Query, UploadFile
from fastapi.responses import JSONResponse
from pydantic import PositiveInt

from app.api.dependencies import FloormapServiceDep, get_current_user_with_scope
from app.schemas.api.floormap import FloormapCreate, FloormapModel, FloormapPagination
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

floormap_router = APIRouter(prefix="/floor-maps", tags=["Floor Maps"])


@floormap_router.get("/")
def retrieve_floor_maps(
    floormap_service: FloormapServiceDep,
    page: PositiveInt = Query(gt=-1),
    limit: PositiveInt = Query(gt=0),
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> FloormapPagination:
    floormaps = floormap_service.get_all_floormap(page, limit)
    count = floormap_service.floormap_page_count(limit)

    return FloormapPagination(
        current_page=page,
        total_pages=count,
        page_limit=limit,
        page=floormaps,
    )


@floormap_router.post("/")
def create_new_floor_map(
    image: UploadFile,
    floormap_service: FloormapServiceDep,
    floormap_data: FloormapCreate = Body(...),
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> JSONResponse:
    image = image.file.read()
    new_floormap = floormap_service.create_floormap(floormap_data, image)

    return JSONResponse(
        {
            "message": "Floormap successfully created.",
            "floormap": new_floormap.model_dump(),
        }
    )


@floormap_router.get("/{floormap_id}")
def get_floor_map_by_id(
    floormap_id: int,
    floormap_service: FloormapServiceDep,
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> FloormapModel:
    floormap = floormap_service.get_floormap(floormap_id)
    return floormap


@floormap_router.delete("/{floormap_id}")
def delete_floor_map_by_id(
    floormap_id: int,
    floormap_service: FloormapServiceDep,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> JSONResponse:
    floormap_service.delete_floor_map_by_id(floormap_id)
    return JSONResponse(
        {"message": f"Successfully deleted floormap with id {floormap_id}"}
    )
