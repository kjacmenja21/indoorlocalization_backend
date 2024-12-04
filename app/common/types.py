from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PydanticBaseModel(BaseModel, Generic[T]):
    pass