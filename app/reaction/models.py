import datetime
import uuid

from sqlalchemy import Integer, Column, Text, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy.generics import GUID
from app.users.models import User
from app.core.database import Base
from datetime import datetime



class Reaction(Base): # bảng nhiều-nhiều
    __tablename__ = 'reactions'
    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(GUID,ForeignKey("users.id"),nullable=False)
    post_id = Column(GUID,ForeignKey("posts.id"),nullable=False)
    user = relationship("User", back_populates="reactions") # reaction.user là lấy user của reaction đó
    post = relationship("Post", back_populates="reactions")#reaction.post lấy tất cả post thuộc reaction id này

    created_at = Column(DateTime, default=datetime.now)