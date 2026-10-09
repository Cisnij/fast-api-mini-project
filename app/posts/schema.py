import uuid
from datetime import datetime
from app.users.schema import UserRead
from pydantic import BaseModel


class PostResponse(BaseModel):
    id: uuid.UUID
    content: str
    url:str
    file_type:str
    file_name:str
    file_size:int
    created_at: datetime
    is_owner:bool
    users : UserRead
    class Config:
        from_attributes = True

class PostUserResponse(BaseModel):
    id: uuid.UUID
    content: str
    url:str
    file_type:str
    file_name:str
    file_size:int
    created_at: datetime
    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    content:str