from typing import Optional

from fastapi import APIRouter, Body, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import PositiveInt

from app.api.dependencies import (
    AssetServiceDep,
    FloormapServiceDep,
    get_current_user_with_scope,
)
from app.functions.exceptions import not_found
from app.schemas.api.asset import AssetCreate, AssetModel, AssetPagination, AssetPut
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

asset_router = APIRouter(prefix="/assets", tags=["Asset"])


@asset_router.get("/")
def retrieve_assets(
    asset_service: AssetServiceDep,
    active: Optional[bool] = None,
    page: PositiveInt = Query(0, gt=-1),
    limit: PositiveInt = Query(1, gt=0),
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> AssetPagination:
    assets = asset_service.get_all_assets(active, page, limit)

    return AssetPagination(
        current_page=page,
        total_pages=len(assets),
        page_limit=limit,
        page=assets,
    )


@asset_router.post("/")
def create_new_asset(
    asset_service: AssetServiceDep,
    data: AssetCreate = Body(),
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> JSONResponse:
    new_asset = asset_service.create_asset(data)

    return JSONResponse(
        {
            "message": "Floormap successfully created.",
            "floormap": jsonable_encoder(new_asset),
        }
    )


@asset_router.put("/{asset_id}")
def update_asset_information(
    data: AssetPut,
    asset_service: AssetServiceDep,
    floormap_service: FloormapServiceDep,
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
) -> AssetModel:
    if not floormap_service.floormap_exists(data.floormap_id):
        raise not_found(f"Floor map with id = {data.id} does not exist.")

    new_asset = asset_service.update_asset(data)
    return new_asset
