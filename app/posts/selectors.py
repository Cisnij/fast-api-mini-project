import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.models import Post
from app.posts.exceptions import PostNotFound


async def get_feed_selectors (db: AsyncSession, skip:int, limit:int) -> List[Post]:
    result = await db.execute(
        select(Post)
        .options(joinedload(Post.users))
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_post_selectors(id:uuid.UUID, db: AsyncSession) ->Post:
    query = await db.execute(select(Post).options(joinedload(Post.users)).filter(Post.id == id))
    post = query.scalars().first()
    if not post:
        raise PostNotFound()
    return post

async def get_user_posts_selectors(id: uuid.UUID, db:AsyncSession, skip:int , limit:int) -> List[Post]:
    query = await db.execute(
        select(Post)
        .options(joinedload(Post.users))
        .filter(Post.user_id == id)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return query.scalars().all()

