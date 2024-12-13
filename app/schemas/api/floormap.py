import json
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, model_validator


class FloormapBase(BaseModel):
    name: str
    width: float
    height: float
    tx: float
    ty: float
    tw: float
    th: float


class FloormapCreate(FloormapBase):
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value) -> Self | Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class FloormapModel(FloormapBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FloormapPagination(BaseModel):
    current_page: int
    total_pages: int
    page_limit: int
    page: list[FloormapModel]
