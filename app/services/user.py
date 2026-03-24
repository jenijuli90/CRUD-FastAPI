from sqlalchemy.orm import Session
from .. import schemas,models,utils
from fastapi import HTTPException,status

class UserService:

    def __init__(self,db: Session):
        self.db = db


    # ---------------------- Create User --------------------------   
    def create_user(self, user: schemas.UserCreate):
   
        # Check if user already exists
        existing_user = self.db.query(models.User).filter(models.User.email == user.email).first()
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
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
    
    # ---------------------- Get User --------------------------
    def get_user_by_email(self,user_email: str):
    
            user_details = self.db.query(models.User).filter(models.User.email == user_email).first()
            if not user_details:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user_details
