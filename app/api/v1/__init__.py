from fastapi import APIRouter

from app.api.v1.asset_positions import asset_position_router
from app.api.v1.assets import asset_router
from app.api.v1.auth import auth_router
from app.api.v1.floormaps import floormap_router
from app.api.v1.mqtt import mqtt_router
from app.api.v1.users import user_router
from app.api.v1.zone_positions import zone_position_router
from app.api.v1.zones import zone_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(asset_position_router)
v1_router.include_router(asset_router)
v1_router.include_router(auth_router)
v1_router.include_router(floormap_router)
v1_router.include_router(mqtt_router)
v1_router.include_router(user_router)
v1_router.include_router(zone_position_router)
v1_router.include_router(zone_router)
