from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.database.services.floormap_service import FloormapService
from app.functions.exceptions import conflict, not_found
from app.models.zone import Zone, ZonePoint
from app.schemas.api.zone import ZoneBase, ZoneCreate, ZoneModel, ZonePointModel


class ZoneService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.floormap_service = FloormapService(session)

    def get_zones_in_floormap(self, floorMapId: int) -> list[ZoneModel]:
        if not self.floormap_service.floormap_exists(floorMapId):
            raise not_found()

        zones = self.session.query(Zone).where(Zone.floorMapId == floorMapId).all()

        zone_models: list[ZoneModel] = []
        for zone in zones:
            zone_points = (
                self.session.query(ZonePoint).where(ZonePoint.zoneId == zone.id).all()
            )
            if len(zone_points) < 3:
                continue

            points = [ZonePointModel.model_validate(p) for p in zone_points]

            zone_models.append(
                ZoneModel.model_validate({**zone.__dict__, "points": points})
            )

        return zone_models

    def create_zone(self, zone: ZoneCreate) -> ZoneModel:
        if self.zone_exists(zone):
            raise conflict()

        new_zone = Zone(**zone.model_dump(exclude="points"))
        self.session.add(new_zone)
        self.session.flush()

        new_points: list[ZonePoint] = []
        for point in zone.points:
            new_points.append(ZonePoint(**point.model_dump(), zoneId=new_zone.id))

        self.session.bulk_save_objects(new_points)
        self.session.commit()

        zone_points = [ZonePointModel.model_validate(zp) for zp in new_points]
        return ZoneModel.model_validate(
            {
                "id": new_zone.id,
                "name": new_zone.name,
                "floorMapId": new_zone.floorMapId,
                "color": new_zone.color,
                "points": zone_points,
            }
        )

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
