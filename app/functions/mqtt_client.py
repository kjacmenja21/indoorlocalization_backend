import inspect
import logging
from typing import Any

from fastapi_mqtt import MQTTClient
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

from app.config import GeneralConfig
from app.schemas.mqtt.handler import MQTTTopicHandler


class MQTTClientHandler:

    async def start(self) -> None:
        await self.fast_mqtt.mqtt_startup()

    async def stop(self) -> None:
        await self.fast_mqtt.mqtt_shutdown()

    def register_topic_handler(self, handler: MQTTTopicHandler) -> None:
        self.fast_mqtt.client.subscribe(handler.topic)
        self._topic_handlers.append(handler)

    async def _handle_topic(self, topic: str, payload: bytes) -> None:
        for handler_entry in self._topic_handlers:
            if handler_entry.topic == topic:
                handler = handler_entry.handler
                if inspect.iscoroutinefunction(handler):
                    # If the handler is awaitable
                    await handler(topic, payload)
                else:
                    # If the handler is a normal function
                    handler(topic, payload)

    def __init__(self) -> None:
        self.config = GeneralConfig()
        fast_mqtt = FastMQTT(
            config=MQTTConfig(
                host=self.config.mqtt_internal_host,
                port=self.config.mqtt_internal_port,
                username=self.config.mqtt_username,
                password=self.config.mqtt_password,
            )
        )
        self.fast_mqtt = fast_mqtt
        self.setup_decorators()
        self._topic_handlers: list[MQTTTopicHandler] = []

    def setup_decorators(self):
        mqtt = self.fast_mqtt

        @mqtt.on_connect()
        def connect(_client: MQTTClient, _flags: int, _rc: int, _properties: Any):
            mqtt.client.subscribe("/test/topic")  # subscribing mqtt topic
            logging.info(
                "Connected to MQTT broker %s:%d",
                self.config.mqtt_internal_host,
                self.config.mqtt_internal_port,
            )

        @mqtt.on_message()
        async def message(
            _client: MQTTClient, topic: str, payload: bytes, _qos: int, _properties: Any
        ) -> None:
            return await self._handle_topic(topic, payload)

        @mqtt.on_disconnect()
        def disconnect(_client: MQTTClient, _packet: Any, _exc: Any | None = None):
            logging.info(
                "[MQTT] Disconnected from MQTT broker %s:%d",
                self.config.mqtt_internal_host,
                self.config.mqtt_internal_port,
            )

        @mqtt.on_subscribe()
        def subscribe(_client: MQTTClient, _mid, _qos: int, _properties: Any) -> None:
            logging.info("[MQTT] Subscribed to topic")
