"""
Database
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


database_url = os.getenv("DATABASE_PUBLIC_URL") or ""

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_table():
    """
    Create database tables
    """
    Base.metadata.create_all(bind=engine)
