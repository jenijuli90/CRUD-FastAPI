
import token
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .decorator import handle_error

from app.database import get_db
from .. import schemas,token,models

router = APIRouter(prefix="/votes",tags=["Votes"])

#-------------------------like a post-------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_error
def vote_post(vote: schemas.VoteCreate,db: Session = Depends(get_db),current_user: int = Depends(token.get_current_user) ):
    
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if post is already liked by user
    existing_vote_query = db.query(models.Vote).filter( models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id )

    existing_vote = existing_vote_query.first()
        
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=400, detail="Post already liked by User")

        # Create like
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return {"message": "Post liked successfully", "post_id": new_vote.post_id}
    
    else:
        if not existing_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "Vote does not exist")
        
        existing_vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message": "Post deleted successfully"}

