from typing import Callable

from pydantic import BaseModel, field_validator


class MQTTTopicHandler:
    topic: str
    handler: Callable[[str, bytes], None]

    @classmethod
    @field_validator("topic", mode="before")
    def validate_topic(cls, topic: str) -> str:
        if not topic or "#" in topic or "+" in topic:
            raise ValueError(
                "Invalid topic name. Wildcards are not allowed in registration."
            )
        return topic


class MQTTAssetUpdateMessage(BaseModel):
    id: int
    x: float
    y: float
    floorMap: int
