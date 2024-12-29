import random

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from shapely.geometry import Polygon


class ZonePointBase(BaseModel):
    ordinalNumber: int
    x: float
    y: float


class ZonePointCreate(ZonePointBase): ...


class ZonePointModel(ZonePointBase):
    model_config = ConfigDict(from_attributes=True)
    zoneId: int


class ZoneBase(BaseModel):
    name: str = Field(examples=["Delivery Dock", "Storage", "Production Line"])
    floorMapId: int = Field(examples=random.sample(range(10), 5))
    color: int
    points: list[ZonePointBase] = Field(..., min_length=3)

    @classmethod
    @field_validator("points", mode="after")
    def validate_points(cls, value: list[ZonePointBase]) -> list[ZonePointBase]:
        # Check for duplicate ordinalNumber
        ordinal_numbers = [point.ordinalNumber for point in value]
        if len(ordinal_numbers) != len(set(ordinal_numbers)):
            raise ValidationError("Duplicate ordinalNumber values found in points.")

        # Sort points by ordinalNumber
        sorted_points = sorted(value, key=lambda point: point.ordinalNumber)
        coordinates = [(point.x, point.y) for point in sorted_points]

        # Ensure there are at least 3 points to form a polygon
        if len(coordinates) < 3:
            raise ValidationError("At least 3 points are required to form a polygon.")

        # Check for self-intersection using Shapely
        polygon = Polygon(coordinates)
        if not polygon.is_valid:
            raise ValidationError(
                "The polygon formed by the points is self-intersecting."
            )

        return value


class ZoneCreate(ZoneBase): ...


class ZoneModel(ZoneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
