import json
from app.adapters.mqtt_client import MQTTClient
from app.controllers.tpms_controller import TPMSController

controller = TPMSController()
mqtt_client = MQTTClient("TPMSService")

def on_message(client, userdata, msg):
    sensor_data = json.loads(msg.payload.decode())
    decision = controller.compute_alert(sensor_data)
    mqtt_client.publish("services/tpms/decision", decision)
    print("TPMS Decision:", decision)

mqtt_client.subscribe("sensors/tpms", on_message)
mqtt_client.loop_forever()
