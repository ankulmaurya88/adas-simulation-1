# services/tpms-service/app/controllers/tpms_controller.py
import time, json
from app.utils.logger import logger
from app.utils.exceptions import ControllerError, DatabaseError, MessagingError
from app.models.orm_models import TPMSRecord

class TPMSController:
    def __init__(self, model, adapter, db_session, mqtt_client):
        self.model = model
        self.adapter = adapter
        self.db_session = db_session
        self.mqtt = mqtt_client

    def step(self):
        try:
            pressures = self.adapter.read_tpms()
            res = self.model.predict(pressures)
            rec = TPMSRecord(timestamp=time.time(), pressures=str(res["pressures"]), status=res["status"], confidence=res["confidence"])
            session = self.db_session()
            session.add(rec)
            session.commit()
            session.close()
            # publish
            try:
                payload = {"feature":"tpms", "ts": time.time(), "data": res}
                self.mqtt.publish("adas/tpms", payload)
            except Exception as e:
                logger.exception("MQTT publish error")
                raise MessagingError(str(e))
            logger.info("TPMS step completed: %s", res)
            return res
        except Exception as e:
            logger.exception("TPMSController step failed")
            raise ControllerError(str(e))
