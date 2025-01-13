import base64
from io import BytesIO

from PIL import Image
from pydantic import Field, PositiveInt
from sqlalchemy import Exists
from sqlalchemy.orm import Session

from app.functions.exceptions import conflict, not_found
from app.models.floor_map import FloorMap
from app.schemas.api.floormap import (
    FloormapBase,
    FloormapCreate,
    FloormapImageModel,
    FloormapModel,
)


class FloormapService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_floormap(
        self,
        floormap: FloormapCreate,
        image: bytes,
        image_type: str,
    ) -> FloormapImageModel:
        if self.floormap_exists(floormap):
            raise conflict()
        new_floormap = FloorMap(
            **floormap.model_dump(),
            image=image,
            image_type=image_type,
        )

        image = self.bytes_to_base64(image, image_type)
        self.session.add(new_floormap)
        self.session.commit()

        floormap_dict = FloormapModel.model_validate(new_floormap).model_dump()
        floormap_dict["image"] = image

        return FloormapImageModel.model_validate(floormap_dict)

    def delete_floor_map_by_id(self, floormap_id: int) -> None:
        floormap = (
            self.session.query(FloorMap).where(FloorMap.id == floormap_id).first()
        )
        if not floormap:
            raise not_found()

        self.session.delete(floormap)
        self.session.commit()

    def get_floormap(self, floormap: FloormapBase | int) -> FloormapImageModel:
        filter_query = None
        if isinstance(floormap, FloormapBase):
            filter_query = FloorMap.name == floormap.name
        if isinstance(floormap, int):
            filter_query = FloorMap.id == floormap

        found_floormap = self.session.query(FloorMap).filter(filter_query).first()

        image = self.bytes_to_base64(
            found_floormap.image,
            found_floormap.image_type,
        )
        floormap_dict = FloormapModel.model_validate(found_floormap).model_dump()
        floormap_dict["image"] = image

        return FloormapImageModel.model_validate(floormap_dict)

    def get_all_floormap(
        self,
        page: PositiveInt = Field(0, gt=-1),
        limit: PositiveInt = Field(1, gt=0),
    ) -> list[FloormapImageModel]:
        offset = page * limit
        floormap_query: list[FloorMap] = (
            self.session.query(FloorMap).limit(limit).offset(offset).all()
        )

        floormaps: list[FloormapImageModel] = []
        for floormap in floormap_query:
            floormap_dict = FloormapModel.model_validate(floormap).model_dump()

            image = self.bytes_to_base64(
                floormap.image,
                floormap.image_type,
            )
            floormap_dict["image"] = image

            floormap_model = FloormapImageModel.model_validate(floormap_dict)
            floormaps.append(floormap_model)

        return floormaps

    def floormap_exists(self, floormap: FloormapBase | int) -> bool:
        query: Exists | None = None
        if isinstance(floormap, FloormapBase):
            query = (
                self.session.query(FloorMap.id)
                .filter(FloorMap.name == floormap.name)
                .exists()
            )
        if isinstance(floormap, int):
            query = (
                self.session.query(FloorMap.id).filter(FloorMap.id == floormap).exists()
            )
        if query is None:
            return False
        floormap_exists = self.session.query(query).scalar()
        return bool(floormap_exists)

    def floormap_page_count(self, limit: int = Field(1, gt=1)) -> int:
        count = self.session.query(FloorMap).count()
        return (count + limit - 1) // limit

    def bytes_to_base64(self, image_bytes: bytes, image_type: str) -> str:
        """
        Convert image bytes into a Base64 encoded string.

        :param image_bytes: The bytes of the image.
        :param image_type: The type of the image ('png', 'jpeg', 'svg', etc.).
        :return: Base64 encoded string of the image.
        """

        if image_type.lower() == "svg":
            return base64.b64encode(image_bytes).decode("utf-8")

        # Load image from bytes
        image = Image.open(BytesIO(image_bytes))

        # Create a bytes buffer to hold the image data
        buffer = BytesIO()
        # Save the image to the buffer in the specified format
        image.save(buffer, format=image_type.upper())

        # Get the byte data from the buffer
        buffer.seek(0)
        encoded_bytes = base64.b64encode(buffer.read())

        # Convert to string
        base64_string = encoded_bytes.decode("utf-8")
        return base64_string
