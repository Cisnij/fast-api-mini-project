from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Post


async def get_feed_selectors (db: AsyncSession) -> List[Post]:
    return await db.execute(
        select(Post).order_by(Post.created_at.desc())
    ).scalars.all()