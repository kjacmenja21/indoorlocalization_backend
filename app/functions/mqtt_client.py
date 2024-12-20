from typing import Any

from fastapi_mqtt import MQTTClient
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT


class MQTTClientHandler:
    def __init__(self):
        fast_mqtt = FastMQTT(
            config=MQTTConfig(
                host="autorack.proxy.rlwy.net",
                port=45390,
            )
        )

        @fast_mqtt.on_connect()
        def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
            fast_mqtt.client.subscribe("/mqtt")  # subscribing mqtt topic
            print("Connected: ", client, flags, rc, properties)

        @fast_mqtt.on_message()
        async def message(
            _client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any
        ):
            print("Received message: ", topic, payload.decode(), qos, properties)
            return 0

        @fast_mqtt.subscribe("my/mqtt/topic/#")
        async def message_to_topic(
            _client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any
        ):
            print(
                "Received message to specific topic: ",
                topic,
                payload.decode(),
                qos,
                properties,
            )

        @fast_mqtt.on_disconnect()
        def disconnect(_client: MQTTClient, packet, exc=None):
            print("Disconnected")

        @fast_mqtt.on_subscribe()
        def subscribe(client: MQTTClient, mid, qos, properties):
            print("subscribed", client, mid, qos, properties)

        self.fast_mqtt = fast_mqtt

    async def start(self):
        await self.fast_mqtt.mqtt_startup()

    async def stop(self):
        await self.fast_mqtt.mqtt_shutdown()
