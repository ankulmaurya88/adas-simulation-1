import json
import numpy as np
import joblib

class FCWController:
    def __init__(self, model_path="app/models/fcw_model.pkl"):
        self.model = joblib.load(model_path)

    def compute_alert(self, sensor_data):
        # Example features: distance, relative speed
        features = np.array([sensor_data["distance"], sensor_data.get("rel_speed", 0)]).reshape(1, -1)
        alert_prob = self.model.predict_proba(features)[0][1]
        decision = {
            "alert": alert_prob > 0.5,
            "priority": 2,
            "probability": alert_prob
        }
        return json.dumps(decision)
