import uuid
from typing import List
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.users.manager import current_active_user
from app.posts.models import Post
from app.posts.selectors import get_feed_selectors, get_user_posts_selectors
from app.posts.exceptions import FileValidateException, PostUnauthorized
from app.posts.images import imagekit, upload_to_imagekit
from app.posts.selectors import get_post_selectors
from app.posts.schema import PostResponse, PostUpdate
from app.users.models import User

ALLOWED_TYPES = {"image/jpeg", "image/png", "video/mp4"} # IME/định dạng
MAX_FILE_SIZE = 50 * 1024 * 1024 #50mb

async def create_post_service(file: UploadFile,content : str ,db: AsyncSession, user_id : uuid.UUID) -> Post:
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
        user_id = user_id,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_feed_service(db: AsyncSession, user_id : uuid.UUID,skip:int, limit:int) -> List[PostResponse]:
    posts = await get_feed_selectors(db,skip,limit)
    return [ # cách tự add field vào schema giống serializer method field
        PostResponse(
            id=post.id,
            content=post.content,
            url=post.url,
            file_type=post.file_type,
            file_name=post.file_name,
            file_size=post.file_size,
            created_at=post.created_at,
            is_owner=(post.user_id == user_id), #field tự thêm
            users = post.users
        )
        for post in posts
    ]


async def delete_post_service(id:uuid.UUID, db:AsyncSession, user_id: uuid.UUID) ->None:
    post = await get_post_selectors(id,db)
    if post.user_id != user_id:
        raise PostUnauthorized()
    await db.delete(post)
    await db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Post deleted")


async def get_user_posts_services(id: uuid.UUID, db: AsyncSession, skip:int , limit: int):
    return await get_user_posts_selectors(id, db)

async def get_detail_service(id: uuid.UUID, db:AsyncSession, user:User):
    post = await get_post_selectors(id,db)
    return PostResponse(
        id=post.id,
        content=post.content,
        url=post.url,
        file_type=post.file_type,
        file_name=post.file_name,
        file_size=post.file_size,
        created_at=post.created_at,
        is_owner=(post.user_id == user.id),  # field tự thêm
        users=post.users
    )
async def update_post_service(data:PostUpdate, id:int, db: AsyncSession, user: User)-> Post:
    post = await get_post_selectors(id,db)
    if post.user_id != user.id:
        raise PostUnauthorized()
    post.content = data.content
    db.add(post)
    await db.commit()
    return post