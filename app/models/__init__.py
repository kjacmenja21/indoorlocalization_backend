# This file is necessary for Alembic to work.
# All ORM models need to be imported here so
# that Alembic can recognise the models and
# create the migrations revision

from app.models.asset import Asset
from app.models.floor_map import FloorMap
from app.models.history import AssetPositionHistory, AssetZoneHistory
from app.models.user import User, UserRole
from app.models.zone import Zone, ZonePoint
