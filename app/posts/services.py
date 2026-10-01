from typing import List
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.posts.models import Post
from app.posts.selectors import get_feed_selectors
from app.posts.exceptions import FileValidateException
from app.posts.images import imagekit, upload_to_imagekit
from app.posts.selectors import get_post_selectors

ALLOWED_TYPES = {"image/jpeg", "image/png", "video/mp4"} # IME/định dạng
MAX_FILE_SIZE = 50 * 1024 * 1024 #50mb

async def create_post_service(file: UploadFile,content : str ,db: AsyncSession) -> Post:
    file_bytes= await file.read() # đọc toàn bộ nội dung bên trong file và lưu dưới dạng bytes

    if file.content_type not in ALLOWED_TYPES: #check đuôi file tải lên
        raise FileValidateException()
    if len(file_bytes) > MAX_FILE_SIZE: # check độ lớn ảnh dựa vào bytes
        raise FileValidateException()

    try: #bọc trong try except để khi lỗi upload lên server k đc
        response = await upload_to_imagekit(file_bytes, str(file.filename))
    except:
        raise FileValidateException()

    post = Post(
        content= content,
        url = response.url,
        file_type = file.content_type,
        file_name = file.filename,
        file_size = len(file_bytes),
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_feed_service(db: AsyncSession) -> List[Post]:
    return await get_feed_selectors(db)

async def delete_post_service(id, db):
    post = await get_post_selectors(id,db)
    await db.delete(post)
    await db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Post deleted")