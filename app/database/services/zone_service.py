from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict
from app.models.zone import Zone
from app.schemas.api.zone import ZoneBase, ZoneCreate, ZoneModel


class ZoneService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_zone(self, zone: ZoneCreate) -> ZoneModel:
        if self.zone_exists(zone):
            raise conflict()
        new_zone = Zone(**zone.model_dump())

        self.session.add(new_zone)
        self.session.commit()

        return ZoneModel.model_validate(new_zone)

    def zone_exists(self, zone: ZoneBase | int) -> bool:
        query = exists()
        if isinstance(zone, ZoneBase):
            query = query.where(
                (Zone.name == zone.name) & (Zone.floorMapId == zone.floorMapId)
            )
        if isinstance(zone, int):
            query = query.where(Zone.id == zone)

        floormap_exists = self.session.query(query).scalar()
        return bool(floormap_exists)
