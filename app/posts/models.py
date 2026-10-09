import datetime
import uuid

from sqlalchemy import Integer, Column, Text, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Relationship
from fastapi_users_db_sqlalchemy.generics import GUID
from app.users.models import User
from app.core.database import Base
from datetime import datetime

#đây là post dạng viddeo
class Post(Base):
    __tablename__ = 'posts'
    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text,nullable=False)

    url = Column(String(255),nullable=False)
    file_type = Column(String(255),nullable=False)
    file_name = Column(String(255),nullable=False)
    file_size = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.now)

    users= Relationship("User",back_populates="posts") # back_populates phải đúng tên field của posts = relationship("Post",back_populates="users")
    user_id = Column(GUID,ForeignKey("users.id"),nullable=False) #users.id phải theo tên bảng là users
    
    # cách gộp index để tối ưu nếu filter nhiều field
    __table_args__ = (
        # tên idex + cột
        Index("ix_user_id_created_at", "user_id", "created_at"),   # composite index, giống models.Index nhiều field
    )

    