import json
from app.adapters.mqtt_client import MQTTClient
from app.controllers.fcw_controller import FCWController

controller = FCWController()
mqtt_client = MQTTClient("FCWService")

def on_message(client, userdata, msg):
    sensor_data = json.loads(msg.payload.decode())
    decision = controller.compute_alert(sensor_data)
    mqtt_client.publish("services/fcw/decision", decision)
    print("FCW Decision:", decision)

mqtt_client.subscribe("sensors/lidar", on_message)
mqtt_client.loop_forever()

