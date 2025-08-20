# services/tpms-service/app/main.py
import os
import uvicorn
from app.views.api import app
from app.utils.db import create_session, Base
from app.models.orm_models import TPMSRecord
from app.models.pressure_model import PressureModel
from app.adapters.sim_adapter import SimAdapter
from app.controllers.tpms_controller import TPMSController
from shared_libs.messaging.mqtt_client import MQTTClient
from app.utils.logger import logger
from threading import Thread
import time

class Orchestrator:
    def __init__(self, controllers):
        self.controllers = controllers

def bootstrap():
    engine, Session = create_session("tpms")
    Base.metadata.create_all(engine)
    # mqtt
    mqtt = MQTTClient(client_id="tpms-svc", host=os.getenv("MQTT_HOST","mqtt"), port=int(os.getenv("MQTT_PORT",1883)))
    mqtt.connect()
    model = PressureModel()
    adapter = SimAdapter()
    tpms_ctrl = TPMSController(model=model, adapter=adapter, db_session=Session, mqtt_client=mqtt)
    orch = Orchestrator({"tpms": tpms_ctrl})
    app.state.orchestrator = orch
    return app

app = bootstrap()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
