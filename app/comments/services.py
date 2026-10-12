import uuid

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.schema import CommentCreate
from app.users.models import User
from app.posts.selectors import get_post_selectors
from app.comments.models import Comment
from app.posts.exceptions import PostUnauthorized
from .exceptions import CommentUnauthorized
from .schema import CommentUpdate
from .selectors import get_comments_from_post_selectors, get_detail_comment


async def create_comment_service(data:CommentCreate, post_id:uuid.UUID, db:AsyncSession, user:User):
    post = await get_post_selectors(post_id, db)
    comment = Comment(
        content = data.content,
        user_id = user.id,
        post_id = post.id,
    )
    db.add(comment)
    await db.commit()
    return comment

async def get_comments_from_post_service(post_id:uuid.UUID, db:AsyncSession, user:User,skip,limit):
    post = await get_post_selectors(post_id, db)
    return await get_comments_from_post_selectors(post.id, db,skip,limit)

async def delete_comment_service(comment_id:uuid.UUID, db:AsyncSession, user:User):
    comment = await get_detail_comment(comment_id, db)
    if not comment.user_id == user.id:
        raise CommentUnauthorized()
    await db.delete(comment)
    await db.commit()

async def update_comment_service(data: CommentUpdate,comment_id:uuid.UUID, db:AsyncSession, user:User) -> Comment:
    comment = await get_detail_comment(comment_id, db)
    if not comment.user_id == user.id:
        raise CommentUnauthorized()
    comment.content = data.content
    db.add(comment)
    await db.commit()
    return comment