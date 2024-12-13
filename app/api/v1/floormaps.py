from fastapi import APIRouter, Body, UploadFile
from fastapi.responses import JSONResponse

from app.api.dependencies import FloormapServiceDep, get_current_user_with_scope
from app.schemas.api.floormap import FloormapCreate, FloormapModel
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

floormap_router = APIRouter(prefix="/floor-maps", tags=["Floor Maps"])


@floormap_router.get("/")
def retrieve_floor_maps(
    floormap_service: FloormapServiceDep,
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> list[FloormapModel]:
    floormaps = floormap_service.get_all_floormap()

    return floormaps


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


@floormap_router.delete("/{floormap_id}")
def delete_floor_map_by_id(
    floormap_id: int,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass
