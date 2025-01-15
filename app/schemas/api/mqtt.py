from pydantic import BaseModel, WebsocketUrl


class MQTTCredentials(BaseModel):
    ws_url: WebsocketUrl
    mqttServerAddress: str
    mqttServerPort: int
    mqttUsername: str
    mqttPassword: str
