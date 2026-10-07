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
    posts = relationship("Post",back_populates="users")

# class RefreshToken(Base):
#     __tablename__ = 'refresh_tokens'
#     id = Column(Uuid, primary_key=True, default= uuid.uuid4)
#     token = Column(String(255), nullable=False, index= True)
#     user_id = Column(Uuid, ForeignKey(users.id), nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     expired_at = Column(DateTime, nullable=False)
#     is_revoked = Column(Boolean, nullable=False)
