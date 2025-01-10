from pydantic import BaseModel


class MQTTCredentials(BaseModel):
    mqttServerAddress: str
    mqttServerPort: int
    mqttUsername: str
    mqttPassword: str
