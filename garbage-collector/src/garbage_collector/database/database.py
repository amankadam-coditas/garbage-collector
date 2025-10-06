from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
from src.garbage_collector.core.config import setting

engine = create_engine(setting.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db()-> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()