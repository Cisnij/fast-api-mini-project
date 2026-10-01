from imagekitio import AsyncImageKit
import os
from app.core.config import settings

imagekit =AsyncImageKit(
    private_key = settings.IMAGEKIT_PRIVATE_KEY,
)
URL_ENDPOINT = settings.IMAGEKIT_URL


async def upload_to_imagekit(file_bytes:bytes, file_name: str, folder: str = "/posts"):
    response = await imagekit.files.upload(
        file = file_bytes, # nội dung file
        file_name = file_name,
        folder = folder, # khi gọi tới kh truyền folder thì tự tạo trong thư mục posts
        tags = ["post"] #tag chỉ để tìm các file trong imagekit
    )
    return response