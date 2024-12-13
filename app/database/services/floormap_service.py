from sqlalchemy.orm import Session

from app.models.floor_map import FloorMap
from app.schemas.api.floormap import FloormapBase, FloormapCreate, FloormapModel


class FloormapService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_floormap(self, floormap: FloormapCreate, image: bytes) -> FloormapModel:
        new_floormap = FloorMap(**floormap.model_dump(), image=image)

        self.session.add(new_floormap)
        self.session.commit()

        return FloormapModel.model_validate(new_floormap)

    def get_floormap(self, floormap: FloormapBase | int) -> FloormapModel:
        filter_query = None
        if isinstance(floormap, FloormapBase):
            filter_query = FloorMap.name == floormap.name
        if isinstance(floormap, int):
            filter_query = FloorMap.id == floormap

        found_floormap = self.session.query(FloorMap).filter(filter_query).first()

        return FloormapModel.model_validate(found_floormap)

    def get_all_floormap(self) -> list[FloormapModel]:
        floormap_query: list[FloorMap] = self.session.query(FloorMap).all()

        floormaps: list[FloormapModel] = []
        for floormap in floormap_query:
            user_model = FloormapModel.model_validate(floormap)
            floormaps.append(user_model)

        return floormaps
