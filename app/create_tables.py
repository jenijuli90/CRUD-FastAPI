from .database import engine
from .models import Base

# Create tables based on models
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
