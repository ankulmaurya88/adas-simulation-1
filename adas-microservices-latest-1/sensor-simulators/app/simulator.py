import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
# from paho.mqtt.client import CallbackAPIVersion, Client
import json
import time
import random

# client = mqtt.Client(client_id="SensorSimulator", callback_api_version=1)
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="SensorSimulator")
client.connect("mqtt-broker", 1883)

while True:
    client.publish("sensors/lidar", json.dumps({"distance": random.uniform(1,10), "speed": random.uniform(0,30)}))
    client.publish("sensors/camera", json.dumps({"lane_offset": random.uniform(-1,1)}))
    client.publish("sensors/driver", json.dumps({"fatigue": random.choice([True, False])}))
    client.publish("sensors/tpms", json.dumps({"pressure": random.uniform(28,36)}))
    time.sleep(1)



