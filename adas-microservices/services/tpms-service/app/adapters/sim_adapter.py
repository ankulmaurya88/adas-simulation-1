# services/tpms-service/app/adapters/sim_adapter.py
import numpy as np
from app.utils.exceptions import SensorReadError
from app.utils.logger import logger

class SimAdapter:
    def __init__(self, seed=42, fault_rate=0.2):
        self.rng = np.random.RandomState(seed)
        self.fault_rate = fault_rate

    def read_tpms(self):
        try:
            base = self.rng.normal(loc=32.0, scale=0.8)
            pressures = self.rng.normal(loc=base, scale=0.7, size=4)
            if self.rng.rand() < self.fault_rate:
                idx = self.rng.randint(0,4)
                pressures[idx] -= self.rng.uniform(3.5,7.0)
            return [round(float(p),1) for p in pressures]
        except Exception as e:
            logger.exception("SimAdapter error")
            raise SensorReadError(str(e))
