from fastapi import APIRouter

asset_router = APIRouter(prefix="/assets", tags=["Asset"])


@asset_router.get("/")
def retrieve_assets(): ...
