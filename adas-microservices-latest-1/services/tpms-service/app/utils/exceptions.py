class ADASException(Exception): pass
class ModelNotFoundError(ADASException): pass
class PredictionError(ADASException): pass
class SensorReadError(ADASException): pass
class DatabaseError(ADASException): pass
class MessagingError(ADASException): pass
class ControllerError(ADASException): pass