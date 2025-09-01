import json
import numpy as np
import joblib

class TPMSController:
    def __init__(self, model_path="app/models/tpms_model.pkl"):
        self.model = joblib.load(model_path)

    def compute_alert(self, sensor_data):
        # Example feature: tire pressure
        features = np.array([sensor_data.get("pressure", 32)]).reshape(1, -1)
        alert_prob = self.model.predict_proba(features)[0][1]
        decision = {
            "alert": alert_prob > 0.5,
            "priority": 5,
            "probability": alert_prob
        }
        return json.dumps(decision)
