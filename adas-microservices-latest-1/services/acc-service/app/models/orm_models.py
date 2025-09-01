# services/acc-service/app/models/orm_models.py
from sqlalchemy import Column, Integer, Float, String
from app.utils.db import Base

class ACCRecord(Base):
    __tablename__ = "acc_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, nullable=False)
    action = Column(String, nullable=False)  # e.g. "maintain", "decelerate"
    meta = Column(String, nullable=True)     # JSON/stringified metadata
