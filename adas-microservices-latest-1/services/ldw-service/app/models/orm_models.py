# services/ldw-service/app/models/orm_models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float
Base = declarative_base()

class LDWRecord(Base):
    __tablename__ = "ldw_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, nullable=False)
    offset = Column(Float, nullable=False)
    status = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
