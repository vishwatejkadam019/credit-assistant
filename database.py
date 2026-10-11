"""Database engine and session. Swap to PostgreSQL by changing DATABASE_URL."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
URL = os.getenv("DATABASE_URL", "sqlite:///./credit.db")
engine = create_engine(URL, connect_args={"check_same_thread": False} if URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
