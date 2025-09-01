import json
import numpy as np
import joblib

class LKAController:
    def __init__(self, model_path="app/models/lka_model.pkl"):
        self.model = joblib.load(model_path)

    def compute_steer(self, sensor_data):
        # Example feature: lane offset
        features = np.array([sensor_data["lane_offset"]]).reshape(1, -1)
        steer = float(self.model.predict(features)[0])
        decision = {
            "steer": steer,
            "priority": 3
        }
        return json.dumps(decision)
