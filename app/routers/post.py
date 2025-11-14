from cProfile import label
from typing import Optional
from httpx import Limits
from sqlalchemy import func
from .. import models, schemas, utils,token
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from .decorator import handle_error

router = APIRouter()
 
# ---------------------- Get all posts ----------------------
@router.get("/", response_model=list[schemas.PostVote])
#@router.get("/")
def get_posts(db: Session = Depends(get_db),current_user: int= Depends(token. get_current_user),limit: int = 10,skip: int = 0,search : Optional[str] = ""):
    try:
        #all_posts = db.query(models.Post).filter(models.Post.user_id == current_user.id,models.Post.title.contains(search)).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all() 


        vote_count_subquery =  db.query(models.Vote.post_id,func.count(models.Vote.user_id).label("votes")).group_by(models.Vote.post_id).subquery()

        all_posts = (
             db.query(models.Post,func.coalesce(vote_count_subquery.c.votes,0).label("votes")).outerjoin(vote_count_subquery,vote_count_subquery.c.post_id == models.Post.id)
        .filter(models.Post.title.contains(search)).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
        )
        
        #posts = db.query(models.Post).join(models.l)
        if not all_posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post  not found"
            )
        
        return all_posts
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")#detail="Internal server error. Please try again later.")


# ---------------------- Get post by ID ----------------------
@router.get("/{post_id}", response_model=schemas.PostVote)

@handle_error
def get_post_by_id(post_id: int, db: Session = Depends(get_db),current_user: int= Depends(token. get_current_user)):

        #post = db.query(models.Post).filter(models.Post.id == post_id).first()

        vote_count_subquery = db.query(models.Vote.post_id,func.count(models.Vote.user_id).label("votes")).group_by(models.Vote.post_id).filter(models.Vote.post_id == post_id).subquery()

        post = db.query(models.Post,func.coalesce(vote_count_subquery.c.votes,0).label("votes")).outerjoin(vote_count_subquery,vote_count_subquery.c.post_id == models.Post.id).first()

        print(post)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )
        return post
    


# ---------------------- Create new post ----------------------
@router.post("/", status_code=201, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),current_user: int= Depends(token. get_current_user)):
    try:
        new_post = models.Post(**post.dict())
        new_post.user_id = current_user.id
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")


# ---------------------- Delete a post ----------------------
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_error
def delete_post(post_id: int, db: Session = Depends(get_db),current_user: int= Depends(token. get_current_user)):
   
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )
        if post.user_id != current_user.id:
             raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail= "Not authorized to perform requested action")
        db.delete(post)
        db.commit()
  

# ---------------------- Update a post ----------------------
@router.put("/{post_id}", response_model=schemas.PostResponse)
@handle_error
def update_post(post_id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),current_user: int= Depends(token. get_current_user)):
    
        post_query = db.query(models.Post).filter(models.Post.id == post_id)
        post = post_query.first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )

        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()

        return post_query.first() 

