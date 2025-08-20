# services/tpms-service/app/utils/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from app.utils.logger import logger

Base = declarative_base()

def get_sqlite_url(service_name="tpms"):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(repo_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, f"{service_name}_data.db")
    return f"sqlite:///{db_path}"

def create_session(service_name="tpms"):
    url = get_sqlite_url(service_name)
    engine = create_engine(url, connect_args={"check_same_thread": False}, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    logger.info("DB engine created at %s", url)
    return engine, Session
