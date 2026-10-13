import uuid
from pydantic import BaseModel



class ReactionResponse(BaseModel):
    post_id: uuid.UUID
    status:str