# services/acc-service/app/utils/mqtt_client.py
import json
import threading
import time
import paho.mqtt.client as mqtt
from app.utils.logger import logger
from app.utils.exceptions import MessagingError

class MQTTClient:
    """
    Minimal MQTT wrapper with on_message_map: {topic: handler_fn}
    handler_fn(payload_dict)
    """
    def __init__(self, client_id: str, host="mqtt", port=1883, on_message_map=None):
        self.client = mqtt.Client(client_id=client_id)
        self.host = host
        self.port = int(port)
        self._on_message_map = on_message_map or {}
        self._thread = None

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT connected rc=%s", rc)
        # subscribe to topics
        for topic in self._on_message_map.keys():
            client.subscribe(topic)
            logger.info("Subscribed to topic %s", topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload) if payload else None
        except Exception:
            data = msg.payload.decode()
        logger.debug("MQTT message on %s: %s", msg.topic, data)
        handler = self._on_message_map.get(msg.topic)
        if handler:
            try:
                handler(data)
            except Exception as e:
                logger.exception("Error in MQTT message handler for %s: %s", msg.topic, e)

    def _on_disconnect(self, client, userdata, rc):
        logger.warning("MQTT disconnected rc=%s", rc)

    def connect(self):
        def _loop():
            while True:
                try:
                    logger.info("Connecting to MQTT broker %s:%s", self.host, self.port)
                    self.client.connect(self.host, self.port, keepalive=60)
                    self.client.loop_forever()
                except Exception as e:
                    logger.exception("MQTT client error: %s", e)
                    time.sleep(2)
        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def publish(self, topic: str, payload: dict):
        try:
            self.client.publish(topic, json.dumps(payload))
            logger.debug("Published %s -> %s", topic, payload)
        except Exception as e:
            logger.exception("MQTT publish failed")
            raise MessagingError(str(e))

    def set_handlers(self, handlers_map: dict):
        """
        Replace handlers. handlers_map: {topic: handler_fn}
        If connected, will subscribe on next connect.
        """
        self._on_message_map = handlers_map
