# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import user, post, auth,like
from .database import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .config import settings
from sqlalchemy.exc import SQLAlchemyError
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration




sentry_sdk.init(
    dsn=settings.sentry_dsn,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),  # captures DB errors too
    ])

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,      # only if you use cookies or Authorization headers
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Global Error Handlers ----
@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Connection Failed"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
# Register routers
app.include_router(user.router, prefix="/users", tags=["User"])
app.include_router(post.router, prefix="/posts", tags=["Post"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(like.router)



# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Updated Page.App is Live.Error Handling!!!!! "}

@app.get("/test-sentry")
def test_sentry():
    raise Exception("Test error from FastAPI!")

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
