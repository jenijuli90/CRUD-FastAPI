# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, post, auth,like
from .database import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,      # only if you use cookies or Authorization headers
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routers
app.include_router(user.router, prefix="/users", tags=["User"])
app.include_router(post.router, prefix="/posts", tags=["Post"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(like.router)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Page! "}

# Startup event to check DB and create tables
@app.on_event("startup")
def startup_event():
    try:
        # Test DB connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    

        # Create tables safely (only if not exist)
        Base.metadata.create_all(bind=engine)
        print("Tables created or already exist.")
    except SQLAlchemyError as e:
        # Log the error, app can still start
        print("Database connection failed at startup:", e)
