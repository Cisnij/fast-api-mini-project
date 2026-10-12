import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.comments.models import Comment
from app.comments.exceptions import CommentNotFound


async def get_comments_from_post_selectors(post_id:uuid.UUID, db: AsyncSession, skip:int, limit:int) -> List[Comment]:
    comments = await db.execute(
        select(Comment)
        .options(
            joinedload(Comment.post),
            joinedload(Comment.user)
        )
        .filter(Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
    )
    return comments.scalars().all()

async def get_detail_comment(comment_id:uuid.UUID, db:AsyncSession) -> Comment:
    comment = await db.execute(
        select(Comment)
        .options(
            joinedload(Comment.post),
            joinedload(Comment.user)
        )
        .filter(Comment.id == comment_id)
    )
    result = comment.scalars().first()
    if not result:
        raise CommentNotFound()
    return result