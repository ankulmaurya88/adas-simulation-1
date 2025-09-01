# services/acc-service/app/main.py
import os
import uvicorn
from fastapi import FastAPI
from app.utils.db import create_session, Base
from app.adapters.sim_radar import SimRadarAdapter
from app.controllers.acc_controller import ACCController
from app.utils.mqtt_client import MQTTClient
from app.views import api as api_router
from app.utils.logger import logger
from app.models.orm_models import ACCRecord

# Configuration via env or defaults
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
HTTP_PORT = int(os.getenv("HTTP_PORT", "8003"))

def bootstrap():
    # DB
    engine, Session = create_session("acc")
    Base.metadata.create_all(engine)

    # adapters/models/controllers
    adapter = SimRadarAdapter()
    # MQTT client with placeholder handlers (we'll set after controller created)
    mqtt = MQTTClient(client_id="acc-service", host=MQTT_HOST, port=MQTT_PORT)

    # controller
    controller = ACCController(adapter=adapter, db_session_factory=Session, mqtt_client=mqtt)

    # set mqtt handlers mapping and connect
    mqtt.set_handlers({
        "adas/fcw": controller.on_fcw,
        "adas/ldw": controller.on_ldw
    })
    mqtt.connect()

    # FastAPI app
    app = FastAPI(title="ACC Service")
    # include API router (note: router endpoints are minimal — controller is on app.state)
    app.include_router(api_router.router)
    app.state.controller = controller
    app.state.mqtt = mqtt
    logger.info("ACC service bootstrap complete")
    return app

app = bootstrap()

# Provide a convenient POST /run endpoint that triggers the controller step
@app.post("/run")
def run_once():
    try:
        return app.state.controller.step()
    except ADASException as ae:
        logger.error("ADAS error on /run: %s", ae)
        raise
    except Exception as e:
        logger.exception("Unexpected error on /run")
        raise

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT)
