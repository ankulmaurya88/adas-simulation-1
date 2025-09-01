# services/tpms-service/app/models/pressure_model.py
import os, joblib, numpy as np
from app.utils.exceptions import ModelNotFoundError, PredictionError
from app.utils.logger import logger

class PressureModel:
    def __init__(self, model_path=None):
        # look for model in models_data or fall back to rule-based
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models_data", "tpms_ai_model.pkl")
        if os.path.exists(model_path):
            try:
                self.clf = joblib.load(model_path)
                logger.info("PressureModel loaded from %s", model_path)
            except Exception as e:
                logger.exception("Failed to load model")
                raise ModelNotFoundError(e)
        else:
            logger.info("No model file found, using rule-based fallback")
            self.clf = None

    def predict(self, pressures):
        try:
            arr = np.array(pressures).reshape(1, -1)
            if self.clf:
                pred = int(self.clf.predict(arr)[0])
                conf = float(self.clf.predict_proba(arr).max()) if hasattr(self.clf, "predict_proba") else None
            else:
                # simple rule: any tire < 28 -> fault
                pred = 1 if any(p < 28.0 for p in pressures) else 0
                conf = None
            return {"status": pred, "confidence": conf, "pressures": pressures}
        except Exception as e:
            logger.exception("Prediction failed")
            raise PredictionError(str(e))
