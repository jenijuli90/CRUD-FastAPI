from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from annotated_types import Ge, Le
from typing import Annotated

# ---------------------- User Schemas ----------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------------- Post Schemas ----------------------

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int
    user: UserBase

    model_config = {"from_attributes": True}


class PostVote(BaseModel):
    post: PostResponse
    votes: int

    model_config = {"from_attributes": True}


# ---------------------- Auth Schemas ----------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# ---------------------- Vote Schemas ----------------------

class VoteBase(BaseModel):
    post_id: int
    user_id: int


class VoteCreate(BaseModel):
    post_id: int
    dir: Annotated[int, Ge(0), Le(1)]