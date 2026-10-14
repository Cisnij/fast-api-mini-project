import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.notifications.models import Notification


async def get_user_notifications_selectors(user_id:uuid.UUID, db: AsyncSession):
    result= await db.execute(
        select(Notification)
        .options(
            joinedload(Notification.post),
            joinedload(Notification.from_user),
            joinedload(Notification.to_user),
        )
        .where(Notification.to_user_id == user_id)
        .order_by(Notification.created_at.desc())
    )
    return result.scalars().all()
