# services/acc-service/app/utils/exceptions.py

class ADASException(Exception):
    """Base ADAS Service Exception"""
    pass

class SensorReadError(ADASException):
    """Raised when sensor or adapter fails"""
    pass

class DatabaseError(ADASException):
    """Raised when DB operations fail"""
    pass

class MessagingError(ADASException):
    """Raised when MQTT publish/subscribe fails"""
    pass

class ControllerError(ADASException):
    """Raised when controller processing fails"""
    pass
