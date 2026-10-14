import uuid
from datetime import datetime
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    content = Column(String(255), nullable=False)
    created_at= Column(DateTime, default = datetime.now)

    user_id = Column(GUID, ForeignKey("users.id", ondelete ="CASCADE"), nullable=False) # comment.user_id
    post_id = Column(GUID, ForeignKey("posts.id", ondelete ="CASCADE"), nullable=False)

    #tên field bên này là tên back_populate bên kia và ngc lại, tất cả bên Post và User phải đặt back_populate là user à post
    user = relationship('User', back_populates="comments") # User.comments lấy ra tất cả comment của user, comments.user lấy ra user có comment có id
    post = relationship('Post', back_populates="comments") # post.comments lấy ra tất cả comment của post, comments.post lấy ra post có comment có id

    __table_args__ = (
        Index('idx_post_id_created_at','post_id','created_at'),
    )
