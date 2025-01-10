import json
import mimetypes
from typing import Any, Self

from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, model_validator

from app.schemas.api.common import PaginationBase

ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/svg+xml"]
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".svg"]


def validate_file_type(file: UploadFile):
    mime_type, _ = mimetypes.guess_type(file.filename)

    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PNG, JPEG, and SVG are allowed.",
        )

    file_extension = file.filename.split(".")[-1].lower()
    if not any(file_extension == ext.lstrip(".") for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Only PNG, JPEG, and SVG are allowed.",
        )


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


class FloormapPagination(PaginationBase):
    page: list[FloormapModel]
