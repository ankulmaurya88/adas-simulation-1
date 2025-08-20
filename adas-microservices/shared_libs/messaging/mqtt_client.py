# shared_libs/messaging/mqtt_client.py
import json
import threading
import time
import os
from typing import Callable, Dict
from logging import getLogger
import paho.mqtt.client as mqtt
from typing import Callable, Dict
from logging import getLogger

logger = getLogger("shared.mqtt")

class MQTTClient:
    # def __init__(self, client_id: str, host="mqtt", port=1883, on_message_map: Dict[str, Callable]=None):
    #     self.client = mqtt.Client(client_id=client_id)
    #     self.host = host
    #     self.port = int(port)
    #     self.on_message_map = on_message_map or {}
    #     self._connected = False
    #     self._thread = None

    #     # callbacks
    #     self.client.on_connect = self._on_connect
    #     self.client.on_message = self._on_message
    #     self.client.on_disconnect = self._on_disconnect

    def __init__(self, client_id: str, host=None, port=None, on_message_map: Dict[str, Callable] = None):
        # Use env vars if no explicit host/port passed
        self.host = host or os.getenv("MQTT_HOST", "mqtt")
        self.port = int(port or os.getenv("MQTT_PORT", 1883))

        self.client = mqtt.Client(client_id=client_id)
        self.on_message_map = on_message_map or {}
        self._connected = False
        self._thread = None

        # callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = True
        logger.info("MQTT connected rc=%s", rc)
        for topic in self.on_message_map:
            client.subscribe(topic)
            logger.info("Subscribed to %s", topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload) if payload else None
        except Exception:
            data = msg.payload.decode()
        logger.debug("MQTT msg %s %s", msg.topic, data)
        handler = self.on_message_map.get(msg.topic)
        if handler:
            try:
                handler(data)
            except Exception as e:
                logger.exception("Error in mqtt handler for %s: %s", msg.topic, e)

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        logger.warning("MQTT disconnected rc=%s", rc)

    def connect(self):
        def _run():
            while True:
                try:
                    logger.info("Connecting MQTT to %s:%s", self.host, self.port)
                    self.client.connect(self.host, self.port, keepalive=60)
                    self.client.loop_forever()
                except Exception as e:
                    logger.exception("MQTT client error: %s", e)
                    time.sleep(2)
        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def publish(self, topic: str, payload: dict):
        try:
            self.client.publish(topic, json.dumps(payload))
            logger.debug("Published %s -> %s", topic, payload)
        except Exception:
            logger.exception("Failed publish to %s", topic)

    def stop(self):
        try:
            self.client.disconnect()
        except Exception:
            pass
