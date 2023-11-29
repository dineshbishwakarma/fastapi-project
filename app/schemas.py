from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from typing import Optional
# Schema to create a post 
# This ensures that user post is in the below data typess
# This means the request is made in the following format

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True

class PostCreate(PostBase):
    # Use the pass keyword when you do not want to add any 
    # other properties or methods to the  parent class.
    pass

# Reponses are given in following format
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserOut
    
    class Config:
        from_attributes = True

# Create User schemas
class UserCreate(BaseModel):
    email : EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None