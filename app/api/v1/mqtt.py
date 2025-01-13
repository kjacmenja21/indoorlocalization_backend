import json
import logging

from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
from pydantic import WebsocketUrl

from app.api.dependencies import get_current_user_with_scope
from app.config import GeneralConfig
from app.functions.mqtt_handlers import connection_manager
from app.schemas.api.mqtt import MQTTCredentials
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role

mqtt_router = APIRouter(prefix="/mqtt", tags=["MQTT"])


@mqtt_router.get("/")
def get_mqtt_credentials(
    request: Request,
    _: UserBase = get_current_user_with_scope([Role.USER]),
) -> MQTTCredentials:
    config = GeneralConfig()
    return MQTTCredentials(
        ws_url=WebsocketUrl(
            url=str(request.url_for("mqtt_broker_ws")),
        ),
        mqttUsername=config.mqtt_username,
        mqttPassword=config.mqtt_password,
        mqttServerAddress=config.mqtt_public_host,
        mqttServerPort=config.mqtt_public_port,
    )


@mqtt_router.websocket("/ws")
async def mqtt_broker_ws(websocket: WebSocket):
    """WebSocket endpoint to handle connections and authenticate clients."""
    config = GeneralConfig()
    try:
        await websocket.accept()

        # Wait for authentication message
        auth_message = await websocket.receive_text()

        # Validate JSON payload
        try:
            auth_data = json.loads(auth_message)
            username = auth_data.get("username")
            password = auth_data.get("password")

            if username != config.mqtt_username or password != config.mqtt_password:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return

        except (json.JSONDecodeError, KeyError):
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            return

        # Authentication successful
        await connection_manager.add_connection(websocket)

        try:
            while True:
                # Keep the WebSocket connection alive
                await websocket.receive_text()
        except WebSocketDisconnect:
            connection_manager.remove_connection(websocket)

    except WebSocketException as e:
        logging.error("WebSocket error: %s", e)
        await websocket.close(code=status.WS_1002_PROTOCOL_ERROR)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)


@mqtt_router.get("/test", response_class=HTMLResponse)
async def websocket_test_page():
    """Serve an HTML page to test the WebSocket connection."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Test</title>
        <script>
            let ws;
            function connectWebSocket() {
                const wsUrl = `wss://${location.host}/api/v1/mqtt/ws`;
                ws = new WebSocket(wsUrl);

                ws.onopen = () => {
                    console.log("Connected to WebSocket.");
                    document.getElementById("status").innerText = "Connected to WebSocket.";
                };

                ws.onmessage = (event) => {
                    const messageList = document.getElementById("messages");
                    const newMessage = document.createElement("li");
                    newMessage.textContent = event.data;
                    messageList.appendChild(newMessage);
                };

                ws.onclose = () => {
                    console.log("WebSocket connection closed.");
                    document.getElementById("status").innerText = "WebSocket connection closed.";
                };

                ws.onerror = (error) => {
                    console.error("WebSocket error:", error);
                    document.getElementById("status").innerText = "WebSocket error.";
                };
            }

            function disconnectWebSocket() {
                if (ws) {
                    ws.close();
                }
            }
        </script>
    </head>
    <body>
        <h1>WebSocket Test Page</h1>
        <p>Status: <span id="status">Not connected</span></p>
        <button onclick="connectWebSocket()">Connect</button>
        <button onclick="disconnectWebSocket()">Disconnect</button>
        <h2>Messages:</h2>
        <ul id="messages"></ul>
    </body>
    </html>
    """
