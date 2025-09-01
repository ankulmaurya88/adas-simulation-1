import json
from app.adapters.mqtt_client import MQTTClient

TOPICS = ["services/aeb/decision","services/fcw/decision","services/lka/decision",
          "services/daw/decision","services/tpms/decision"]
PRIORITY = ["aeb","fcw","lka","daw","tpms"]
latest = {}

def arbitrate():
    cmd = {"brake": False, "steer": 0.0, "alerts": []}
    for svc in PRIORITY:
        d = latest.get(svc)
        if d:
            if svc == "aeb" and d.get("brake"):
                cmd["brake"] = True
                cmd["steer"] = 0.0
            elif svc == "lka" and not cmd["brake"]:
                cmd["steer"] = d.get("steer",0.0)
            elif svc in ["fcw","daw","tpms"] and d.get("alert"):
                cmd["alerts"].append(d["alert"])
    return cmd

def on_message(client, userdata, msg):
    svc = msg.topic.split("/")[1]
    latest[svc] = json.loads(msg.payload.decode())
    final_cmd = arbitrate()
    client.publish("car/control", json.dumps(final_cmd))
    print("Gatekeeper:", final_cmd)

mqtt_client = MQTTClient("Gatekeeper")
for t in TOPICS:
    mqtt_client.subscribe(t, on_message)
mqtt_client.loop_forever()
