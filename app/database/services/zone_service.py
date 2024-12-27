from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.database.services.floormap_service import FloormapService
from app.functions.exceptions import conflict, not_found
from app.models.zone import Zone
from app.schemas.api.zone import ZoneBase, ZoneCreate, ZoneModel


class ZoneService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.floormap_service = FloormapService(session)

    def get_zones_in_floormap(self, floorMapId: int) -> list[ZoneModel]:
        if not self.floormap_service.floormap_exists(floorMapId):
            raise not_found()

        zones = self.session.query(Zone).where(Zone.floorMapId == floorMapId).all()
        return [ZoneModel.model_validate(zone) for zone in zones]

    def create_zone(self, zone: ZoneCreate) -> ZoneModel:
        if self.zone_exists(zone):
            raise conflict()
        new_zone = Zone(**zone.model_dump())

        self.session.add(new_zone)
        self.session.commit()

        return ZoneModel.model_validate(new_zone)

    def delete_zone_by_id(self, zone_id: int) -> None:
        zone = self.session.query(Zone).where(Zone.id == zone_id).first()
        if not zone:
            raise not_found()

        self.session.delete(zone)
        self.session.commit()

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
