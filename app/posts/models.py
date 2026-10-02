import datetime
import uuid

from sqlalchemy import Integer, Column, Uuid, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship

from app.core.database import Base
from datetime import datetime

#đây là post dạng viddeo
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text,nullable=False)

    url = Column(String(255),nullable=False)
    file_type = Column(String(255),nullable=False)
    file_name = Column(String(255),nullable=False)
    file_size = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.now)

    user= Relationship("User",back_populates="posts")
    user_id = Column(Uuid,ForeignKey("users.id"),nullable=False) #users.id phải theo tên bảng là users
    # cách gộp index để tối ưu nếu filter nhiều field
    # __table_args__ = (
        # tên idex + cột
    #     Index("ix_user_published", "user_id", "published"),   # composite index, giống models.Index nhiều field
    # )