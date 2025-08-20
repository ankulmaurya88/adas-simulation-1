# services/acc-service/app/adapters/sim_radar.py
import numpy as np
from app.utils.exceptions import SensorReadError
from app.utils.logger import logger

class SimRadarAdapter:
    def __init__(self, seed=202):
        self.rng = np.random.RandomState(seed)

    def read_radar(self):
        try:
            # distance to lead car in meters (simulate 5m-80m)
            dist = round(float(self.rng.uniform(5.0, 80.0)), 1)
            speed = round(float(self.rng.uniform(20.0, 120.0)), 1)
            return {"distance": dist, "speed": speed}
        except Exception as e:
            logger.exception("SimRadar error")
            raise SensorReadError(str(e))
