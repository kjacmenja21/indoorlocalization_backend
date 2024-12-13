from fastapi import APIRouter, Body, UploadFile
from fastapi.responses import JSONResponse

from app.api.dependencies import FloormapServiceDep, get_current_user_with_scope
from app.schemas.api.floormap import FloormapCreate
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
    image: UploadFile,
    floormap_service: FloormapServiceDep,
    floormap_data: FloormapCreate = Body(...),
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    image = image.file.read()
    new_floormap = floormap_service.create_floormap(floormap_data, image)

    return JSONResponse(
        {
            "message": "Floormap successfully created.",
            "user": new_floormap.model_dump(),
        }
    )


@floormap_router.delete("/{floormap_id}")
def delete_floor_map_by_id(
    floormap_id: int,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
):
    pass
