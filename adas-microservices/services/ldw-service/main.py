# services/ldw-service/app/main.py
from fastapi import FastAPI
from app.adapters.sim_camera import SimCameraAdapter
from app.models.ldw_model import LDWModel
from app.controllers.ldw_controller import LDWController
from app.utils.db import get_engine, get_session
from app.models.orm_models import Base
from app.utils.mqtt_client import MQTTClient
from app.views import api
from app.config import MQTT_HOST

engine = get_engine()
Base.metadata.create_all(engine)
SessionLocal = get_session(engine)

adapter = SimCameraAdapter()
model = LDWModel()
mqtt_client = MQTTClient(client_id="ldw-service", host=MQTT_HOST)
mqtt_client.connect()

controller = LDWController(model, adapter, SessionLocal, mqtt_client)

app = FastAPI(title="LDW Service", version="1.0")
app.include_router(api.router)

# Dependency injection for controller
@app.on_event("startup")
def startup_event():
    api.controller = controller
