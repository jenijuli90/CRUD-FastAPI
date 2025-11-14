from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from .decorator import handle_error

router = APIRouter()

# ---------------------- User Create --------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
@handle_error
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        # Hash password
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password

        # Create new user
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    
# ---------------------- Get User --------------------------
@router.get("/{user_email}", response_model=schemas.UserResponse)
@handle_error
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
   
        user_details = db.query(models.User).filter(models.User.email == user_email).first()
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user_details
