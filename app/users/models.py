from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.core.database import Base
from core.database import get_db


#thư viện của fastapi-users
class User(SQLAlchemyBaseUserTableUUID,Base): #SQLAlchemyBaseUserTableUUID dùng này cho uuid
    __tablename__ = "users"
    posts = relationship("Post",back_populates="users")
