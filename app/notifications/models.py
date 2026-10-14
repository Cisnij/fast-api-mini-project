from datetime import datetime

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, default = datetime.now)

    post_id = Column(GUID,ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    from_user_id = Column(GUID,ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # người gửi
    to_user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # người nhận

    post = relationship("Post", back_populates="notifications")
    from_user = relationship("User", back_populates="sent_notifications", foreign_keys=[from_user_id],) # foreign_keys: khi có 2 fk cùng tới 1 bảng thì nên khai báo rõ ở đây là tới User 2 fk
    to_user = relationship("User", back_populates="received_notifications",foreign_keys=[to_user_id],)