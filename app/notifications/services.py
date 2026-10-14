import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.notifications.models import Notification
from app.notifications.schema import NotificationResponse
from app.notifications.selectors import get_user_notifications_selectors
from app.notifications.websocket import manager
from app.posts.selectors import get_post_selectors
from app.users.models import User


async def get_notifications_services(db: AsyncSession, user: User):
    return await get_user_notifications_selectors(user.id,db)

async def create_notifications(post_id: uuid.UUID, db: AsyncSession, user: User):
    post = await get_post_selectors(post_id,db)
    notification = Notification(
        content = f"{user.name} đã thích bài viết '{post.content}' của bạn",
        from_user_id = post.user_id,
        to_user_id = user.id,
        post_id = post.id,
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    await manager.send_to_user(
        post.user_id,
        {
            "id": str(notification.id),
            "content": notification.content,
            "post_id": str(notification.post_id),
        }
    )
    return notification