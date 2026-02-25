from fastapi.testclient import TestClient
from app.database import get_db,Base
from app.main import app
from app.config import settings

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError 
import pytest



DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'



# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Check connection before using
   
)

# Session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="module")
def session():
    # Drop tables safely (only if not exist)
    Base.metadata.drop_all(bind=engine)
     # Create tables safely (only if not exist)
    Base.metadata.create_all(bind=engine)

    try:
        db = TestingSessionLocal()  
        yield db
    except SQLAlchemyError as e:
        print("DB session creation failed:", e)
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        db.close() 


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()


    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)