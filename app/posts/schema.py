from datetime import datetime

from pydantic import BaseModel


class PostResponse(BaseModel):
    content: str
    url:str
    file_type:str
    file_name:str
    file_size:str
    created_at: datetime