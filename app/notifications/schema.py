import uuid
from datetime import datetime

from pydantic import BaseModel

from app.posts.schema import PostResponse
from app.users.schema import UserRead


class NotificationResponse(BaseModel):
    content:str
    created_at: datetime
    from_user_id : uuid.UUID
    post_id : uuid.UUID