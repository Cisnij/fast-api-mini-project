import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Post
from app.posts.exceptions import PostNotFound


async def get_feed_selectors (db: AsyncSession) -> List[Post]:
    return (await db.execute(
        select(Post).order_by(Post.created_at.desc()))).scalars().all()

async def get_post_selectors(id:uuid.UUID, db: AsyncSession) ->Post:
    query = await db.execute(select(Post).filter(Post.id == id))
    post = query.scalars().first()
    if not post:
        raise PostNotFound()
    return post