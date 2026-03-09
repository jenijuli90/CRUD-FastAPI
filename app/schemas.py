from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel,EmailStr, conint

# Base model with common fields
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#Base model for User
class UserBase(BaseModel):
    username : str
    email : EmailStr

    class Config:
        orm_mode = True

# Request model for creating a post (no id)
class CreatePost(PostBase):
    pass

class VoteBase(BaseModel):
    post_id :int
    user_id : int

 
# Response model (includes id)
class PostResponse(PostBase):
    id: int  # database-generated id
    user_id: int
    user : UserBase

    class Config:
        orm_mode = True


# Request model for creating User
class UserCreate(UserBase):
    password : str

# Response model for user
class UserResponse(UserBase):
    id : int
    created_at : datetime

#Request model for UserLogin
class UserLogin(UserBase):
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class VoteCreate(BaseModel):
    post_id :int
    dir : conint(le =1)

class PostVote(BaseModel):
    post :  PostResponse
    votes : int

   