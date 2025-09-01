# services/ldw-service/app/utils/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.exceptions import DatabaseError
from app.utils.logger import logger

DB_PATH = "data/ldw_service.db"

def get_engine():
    try:
        return create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})
    except Exception as e:
        logger.exception("Database engine creation failed")
        raise DatabaseError(str(e))

def get_session(engine):
    try:
        return sessionmaker(bind=engine)
    except Exception as e:
        logger.exception("Database session creation failed")
        raise DatabaseError(str(e))
