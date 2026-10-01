import uuid

from fastapi import UploadFile, File, Form, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.posts.models import Post
from app.posts.schema import PostResponse
from app.posts.services import create_post_service, get_feed_service, delete_post_service

router = APIRouter()

# hàm này chỉ nhận formdata và k nhận json nên các giá trị truyền vào lấy từ formdata
@router.post("/upload/", response_model=PostResponse)
async def upload_file(
        file: UploadFile = File(...), # dùng để nhận form-data, UploadFile là kiểu dữ liệu, File(...) báo lấy file từ form-data và dấu ... để bắt buộc gửi
        content: str = Form(...), # vì fast api khác django là django nhận cùng lúc body data và form data còn fastapi chỉ nhận 1 trong 2. 1 là body hết 2 là form hết. Form ở đây báo lấy content ở Form
        db : AsyncSession = Depends(get_db), # gọi tới tạo async session
):
    return await create_post_service(file, content, db)

@router.get("/feed/")
async def get_feed(db : AsyncSession = Depends(get_db)):
    return await get_feed_service(db)

@router.delete("/post/{id}/",)
async def delete_post(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await delete_post_service(id,db)