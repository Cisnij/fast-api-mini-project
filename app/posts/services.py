from typing import List

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Post
from app.posts.selectors import get_feed_selectors


async def create_post_service(file: UploadFile,content : str ,db: AsyncSession) -> Post:
    post = Post(
        content= content,
        url = file.url,
        file_type = file.file_type,
        file_name = file.file_name,
        file_size = file.file_size,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_feed_service(db: AsyncSession) -> List[Post]:
    return await get_feed_selectors(db)