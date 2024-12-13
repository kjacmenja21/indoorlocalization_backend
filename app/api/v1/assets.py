from typing import Optional

from fastapi import APIRouter, Query
from pydantic import PositiveInt

from app.api.dependencies import AssetServiceDep

asset_router = APIRouter(prefix="/assets", tags=["Asset"])


@asset_router.get("/")
def retrieve_assets(
    active: Optional[bool],
    asset_service: AssetServiceDep,
    page: PositiveInt = Query(0, gt=-1),
    limit: PositiveInt = Query(1, gt=0),
):
    assets = asset_service.get_all_assets(active, page, limit)

