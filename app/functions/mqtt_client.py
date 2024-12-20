import logging
from typing import Any

from fastapi_mqtt import MQTTClient
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

from app.config import GeneralConfig


class MQTTClientHandler:

    async def start(self):
        await self.fast_mqtt.mqtt_startup()

    async def stop(self):
        await self.fast_mqtt.mqtt_shutdown()

    def __init__(self):
        general_config = GeneralConfig()
        fast_mqtt = FastMQTT(
            config=MQTTConfig(
                host=general_config.mqtt_host,
                port=general_config.mqtt_port,
                username=general_config.mqtt_username,
                password=general_config.mqtt_password,
            )
        )

        @fast_mqtt.on_connect()
        def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
            fast_mqtt.client.subscribe("/test/topic")  # subscribing mqtt topic
            logging.info("Connected to MQTT broker %s:%d", client._host, client._port)

        @fast_mqtt.on_message()
        async def message(
            _client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any
        ):
            logging.info(
                "[MQTT Message] %s | %s | %s | %s",
                topic,
                payload.decode(),
                qos,
                properties,
            )
            return 0

        @fast_mqtt.subscribe("my/mqtt/topic/#")
        async def message_to_topic(
            _client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any
        ):
            logging.info(
                "[MQTT Subscribe] %s | %s | %s | %s",
                topic,
                payload.decode(),
                qos,
                properties,
            )

        @fast_mqtt.on_disconnect()
        def disconnect(client: MQTTClient, _packet: Any, _exc: Any | None = None):
            logging.info(
                "[MQTT] Disconnected from MQTT broker %s:%d",
                general_config.mqtt_host,
                general_config.mqtt_port,
            )

        @fast_mqtt.on_subscribe()
        def subscribe(client: MQTTClient, mid, qos: int, properties: Any):
            print("subscribed", client, mid, qos, properties)

        self.fast_mqtt = fast_mqtt
