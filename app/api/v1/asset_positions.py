from fastapi import APIRouter

asset_position_router = APIRouter(prefix="asset-position", tags=["Asset Position"])


@asset_position_router.get("/")
def retrieve_asset_position():
    pass


@asset_position_router.post("/")
def record_new_asset_position():
    pass
