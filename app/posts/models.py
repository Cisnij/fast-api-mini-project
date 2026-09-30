import datetime
import uuid

from sqlalchemy import Integer, Column, Uuid, Text, String, DateTime

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

    # cách gộp index để tối ưu nếu filter nhiều field
    # __table_args__ = (
    #     Index("ix_user_published", "user_id", "published"),   # composite index, giống models.Index nhiều field
    # )