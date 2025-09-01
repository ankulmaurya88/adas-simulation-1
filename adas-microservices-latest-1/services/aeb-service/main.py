import time
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883
TOPIC = "services/aeb/decision"

client = mqtt.Client()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        print("AEB connected to MQTT with result code " + str(rc))
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)

def run():
    connect_mqtt()
    client.loop_start()
    while True:
        decision = {"aeb": "NO_OBSTACLE"}  # placeholder logic
        client.publish(TOPIC, str(decision))
        print(f"AEB → published {decision}")
        time.sleep(5)

if __name__ == "__main__":
    run()
