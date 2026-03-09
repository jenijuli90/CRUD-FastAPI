# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from .config import settings



DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'



if not DATABASE_URL:
    raise Exception("Database connection string not found in .env file")

# Create SQLAlchemy engine 
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Check connection before using
   
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:      
        yield db   
    finally:
        db.close()
