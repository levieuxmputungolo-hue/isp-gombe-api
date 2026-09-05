import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import app.models_payment

DB_PATH = os.environ.get("DB_PATH", "/tmp/results.db")
DATABASE_URL = f"sqlite:///{DB_PATH}" if not DB_PATH.startswith("sqlite") else DB_PATH

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def init_db():
    from app.models_payment import Base as PaymentBase
    Base.metadata.create_all(bind=engine)
    PaymentBase.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
