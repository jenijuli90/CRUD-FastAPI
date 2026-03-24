from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from .decorator import handle_error
from ..services.user import UserService

router = APIRouter()

# ---------------------- User Create --------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
@handle_error
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
      user_service = UserService(db)
      return user_service.create_user(user)
   
        

    
# ---------------------- Get User --------------------------
@router.get("/{user_email}", response_model=schemas.UserResponse)
@handle_error
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
   
        user_service = UserService(db)
        return user_service.get_user_by_email(user_email)