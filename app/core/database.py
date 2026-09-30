from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL,echo=True)

SessionLocal= async_sessionmaker( # tạo session kết nối db khi đc gọi
    autoflush=False, # là db gửi câu lệnh (INSERT/UPDATE/DELETE) xuống db và đã chạy, nhưng vẫn trong commit nên có thể roll back , có thể dùng db.rollback() sau db.flush() để rollback. Dùng để có được dữ liệu cần có mà chưa cần commit, flush=True để tự động chạy khi có lệnh query thay vì gọi tay
    autocommit=False,# không thực thi mà phải gọi db.commit() mới thực thi
    bind=engine, # khởi tạo session kết nối với engine chứa db url
    expire_on_commit=False # để giữ giá trị sau khi commit không bị mysql đánh hết hạn mà k cần query lại
)

async def get_db(): # gọi tới sẽ khởi tạo session và trả về session cho hàm truy cập để truy vấn
    db = SessionLocal() #khởi tạo session
    try:
        yield db
    finally:
        await db.close()

class Base(DeclarativeBase):
    pass