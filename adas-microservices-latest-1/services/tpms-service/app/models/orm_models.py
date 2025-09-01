# services/tpms-service/app/models/orm_models.py
from sqlalchemy import Column, Integer, Float, String
from app.utils.db import Base

class TPMSRecord(Base):
    __tablename__ = "tpms_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, nullable=False)
    pressures = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=True)
    meta = Column(String, nullable=True)
