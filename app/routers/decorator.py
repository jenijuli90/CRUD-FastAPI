from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

def handle_error(func):
   
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            if db:
                db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error ,{str(e)}"
            )
        except HTTPException:
            # Let HTTPExceptions pass through
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"{str(e)}" #detail="Internal server error. Please try again later.")
            )
    return wrapper
