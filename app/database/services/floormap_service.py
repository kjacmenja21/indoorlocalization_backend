from pydantic import Field, PositiveInt
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict, not_found
from app.models.floor_map import FloorMap
from app.schemas.api.floormap import FloormapBase, FloormapCreate, FloormapModel


class FloormapService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_floormap(self, floormap: FloormapCreate, image: bytes) -> FloormapModel:
        if self.floormap_exists(floormap):
            raise conflict()
        new_floormap = FloorMap(**floormap.model_dump(), image=image)

        self.session.add(new_floormap)
        self.session.commit()

        return FloormapModel.model_validate(new_floormap)

    def delete_floor_map_by_id(self, floormap_id: int) -> None:
        floormap = (
            self.session.query(FloorMap).where(FloorMap.id == floormap_id).first()
        )
        if not floormap:
            raise not_found()

        self.session.delete(floormap)
        self.session.commit()

    def get_floormap(self, floormap: FloormapBase | int) -> FloormapModel:
        filter_query = None
        if isinstance(floormap, FloormapBase):
            filter_query = FloorMap.name == floormap.name
        if isinstance(floormap, int):
            filter_query = FloorMap.id == floormap

        found_floormap = self.session.query(FloorMap).filter(filter_query).first()

        return FloormapModel.model_validate(found_floormap)

    def get_all_floormap(
        self,
        page: PositiveInt = Field(0, gt=-1),
        limit: PositiveInt = Field(1, gt=0),
    ) -> list[FloormapModel]:
        offset = page * limit
        floormap_query: list[FloorMap] = (
            self.session.query(FloorMap).limit(limit).offset(offset).all()
        )

        floormaps: list[FloormapModel] = []
        for floormap in floormap_query:
            user_model = FloormapModel.model_validate(floormap)
            floormaps.append(user_model)

        return floormaps

    def floormap_exists(self, floormap: FloormapBase | int) -> bool:
        query = exists()
        if isinstance(floormap, FloormapBase):
            query = query.where((FloorMap.name == floormap.name))
        if isinstance(floormap, int):
            query = query.where(FloorMap.id == floormap)

        floormap_exists = self.session.query(query).scalar()
        return bool(floormap_exists)

    def floormap_page_count(self, limit: int = Field(1, gt=1)) -> int:
        count = self.session.query(FloorMap).count()
        return (count + limit - 1) // limit
