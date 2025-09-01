import json
from app.adapters.mqtt_client import MQTTClient

def on_message(client, userdata, msg):
    cmd = json.loads(msg.payload.decode())
    if cmd["brake"]: print("🚨 Brake Applied")
    if cmd["steer"]: print(f"🔄 Steering: {cmd['steer']}")
    if cmd["alerts"]: print(f"⚠️ Alerts: {cmd['alerts']}")

mqtt_client = MQTTClient("ActuatorMock")
mqtt_client.subscribe("car/control", on_message)
mqtt_client.loop_forever()
