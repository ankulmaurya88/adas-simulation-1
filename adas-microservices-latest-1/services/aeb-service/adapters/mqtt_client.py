import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, client_id, broker="mqtt-broker", port=1883):
        self.client = mqtt.Client(client_id)
        self.client.connect(broker, port)

    def subscribe(self, topic, callback):
        self.client.on_message = callback
        self.client.subscribe(topic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def loop_forever(self):
        self.client.loop_forever()
