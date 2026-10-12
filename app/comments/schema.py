import uuid

from pydantic import BaseModel

from app.users.schema import UserRead


class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: uuid.UUID
    content: str
    user : UserRead
    post_id: uuid.UUID
    class Config:
        from_attributes = True

class CommentUpdate(CommentCreate):
    pass