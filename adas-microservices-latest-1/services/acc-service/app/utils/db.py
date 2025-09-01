# services/acc-service/app/utils/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from app.utils.logger import logger
from app.utils.exceptions import DatabaseError

Base = declarative_base()

def get_db_path():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(repo_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "acc_service.db")

def create_session(service_name="acc"):
    try:
        db_path = get_db_path()
        url = f"sqlite:///{db_path}"
        engine = create_engine(url, connect_args={"check_same_thread": False}, echo=False)
        Session = scoped_session(sessionmaker(bind=engine))
        logger.info("DB engine created for %s at %s", service_name, url)
        return engine, Session
    except Exception as e:
        logger.exception("Failed to create DB session")
        raise DatabaseError(str(e))
