import json
import numpy as np
import joblib

class AEBController:
    def __init__(self, model_path="app/models/aeb_model.pkl"):
        self.model = joblib.load(model_path)

    def compute_brake(self, sensor_data):
        features = np.array([sensor_data["distance"], sensor_data.get("speed",0)]).reshape(1, -1)
        brake_prob = self.model.predict_proba(features)[0][1]
        decision = {
            "brake": brake_prob > 0.5,
            "priority": 1,
            "probability": brake_prob
        }
        return json.dumps(decision)
