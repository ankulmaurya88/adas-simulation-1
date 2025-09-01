# services/ldw-service/app/utils/mqtt_client.py
import json
import paho.mqtt.client as mqtt
from app.utils.logger import logger
from app.utils.exceptions import MessagingError

class MQTTClient:
    def __init__(self, client_id, host="mqtt", port=1883):
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            logger.info("Connected to MQTT broker at %s:%d", self.host, self.port)
        except Exception as e:
            logger.exception("MQTT connection failed")
            raise MessagingError(str(e))

    def publish(self, topic, payload):
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.exception("MQTT publish failed")
            raise MessagingError(str(e))
