from fastapi import APIRouter

from app.api.dependencies import get_current_user_with_scope
from app.config import GeneralConfig
from app.schemas.api.mqtt import MQTTCredentials
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

mqtt_router = APIRouter(prefix="/mqtt", tags=["MQTT"])


@mqtt_router.get("/")
def get_mqtt_credentials(
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> MQTTCredentials:
    config = GeneralConfig()
    return MQTTCredentials(
        mqttUsername=config.mqtt_username,
        mqttPassword=config.mqtt_password,
        mqttServerAddress=config.mqtt_public_host,
        mqttServerPort=config.mqtt_public_port,
    )
