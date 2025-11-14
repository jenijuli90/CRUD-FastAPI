
from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
#from .database import engine


class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer, primary_key = True) 
    username = Column(String(150),nullable= False,index= True)  
    email = Column(String(150),nullable=False,unique=True,index = True)
    password = Column(String,nullable = False)
    phonenumber = Column(String(50))
    is_active = Column(Boolean,default= True)
    created_at = Column(DateTime, server_default=func.getdate(), nullable=False)
    updated_at = Column(DateTime, server_default=func.getdate(),onupdate=func.getdate(), nullable=False)

class Vote(Base): 
    __tablename__ = "votes"

 
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True, nullable = False)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key= True, nullable= False)
    created_at = Column(DateTime, server_default=func.getdate(), nullable=False)
    #user = relationship("User")
    #post = relationship("Post")
    

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False,)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False) 
    published = Column(Boolean, server_default= "True", nullable=False)
    created_at = Column(DateTime, server_default=func.getdate(), nullable=False)
    updated_at = Column(DateTime, server_default=func.getdate(),onupdate=func.getdate(), nullable=False)
    user_details = relationship("User")
  


    
