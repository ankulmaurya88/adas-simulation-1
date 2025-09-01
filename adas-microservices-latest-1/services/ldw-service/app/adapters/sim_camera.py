# services/ldw-service/app/adapters/sim_camera.py
import numpy as np
from app.utils.exceptions import SensorReadError
from app.utils.logger import logger

class SimCameraAdapter:
    def __init__(self, seed=101, drift_rate=0.05):
        self.rng = np.random.RandomState(seed)
        self.drift_rate = drift_rate

    def read_lane_offset(self):
        try:
            offset = self.rng.normal(loc=0.0, scale=0.3)
            if self.rng.rand() < 0.12:
                offset += self.rng.choice([-1,1]) * self.rng.uniform(0.5, 1.5)
            return round(float(offset), 2)
        except Exception as e:
            logger.exception("SimCamera read failed")
            raise SensorReadError(str(e))
