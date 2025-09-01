# services/acc-service/app/controllers/acc_controller.py
import time
import json
from app.utils.logger import logger
from app.utils.exceptions import ControllerError, DatabaseError, MessagingError
from app.models.orm_models import ACCRecord

class ACCController:
    def __init__(self, adapter, db_session_factory, mqtt_client):
        self.adapter = adapter
        self.db_session_factory = db_session_factory
        self.mqtt = mqtt_client
        # caches for subscribed topics
        self.latest_fcw = None  # expected format: {"feature": "fcw", "ts": ..., "data": {...}}
        self.latest_ldw = None

    # mqtt handlers set these (safe: wrap with try/except)
    def on_fcw(self, payload):
        try:
            logger.info("ACC received FCW: %s", payload)
            self.latest_fcw = payload
        except Exception:
            logger.exception("Error handling FCW payload")

    def on_ldw(self, payload):
        try:
            logger.info("ACC received LDW: %s", payload)
            self.latest_ldw = payload
        except Exception:
            logger.exception("Error handling LDW payload")

    def step(self):
        """
        One control step: read radar, consult latest fcw/ldw, decide action, persist and publish.
        """
        try:
            radar = self.adapter.read_radar()
            action = "maintain"
            reason = None

            fcw = self.latest_fcw
            # fcw expected to be dict with data.status and optionally data.distance
            try:
                fcw_status = 0
                fcw_dist = None
                if fcw and isinstance(fcw, dict):
                    fcw_data = fcw.get("data", {}) if isinstance(fcw.get("data", {}), dict) else {}
                    fcw_status = int(fcw_data.get("status", 0))
                    fcw_dist = float(fcw_data.get("distance")) if fcw_data.get("distance") is not None else None
                else:
                    fcw_status = 0
            except Exception:
                fcw_status = 0
                fcw_dist = None

            # Rule: if FCW indicates imminent collision -> decelerate
            if fcw_status == 1:
                d = radar.get("distance", 999.0)
                # consider fcw distance if provided
                if (d is not None and d < 15.0) or (fcw_dist is not None and fcw_dist < 12.0):
                    action = "decelerate"
                    reason = "fcw"

            # Radar-only fallback rule
            if action == "maintain" and radar.get("distance", 999.0) < 8.0:
                action = "decelerate"
                reason = "radar_close"

            res = {
                "action": action,
                "reason": reason,
                "radar": radar,
                "fcw": fcw,
                "ldw": self.latest_ldw
            }

            # persist
            session = self.db_session_factory()
            rec = ACCRecord(timestamp=time.time(), action=action, meta=json.dumps(res))
            session.add(rec)
            session.commit()
            session.close()

            # publish on mqtt
            try:
                self.mqtt.publish("adas/acc", {"feature": "acc", "ts": time.time(), "data": res})
            except Exception as e:
                logger.exception("MQTT publish failed")
                # don't fail whole step because of publish; escalate if desired
                raise MessagingError(str(e))

            logger.info("ACC step result: %s", res)
            return res

        except MessagingError:
            raise  # already logged
        except DatabaseError as de:
            logger.exception("DB error in ACC step")
            raise
        except Exception as e:
            logger.exception("ACCController step failed")
            raise ControllerError(str(e))
