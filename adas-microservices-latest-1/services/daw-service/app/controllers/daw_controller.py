import json
import numpy as np
import joblib

class DAWController:
    def __init__(self, model_path="app/models/daw_model.pkl"):
        self.model = joblib.load(model_path)

    def compute_alert(self, sensor_data):
        # Example feature: fatigue score
        features = np.array([sensor_data.get("fatigue_score", 0)]).reshape(1, -1)
        alert_prob = self.model.predict_proba(features)[0][1]
        decision = {
            "alert": alert_prob > 0.5,
            "priority": 4,
            "probability": alert_prob
        }
        return json.dumps(decision)
