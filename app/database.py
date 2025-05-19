# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create the engine
engine = create_engine(
    str(settings.db_url),
    echo=True,               # log SQL for debugging; turn off in production
    future=True              # use SQLAlchemy 2.0 style
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for our ORM models
Base = declarative_base()
