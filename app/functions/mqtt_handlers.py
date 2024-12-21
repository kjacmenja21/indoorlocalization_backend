from app.schemas.mqtt.message import MQTTTopicHandler


class MQTTCoordinateHandler(MQTTTopicHandler):
    def __init__(self) -> None:
        super().__init__()
        self.topic = "/test/topic"
        self.handler = self.handle

    def handle(self, topic: str, payload: bytes) -> None:
        print(topic, payload.decode())
