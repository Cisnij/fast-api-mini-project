from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base
from sqlalchemy import Uuid,DateTime,Boolean,String,Column

#thư viện của fastapi-users
class User(SQLAlchemyBaseUserTableUUID,Base): #SQLAlchemyBaseUserTableUUID dùng này cho uuid
    __tablename__ = "users"
    name = Column(String(255), nullable=False)
    posts = relationship("Post",back_populates="users", passive_deletes=True, cascade="all, delete-orphan") #User.posts lấy tất cả post của user, posts.user lấy user của post có id
    comments = relationship("Comment",back_populates="user", passive_deletes=True, cascade="all, delete-orphan")#User.comments lấy tất cả comments của user, comments.user lấy user của comments có id
    reactions = relationship("Reaction",back_populates="user", passive_deletes=True, cascade="all, delete-orphan")#User.reactions lấy tất cả reactions của user, reactions.user lấy user của reactions có id
    sent_notifications = relationship("Notification", back_populates="from_user", passive_deletes=True, cascade="all, delete-orphan", foreign_keys="Notification.from_user_id") #khi có 2 fk cùng tới 1 bảng thì nên khai báo rõ
    received_notifications = relationship("Notification", back_populates="to_user", passive_deletes=True,cascade="all, delete-orphan", foreign_keys="Notification.to_user_id")
# class RefreshToken(Base):
#     __tablename__ = 'refresh_tokens'
#     id = Column(Uuid, primary_key=True, default= uuid.uuid4)
#     token = Column(String(255), nullable=False, index= True)
#     user_id = Column(Uuid, ForeignKey(users.id), nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     expired_at = Column(DateTime, nullable=False)
#     is_revoked = Column(Boolean, nullable=False)
