from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models,token,utils
from .decorator import handle_error
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# ---------------------- User Login --------------------------
@router.post("/login",response_model= schemas.Token)
@handle_error
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch user by email    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()


    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if utils.needs_rehash(user.password):
        user.password = utils.hash_password(user_credentials.password)
        db.commit()

    #Create JWT token
    access_token = token.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token,"token_type": "bearer"}
    
   

        