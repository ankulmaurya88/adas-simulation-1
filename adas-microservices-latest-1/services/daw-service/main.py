# import json
# from app.adapters.mqtt_client import MQTTClient
# from app.controllers.daw_controller import DAWController

# controller = DAWController()
# mqtt_client = MQTTClient("DAWService")

# def on_message(client, userdata, msg):
#     sensor_data = json.loads(msg.payload.decode())
#     decision = controller.compute_alert(sensor_data)
#     mqtt_client.publish("services/daw/decision", decision)
#     print("DAW Decision:", decision)

# mqtt_client.subscribe("sensors/driver", on_message)
# mqtt_client.loop_forever()

import time
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883
TOPIC = "services/daw/decision"

def publish_daw(client):
    while True:
        message = {"service": "DAW", "status": "alert", "details": "Driver drowsy detected"}
        client.publish(TOPIC, str(message))
        print(f"[DAW] Published: {message}")
        time.sleep(5)

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    publish_daw(client)
