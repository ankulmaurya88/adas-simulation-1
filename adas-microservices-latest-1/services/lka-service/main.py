import json
from app.adapters.mqtt_client import MQTTClient
from app.controllers.lka_controller import LKAController

controller = LKAController()
mqtt_client = MQTTClient("LKAService")

def on_message(client, userdata, msg):
    sensor_data = json.loads(msg.payload.decode())
    decision = controller.compute_steer(sensor_data)
    mqtt_client.publish("services/lka/decision", decision)
    print("LKA Decision:", decision)

mqtt_client.subscribe("sensors/camera", on_message)
mqtt_client.loop_forever()
