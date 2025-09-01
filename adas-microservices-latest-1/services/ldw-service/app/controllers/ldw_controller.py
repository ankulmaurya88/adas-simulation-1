# services/ldw-service/app/controllers/ldw_controller.py
import time
from app.utils.logger import logger
from app.utils.exceptions import ControllerError, DatabaseError
from app.models.orm_models import LDWRecord

class LDWController:
    def __init__(self, model, adapter, db_session, mqtt_client):
        self.model = model
        self.adapter = adapter
        self.db_session = db_session
        self.mqtt = mqtt_client

    def step(self):
        try:
            offset = self.adapter.read_lane_offset()
            res = self.model.predict(offset)

            session = self.db_session()
            rec = LDWRecord(
                timestamp=time.time(),
                offset=offset,
                status=res["status"],
                confidence=res["confidence"]
            )
            session.add(rec)
            session.commit()
            session.close()

            self.mqtt.publish("adas/ldw", {
                "feature": "ldw",
                "ts": time.time(),
                "data": res
            })
            logger.info("LDW published %s", res)
            return res
        except DatabaseError as de:
            logger.error("Database error in LDWController: %s", de)
            raise
        except Exception as e:
            logger.exception("LDWController step failed")
            raise ControllerError(str(e))
