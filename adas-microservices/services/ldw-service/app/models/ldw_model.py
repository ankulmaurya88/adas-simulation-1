# services/ldw-service/app/models/ldw_model.py
from app.utils.logger import logger

class LDWModel:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def predict(self, lateral_offset: float):
        status = 1 if abs(lateral_offset) > self.threshold else 0
        confidence = min(1.0, abs(lateral_offset) / (self.threshold + 0.01))
        res = {
            "status": status,
            "confidence": round(confidence, 2),
            "offset": lateral_offset
        }
        logger.debug("LDWModel.predict -> %s", res)
        return res
