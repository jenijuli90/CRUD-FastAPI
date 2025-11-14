# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .config import settings



DATABASE_URL = settings.database_connection

if not DATABASE_URL:
    raise Exception("Database connection string not found in .env file")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Check connection before using
    connect_args={"timeout": 5}  # Optional: timeout for DB connection
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        print("DB session creation failed:", e)
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        db.close()
